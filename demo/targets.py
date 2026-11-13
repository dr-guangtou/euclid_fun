"""Demo targets: galaxies of different types that are featured in the DR1 (and Q1-ICL) papers.

Coordinates: from the papers' tables or names (J2000 designations), or Sesame for NGC/PGC/LEDA names.
See kb/12_galaxy_examples.md for the context of each object.
"""

from dr1_access import Target, deep_survey_selection, wide_survey_selection

gallery_targets = [
    Target(
        "NGC 1483",
        58.19837,
        -47.47752,
        "barred spiral",
        "Polenta et al. 2026 (DR1 NIR processing), Fig. 4: NIR background-subtraction comparison",
    ),
    Target(
        "PGC 61126",
        269.03570,
        64.28375,
        "large disc, EDF-N deep",
        "Romelli et al. 2025 (Q1 MER), Fig. 3: large galaxy handled with an enlarged ('breathing') tile",
    ),
    Target(
        "LVDw 11 (LEDA 166124)",
        183.1684,
        68.9277,
        "resolved dwarf (LSB)",
        "Gatto et al. 2026 (DR1 LSB stellar systems), Table 2: 4.74 Mpc, M_V=-11.3",
    ),
    Target(
        "LVDw 9",
        145.3759,
        66.0859,
        "ultra-diffuse dwarf",
        "Gatto et al. 2026, Table 2: 4.2 Mpc, mu_V~28.5 mag/arcsec^2",
    ),
    Target(
        "J170734+555259",
        256.8931,
        55.8830,
        "early-type, $z=0.26$",
        "Lines et al. 2026 (ECLIPSE A), lens candidate with DESI z_lens=0.258",
    ),
    Target(
        "J022455-601236",
        36.2294,
        -60.2100,
        "edge-on disc",
        "Lines et al. 2026 (ECLIPSE A), Fig. 3m: double ring around an edge-on disc",
    ),
    Target(
        "J100937+724953",
        152.4078,
        72.8314,
        "collisional ring galaxy",
        "Lines et al. 2026 (ECLIPSE A), Fig. C.2: 'empty ring', probable collisional ring",
    ),
    Target(
        "J042911-204453",
        67.2976,
        -20.7482,
        "face-on spiral, lens",
        "Lines et al. 2026 (ECLIPSE A), Fig. 4a: face-on spiral deflector with complete ring",
    ),
]

# Cutout half-size per target (arcmin) and the mosaic family to use.
cutout_radius_arcmin = {
    "NGC 1483": 1.6,
    "PGC 61126": 1.6,
    "LVDw 11 (LEDA 166124)": 0.8,
    "LVDw 9": 0.6,
    "J170734+555259": 0.25,
    "J022455-601236": 0.2,
    "J100937+724953": 0.3,
    "J042911-204453": 0.2,
}
mosaic_selection = {name: wide_survey_selection for name in cutout_radius_arcmin}
# PGC 61126 lies in the Euclid Deep Field North: the wide-survey (DATA_RELEASE) mosaic of tile 102158273 has only
# zeros there (footprint polygon larger than the data), so the deep stack is used instead.
mosaic_selection["PGC 61126"] = deep_survey_selection

# Low-surface-brightness demo: NGC 1483 has both a wide-survey tile and an EDF-South deep stack.
lsb_target = gallery_targets[0]
lsb_wide_tile = 102021980
lsb_deep_tile = 101287204
lsb_selections = {"wide": (wide_survey_selection, lsb_wide_tile), "deep": (deep_survey_selection, lsb_deep_tile)}

# Intra-cluster light example from the Q1 cluster-team papers (EDF-North deep field).
icl_cluster = Target(
    "MCXC J1754.6+6803",
    268.65,
    68.05,
    "galaxy cluster z=0.077 (BCG + ICL)",
    "Bamford et al. 2026 (Q1 ICL processing), Figs. 1-2; coordinates from the designation",
)
