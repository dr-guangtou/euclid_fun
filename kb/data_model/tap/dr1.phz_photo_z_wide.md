# TAP table `dr1.phz_photo_z_wide`



| Column | Type | Unit | UCD | Indexed | Description |
|---|---|---|---|---|---|
| `fluxerr_u_ext_megacam_unif` | double |  |  | 0 |  |
| `fluxerr_i_ext_panstarrs_unif` | double |  |  | 0 |  |
| `fluxerr_r_ext_megacam_unif` | double |  |  | 0 |  |
| `patch_id_list` | long |  |  | 1 |  |
| `phz_flags` | int | NA |  | 1 | An integer containing the flags of the PHZ processing. Bitwise meaning: 0 =&gt; OK, +1 =&gt; NNPZ flag: no close neighbor +2 incomplete set of flux |
| `fluxerr_z_ext_decam_unif` | double |  |  | 0 |  |
| `phz_median` | double | NA |  | 1 | The median of the PHZ PDF |
| `flag_som_tomobin` | long |  |  | 0 |  |
| `phz_weight` | double | NA |  | 1 | Probability to be a usable source (To be used for Galaxy Clustering) |
| `fluxerr_r_ext_lsst_unif` | double |  |  | 0 |  |
| `fluxerr_g_ext_hsc_unif` | double |  |  | 0 |  |
| `flux_i_ext_decam_unif` | double |  |  | 0 |  |
| `basic_download_data_oid` | long |  |  | 1 |  |
| `phz_classification` | int | NA |  | 1 | Classification flag: +1 if the source is accepted as galaxy, +2 if it is accepted as a star +4 if it is accepted as a QSO +8 if the source is accepted as a globular Clustert |
| `alt_tom_bin_id` | long | NA |  | 0 | The identifier of the alternate tomographic bin the source belongs to |
| `ie_cuts_weights` | double |  |  | 0 |  |
| `phz_pdf` | double | NA |  | 0 | A vector containing the PHZ PDF values, for Z in range [0,6] with 0.01 step |
| `phz_mode_1_area` | double | NA |  | 0 | The total area of the first mode |
| `flux_g_ext_decam_unif` | double |  |  | 0 |  |
| `flux_i_ext_lsst_unif` | double |  |  | 0 |  |
| `flux_r_ext_megacam_unif` | double |  |  | 0 |  |
| `photometric_system` | int | NA |  | 0 | Encode the Photometric band configuration (indicating also the number of missing columns) |
| `data_set_release_part3` | int |  |  | 0 |  |
| `fluxerr_g_ext_decam_unif` | double |  |  | 0 |  |
| `phz_mode_2_area` | double | NA |  | 0 | The total area of the second mode |
| `object_id` | long | NA |  | 1 | Unique ID of the object in the survey, as set by MER |
| `data_set_release_part1` | char |  |  | 0 |  |
| `flag_som_pos_tomobin` | long |  |  | 0 |  |
| `bias_id` | int | NA |  | 0 | The identifier to be used for retrieving the bias correction shift from the bias correction map |
| `flux_vis_unif` | double |  |  | 0 |  |
| `fluxerr_r_ext_decam_unif` | double |  |  | 0 |  |
| `fluxerr_i_ext_lsst_unif` | double |  |  | 0 |  |
| `phz_70_int` | double | NA |  | 1 | The smallest PHZ PDF interval containing 70% of the probability |
| `tom_bin_id` | long | NA |  | 0 | The identifier of the tomographic bin the source belongs to |
| `flux_h_unif` | double |  |  | 0 |  |
| `flux_u_ext_decam_unif` | double |  |  | 0 |  |
| `fluxerr_u_ext_decam_unif` | double |  |  | 0 |  |
| `fluxerr_j_unif` | double |  |  | 0 |  |
| `best_chi2` | double |  |  | 0 |  |
| `flux_g_ext_hsc_unif` | double |  |  | 0 |  |
| `flux_z_ext_lsst_unif` | double |  |  | 0 |  |
| `phz_mode_1` | double | NA |  | 1 | The first mode of the PHZ PDF |
| `fluxerr_i_ext_decam_unif` | double |  |  | 0 |  |
| `flux_u_ext_megacam_unif` | double |  |  | 0 |  |
| `phz_90_int` | double | NA |  | 1 | The smallest PHZ PDF interval containing 90% of the probability |
| `fluxerr_g_ext_lsst_unif` | double |  |  | 0 |  |
| `flux_z_ext_decam_unif` | double |  |  | 0 |  |
| `fluxerr_vis_unif` | double |  |  | 0 |  |
| `flux_j_unif` | double |  |  | 0 |  |
| `fluxerr_y_unif` | double |  |  | 0 |  |
| `flux_y_unif` | double |  |  | 0 |  |
| `fluxerr_u_ext_lsst_unif` | double |  |  | 0 |  |
| `phz_95_int` | double | NA |  | 1 | The smallest PHZ PDF interval containing 95% of the probability |
| `data_set_release` | char |  |  | 0 |  |
| `flux_r_ext_lsst_unif` | double |  |  | 0 |  |
| `flux_g_ext_lsst_unif` | double |  |  | 0 |  |
| `flux_z_ext_hsc_unif` | double |  |  | 0 |  |
| `flag_som_alt_tomobin` | long |  |  | 0 |  |
| `phz_mode_2` | double | NA |  | 0 | The second mode of the PHZ PDF |
| `fluxerr_h_unif` | double |  |  | 0 |  |
| `pos_tom_bin_id` | long |  |  | 0 |  |
| `fluxerr_z_ext_lsst_unif` | double |  |  | 0 |  |
| `flux_r_ext_decam_unif` | double |  |  | 0 |  |
| `fluxerr_z_ext_hsc_unif` | double |  |  | 0 |  |
| `data_set_release_part2` | char |  |  | 0 |  |
| `flux_u_ext_lsst_unif` | double |  |  | 0 |  |
| `flux_i_ext_panstarrs_unif` | double |  |  | 0 |  |
| `calblock_id_list` | char |  |  | 1 |  |
