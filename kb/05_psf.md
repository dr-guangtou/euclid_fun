# PSFs in Euclid DR1

> **Key points**
> - For fitting a **MER mosaic** use the MER-propagated PSF (`GRID-PSF-VIS`, `CATALOG-PSF-NIR-*` etc.), not the per-exposure VIS/NIR models: stacking and bilinear resampling widen the PSF by 30-35% (I_E FWHM ~0.20" in the mosaic vs ~0.14-0.16" in single frames).
> - DR1 MER stamps are **not renormalised**: the stamp sum S is ~0.958 in I_E (16-84%: 0.947-0.970 in the tile tested here) and ~0.985 in H_E. The missing 4% (1.5% in NIR) is flux beyond the stamp (VIS grid stamps 21 px = 2.1"; NIR catalogue stamps 45 px = 4.5"). There are no PSF wings beyond that in any DR1 product.
> - The VIS PSF model underestimates the true PSF size (found early 2026) and does not yet meet the shear requirement; MER FWHMs agree with Gaia stars to a few per cent. The NIR stack PSFs are the weakest NISP product.
> - For galaxies within a few arcsec, the nearest `GRID-PSF` node (nodes every 120 px = 12", so at most ~8.5" away) is adequate; a tested code sketch is in section 7. For haloes and outskirts build your own PSF from stars or use the ERO extended PSF.
> - Facts marked "verified locally" were measured on tile 102021980 (files in `~/data/euclid/dr1_demo/tiles/102021980/`).

File structure and units are from [data_model/verified_on_archive.md](data_model/verified_on_archive.md) (it overrides papers and DPDD).
Pipeline context: [04_imaging_processing.md](04_imaging_processing.md); LSB background and wings: [10_low_surface_brightness.md](10_low_surface_brightness.md).

## 1. Inventory of PSF products

| Level | Product (archive `stype` / file) | Content | Size and sampling | Source |
|---|---|---|---|---|
| VIS, per exposure | `PSF` file attached to `DpdVisCalibratedQuadFrame` (PSFEx model; new in DR1 as part of the quad-frame product) | PSFEx model per quadrant, 2nd-degree polynomial in position, no colour dependence, built from self-cal field short exposures | 21-px stamps at native 0.1" (Q1); Gaussian FWHM 0.157-0.164" (mean 0.158") in Q1 | [McCracken+26](papers/mccracken.md) p. 3; [McCracken+26 Q1](papers/q1_mccracken_vis.md) p. 8-9 |
| VIS, stack | `PSF` file with `STK` (EDS help page "Images" lists it) | PSF associated with the stacked frame | not documented in the local sources | EDS help "Images" |
| NIR, per dither, global | `GLOBAL-PSF-I` (image) / `-M` (PSFEx `.psf`) = `PsfStorage` | PSF derived in advance from the 76-dither self-calibration field, constant within each of the 16 detectors | oversampled x6 (0.05"/px); "extended" model 141/6 x 141/6 detector px = ~23.5 px = ~7" | [Polenta+26](papers/polenta.md) p. 5, 19; [da Silva+26](papers/dasilva.md) p. 3 |
| NIR, per dither, single | `CAL-PSF-I` / `-M` = `PsfSingleStorage` (new in DR1) | PSF from the calibrated image itself | oversampled x6; 61/6 x 61/6 detector px = ~10 px = ~3" | Polenta+26 p. 19; da Silva+26 p. 3 |
| NIR, stack | `PSF-I` / `PSF-M` (one file per band) | PSFEx model on the stacked frame | oversampled x6; ~3" | EDS help "Images"; da Silva+26 p. 3-4 |
| MER, catalogue | `EUC_MER_CATALOG-PSF-<band>_TILE*` | HDU1 mosaic of stamps (one per catalogue object, mostly), HDU2 table of positions | VIS/NIR on the 0.1" mosaic grid; NIR-H stamps **45 x 45 px = 4.5"**, `STMPSIZE = 45` (verified locally) | verified_on_archive.md; [Kuemmel+26](papers/kuemmel.md) p. 9 (limit 5") |
| MER, grid | `EUC_MER_GRID-PSF-<band>_TILE*` | HDU1 "PSF image" with the **same 19200 x 19200 grid and WCS as the mosaic**, stamps at nodes every 120 px; HDU2 table `x, y, FWHM` | VIS: **21 x 21 px = 2.1"**, `STMPSIZE = 21`, `BUNIT = ADU`, 25 597 rows (of 160 x 160 = 25 600 nodes), centres at x, y = 61, 181, ... 19 141 (verified locally) | verified_on_archive.md |
| Calibration | MDB physical-optics PSF library | 2160 shapes, 512/6 px wide; tests only, not delivered | | da Silva+26 p. 3, 8 |

Notes:

- The DPDD says there is no file called `GRID_PSF` and gives `STMPSIZE` without a value ([dpdd_mer.md](data_model/dpdd_mer.md)); the archive and the verified structure above are authoritative. Which bands exist as `GRID-PSF` and which as `CATALOG-PSF` was not checked for every band: only `GRID-PSF-VIS` and `CATALOG-PSF-NIR-H` were opened.
- The mapping of `GLOBAL-PSF` to the 7" "extended" model and `CAL-PSF` to the 3" "simplified" model is an inference from Polenta+26 p. 19 and da Silva+26 p. 2-3; da Silva+26 states that the user-facing mapping is not specified. Check the headers (`STMPSIZE`/`PSF_SAMP` equivalents) before relying on it.
- Q1 note: ten Q1 observations lack a PSF file (all Q1 observations share one PSF file); not a DR1 issue.
- MER builds mosaic PSFs by running SWarp on empty images with the input stamps injected at source positions, so the stack, weights, WCS and flags are included. Stamps are propagated three times with different source subsets to avoid overlap; >80% of sources get their own stamp, the rest take the nearest ([Romelli+26](papers/q1_romelli_mer.md) p. 8). Convolution kernels between bands use Wiener filtering (Romelli+26 p. 8).

## 2. Normalisation (DR1 change)

- The stamp sum S should be 1 for a complete PSF; cut stamps have S < 1. Q1 renormalised every stamp to S = 1, causing up to ~10% photometric offsets in bands with large PSFs (Pan-STARRS i, FWHM > 5"). **DR1 does not renormalise** (Kuemmel+26 p. 10).
- Measured S: I_E median 0.957 (NMAD 0.011), Y/J/H_E ~0.984-0.987 (NMAD 0.005-0.007), DECam 0.97-0.99, Pan-STARRS i ~0.880 (Kuemmel+26 Table 4, tiles 102020534 and 102159192).
- Verified locally (tile 102021980): all 25 597 VIS stamps: median S = 0.958, 16-84% = 0.947-0.970, 1-99% = 0.933-0.986; **9 stamps have S < 0.9** (minimum 0.411, with a spurious `FWHM` = 0.029"), so screen the stamps. H_E catalogue stamps (every 7th, 12 689 of 88 820): median S = 0.984, 16-84% = 0.979-0.989, 1% quantile 0.965, minimum 0.55.
- First-order effects on MER fluxes (Kuemmel+26 p. 10): A-PHOT and T-PHOT in band B: F_new = F_old / (S(B) / S(detection band)); Sersic: F_new = F_old / S(B); VIS PSF fitting: F_new = F_old / S(I_E). `FLUX_DETECTION_TOTAL` does not depend on the PSF. The I_E normalisation (~1% NMAD tile to tile) limits DR1 absolute photometry; I_E-based colours cancel it. The authors caution that non-normalised PSFs are not the best choice for large extended sources (p. 10).
- Implication for your own fits: if you convolve a model with the stamp as delivered, the model flux is reduced by S (~4% in I_E); the fitted total flux then absorbs the missing light. Decide explicitly: either keep S and correct fluxes (Kuemmel+26 route), or divide by the sum, which assumes the missing ~4% is distributed like the stamp although it really sits in the wings.

## 3. FWHM values, sizes and radii

| Stage | I_E | Y_E | J_E | H_E | Source |
|---|---|---|---|---|---|
| VIS single frame, median over FPA (`FWHM_IMAGE` of stars) | 0.140" (16-84%: 0.135-0.150; edge quadrants up to ~0.176; requirement < 0.18") | | | | McCracken+26 p. 9 |
| VIS Q1 PSFEx model (Gaussian fit) | 0.158" | | | | Q1 McCracken+26 p. 8 |
| NIR single dither (PSFEx, Table 1) | | 0.35" (r_EE50 0.22-0.225", r_EE80 0.375-0.387") | 0.35" (0.24-0.246", 0.44-0.45") | 0.365-0.374" (0.276-0.281", 0.55-0.56") | da Silva+26 p. 5 |
| NIR stack PSF (obs. 2955, Table 1) | | 0.465" | 0.488" | 0.511" | da Silva+26 p. 5 |
| **MER mosaic, EWS median (VMPZ maps)** | **0.2028"** | **0.488"** | **0.514"** | **0.559"** | [Odier+26](papers/odier.md) Table 2 |
| MER mosaic, Gaia stars (Q1) | 0.204" (propagated 0.203; range 0.197-0.212) | 0.492" (prop. 0.475) | 0.513" (0.504) | 0.552" (0.542) | Romelli+26 p. 9 |
| Local tile 102021980 (stamp `FWHM` table column, Gaussian fit) | median 0.2014" (16-84%: 0.192-0.210; 1-99%: 0.176-0.221) | | | median 0.559" (16-84%: 0.537-0.579) | verified locally |

- Mosaic PSFs are 30-35% wider than the input PSFs because of stacking; the bilinear kernel adds ~15% over Lanczos-3 (Romelli+26 p. 8). The single-frame VIS value (0.14") and the mosaic value (0.20") are therefore different stages of the same data, not an inconsistency. Use the one that corresponds to the image you fit.
- `FWHM` columns in the PSF tables are Gaussian-fit FWHMs in arcsec (DPDD). The header `FWHM` of the grid image is the central stamp's value (0.2109" in our tile).
- Pixel sampling: the MER VIS PSF has FWHM ~2 pixels of 0.1"; the stamps are on the data grid (no oversampling). PSFEx models are oversampled x6 for NIR (0.05") but resampled to 0.1" in MER.
- Other quoted NIR numbers: 6-pixel (1.8") aperture encloses 92-94% (single dither), aperture-correction factors 1.06/1.07/1.083 for Y/J/H; PSF-fit centroid error < 0.003 detector px mean, < 0.03 std (da Silva+26 p. 7-8). Imaging requirements: NIR r_EE50 < 0.4", r_EE80 < 0.7"; VIS PSF ellipticity <~ 0.025 and (R_PSF/R_ref)^2 ~ 1.9 against a requirement of 4 ([Schirmer+26a](papers/schirmer-calibration.md) p. 23, Table A.1).
- Dunn+26 ([dunn.md](papers/dunn.md)) uses 0.16" as the VIS PSF FWHM for a size cut and Nightingale+26 ([nightingale.md](papers/nightingale.md)) quotes ~0.16": these correspond to the single-frame scale, not to the 0.20" of the mosaic stamps. For mosaic fits, resolved-size cuts should use ~0.20".

## 4. Variation with position, time and colour

**Position.** VIS: FWHM varies by more than 20% across a tile (Romelli+26 Q1 p. 16-17); spatial standard deviation in EWS ~0.004" (I_E) and ~0.01" (NISP) (Odier+26 Table 2); in our tile the VIS stamp FWHM 16-84% range is 0.192-0.210", i.e. about +-4%. FWHM is larger in tile-overlap regions where several exposures combine (Odier+26 p. 6-8). NIR: PSF constant within each detector, variable between detectors, but detector-to-detector differences are small (da Silva+26 p. 3, 12); the mosaic mixes detectors and dither orientations, so it is a spatial average. VMPZ-ID maps give FWHM at survey level but interpolated from sparse bright stars (Odier+26 p. 4).

**Time.** VIS PSF depends on the telescope thermal state: defocus 0.32-0.56 um, driven by solar aspect angle with a 21-46 h response and ~3 days to settle after a large attitude step ([Schirmer+26b](papers/schirmer-spacecraft.md) p. 7-9). The I_E mosaic FWHM drifted from 0.210" to ~0.203" in ILS-WAVES-S after the de-focused phase-diversity campaign (Kuemmel+26 p. 14). Data from that campaign (Dec 2023-Feb 2024) can have evolving PSFs (Explanatory Supplement 4.4.1). NIR: ellipticity within 0.05 over >180 days; encircled-energy differences between visits (Jan vs Apr 2025) exceed detector-to-detector differences (da Silva+26 p. 13).

**Colour.** The VIS band is broad: red stars (BP-RP > 1.5) have median FWHM 3.3% larger than blue stars in the same quadrant (McCracken+26 p. 9, Fig. 10), and centroids shift by a few mas (p. 7). DR1 PSF models have **no colour dependence**: neither the VIS PSFEx model, nor the MER propagation (Romelli+26 p. 8), nor the NIR models (da Silva+26 p. 14, SED-dependent PSFs are future work). Galaxies are redder/different from stars and change PSF with radius (colour gradients). The shear pipeline uses its own colour-dependent PSF model (Nightingale+26 p. 3), which is not part of the DR1-Foundation imaging products.

## 5. Accuracy and known problems

| Issue | Detail | Source |
|---|---|---|
| **VIS PSF model too small** | underestimates the true PSF size (found early 2026): compromised shear, hence shear released June 2027; the VIS PSF model requirements are not yet met | [Aussel+26](papers/aussel.md) p. 4; Schirmer+26a p. 3 |
| Per-quadrant over-fit | 2nd-degree polynomial per quadrant gives inconsistent normalisation between quadrants, hence unreliable `MAG_MODEL`; first-order PSF planned for DR2 | McCracken+26 p. 11 |
| Q1 VIS model | slightly larger and rounder than reality due to undersampling | Q1 McCracken+26 p. 8 |
| MER vs Gaia | VIS +-2% (Q1); percent level for VIS and NIR in DR1, sub-percent EXT; tiles with > 5% discrepancy flagged but not invalidated | Romelli+26 p. 17; Kuemmel+26 p. 7 |
| NIR PSF fidelity | NIR FWHM now agrees with Gaia stars to ~1% (Q1: 1.75-3.5% off; the sign differs between papers, see [04_imaging_processing.md](04_imaging_processing.md)) | Kuemmel+26 p. 4 |
| **NIR stack PSFs** | not optimised: encircled energy reaches 100% at a wrong radius (Y, J), first diffraction rings do not match stacked stamps, small negative pixels (> -0.0015 Y), only ~600-800 stars and few basis vectors | da Silva+26 p. 4, 11, 14 |
| **No wings** | NIR stamps ~3" (stack/single) or ~7" (extended single-dither); MER stamps <= 5" (2.1" VIS grid, 4.5" NIR catalogue). 1-2% (Y 1%, J 1.8%, H 2.1%) of the NIR flux lies outside even the 7" stamp (diffraction spikes); no scattered-light or ghost model | da Silva+26 p. 8; Kuemmel+26 p. 9 |
| **Brighter-fatter effect** | corrected in VIS pixels (11 x 11 kernel; no residual detected); **not corrected in NISP**, so bright stars have inflated FWHM and flux | Q1 McCracken+26 p. 7-8; da Silva+26 p. 12 |
| NIR PSF-fit photometry | `MAG_PSF - MAG_APER` offset ~0.05 mag with sub-pixel dependence (IPC, IPS, normalisation); recommended correction for point sources | da Silva+26 p. 10 |
| Within-detector variation | none in NIR models (PSFVAR_DEGREES = 0); IPC/IPS kernels simplified and constant over the FoV | da Silva+26 p. 3-4 |
| Pan-STARRS i | extended PSF tails (> 5"), S ~ 0.88, local defects | Kuemmel+26 p. 10; Corcho-Caballero+26 |
| Sparse stamps | EXT PSF models are not sampled at every detection (nearest used); no Poisson term in EXT noise | [Corcho-Caballero+26](papers/corcho-caballero.md) p. 14 |
| Bad stamps | verified locally: 9 of 25 597 VIS grid stamps with S < 0.9 and one with `FWHM` = 0.029" | verified locally |

Practical test of PSF quality: Kuemmel+26 compare the stamp FWHM with Gaia stars per tile; do the same on your own stars (non-saturated Gaia stars with I_E ~ 18-21, classified as stars) before trusting the stamp for a specific tile.

## 6. Extended wings and own PSFs

**ERO extended PSF (Cuillandre+25, A&A 697, A6).** Used by [Bamford+26](papers/q1_icl_processing_bamford.md) to convolve mock clusters ("includes large-scale wings") and noted by Schirmer+26b as showing a nearly diffraction-limited PSF; the ERO LSB reduction by the same authors reaches 28.3 mag/arcsec^2 in I_E (3 sigma, 10" x 10", per Bamford+26). The paper is not in the local corpus: its profile, radial range and normalisation are **not documented in this knowledge base**; fetch it before use. No DR1 product provides a PSF wing model.

**Building your own from stars** (general practice, not an Euclid-documented recipe):

1. Work on the product you fit: stars in the `BGSUB` (+ `BGMOD` if you restored it) mosaic if you fit mosaic cutouts, so that stacking, bilinear kernel and MER sky are included; use calibrated frames for single-frame fits.
2. Choose isolated, unsaturated Gaia stars of similar colour to your galaxy (I_E-band PSF width depends on colour by 3-5%); the Euclid PSF fields use stars with 17.5 < I_E < 21 (Schirmer+26a p. 10). Avoid very bright stars in NIR (brighter-fatter effect, persistence, arcs) and stars with ghosts or spikes in the stamp.
3. Subtract a local sky from a large annulus; stack stars in sub-pixel-aligned or centroid-aligned stamps. For wings extend the radius by combining stamps from stars of different brightness (bright stars for the outer profile, faint ones for the core) and normalise the profile in an annulus.
4. Cross-check the result against the MER stamp inside 2-4" and the encircled-energy numbers of section 3.
5. Wings matter for stellar haloes and ICL, not for compact galaxies; the bright-star wing level is the limit for LSB measurements beyond ~10" ([10_low_surface_brightness.md](10_low_surface_brightness.md)).

## 7. Recipe: a PSF at a galaxy position for Sersic / bulge-disc fits

1. **Pick the tile** containing the galaxy (choose the tile where it is farthest from the border if it sits in the 2' overlap; `GRID-PSF` and the mosaic share the same grid, so pixel coordinates are identical).
2. **Sky to pixel**: use the `BGSUB` mosaic header WCS; astropy returns 0-based pixels, the stamp table uses **1-based FITS pixels** on the mosaic grid.
3. **Nearest node**: nodes are at x, y = 61 + 120 k (k = 0..159), spacing 12"; the largest possible distance is ~85 px (8.5"). For galaxies below ~10" the nearest stamp is adequate; for larger objects, or when position dependence matters, interpolate the four surrounding stamps bilinearly in (x, y) (FWHM changes by only a few per cent per 12", but stamps are not guaranteed to be smooth: check).
4. **Cut the stamp**: 21 x 21 pixels centred on the node pixel (0-based index = node - 1); the PSF peak is at index (10, 10) in the stamp (verified: peak at the central pixel, centroid within 0.05 px).
5. **Screen**: reject the node if the stamp sum is < 0.9 or the table `FWHM` is outside ~0.15-0.25"; use the next-nearest node. Decide on normalisation (section 2) and keep S to correct the fluxes.
6. **Use it**: pass the stamp to your fitter (e.g. GALFIT, pysersic, SE++, ProFit-like code) at the **data pixel scale** (0.1"). The PSF is centred on a pixel; for sub-pixel galaxy centres the model convolution is only approximate (PSF is barely sampled at 2 px FWHM).
7. **NIR bands**: use the `x, y` columns of the `CATALOG-PSF-NIR-*` table (mosaic pixel of the object), cut a 45 x 45 stamp at (`x_center`, `y_center`) (also 1-based), choose the nearest stamp to your galaxy, or the stamp of the catalogue object itself (it is mostly one stamp per object).
8. **Several bands**: because the EXT PSFs are not homogenised and the NIR PSFs are 2.5-3x wider than I_E, convolve the I_E model with each band's PSF; or fit the bands jointly with a shared structural model.
9. **Validate** on 5-10 unsaturated stars near the galaxy: fit the star with the stamp as model and compare residuals.

Code sketch (tested on tile 102021980: stamp 21 x 21, sum 0.939 at the tile centre, table FWHM 0.211", peak at (10, 10); three positions gave nearest-node offsets of 59-83 px; the NIR branch is untested):

```python
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS


def extract_nearest_grid_psf_stamp(grid_psf_path, mosaic_path, galaxy_coordinate):
    """Return (stamp, info) for the GRID-PSF node nearest to a sky position.

    Pixel coordinates in the stamp table are 1-based FITS positions on the mosaic grid.
    The memmap keeps the 1.5 GB PSF image out of memory; only one stamp is read.
    """
    with fits.open(mosaic_path, memmap=True) as mosaic_hdul:
        mosaic_wcs = WCS(mosaic_hdul[0].header)
    galaxy_x_zero_based, galaxy_y_zero_based = mosaic_wcs.world_to_pixel(galaxy_coordinate)
    galaxy_x_fits = float(galaxy_x_zero_based) + 1.0
    galaxy_y_fits = float(galaxy_y_zero_based) + 1.0

    with fits.open(grid_psf_path, memmap=True) as psf_hdul:
        psf_image_hdu = psf_hdul[1]          # "PSF image", 19200 x 19200
        stamp_table = psf_hdul[2].data       # columns x, y, FWHM
        stamp_size = int(psf_image_hdu.header["STMPSIZE"])   # 21 for VIS
        half_size = stamp_size // 2

        node_x_fits = np.asarray(stamp_table["x"], dtype=float)
        node_y_fits = np.asarray(stamp_table["y"], dtype=float)
        squared_distance = (node_x_fits - galaxy_x_fits) ** 2 + (node_y_fits - galaxy_y_fits) ** 2
        nearest_index = int(np.argmin(squared_distance))

        center_x_zero_based = int(round(node_x_fits[nearest_index])) - 1
        center_y_zero_based = int(round(node_y_fits[nearest_index])) - 1
        psf_stamp = np.array(
            psf_image_hdu.data[
                center_y_zero_based - half_size : center_y_zero_based + half_size + 1,
                center_x_zero_based - half_size : center_x_zero_based + half_size + 1,
            ],
            dtype=float,
        )
        info = {
            "node_x_fits": node_x_fits[nearest_index],
            "node_y_fits": node_y_fits[nearest_index],
            "offset_pixels": float(np.sqrt(squared_distance[nearest_index])),
            "fwhm_arcsec": float(stamp_table["FWHM"][nearest_index]),
            "stamp_sum": float(psf_stamp.sum()),
        }
    return psf_stamp, info


# usage (all file names from dr1.aux_mosaic / dr1.mosaic_product):
# stamp, info = extract_nearest_grid_psf_stamp(grid_psf_path, bgsub_mosaic_path, SkyCoord(ra, dec, unit="deg"))
# if info["stamp_sum"] < 0.9 or not 0.15 < info["fwhm_arcsec"] < 0.25:
#     ...  # choose another node
# normalised_stamp = stamp / stamp.sum()   # optional; see section 2
#
# NIR (untested sketch): same logic with table columns x, y and centres x_center, y_center,
# stamp size 45, e.g. nearest = argmin((table["x"] - gx) ** 2 + (table["y"] - gy) ** 2);
# stamp = image[yc - 1 - 22 : yc - 1 + 23, xc - 1 - 22 : xc - 1 + 23]  with xc, yc = x_center, y_center.
```

Run it with `uv run python -I script.py` and keep the PSF file under a data directory (not the code directory).

## 8. What to cite

- PSF models: [da Silva+26](papers/dasilva.md) (NISP-P), [McCracken+26](papers/mccracken.md) and McCracken+26 Q1 (VIS); the VIS PSF model paper (Miller et al., in prep.) is not yet available.
- MER propagation and normalisation: [Kuemmel+26](papers/kuemmel.md) (Sect. 4) and [Romelli+26](papers/q1_romelli_mer.md).
- Survey-level FWHM: [Odier+26](papers/odier.md). Thermal/PSF drivers: [Schirmer+26b](papers/schirmer-spacecraft.md), [Schirmer+26a](papers/schirmer-calibration.md).
- Extended wings: Cuillandre et al. 2025 (ERO), via [Bamford+26](papers/q1_icl_processing_bamford.md).
- Use of the MER PSF for lens-light/Sersic modelling: [Nightingale+26](papers/nightingale.md); Sersic reliability: [Dunn+26](papers/dunn.md).
