# Galaxies and fields featured in the DR1 papers (demo targets)

Coordinates are J2000 degrees from the papers' tables or designations (decoded), or Sesame for catalogue names.
"DR1 tile" = tile used in `demo/` (verified to contain data on 2026-11-12). Gallery: `figures/dr1_gallery.png`
(`demo/01_get_cutouts.py`, `demo/02_gallery.py`).

## Gallery targets (one per galaxy type)

| Object | RA, Dec | Type | Paper | DR1 tile (family) | Notes |
|---|---|---|---|---|---|
| NGC 1483 | 58.19837, -47.47752 | barred spiral, D ~ 2' | [Polenta+26](papers/polenta.md) Fig. 4 (NIR background comparison) | 102021980 (wide) and 101287204 (EDF-S deep, 10 visits) | LSB demo target; shredded into 6 big entries (one `parent_id`) + 760 entries at 40"-70" where 356 are expected (see [06](06_catalogues_photometry_morphology.md)); disc fragments get spurious SPE redshifts |
| PGC 61126 | 269.03570, +64.28375 | large disc galaxy in EDF-N | [Romelli+25](papers/q1_romelli_mer.md) Fig. 3 ("breathing" enlarged tile) | 101829770 (deep) | wide-survey mosaic of tile 102158273 is empty there; use deep |
| LVDw 11 (LEDA 166124) | 183.1684, +68.9277 | resolved dwarf irregular, 4.74 Mpc, M_V = -11.3 | [Gatto+26](papers/gatto.md) Table 2 | 102160810 (wide) | next to a bright star with NIR reflection arc and spikes (artefact example) |
| LVDw 9 | 145.3759, +66.0859 | ultra-diffuse dwarf, 4.2 Mpc, mu_V ~ 28.5 | Gatto+26 | 102159089 (wide) | invisible in integrated light at EWS depth: detected only via resolved stars |
| J170734.355+555258.98 | 256.8931, +55.8830 | massive early-type, z = 0.258 (DESI), lens candidate | [Lines+26](papers/lines.md) | 102152112 (wide) | single-band NIR artefacts nearby |
| J022455.052-601235.97 | 36.2294, -60.2100 | edge-on disc with two candidate Einstein rings | Lines+26 Fig. 3m | 102011239 (wide) | |
| J100937.880+724953.06 | 152.4078, +72.8314 | probable collisional ring galaxy ("empty ring") | Lines+26 Fig. C.2 | 102162719 (wide) | |
| J042911.429-204453.48 | 67.2976, -20.7482 | face-on spiral deflector with complete ring | Lines+26 Fig. 4a | 102053409 (wide) | DESI lens and source redshifts |

## Other useful objects from the papers

| Object | RA, Dec | Type | Paper |
|---|---|---|---|
| MCXC J1754.6+6803 | ~268.65, ~+68.05 (from name) | galaxy cluster z = 0.077 (BCG + ICL), Q1 obs. 2683; DR1 deep tile 101838582 | [Bamford+26](papers/q1_icl_processing_bamford.md) Figs. 1-2 |
| 1eRASS J040508.4-464833 | ~61.285, ~-46.809 (from name) | cluster z = 0.37 with ICL shape measurement | [Kolcu+26](papers/q1_icl_halo_shapes_kolcu.md) Fig. 2 |
| Abell 2280 | 265.87663, +63.69491 | cluster z = 0.326 with red giant arc (EDF-N; deep tiles 101828492/3) | [Bergamini+26](papers/bergamini.md) |
| SPT-CLJ0411-4819 | 62.79574, -48.32765 | cluster z = 0.424 (EDF-S) | Bergamini+26 |
| PS1J1821+7130 | 275.41843, +71.50267 | galaxy-galaxy Einstein ring, lens z = 0.235, H_E = 17.1; tile 102162119 | Bergamini+26 |
| WHJ181607.9+681651 | 274.03285, +68.28095 | quad lens, early-type deflector z_ph = 0.68 | Bergamini+26 |
| J045417.497-340950.95 | 73.5729, -34.1642 | double-source-plane lens | Lines+26 |
| J023656.861-583041.95 | 39.2369, -58.5117 | bright extended arcs | Lines+26 |
| J094904.876+652707.32 | 147.2703, +65.4520 | compact red deflector z = 0.805 | Lines+26 |
| J171525.314+583731.15 | 258.8555, +58.6253 | inclined disc z = 0.302 | Lines+26 |
| J030313.592-580619.97 | 45.8066, -58.1055 | lens-modelling demonstration system | [Nightingale+26](papers/nightingale.md) |
| J100106.88+015815.4 | 150.2787, +1.9710 | face-on spiral z = 0.528 (H-alpha map) | [Gabarra+26](papers/gabarra.md) |
| J100022.52+023014.2 | 150.0938, +2.5039 | interacting system z = 0.751 | Gabarra+26 |
| NGC 4236 | 184.17549, +69.46257 | large nearby spiral (Sesame); wide tile 102161072 | host of LVDw 10/11 region (Gatto+26) |
| Ursa Minor II, Fornax 7, Eridanus V | (196.1542, +75.5724), (38.8244, -33.9567), (28.8623, -47.7105) | new Milky Way satellites (20-166 kpc) | Gatto+26 |
| LVDw 1, 2, 3-12 | see [gatto](papers/gatto.md) | Local Volume dwarfs 3-5.5 Mpc | Gatto+26 |

## Fields

| Field | RA, Dec | Notes |
|---|---|---|
| EDF-N | 269.733, +66.02 | 11 visits; no EWS underneath; contains SelfCal (268.813, +65.29) |
| EDF-S | 61.241, -48.42 | 10 visits; overlaps EWS; low extinction |
| EDF-F | 52.932, -28.09 | 2 visits; contains CDFS (53.118, -27.81) |
| COSMOS | 150.120, +2.21 | 27 visits |
| AEGIS | 214.827, +52.82 | 18 visits, no EXT |
| ILS-WAVES-S | 355.7, -31.2 | PDC science field chosen partly for LSB dwarfs |
| EMDS-HSC-HL-1..4 | ~(209-237, +44) | medium-deep, overlap HSC-SSP |

## Picking your own targets

1. Check coverage: `SELECT ... FROM dr1.mosaic_product WHERE INTERSECTS(CIRCLE(ra, dec, 1e-4), fov) = 1` with the
   family selection ([03_data_access](03_data_access.md)), then look at a cutout (zeros = no data).
2. EWS footprint: ~1400 deg^2 south (mostly DES area, RA ~ 0-90 deg and the south cap) + ~500 deg^2 north (UNIONS
   area); exact coverage map: https://www.cosmos.esa.int/web/euclid/euclid-dr1-expected-coverage and the VMPZ
   footprint maps.
3. Large nearby galaxies (> 2') are in the special-object list but not specially processed in DR1: check tile edges.
