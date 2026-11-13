# TAP table `dr1.phz_classification_deep_survey`



| Column | Type | Unit | UCD | Indexed | Description |
|---|---|---|---|---|---|
| `object_id` | long | NA |  | 1 | Unique ID of the object in the survey, as set by MER |
| `data_set_release_part3` | int |  |  | 0 |  |
| `galaxy_threshold` | double | NA |  | 0 | The galaxy probability above which the object is accepted as a galaxy |
| `star_threshold` | double | NA |  | 0 | The star probability above which the object is accepted as a star |
| `phz_gal_prob` | double | NA |  | 1 | The probability of the object to be a galaxy |
| `qso_threshold` | double |  |  | 0 |  |
| `patch_id_list` | long |  |  | 0 |  |
| `basic_download_data_oid` | long |  |  | 1 |  |
| `phz_star_prob` | double | NA |  | 1 | The probability of the object to be a star |
| `data_set_release_part1` | char |  |  | 0 |  |
| `vis_det` | long |  |  | 0 |  |
| `globc_threshold` | double | NA |  | 0 | The globular cluster probability above which the object is accepted as a globular cluster |
| `configuration` | int | NA |  | 0 | Encode the Photometric band configuration (indicating also the number of missing columns) |
| `missing_band` | char |  |  | 0 |  |
| `data_set_release_part2` | char |  |  | 0 |  |
| `data_set_release` | char |  |  | 0 |  |
| `phz_classification` | int | NA |  | 1 | Classification flag: +1 if the source is accepted as galaxy, +2 if it is accepted as a star +4 if it is accepted as a QSO +8 if the source is accepted as a globular Clustert |
| `phz_qso_prob` | double | NA |  | 1 | The probability of the object to be a QSO |
| `phz_glob_cl_prob` | double | NA |  | 0 | The probability of the object to be a Globular Cluster |
| `calblock_id_list` | char |  |  | 0 |  |
