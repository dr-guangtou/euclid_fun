"""Step 4 of the demo: NISP red-grism 1-D spectra from DR1 for low-z galaxies, and a cautionary example.

1. Find sources with spectra and confident SPE redshifts around NGC 1483 (ADQL join of dr1.spectra_source_wide,
   dr1.spectro_z_spe_galaxy_candidates_wide and dr1.mer_catalogue_wide_survey).
2. Download the combined spectra with astroquery (git main) ``Euclid.get_spectrum(ids=..., schema='dr1',
   retrieval_type='SPECTRA_RGS')``.
3. Plot (a) a bright z = 0.149 galaxy with the near-IR lines that fall into the red grism at low z (here a
   continuum-dominated, quiescent spectrum), and (b) a fragment of NGC 1483's disc that SPE assigned z ~ 4.6 with
   SPE_Z_PROB ~ 1: its "spectrum" is a broad, sharp-edged hump from the dispersed light of the host disc
   (contamination), with no line at the host redshift. SPE redshifts of pieces of nearby galaxies, and SPE_Z_PROB
   for such objects, must not be trusted.

Spectrum format (one BINTABLE per source): WAVELENGTH [Angstrom], SIGNAL [1e-16 erg/s/cm2/A], MASK (bit mask, 0 = good),
QUALITY, VAR [1e-32 ...], NDITH (number of dithers contributing); header FSCALE = 1e-16 is already applied in the unit.
MASK bit values: 1 NOT_USE, 2 LOW_SNR, 4 EXT_PRB, 8 HIGH, 16 LOW, 32 REL_FLUX, 64 ABS_FLUX.

Usage: uv run python demo/04_spectra.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table
from astroquery.esa.euclid import Euclid
from dr1_access import catalogue_zero_point_ujy, default_data_root, run_query

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from plot_style import figure_width_double, use_publication_style  # noqa: E402

figure_dir = Path(__file__).resolve().parents[1] / "figures"
spectra_dir = default_data_root / "spectra"
low_z_galaxy_id = -582334178474562017  # z_SPE = 0.149, H_E ~ 16.2, 2' north-east of NGC 1483
ngc1483_fragment_id = -582049692474919484  # inside NGC 1483's disc, z_SPE = 4.59 with SPE_Z_PROB > 0.99
ngc1483_redshift = 0.00383  # NED systemic velocity ~1149 km/s (used only to mark where host lines would fall)

# Rest-frame vacuum wavelengths [Angstrom] of lines that can enter the red grism (1.2-1.9 micron) at z < 0.6.
near_infrared_lines = {
    r"[S\,\textsc{iii}]": 9533.2,
    r"He\,\textsc{i}": 10833.3,
    r"Pa$\gamma$": 10941.1,
    r"[Fe\,\textsc{ii}]": 12570.2,
    r"Pa$\beta$": 12821.6,
    r"Pa$\alpha$": 18756.1,
    r"H$\alpha$": 6564.6,
}


def fetch_spectrum(source_id: int) -> Table:
    spectra_dir.mkdir(parents=True, exist_ok=True)
    expected = spectra_dir / f"SPECTRA_RGS-dr1 {source_id}.fits"
    if not expected.exists():
        Euclid.get_spectrum(
            ids=str(source_id),
            schema="dr1",
            retrieval_type="SPECTRA_RGS",
            output_file=str(spectra_dir / f"download_{source_id}.fits"),
        )
    return Table.read(expected, hdu=1, unit_parse_strict="silent")


def source_information(source_ids: list[int]) -> Table:
    id_list = ", ".join(str(value) for value in source_ids)
    return run_query(
        "SELECT z.object_id, z.spe_z, z.spe_z_prob, z.spe_rank, m.right_ascension, m.declination, "
        "m.flux_h_templfit, m.flux_detection_total "
        "FROM dr1.spectro_z_spe_galaxy_candidates_wide AS z "
        "JOIN dr1.mer_catalogue_wide_survey AS m ON m.object_id = z.object_id "
        f"WHERE z.object_id IN ({id_list}) AND z.spe_rank = 0"
    )


def plot_spectrum(axis: plt.Axes, spectrum: Table, redshift: float, line_redshift: float, title: str) -> None:
    wavelength = np.asarray(spectrum["WAVELENGTH"], float) / 1e4  # micron
    signal = np.asarray(spectrum["SIGNAL"], float)
    variance = np.asarray(spectrum["VAR"], float)
    # MASK bit values (primary-header dictionary MSK_FLAG_*): 1 NOT_USE, 2 LOW_SNR, 4 EXT_PRB, 8 HIGH, 16 LOW,
    # 32 REL_FLUX, 64 ABS_FLUX. LOW_SNR/EXT_PRB are set over long ranges even for bright galaxies, so only
    # NOT_USE and ABS_FLUX (band edges) pixels are hidden here.
    mask = np.asarray(spectrum["MASK"])
    good = ((mask & (1 | 64)) == 0) & (np.asarray(spectrum["NDITH"]) > 0) & (variance > 0)
    error = np.sqrt(np.where(variance > 0, variance, np.nan))
    shown = np.where(good, signal, np.nan)  # NaN breaks the curve at masked pixels instead of bridging gaps
    axis.fill_between(wavelength, shown - error, shown + error, color="0.8", lw=0, step="mid")
    axis.step(wavelength, shown, where="mid", color="k", lw=0.7)
    top = np.nanpercentile(signal[good], 99.5) * 1.25
    for name, rest in near_infrared_lines.items():
        observed = rest * (1 + line_redshift) / 1e4
        if wavelength[good].min() < observed < wavelength[good].max():
            axis.axvline(observed, color="tab:red", lw=0.6, ls="--")
            axis.text(observed, top * 0.97, name, rotation=90, ha="right", va="top", fontsize=6.5, color="tab:red")
    axis.set_xlim(1.19, 1.90)
    axis.set_ylim(min(0, np.nanpercentile(signal[good], 0.5)), top)
    axis.set_ylabel(r"$f_\lambda$ [$10^{-16}$ erg s$^{-1}$ cm$^{-2}$ \AA$^{-1}$]")
    axis.set_title(title, fontsize=8)


def main() -> None:
    use_publication_style()
    information = source_information([low_z_galaxy_id, ngc1483_fragment_id])
    by_id = {int(row["object_id"]): row for row in information}
    figure, axes = plt.subplots(2, 1, figsize=(figure_width_double, figure_width_double * 0.55), sharex=True)

    row = by_id[low_z_galaxy_id]
    h_magnitude = catalogue_zero_point_ujy - 2.5 * np.log10(float(row["flux_h_templfit"]))
    plot_spectrum(
        axes[0],
        fetch_spectrum(low_z_galaxy_id),
        float(row["spe_z"]),
        float(row["spe_z"]),
        rf"(a) MER {low_z_galaxy_id}: $z_{{\rm SPE}}={float(row['spe_z']):.3f}$ "
        rf"(prob.\ {float(row['spe_z_prob']):.4f}), $H_E={h_magnitude:.1f}$; lines at $z_{{\rm SPE}}$",
    )

    row = by_id[ngc1483_fragment_id]
    plot_spectrum(
        axes[1],
        fetch_spectrum(ngc1483_fragment_id),
        float(row["spe_z"]),
        ngc1483_redshift,
        rf"(b) NGC 1483 disc fragment {ngc1483_fragment_id}: SPE claims $z={float(row['spe_z']):.2f}$ "
        rf"(prob.\ {float(row['spe_z_prob']):.4f}); dashed: host lines at $z={ngc1483_redshift}$ (absent)",
    )
    axes[1].set_xlabel(r"observed wavelength [$\mu$m]")
    figure.tight_layout(h_pad=0.6)
    output = figure_dir / "dr1_spectra_demo.png"
    figure.savefig(output)
    print(f"saved {output}")


if __name__ == "__main__":
    main()
