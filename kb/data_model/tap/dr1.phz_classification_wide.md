# TAP table `dr1.phz_classification_wide`



| Column | Type | Unit | UCD | Indexed | Description |
|---|---|---|---|---|---|
| `phz_qso_prob` | double | NA |  | 1 | The probability of the object to be a QSO |
| `phz_classification` | int | NA |  | 1 | Classification flag: +1 if the source is accepted as galaxy, +2 if it is accepted as a star +4 if it is accepted as a QSO +8 if the source is accepted as a globular Clustert |
| `phz_glob_cl_prob` | double | NA |  | 0 | The probability of the object to be a Globular Cluster |
| `missing_band` | char |  |  | 0 |  |
| `data_set_release_part2` | char |  |  | 0 |  |
| `data_set_release` | char |  |  | 0 |  |
| `vis_det` | long |  |  | 0 |  |
| `configuration` | int | NA |  | 0 | Encode the Photometric band configuration (indicating also the number of missing columns) |
| `globc_threshold` | double | NA |  | 0 | The globular cluster probability above which the object is accepted as a globular cluster |
| `basic_download_data_oid` | long |  |  | 1 |  |
| `data_set_release_part1` | char |  |  | 0 |  |
| `phz_star_prob` | double | NA |  | 1 | The probability of the object to be a star |
| `galaxy_threshold` | double | NA |  | 0 | The galaxy probability above which the object is accepted as a galaxy |
| `data_set_release_part3` | int |  |  | 0 |  |
| `object_id` | long | NA |  | 1 | Unique ID of the object in the survey, as set by MER |
| `star_threshold` | double | NA |  | 0 | The star probability above which the object is accepted as a star |
| `patch_id_list` | long |  |  | 1 |  |
| `qso_threshold` | double |  |  | 0 |  |
| `phz_gal_prob` | double | NA |  | 1 | The probability of the object to be a galaxy |
| `calblock_id_list` | char |  |  | 1 |  |
