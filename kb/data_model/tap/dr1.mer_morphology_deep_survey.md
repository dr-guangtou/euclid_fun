# TAP table `dr1.mer_morphology_deep_survey`



| Column | Type | Unit | UCD | Indexed | Description |
|---|---|---|---|---|---|
| `disk_sersic_disk_radius_err` | double | arcsec |  | 0 | Error of the disk radius |
| `peculiar_yes` | double | NA |  | 0 | Dirichlet param. of question identifying peculiar galaxies (visually, highly disturbed or otherwise unusual, without companion) having response 'Yes' |
| `smooth_or_featured_artifact_star_zoom` | double | NA |  | 0 | Dirichlet param. of question 'Is the galaxy smooth, featured/disk, or an artifact?' having response 'Artifact, Star, or Bad Zoom' |
| `bulge_size_none` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have a bulge, and if so, how visually obvious?' having response 'None' |
| `spiral_winding_loose` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy has spiral arms, how tightly wound are they?' having response 'Loose' |
| `disk_sersic_sersic_radius_err` | double | arcsec |  | 0 | Error of the Sersic radius |
| `edge_on_bulge_boxy` | double | NA |  | 0 | Dirichlet param. of question 'What shape is the bulge in the edge-on disk' having response 'Boxy' |
| `disk_sersic_disk_axis_ratio_err` | double | NA |  | 0 | Error of the disk axis ratio |
| `disk_sersic_angle` | double | deg |  | 0 | Position angle of Disk+Sersic |
| `edge_on_bulge_rounded` | double | NA |  | 0 | Dirichlet param. of question 'What shape is the bulge in the edge-on disk' having response 'Rounded' |
| `basic_download_data_oid` | long |  |  | 1 |  |
| `bulge_size_moderate` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have a bulge, and if so, how visually obvious?' having response 'Moderate' |
| `disk_sersic_disk_axis_ratio` | double | NA |  | 0 | Axis ratio of the disk |
| `sersic_sersic_vis_axis_ratio_err` | double |  |  | 0 |  |
| `lopsided_no` | double | NA |  | 0 | Dirichlet param. of question 'Is the galaxy lopsided?' having response 'No' |
| `disk_sersic_sersic_index` | double | NA |  | 0 | Sersic index |
| `bulge_size_small` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have a bulge, and if so, how visually obvious?' having response 'Small' |
| `major_merger_stage` | short | NA |  | 0 | The most likely merger stage of the major merger |
| `sersic_visnir_iterations` | int |  |  | 0 |  |
| `concentration_err` | double | NA |  | 0 | Concentratrion error |
| `gini` | double | NA |  | 1 | It is a statistic parameter based on the Lorentz curve that presents the cumulative distribution function of galaxy's pixel i values |
| `spiral_arm_count_cant_tell` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy has spiral arms, how many?' having response 'Can't tell' |
| `concentration` | double | NA |  | 1 | This parameter, simply referred to as the concentration, is defined as the logarithm of the ratio between circular radii containing 80% and 20% of the total flux |
| `clump_count_any_threshold` | short | NA |  | 0 | Number of clumps detected before applying confidence threshold |
| `flux_radius_err` | double |  |  | 0 |  |
| `sersic_sersic_nir_axis_ratio` | double |  |  | 0 |  |
| `major_merger_stage_probability` | double | NA |  | 0 | The probability of the most likely merger stage |
| `sersic_sersic_vis_radius_err` | double |  |  | 0 |  |
| `moment_20_err` | double | NA |  | 0 | Moment of light error |
| `sersic_ext_iterations` | int |  |  | 0 |  |
| `sersic_visnir_duration` | double |  |  | 0 |  |
| `clump_count_unusual_above_threshold` | short | NA |  | 0 | Number of 'unusual' (e.g. color, shape) clumps detected after applying confidence threshold |
| `object_id` | long | NA |  | 1 | Euclid unique source identifier |
| `has_spiral_arms_no` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have spiral arms?' having response 'No' |
| `t_type` | double | NA |  | 0 | T-Type regression model, from Dominguez Sanchez+2022 |
| `disk_sersic_flags` | long | NA |  | 0 | Flags from the fit |
| `moment_20` | double | NA |  | 1 | It is defined as a normalized second-order moment of the 20% brightest pixels of the galaxy. This parameter can trace the spatial distribution of any bright core, bar, spiral arm, and off-centre star cluster |
| `spiral_arm_count_more_than_4` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy has spiral arms, how many?' having response 'More than 4' |
| `disk_edge_on_yes` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy appear to be an edge-on-disk?' having response 'Yes, edge-on-disk' |
| `bulge_size_large` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have a bulge, and if so, how visually obvious?' having response 'Large' |
| `sersic_angle` | double | deg |  | 0 | Position angle of the Sersic |
| `spiral_winding_medium` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy has spiral arms, how tightly wound are they?' having response 'Medium' |
| `flux_radius` | double |  |  | 0 |  |
| `asymmetry` | double | NA |  | 1 | The asymmetry quantifies the degree to which the galaxy flux is rotationally symmetric. It is obtained by subtracting from the original image, the flipped galaxy (rotated by 180deg) |
| `smooth_or_featured_smooth` | double | NA |  | 0 | Dirichlet param. of question 'Is the galaxy smooth, featured/disk, or an artifact?' having response 'Smooth' |
| `disk_sersic_sersic_index_err` | double | NA |  | 0 | Error of the Sersic index |
| `has_spiral_arms_yes` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have spiral arms?' having response 'Yes' |
| `disk_sersic_duration` | double | s |  | 0 | Duration of the fit |
| `merging_merger` | double | NA |  | 0 | Dirichlet param of question 'Is the galaxy visually disturbed or merging?' having response 'Merger' |
| `agn_no` | double | NA |  | 0 | Dirichlet param. of question asking if the galaxy has a central PSF-like (very) bright spot, for negative response |
| `bar_weak` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have a bar, and if so, how strong?' having response 'Weak' |
| `disk_sersic_iterations` | int | NA |  | 0 | Number of iterations from the fit |
| `peculiar_no` | double | NA |  | 0 | Dirichlet param. of question identifying peculiar galaxies (visually, highly disturbed or otherwise unusual, without companion) having response 'No' |
| `major_merger_stage_uncertainty` | double | NA |  | 0 | Uncertainty on the probability of the most likely merger stage |
| `sersic_sersic_vis_radius` | double |  |  | 0 |  |
| `disk_sersic_reduced_chi2` | double | NA |  | 0 | Chi-square value from the fit |
| `ring_yes` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have a ring' (intended to include pseudo-ring) having response 'Yes' |
| `smoothness_err` | double | NA |  | 0 | Smoothness error |
| `merging_none` | double | NA |  | 0 | Dirichlet param of question 'Is the galaxy visually disturbed or merging?' having response 'None (no)' |
| `data_set_release_part1` | char |  |  | 0 |  |
| `sersic_sersic_nir_axis_ratio_err` | double |  |  | 0 |  |
| `dwarf_no` | double | NA |  | 0 | Dirichlet param. of question identifying dwarf galaxies (visually, like a 'smudge') having response 'No' |
| `agn_yes` | double | NA |  | 0 | Dirichlet param. of question asking if the galaxy has a central PSF-like (very) bright spot, for positive response |
| `sersic_sersic_nir_index_err` | double |  |  | 0 |  |
| `clump_count_above_threshold` | short | NA |  | 0 | Number of clumps detected after applying confidence threshold |
| `merging_minor_disturbance` | double | NA |  | 0 | Dirichlet param of question 'Is the galaxy visually disturbed or merging?' having response 'Minor disturbance' |
| `spiral_arm_count_1` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy has spiral arms, how many?' having response '1' |
| `how_rounded_cigar_shaped` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy is visually smooth, how round is it?' having response 'Cigar-shaped' |
| `sersic_sersic_nir_index` | double |  |  | 0 |  |
| `asymmetry_err` | double | NA |  | 0 | Asymmetry error |
| `disk_sersic_sersic_radius` | double | arcsec |  | 0 | The Sersic radius |
| `how_rounded_in_between` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy is visually smooth, how round is it?' having response 'In-between' |
| `data_set_release_part2` | char |  |  | 0 |  |
| `spiral_arm_count_3` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy has spiral arms, how many?' having response '3' |
| `how_rounded_completely` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy is visually smooth, how round is it?' having response 'Completely' |
| `major_merger` | double | NA |  | 0 | The probability of the galaxy classified as a major merger |
| `bar_strong` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have a bar, and if so, how strong?' having response 'Strong' |
| `sersic_ext_duration` | double |  |  | 0 |  |
| `spiral_winding_tight` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy has spiral arms, how tightly wound are they?' having response 'Tight' |
| `bar_no` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have a bar, and if so, how strong?' Having response 'No bar' |
| `disk_sersic_sersic_axis_ratio_err` | double | NA |  | 0 | Error of the sersic axis ratio |
| `sersic_sersic_vis_index` | double |  |  | 1 |  |
| `clump_count_unusual_any_threshold` | short | NA |  | 0 | Number of 'unusual' (e.g. color, shape) clumps detected before applying confidence threshold |
| `smoothness` | double | NA |  | 1 | The smoothness quantifies the degree of small-scale structure of the galaxy. The image is smoothed with a box of width 0.25 rp and then subtracted from the original image |
| `disk_sersic_sersic_axis_ratio` | double | NA |  | 0 | Axis ratio of the Sersic |
| `spiral_arm_count_4` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy has spiral arms, how many?' having response '4' |
| `sersic_ext_flags` | long |  |  | 0 |  |
| `sersic_sersic_nir_radius` | double |  |  | 0 |  |
| `smooth_or_featured_featured_or_disk` | double | NA |  | 0 | Dirichlet param. of question 'Is the galaxy smooth, featured/disk, or an artifact?' having response 'Featured or Disk' |
| `sersic_sersic_nir_radius_err` | double |  |  | 0 |  |
| `dwarf_yes` | double | NA |  | 0 | Dirichlet param. of question identifying dwarf galaxies (visually, like a 'smudge') having response 'Yes' |
| `etg_or_ltg` | double | NA |  | 0 | Binary classification between early and late types, from Dominguez Sanchez+2022 |
| `gini_err` | double | NA |  | 0 | GINI error |
| `ring_no` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have a ring' (intended to include pseudo-ring) having response 'No' |
| `major_merger_uncertainty` | double | NA |  | 0 | Uncertainty on the probability of the major merger classification |
| `lopsided_yes` | double | NA |  | 0 | Dirichlet param. of question 'Is the galaxy lopsided?' having response 'Yes' |
| `sersic_visnir_flags` | long |  |  | 0 |  |
| `sersic_ext_reduced_chi2` | double |  |  | 0 |  |
| `data_set_release` | char |  |  | 0 |  |
| `sersic_sersic_vis_axis_ratio` | double |  |  | 0 |  |
| `disk_sersic_disk_radius` | double | arcsec |  | 0 | Disk radius of the fit |
| `sersic_visnir_reduced_chi2` | double |  |  | 0 |  |
| `merging_major_disturbance` | double | NA |  | 0 | Dirichlet param of question 'Is the galaxy visually disturbed or merging?' having response 'Major disturbance' |
| `bulge_size_dominant` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy have a bulge, and if so, how visually obvious?' having response 'Dominant' |
| `sersic_angle_err` | double | deg |  | 0 | Position angle error of the Sersic |
| `spiral_arm_count_2` | double | NA |  | 0 | Dirichlet param. of question 'Given the galaxy has spiral arms, how many?' having response '2' |
| `sersic_sersic_vis_index_err` | double |  |  | 0 |  |
| `patch_id_list` | long |  |  | 1 |  |
| `edge_on_bulge_none` | double | NA |  | 0 | Dirichlet param. of question 'What shape is the bulge in the edge-on disk' having response 'No bulge' |
| `data_set_release_part3` | int |  |  | 0 |  |
| `catalogue_oid` | long |  |  | 0 |  |
| `disk_sersic_angle_err` | double | deg |  | 0 | Position angle error of tDisk+Sersic |
| `disk_edge_on_no` | double | NA |  | 0 | Dirichlet param. of question 'Does the galaxy appear to be an edge-on-disk?' having response 'Not edge-on-disk' |
| `calblock_id_list` | char |  |  | 1 |  |
