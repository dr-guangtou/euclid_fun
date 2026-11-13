# TAP table `ivoa.obscore`



| Column | Type | Unit | UCD | Indexed | Description |
|---|---|---|---|---|---|
| `em_min` | double | m | em.wl;stat.min | 0 | Start in spectral coordinates |
| `em_res_power` | double |  | spect.resolution | 0 | Value of the resolving power along the spectral axis. (R) |
| `s_region` | char |  | pos.outline;obs.field | 0 | Sky region covered by the data product (expressed in ICRS frame) |
| `s_ra` | double | deg | pos.eq.ra | 0 | Central Spatial Position in ICRS - Right ascension |
| `em_max` | double | m | em.wl;stat.max | 0 | Stop in spectral coordinates |
| `data_set_release` | char |  |  | 0 |  |
| `s_xel1` | long |  | meta.number | 0 | Number of elements along the first coordinate of the spatial axis |
| `file_name` | char |  |  | 0 |  |
| `s_dec` | double | deg | pos.eq.dec | 0 | Central Spatial Position in ICRS - Declination |
| `s_resolution` | double | arcsec | pos.angResolution | 0 | Spatial resolution of data as FWHM of PSF |
| `t_resolution` | double | s | time.resolution | 0 | Temporal resolution FWHM |
| `calib_level` | int |  | meta.code;obs.calib | 0 | Calibration level of the observation: in {0, 1, 2, 3, 4} |
| `pol_states` | char |  | meta.code;phys.polarization | 0 | List of polarization states present in the data file |
| `t_max` | double | d | time.end;obs.exposure | 0 | Stop time in MJD |
| `cutout_access_url` | char |  |  | 0 |  |
| `target_name` | char |  | meta.id;src | 0 | Object of interest |
| `o_ucd` | char |  | meta.ucd | 0 | Nature of the observable axis |
| `s_xel2` | long |  | meta.number | 0 | Number of elements along the second coordinate of the spatial axis |
| `obs_id` | char |  | meta.id | 0 | Internal ID given by the ObsTAP service |
| `access_url` | char |  | meta.ref.url | 0 | URL used to access dataset |
| `dataproduct_type` | char |  | meta.id | 0 | Data product (file content) primary type |
| `s_fov` | double | deg | phys.angSize;instr.fov | 0 | Estimated size of the covered region as the diameter of a containing circle |
| `filter` | char |  |  | 0 |  |
| `obs_collection` | char |  | meta.id | 0 | Name of the data collection |
| `t_min` | double | d | time.start;obs.exposure | 0 | Start time in MJD |
| `access_estsize` | long | kbyte | phys.size;meta.file | 0 | Estimated size of dataset: in kilobytes |
| `t_xel` | long |  | meta.number | 0 | Number of elements along the time axis |
| `em_xel` | long |  | meta.number | 0 | Number of elements along the spectral axis |
| `t_exptime` | double | s | time.duration;obs.exposure | 0 | Total exposure time |
| `version` | int |  |  | 0 |  |
| `dataproduct_subtype` | char |  | meta.id | 0 | Data product specific type |
| `pol_xel` | long |  | meta.number | 0 | Number of elements along the polarization axis |
| `facility_name` | char |  | meta.id;instr.tel | 0 |  |
| `tile_index` | long |  |  | 0 |  |
| `environment` | char |  |  | 0 |  |
| `obs_publisher_did` | char |  | meta.ref.uri;meta.curation | 0 | ID for the Dataset given by the publisher. |
| `instrument_name` | char |  | meta.id;instr | 0 | The name of the instrument used for the observation |
| `access_format` | char |  | meta.code.mime | 0 | Content format of the dataset |
| `activity_code` | char |  |  | 0 |  |
