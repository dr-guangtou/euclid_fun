"""Stage 1: detection and resolution limits of Gaia and Euclid for UCD-like objects.

Runs after stages 2 and 3, because the empirical parts need the Gaia and Euclid tables of the control field.
Nothing here uses the known Fornax objects to set a number; they appear only as labelled points in one figure.

Parts:
  A. known population (sizes, luminosities) from the bubbletea snapshot, and its angular size / magnitude with distance
  B. Gaia completeness versus Euclid I_E for compact Euclid sources (control field)
  C. Euclid stellar locus in compactness and Sersic radius versus I_E (secure Gaia stars), and its upper quantile
  D. simulated compactness of King and Sersic profiles convolved with an empirical VIS PSF
  E. Gaia excess noise versus angular size for reference UCDs outside Fornax (Virgo, Liu et al. 2020)
  F. limits table on the (distance, M_V) grid and the discovery-space figure

Usage: uv run python -m ucd.stages.stage_1_limits
"""

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.io import ascii as astropy_ascii
from astropy.io import fits
from scipy import ndimage, signal

from ucd.lib import crossmatch, euclid_catalogue, qa_plots, run_state

stage_name = "stage_1_limits"
parsec_per_arcsec_per_mpc = 4.848137
locus_quantile = 0.99
g_minus_v = -0.23  # Gaia DR3 photometric relation at V - I = 1.05 (old stellar population)
magnitude_edges = np.arange(16.0, 22.01, 0.5)
clean_star_rejected_bits = (
    1 | 4 | 8 | 512 | 1024
)  # neighbours/bad pixels, saturated, border, extended area, not deblended
size_grid_arcsec = np.array([0.0, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0])
oversampling = 5
virgo_distance_mpc = 16.5


def magnitude(flux):
    return 23.9 - 2.5 * np.log10(np.where(flux > 0, flux, np.nan))


def robust_sigma(values) -> float:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    return float(1.4826 * np.median(np.abs(values - np.median(values)))) if len(values) else np.nan


# ---------------------------------------------------------------- A. population


def load_population(config: dict) -> pd.DataFrame:
    repository = run_state.reference_dir(config) / "repository"
    rows = []
    for line in (repository / "reference/fahrion2019/tableb1.dat").read_text().splitlines():
        tokens = line.split()
        try:
            absolute_v, _, radius = float(tokens[-4]), float(tokens[-3]), float(tokens[-2])
        except (ValueError, IndexError):
            continue
        if radius > 0:
            host = line[20:36].strip()
            rows.append({"source": "Fahrion+19 compilation", "host": host, "half_light_radius_pc": radius,
                         "absolute_v": absolute_v})  # fmt: skip
    liu = astropy_ascii.read(
        repository / "reference/liu2020/table4.dat", readme=repository / "reference/liu2020/ReadMe.txt", format="cds"
    ).to_pandas()
    liu = liu[np.isfinite(liu["rh"]) & np.isfinite(liu["VMAG"])]
    rows += [
        {"source": "Liu+20 Virgo", "host": "Virgo", "half_light_radius_pc": row.rh, "absolute_v": row.VMAG}
        for row in liu.itertuples()
    ]
    population = pd.DataFrame(rows)
    population["in_fornax"] = population["host"].str.contains("1399|Fornax|FCC|1336|1404", regex=True)
    return population


def plot_population(config: dict, population: pd.DataFrame, folder) -> None:
    definition = config["ucd_definition"]
    figure, axis = plt.subplots(figsize=(qa_plots.double_width, 4.2))
    for source, color in (
        ("Liu+20 Virgo", qa_plots.colors["star"]),
        ("Fahrion+19 compilation", qa_plots.colors["selected"]),
    ):
        subset = population[population["source"] == source]
        axis.scatter(
            subset["absolute_v"],
            subset["half_light_radius_pc"],
            s=5,
            color=color,
            alpha=0.7,
            label=rf"{source.replace('+', '+ ')} ({len(subset)})",
        )
    axis.axhline(definition["minimum_half_light_radius_pc"], color="k", lw=0.7, ls="--")
    axis.axvline(definition["maximum_absolute_v_magnitude"], color="k", lw=0.7, ls="--")
    axis.set_yscale("log")
    axis.set_ylim(1.5, 200)
    axis.set_xlim(-8, -14.5)
    axis.set_xlabel(r"$M_V$ (mag)")
    axis.set_ylabel(r"half-light radius $r_{\rm h}$ (pc)")
    for distance, style in zip((5, 10, 20, 50), ("-", "--", "-.", ":"), strict=True):
        for size_arcsec in (0.1,):
            axis.axhline(size_arcsec * distance * parsec_per_arcsec_per_mpc, color="0.4", lw=0.8, ls=style)
            axis.annotate(
                rf"$0.1''$ at {distance} Mpc",
                (-14.45, size_arcsec * distance * parsec_per_arcsec_per_mpc * 1.05),
                fontsize=6.5,
                color="0.3",
                ha="right",
            )
    top = axis.secondary_xaxis("top", functions=(lambda m: m + 31.505 + g_minus_v, lambda g: g - 31.505 - g_minus_v))
    top.set_xlabel(r"apparent $G$ at 20 Mpc (mag)")
    axis.legend(loc="lower left", frameon=True)
    axis.set_title(
        r"Known compact stellar systems; dashed box edges: UCD definition of this project", fontsize=8, pad=28
    )
    qa_plots.save(figure, folder, "population_size_luminosity")


# ---------------------------------------------------------------- B. Gaia completeness


def gaia_completeness(config: dict, gaia: pd.DataFrame, folder_stage_3) -> pd.DataFrame:
    """Fraction of clean Euclid sources with a Gaia source within 0.6 arcsec, by I_E and compactness class."""
    cone = pd.concat(
        [
            pd.read_parquet(path)
            for path in sorted((folder_stage_3 / "tables" / "cone_control").glob("strip_*.parquet"))
        ],
        ignore_index=True,
    )
    cone["ie_mag"] = magnitude(cone["flux_detection_total"].to_numpy())
    clean = cone[
        (cone["vis_det"] == 1)
        & (cone["spurious_flag"] == 0)
        & (cone["det_quality_flag"] == 0)
        & (cone["ie_mag"] < 22.5)
    ].reset_index(drop=True)
    all_coordinates = SkyCoord(cone["right_ascension"].to_numpy(), cone["declination"].to_numpy(), unit="deg")
    coordinates = SkyCoord(clean["right_ascension"].to_numpy(), clean["declination"].to_numpy(), unit="deg")
    neighbour_index, _, _, _ = all_coordinates.search_around_sky(coordinates, 3.0 * u.arcsec)
    clean = clean[np.bincount(neighbour_index, minlength=len(clean)) == 1].reset_index(drop=True)
    coordinates = SkyCoord(clean["right_ascension"].to_numpy(), clean["declination"].to_numpy(), unit="deg")
    # Gaia positions propagated to the Euclid epoch, so moving stars are not lost from the completeness.
    baseline = gaia["euclid_baseline_years"].median()
    has_motion = gaia["has_five_parameter_astrometry"].to_numpy()
    gaia_coordinates = SkyCoord(gaia["ra"].to_numpy(), gaia["dec"].to_numpy(), unit="deg").spherical_offsets_by(
        np.where(has_motion, np.nan_to_num(gaia["pmra"].to_numpy()) * baseline, 0.0) * u.mas,
        np.where(has_motion, np.nan_to_num(gaia["pmdec"].to_numpy()) * baseline, 0.0) * u.mas,
    )
    matched = crossmatch.nearest_match(coordinates, gaia_coordinates, 0.6)
    clean["in_gaia"] = (matched["catalogue_index"] >= 0).to_numpy()
    classes = {
        "point-like": clean["mumax_minus_mag"] < -2.75,
        "marginally resolved": clean["mumax_minus_mag"].between(-2.75, -2.2),
        "resolved": clean["mumax_minus_mag"].between(-2.2, -1.2),
    }
    edges = np.arange(17.0, 22.51, 0.25)
    rows = []
    for label, mask in classes.items():
        for low, high in zip(edges[:-1], edges[1:], strict=True):
            members = clean[mask & clean["ie_mag"].between(low, high)]
            if len(members) >= 15:
                rows.append({"class": label, "ie_low": low, "ie_high": high, "sources": len(members),
                             "in_gaia_fraction": float(members["in_gaia"].mean())})  # fmt: skip
    return pd.DataFrame(rows)


def magnitude_at_half(table: pd.DataFrame) -> float:
    centres = 0.5 * (table["ie_low"] + table["ie_high"]).to_numpy()
    fraction = table["in_gaia_fraction"].to_numpy()
    below = np.where(fraction < 0.5)[0]
    if len(below) == 0 or below[0] == 0:
        return float("nan")
    first = below[0]
    return float(np.interp(0.5, [fraction[first], fraction[first - 1]], [centres[first], centres[first - 1]]))


# ---------------------------------------------------------------- C. stellar locus


def stellar_locus(control: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    stars = control[
        control["euclid_matched"]
        & control["has_five_parameter_astrometry"]
        & ((control["parallax_significance"] > 5) | (control["proper_motion_zero_significance"] > 5))
        & (control["euclid_matches_in_radius"] == 1)
        & (control["euclid_entries_within_3_arcsec"] == 1)
        & ((control["euclid_det_quality_flag"].fillna(-1).astype("int64") & clean_star_rejected_bits) == 0)
        & (control["ruwe"] < 1.4)
        & (control["ipd_frac_multi_peak"] <= 2)
        & (control["non_single_star"].fillna(0) == 0)
    ].copy()
    stars["psf_minus_total"] = stars["euclid_ie_psf_mag"] - stars["euclid_ie_mag"]
    rows = []
    for low, high in zip(magnitude_edges[:-1], magnitude_edges[1:], strict=True):
        members = stars[stars["euclid_ie_mag"].between(low, high)]
        if len(members) < 25:
            continue
        row = {"ie_low": low, "ie_high": high, "stars": len(members)}
        for column, label in (
            ("euclid_mumax_minus_mag", "mumax_minus_mag"),
            ("euclid_sersic_sersic_vis_radius", "sersic_radius_arcsec"),
            ("psf_minus_total", "psf_minus_total_mag"),
            ("euclid_point_like_prob", "point_like_prob"),
        ):
            values = members[column].dropna()
            row[f"{label}_median"] = float(values.median())
            row[f"{label}_sigma"] = robust_sigma(values)
            row[f"{label}_upper"] = float(values.quantile(locus_quantile))
            row[f"{label}_lower"] = float(values.quantile(1 - locus_quantile))
        rows.append(row)
    return pd.DataFrame(rows), stars


# ---------------------------------------------------------------- D. simulation


def build_empirical_psf(config: dict, stars: pd.DataFrame, folder) -> tuple[np.ndarray, dict]:
    """Median stack of isolated, unsaturated stars from one tile of the control field (native 0.1 arcsec pixels)."""
    cache = folder / "tables" / "empirical_vis_psf.fits"
    if cache.exists():
        return fits.getdata(cache), dict(fits.getheader(cache))
    candidates = stars[stars["euclid_ie_mag"].between(18.6, 19.8)]
    tile = candidates["euclid_tile_index"].value_counts().index[0]
    chosen = candidates[candidates["euclid_tile_index"] == tile].sort_values("euclid_ie_mag").head(24)
    first = chosen.iloc[0]
    mosaics = euclid_catalogue.find_mosaics(first["euclid_right_ascension"], first["euclid_declination"])
    vis = [row for row in mosaics if row["filter_name"] == "VIS" and int(row["tile_index"]) == int(tile)][0]
    half = 20
    stamps = []
    for index, star in enumerate(chosen.itertuples()):
        path = folder / "tables" / "psf_stars" / f"star_{index:02d}.fits"
        try:
            euclid_catalogue.get_cutout(vis["file_path"], vis["file_name"], star.euclid_right_ascension,
                                        star.euclid_declination, 0.06, path)  # fmt: skip
        except RuntimeError:
            continue
        data = fits.getdata(path).astype(float)
        if not np.isfinite(data).all() or min(data.shape) < 2 * half + 9:
            continue
        data -= np.median(data[[0, -1], :])
        peak_y, peak_x = np.unravel_index(np.argmax(ndimage.gaussian_filter(data, 1.0)), data.shape)
        if min(peak_y, peak_x) < half + 3 or peak_y > data.shape[0] - half - 4 or peak_x > data.shape[1] - half - 4:
            continue
        window = data[peak_y - 3 : peak_y + 4, peak_x - 3 : peak_x + 4]
        grid_y, grid_x = np.mgrid[-3:4, -3:4]
        shift_y = (window * grid_y).sum() / window.sum()
        shift_x = (window * grid_x).sum() / window.sum()
        shifted = ndimage.shift(data, (-shift_y, -shift_x), order=3)
        stamp = shifted[peak_y - half : peak_y + half + 1, peak_x - half : peak_x + half + 1]
        stamps.append(stamp / stamp.sum())
    psf = np.median(stamps, axis=0)
    psf /= psf.sum()
    header = fits.Header({"NSTARS": len(stamps), "TILE": int(tile), "PIXSCALE": 0.1})
    fits.writeto(cache, psf, header, overwrite=True)
    return psf, dict(header)


def profile_image(kind: str, half_light_radius_arcsec: float, size: int, pixel: float) -> np.ndarray:
    """Normalised 2-D profile on a fine grid; a zero radius gives a point source."""
    image = np.zeros((size, size))
    centre = size // 2
    if half_light_radius_arcsec <= 0:
        image[centre, centre] = 1.0
        return image
    sub = 3
    axis = (np.arange(size * sub) - (size * sub - 1) / 2) * pixel / sub
    radius = np.hypot(*np.meshgrid(axis, axis))
    if kind == "sersic_n2":
        index = 2.0
        b_n = 2 * index - 1 / 3 + 4 / (405 * index)
        values = np.exp(-b_n * ((radius / half_light_radius_arcsec) ** (1 / index) - 1))
    else:  # King (1962) with concentration r_t / r_c = 30; r_h / r_c computed numerically below
        concentration = 30.0
        ratio = king_half_light_ratio(concentration)
        core = half_light_radius_arcsec / ratio
        tidal = concentration * core
        values = (1 / np.sqrt(1 + (radius / core) ** 2) - 1 / np.sqrt(1 + concentration**2)) ** 2
        values[radius >= tidal] = 0.0
    image = values.reshape(size, sub, size, sub).sum(axis=(1, 3))
    return image / image.sum()


def king_half_light_ratio(concentration: float) -> float:
    radius = np.linspace(0, concentration, 200001)
    profile = (1 / np.sqrt(1 + radius**2) - 1 / np.sqrt(1 + concentration**2)) ** 2
    cumulative = np.cumsum(profile * radius)
    return float(radius[np.searchsorted(cumulative, 0.5 * cumulative[-1])])


def simulate_compactness(psf: np.ndarray) -> pd.DataFrame:
    """mu_max - mag (peak pixel over total flux, as in the MER catalogue) versus half-light radius, noise-free."""
    fine_psf = np.clip(ndimage.zoom(psf, oversampling, order=3), 0, None)
    fine_psf /= fine_psf.sum()
    fine_pixel = 0.1 / oversampling
    size = 401
    rows = []
    for kind in ("king_c30", "sersic_n2"):
        for radius in size_grid_arcsec:
            model = profile_image(kind, radius, size, fine_pixel)
            convolved = signal.fftconvolve(model, fine_psf, mode="same") * oversampling**2
            peaks = [
                convolved[oy::oversampling, ox::oversampling].max()
                for oy in range(oversampling)
                for ox in range(oversampling)
            ]
            rows.append({"profile": kind, "half_light_radius_arcsec": radius,
                         "mumax_minus_mag": float(-2.5 * np.log10(np.mean(peaks)) - 5.0)})  # fmt: skip
    table = pd.DataFrame(rows)
    point = table[table["half_light_radius_arcsec"] == 0].set_index("profile")["mumax_minus_mag"]
    table["shift_from_point_source"] = table["mumax_minus_mag"] - table["profile"].map(point)
    return table


def minimum_resolved_size(locus: pd.DataFrame, simulation: pd.DataFrame) -> pd.DataFrame:
    """Smallest half-light radius whose compactness shift exceeds the stellar-locus upper quantile, per I_E bin."""
    rows = []
    for row in locus.itertuples():
        threshold = row.mumax_minus_mag_upper - row.mumax_minus_mag_median
        entry = {"ie_low": row.ie_low, "ie_high": row.ie_high, "locus_upper_minus_median": threshold}
        for kind, table in simulation.groupby("profile"):
            entry[f"minimum_radius_arcsec_{kind}"] = float(
                np.interp(threshold, table["shift_from_point_source"], table["half_light_radius_arcsec"])
            )
        entry["sersic_radius_locus_upper_arcsec"] = row.sersic_radius_arcsec_upper
        rows.append(entry)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- E. Gaia versus angular size


def gaia_size_relation(config: dict) -> pd.DataFrame:
    """Gaia excess noise versus angular half-light radius for Virgo objects (Liu et al. 2020), matched by position."""
    repository = run_state.reference_dir(config) / "repository"
    readme = repository / "reference/liu2020/ReadMe.txt"
    columns = ["canonical_object_id", "half_light_radius_pc", "half_light_radius_arcsec", "phot_g_mean_mag",
               "astrometric_excess_noise", "astrometric_excess_noise_sig", "ruwe"]  # fmt: skip
    try:
        table3 = astropy_ascii.read(
            repository / "reference/liu2020/table3.dat", readme=readme, format="cds"
        ).to_pandas()
        table4 = astropy_ascii.read(
            repository / "reference/liu2020/table4.dat", readme=readme, format="cds"
        ).to_pandas()
    except Exception:
        return pd.DataFrame(columns=columns)
    if not {"RAdeg", "DEdeg"}.issubset(table3.columns) or len(table3) != len(table4):
        return pd.DataFrame(columns=columns)
    gaia = pd.read_csv(repository / "data/literature/catalogs/canonical_gaia_dr3_crossmatch.csv")
    gaia = gaia[np.isfinite(gaia["astrometric_excess_noise"])].reset_index(drop=True)
    liu = SkyCoord(table3["RAdeg"].to_numpy(), table3["DEdeg"].to_numpy(), unit="deg")
    targets = SkyCoord(gaia["target_ra"].to_numpy(), gaia["target_dec"].to_numpy(), unit="deg")
    matched = crossmatch.nearest_match(targets, liu, 1.0)
    has_match = (matched["catalogue_index"] >= 0).to_numpy()
    result = gaia[has_match].copy()
    result["half_light_radius_pc"] = table4["rh"].to_numpy()[matched["catalogue_index"].to_numpy()[has_match]]
    result = result[np.isfinite(result["half_light_radius_pc"])]
    result["half_light_radius_arcsec"] = result["half_light_radius_pc"] / (
        virgo_distance_mpc * parsec_per_arcsec_per_mpc
    )
    return result[columns]


# ---------------------------------------------------------------- figures


def plot_completeness(table: pd.DataFrame, folder) -> None:
    figure, axis = plt.subplots(figsize=(qa_plots.single_width * 1.25, 3.0))
    for (label, group), color in zip(
        table.groupby("class", sort=False), ("#4477AA", "#EE7733", "#CC3311"), strict=False
    ):
        axis.plot(
            0.5 * (group["ie_low"] + group["ie_high"]),
            group["in_gaia_fraction"],
            marker="o",
            ms=3,
            color=color,
            label=rf"{label}",
        )
    axis.axhline(0.5, color="k", lw=0.6, ls=":")
    axis.set_xlabel(r"$I_{\rm E}$ (Kron, mag)")
    axis.set_ylabel(r"fraction with a Gaia DR3 source")
    axis.set_ylim(-0.02, 1.05)
    axis.legend(title=r"Euclid compactness class", fontsize=7)
    qa_plots.save(figure, folder, "gaia_completeness_vs_euclid")


def plot_locus(control: pd.DataFrame, stars: pd.DataFrame, locus: pd.DataFrame, fornax: pd.DataFrame, folder) -> None:
    figure, axes = plt.subplots(1, 3, figsize=(qa_plots.double_width, 2.9))
    other = control[control["euclid_matched"] & ~control["gaia_star_like_motion"]]
    known = fornax[fornax["euclid_matched"] & (fornax["known_state"] == "confirmed")]
    panels = [
        ("euclid_mumax_minus_mag", "mumax_minus_mag", r"$\mu_{\rm max}-{\rm mag}$", (-3.6, -0.5), False),
        ("euclid_sersic_sersic_vis_radius", "sersic_radius_arcsec", r"S\'ersic radius (arcsec)", (3e-3, 3), True),
        ("psf_minus_total", "psf_minus_total_mag", r"$I_{\rm E,PSF}-I_{\rm E,Kron}$ (mag)", (-0.6, 1.5), False),
    ]
    other = other.assign(psf_minus_total=other["euclid_ie_psf_mag"] - other["euclid_ie_mag"])
    known = known.assign(psf_minus_total=known["euclid_ie_psf_mag"] - known["euclid_ie_mag"])
    centres = 0.5 * (locus["ie_low"] + locus["ie_high"])
    for axis, (column, label, y_label, limits, log_scale) in zip(axes, panels, strict=True):
        axis.scatter(
            other["euclid_ie_mag"],
            other[column],
            s=1,
            color=qa_plots.colors["all"],
            rasterized=True,
            label=r"control: no significant Gaia motion",
        )
        axis.scatter(
            stars["euclid_ie_mag"],
            stars[column],
            s=1.5,
            color=qa_plots.colors["star"],
            rasterized=True,
            label=r"control: secure Gaia stars",
        )
        axis.scatter(
            known["euclid_ie_mag"],
            known[column],
            s=12,
            facecolor="none",
            edgecolor=qa_plots.colors["known"],
            linewidths=0.6,
            label=r"Fornax known (shown only)",
        )
        axis.plot(
            centres,
            locus[f"{label}_upper"],
            color="k",
            lw=1.0,
            label=rf"stellar {int(locus_quantile * 100)}\% quantile",
        )
        axis.plot(centres, locus[f"{label}_median"], color="k", lw=0.6, ls="--")
        axis.set_xlim(17, 22.3)
        axis.set_ylim(*limits)
        if log_scale:
            axis.set_yscale("log")
        axis.set_xlabel(r"$I_{\rm E}$ (mag)")
        axis.set_ylabel(y_label)
    axes[0].legend(fontsize=5.5, markerscale=3, frameon=True, loc="upper left")
    figure.tight_layout()
    qa_plots.save(figure, folder, "euclid_stellar_locus")


def plot_simulation(psf: np.ndarray, simulation: pd.DataFrame, resolved: pd.DataFrame, folder) -> None:
    figure, axes = plt.subplots(1, 3, figsize=(qa_plots.double_width, 2.7))
    axes[0].imshow(np.arcsinh(psf / psf.max() * 200), cmap="magma", extent=(-2.05, 2.05, -2.05, 2.05))
    axes[0].set_xlabel(r"arcsec")
    axes[0].set_title(r"empirical VIS PSF (stack)", fontsize=8)
    for kind, style, label in (("king_c30", "-", r"King, $c=30$"), ("sersic_n2", "--", r"S\'ersic, $n=2$")):
        table = simulation[(simulation["profile"] == kind) & (simulation["half_light_radius_arcsec"] > 0)]
        axes[1].plot(
            table["half_light_radius_arcsec"], table["shift_from_point_source"], ls=style, color="k", label=label
        )
        axes[2].plot(
            0.5 * (resolved["ie_low"] + resolved["ie_high"]),
            resolved[f"minimum_radius_arcsec_{kind}"],
            ls=style,
            color="k",
            marker="o",
            ms=3,
            label=label,
        )
    axes[1].set_xscale("log")
    axes[1].set_xlabel(r"half-light radius (arcsec)")
    axes[1].set_ylabel(r"shift of $\mu_{\rm max}-{\rm mag}$ from a point source")
    axes[1].legend()
    axes[2].set_xlabel(r"$I_{\rm E}$ (mag)")
    axes[2].set_ylabel(r"smallest resolved $r_{\rm h}$ (arcsec)")
    axes[2].set_yscale("log")
    axes[2].legend()
    figure.tight_layout()
    qa_plots.save(figure, folder, "euclid_resolution_simulation")


def plot_gaia_size(relation: pd.DataFrame, folder) -> None:
    figure, axis = plt.subplots(figsize=(qa_plots.single_width * 1.3, 3.0))
    points = axis.scatter(relation["half_light_radius_arcsec"], relation["astrometric_excess_noise"].clip(lower=0.05),
                          c=relation["phot_g_mean_mag"], s=10, cmap="viridis_r", vmin=18, vmax=21)  # fmt: skip
    figure.colorbar(points, ax=axis, label=r"$G$ (mag)")
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel(r"half-light radius (arcsec), Virgo UCDs at 16.5 Mpc")
    axis.set_ylabel(r"Gaia astrometric excess noise (mas)")
    qa_plots.save(figure, folder, "gaia_excess_noise_vs_size")


def plot_discovery_space(config: dict, population: pd.DataFrame, limits: pd.DataFrame, folder) -> None:
    definition = config["ucd_definition"]
    distances = [5, 10, 20, 50]
    figure, axes = plt.subplots(1, len(distances), figsize=(qa_plots.double_width, 2.6), sharey=True)
    for axis, distance in zip(axes, distances, strict=True):
        table = limits[limits["distance_mpc"] == distance].sort_values("absolute_v")
        axis.scatter(
            population["absolute_v"],
            population["half_light_radius_pc"],
            s=2,
            color=qa_plots.colors["all"],
            rasterized=True,
        )
        axis.fill_between(
            table["absolute_v"],
            table["euclid_minimum_radius_pc"],
            300,
            color=qa_plots.colors["candidate"],
            alpha=0.18,
            lw=0,
        )
        axis.plot(
            table["absolute_v"],
            table["euclid_minimum_radius_pc"],
            color=qa_plots.colors["candidate"],
            lw=1.2,
            label=r"Euclid resolves above",
        )
        gaia_limit = table.loc[table["gaia_detectable"], "absolute_v"].max()
        if np.isfinite(gaia_limit):
            axis.axvline(gaia_limit, color=qa_plots.colors["selected"], lw=1.2, label=r"Gaia 50\% detection")
        axis.axhline(definition["minimum_half_light_radius_pc"], color="k", lw=0.6, ls="--")
        axis.axvline(definition["maximum_absolute_v_magnitude"], color="k", lw=0.6, ls="--")
        axis.set_yscale("log")
        axis.set_ylim(2, 200)
        axis.set_xlim(-8, -14)
        axis.set_xlabel(r"$M_V$")
        axis.set_title(rf"{distance} Mpc", fontsize=8)
    axes[0].set_ylabel(r"$r_{\rm h}$ (pc)")
    axes[0].legend(fontsize=6, loc="upper left", frameon=True)
    qa_plots.save(figure, folder, "discovery_space")


def main() -> None:
    config = run_state.load_config()
    run_state.require_stages(config, ["stage_2_gaia", "stage_3_euclid"])
    folder = run_state.stage_dir(config, stage_name)
    stage_3 = run_state.run_dir(config) / "stage_3_euclid"
    control = pd.read_parquet(stage_3 / "tables" / "gaia_euclid_control.parquet")
    fornax = pd.read_parquet(stage_3 / "tables" / "gaia_euclid_fornax.parquet")

    population = load_population(config)
    plot_population(config, population, folder / "figures")
    in_box = (population["half_light_radius_pc"] >= config["ucd_definition"]["minimum_half_light_radius_pc"]) & (
        population["absolute_v"] <= config["ucd_definition"]["maximum_absolute_v_magnitude"]
    )

    completeness = gaia_completeness(config, control, stage_3)
    completeness.to_csv(folder / "tables" / "gaia_completeness.csv", index=False)
    plot_completeness(completeness, folder / "figures")
    half_magnitudes = {label: magnitude_at_half(group) for label, group in completeness.groupby("class", sort=False)}

    locus, stars = stellar_locus(control)
    locus.to_csv(folder / "tables" / "stellar_locus.csv", index=False)
    plot_locus(control, stars, locus, fornax, folder / "figures")

    psf, psf_header = build_empirical_psf(config, stars, folder)
    simulation = simulate_compactness(psf)
    simulation.to_csv(folder / "tables" / "compactness_simulation.csv", index=False)
    resolved = minimum_resolved_size(locus, simulation)
    resolved.to_csv(folder / "tables" / "minimum_resolved_size.csv", index=False)
    plot_simulation(psf, simulation, resolved, folder / "figures")

    relation = gaia_size_relation(config)
    relation.to_csv(folder / "tables" / "gaia_excess_noise_vs_size.csv", index=False)
    if len(relation):
        plot_gaia_size(relation, folder / "figures")

    # G - I_E for old-population colours, from control-field stars (not from Fornax objects).
    colour_stars = stars[stars["bp_rp"].between(0.9, 1.3) & stars["euclid_ie_mag"].between(18, 20.5)]
    g_minus_ie = float((colour_stars["phot_g_mean_mag"] - colour_stars["euclid_ie_mag"]).median())
    gaia_half = half_magnitudes.get("point-like", np.nan)
    gaia_half_marginal = half_magnitudes.get("marginally resolved", np.nan)
    centres = 0.5 * (resolved["ie_low"] + resolved["ie_high"]).to_numpy()
    gaia_limit = gaia_half_marginal if np.isfinite(gaia_half_marginal) else gaia_half
    rows = []
    for distance in config["ucd_definition"]["distance_grid_mpc"]:
        modulus = 5 * np.log10(distance * 1e6) - 5
        for absolute_v in np.arange(-14.0, -7.99, 0.25):
            g_mag = absolute_v + modulus + g_minus_v
            ie_mag = g_mag - g_minus_ie
            minimum_arcsec = float(np.interp(ie_mag, centres, resolved["minimum_radius_arcsec_king_c30"]))
            rows.append({
                "distance_mpc": distance, "absolute_v": absolute_v, "apparent_g": g_mag, "apparent_ie": ie_mag,
                "arcsec_per_10_pc": 10 / (distance * parsec_per_arcsec_per_mpc),
                "euclid_minimum_radius_arcsec": minimum_arcsec,
                "euclid_minimum_radius_pc": minimum_arcsec * distance * parsec_per_arcsec_per_mpc,
                "ie_inside_measured_locus": bool(centres.min() <= ie_mag <= centres.max()),
                "gaia_detectable": bool(ie_mag < gaia_limit),
            })  # fmt: skip
    limits = pd.DataFrame(rows)
    limits.to_csv(folder / "tables" / "limits_grid.csv", index=False)
    plot_discovery_space(config, population, limits, folder / "figures")

    point_simulated = float(simulation.loc[simulation["half_light_radius_arcsec"] == 0, "mumax_minus_mag"].iloc[0])
    observed_point = float(locus["mumax_minus_mag_median"].median())
    at_20 = limits[(limits["distance_mpc"] == 20) & limits["absolute_v"].isin([-10.0, -11.0, -12.0])]
    metrics = {
        "population": {"objects_with_size_and_luminosity": len(population), "inside_ucd_definition": int(in_box.sum())},
        "gaia_half_completeness_ie": half_magnitudes,
        "g_minus_ie_for_old_population_colour": g_minus_ie,
        "stellar_locus_bins": len(locus),
        "stellar_locus": locus.round(3).to_dict("records"),
        "psf": {
            **psf_header,
            "simulated_point_source_mumax_minus_mag": point_simulated,
            "observed_stellar_mumax_minus_mag": observed_point,
        },  # fmt: skip
        "minimum_resolved_size": resolved.round(4).to_dict("records"),
        "limits_at_20_mpc": at_20.round(3).to_dict("records"),
        "virgo_ucds_with_gaia_and_size": len(relation),
    }
    gates = [
        run_state.gate(
            "stellar_locus_bins", "locus measured in at least 5 magnitude bins", len(locus), len(locus) >= 5
        ),
        run_state.gate(
            "simulation_matches_catalogue",
            "simulated point source within 0.3 mag of the observed stellar mu_max - mag",
            {"simulated": round(point_simulated, 3), "observed": round(observed_point, 3)},
            abs(point_simulated - observed_point) < 0.3,
            fatal=False,
        ),
        run_state.gate(
            "limits_table", "limits written for the full distance and luminosity grid", len(limits), len(limits) > 0
        ),
    ]
    run_state.write_summary(config, stage_name, metrics, gates)


if __name__ == "__main__":
    main()
