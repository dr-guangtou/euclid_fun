# TAP table `dr1.spectro_z_spe_classification_deep`



| Column | Type | Unit | UCD | Indexed | Description |
|---|---|---|---|---|---|
| `object_id` | long |  |  | 1 |  |
| `patch_id_list` | long |  |  | 1 |  |
| `spe_qso_prob` | double | NA |  | 1 | The probability of the object to be a quasar |
| `basic_download_data_oid` | long |  |  | 1 |  |
| `spe_gal_prob` | double | NA |  | 1 | The probability of the object to be a galaxy |
| `data_set_release_part2` | char |  |  | 0 |  |
| `spe_star_prob` | double | NA |  | 1 | The probability of the object to be a star |
| `data_set_release_part3` | int |  |  | 0 |  |
| `data_set_release_part1` | char |  |  | 0 |  |
| `spe_class` | char | NA |  | 1 | The classification of the object related to highest probability [STAR, GALAXY, QSO, UNDEF] |
| `data_set_release` | char |  |  | 0 |  |
| `calblock_id_list` | char |  |  | 1 |  |
