# TAP table `dr1.spectro_model_spe_qso_models_wide_survey`



| Column | Type | Unit | UCD | Indexed | Description |
|---|---|---|---|---|---|
| `basic_download_data_oid` | long |  |  | 1 |  |
| `spe_flux_offset_b` | double | erg/s/cm2/Angstrom |  | 0 | The flux offset of the Blue spectra |
| `spe_vel_disp_a` | double | km/s |  | 0 | The velocity dispersion of absorption lines |
| `spe_z` | double | NA |  | 0 | The estimated spectroscopic redshift |
| `spe_tpl_rat_id` | char | NA |  | 0 | The template ratio ID |
| `spe_rank` | short | NA |  | 0 | The rank of estimate (i.e. =1 mean best estimate) |
| `spe_lines_amp` | double | erg/s/cm2/Angstrom |  | 0 | The amplitude of each line |
| `patch_id_list` | long |  |  | 1 |  |
| `spe_ical_factor_b` | double | NA |  | 0 | The inter-calibration factor between Red and Blue spectra |
| `lya_width` | double | Angstrom |  | 0 | The Lya line width |
| `spe_tpl_rat_ism_coeff` | double | NA |  | 0 | The Ebmv coefficient for emission lines inside [0.,1.] |
| `object_id` | long |  |  | 1 |  |
| `spe_tpl_rat_a_amp` | double | NA |  | 0 | The amplitude of absorption template ratio |
| `spe_lines_id` | short | NA |  | 0 | ID of each line |
| `spe_cnt_tpl_id` | char | NA |  | 0 | The continuum template ID |
| `lya_assym_coef` | double | NA |  | 0 | The alpha coefficient for skewed gaussian Lya model |
| `spe_cnt_ism_coef` | double | NA |  | 0 | The Ebmv coefficient inside [0.,1.] |
| `spe_cnt_tpl_amp` | double | NA |  | 0 | The amplitude of continuum template |
| `data_set_release` | char |  |  | 0 |  |
| `spe_cnt_igm_tpl_id` | short | NA |  | 0 | The IGM template ID |
| `data_set_release_part3` | int |  |  | 0 |  |
| `data_set_release_part2` | char |  |  | 0 |  |
| `spe_tpl_rat_e_amp` | double | erg/s/cm2/Angstrom |  | 0 | The amplitude of emission template ratio |
| `lya_offset` | double | Angstrom |  | 0 | The Lya central wavelength offset |
| `spe_flux_offset_r` | double | erg/s/cm2/Angstrom |  | 0 | The flux offset of the Red spectra |
| `spe_vel_disp_e` | double | km/s |  | 0 | The velocity dispersion of emission lines |
| `data_set_release_part1` | char |  |  | 0 |  |
| `calblock_id_list` | char |  |  | 1 |  |
