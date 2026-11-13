# TAP table `dr1.mer_catalogue_deep_visits`



| Column | Type | Unit | UCD | Indexed | Description |
|---|---|---|---|---|---|
| `flux_z_ext_decam_templfit` | double | uJy |  | 0 | Zext DECam band source template fitting flux (TPHOT measurement) |
| `fluxerr_vis_1fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_z_ext_panstarrs_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Zext PS band (TPHOT measurement) |
| `fluxerr_g_ext_jpcam_2fwhm_aper` | double |  |  | 0 |  |
| `avg_trans_wave_z_ext_decam` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the DECam Z band |
| `flux_vis_1fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_lsst_sersic` | double | uJy |  | 0 | Gext LSST band source flux from the Sersic fit |
| `fluxerr_h_sersic` | double | uJy |  | 0 | NIR H band source flux error from the Sersic fit |
| `fluxerr_r_ext_lsst_1fwhm_aper` | double |  |  | 0 |  |
| `flux_u_ext_megacam_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_z_ext_decam_disk_sersic` | double | uJy |  | 0 | Zext DECam band source flux error from the Disk+Sersic fit |
| `flux_y_templfit` | double | uJy |  | 0 | NIR Y band source template fitting flux (TPHOT measurement) |
| `designation` | char |  | meta.id | 0 | Designation of the source |
| `fluxerr_g_ext_lsst_4fwhm_aper` | double |  |  | 0 |  |
| `segmentation_area` | int | pix |  | 1 | Isophotal area of the source above the analysis threshold (SExtractor ISOAREA_IMAGE) |
| `flag_u_ext_megacam` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Uext Megacam flag image |
| `fluxerr_r_ext_megacam_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_y_3fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_lsst_templfit` | double | uJy |  | 0 | Zext LSST band source template fitting flux (TPHOT measurement) |
| `fluxerr_i_ext_decam_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_g_ext_hsc_1fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_vis_to_i_ext_decam_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Iext DECam band (TPHOT measurement) |
| `fluxerr_j_4fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_y_disk_sersic` | double | NA |  | 0 | NIR Y band Sersic fraction |
| `flux_vis_to_g_ext_jpcam_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Gext JPCAM band (TPHOT measurement) |
| `flux_r_ext_lsst_disk_sersic` | double | uJy |  | 0 | Rext LSST band source flux from the Disk+Sersic fit |
| `flux_y_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_g_ext_lsst_1fwhm_aper` | double |  |  | 0 |  |
| `flux_u_ext_decam_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_z_ext_decam_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_z_ext_lsst_templfit` | double | uJy |  | 0 | Zext LSST band source template fitting flux error (TPHOT measurement) |
| `flux_r_ext_lsst_templfit` | double | uJy |  | 0 | Rext LSST band source template fitting flux (TPHOT measurement) |
| `sersic_fract_i_ext_panstarrs_disk_sersic` | double | NA |  | 0 | Iext PS band Sersic fraction |
| `flux_h_4fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_panstarrs_1fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_h_disk_sersic` | double | NA |  | 0 | NIR H band Sersic fraction |
| `fluxerr_z_ext_decam_templfit` | double | uJy |  | 0 | Zext DECam band source template fitting flux error (TPHOT measurement) |
| `flux_nir_stack_1fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_u_ext_megacam_sersic` | double | uJy |  | 0 | Uext Megacam band source flux error from the Sersic fit |
| `flux_g_ext_hsc_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_r_ext_lsst_4fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_g_ext_decam_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Gext DECam band (TPHOT measurement) |
| `point_like_prob` | double | NA |  | 1 | Probability between 0 and 1 that the source is point-like (the estimation uses a "star probability cube" defined in the MDB). Value is set to NaN for NIR-only objects (use MUMAX_MINUS_MAG for NIR-only objcts) |
| `flag_r_ext_megacam` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Rext Megacam flag image |
| `det_quality_flag` | short | NA |  | 1 | Detection step flags that could indicate the possible corruption of the MAG_STARGAL_SEP values |
| `fluxerr_u_ext_decam_templfit` | double | uJy |  | 0 | Uext DECam band source template fitting flux error (TPHOT measurement) |
| `flux_u_ext_decam_sersic` | double | uJy |  | 0 | Uext DECam band source flux from the Sersic fit |
| `fluxerr_vis_to_r_ext_decam_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Rext DECam band (TPHOT measurement) |
| `fluxerr_vis_to_g_ext_hsc_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Gext HSC band (TPHOT measurement) |
| `avg_trans_wave_i_ext_panstarrs` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the PS I band |
| `fluxerr_u_ext_decam_disk_sersic` | double | uJy |  | 0 | Uext DECam band source flux error from the Disk+Sersic fit |
| `fluxerr_vis_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_vis_to_z_ext_decam_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Zext DECam band (TPHOT measurement) |
| `fluxerr_i_ext_lsst_2fwhm_aper` | double |  |  | 0 |  |
| `flux_detection_total` | double | uJy |  | 1 | VIS or NIR stack band source total flux error (Kron aperture) |
| `fluxerr_u_ext_decam_2fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_panstarrs_sersic` | double | uJy |  | 0 | Iext PS band source flux from the Sersic fit |
| `flag_i_ext_panstarrs` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Iext PS flag image |
| `parent_visnir` | long | NA |  | 0 | ID of the parent sources of a deblended object |
| `avg_trans_wave_i_ext_decam` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the DECam I band |
| `flux_vis_to_i_ext_decam_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Iext DECam band (TPHOT measurement) |
| `fluxerr_z_ext_hsc_3fwhm_aper` | double |  |  | 0 |  |
| `flux_h_3fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_vis_disk_sersic_err` | double | NA |  | 0 | VIS band Sersic fraction error |
| `fluxerr_h_4fwhm_aper` | double |  |  | 0 |  |
| `flux_u_ext_decam_3fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_panstarrs_4fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_j_disk_sersic` | double | NA |  | 0 | NIR J band Sersic fraction |
| `flux_r_ext_decam_sersic` | double | uJy |  | 0 | Rext DECam band source flux from the Sersic fit |
| `fluxerr_vis_to_r_ext_lsst_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Rext LSST band (TPHOT measurement) |
| `flux_i_ext_panstarrs_templfit` | double | uJy |  | 0 | Iext PS band source template fitting flux (TPHOT measurement) |
| `fluxerr_r_ext_lsst_templfit` | double | uJy |  | 0 | Rext LSST band source template fitting flux error (TPHOT measurement) |
| `flux_vis_psf` | double | uJy |  | 0 | VIS band source PSF-fitting photometry flux (TPHOT measurement) |
| `flux_z_ext_lsst_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_i_ext_decam_sersic` | double | uJy |  | 0 | Iext DECam band source flux error from the Sersic fit |
| `mu_max` | double | mag/arcsec2 |  | 0 | Peak surface brightness above the background in the detection band (directly from SExtractor) |
| `avg_trans_wave_u_ext_lsst` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the LSST U band |
| `fluxerr_h_3fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_r_ext_lsst_disk_sersic` | double | NA |  | 0 | Rext LSST band Sersic fraction |
| `fluxerr_g_ext_decam_sersic` | double | uJy |  | 0 | Gext DECam band source flux error from the Sersic fit |
| `fluxerr_j_3fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_g_ext_lsst_disk_sersic` | double | NA |  | 0 | Gext LSST band Sersic fraction |
| `flux_u_ext_lsst_3fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_lsst_4fwhm_aper` | double |  |  | 0 |  |
| `avg_trans_wave_z_ext_hsc` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the HSC Z band |
| `flux_g_ext_decam_disk_sersic` | double | uJy |  | 0 | Gext DECam band source flux from the Disk+Sersic fit |
| `avg_trans_wave_r_ext_megacam` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the Megacam R band |
| `fluxerr_g_ext_jpcam_templfit` | double | uJy |  | 0 | Gext JPCAM band source template fitting flux error (TPHOT measurement) |
| `sersic_fract_z_ext_hsc_disk_sersic` | double | NA |  | 0 | Zext HSC band Sersic fraction |
| `flux_g_ext_hsc_disk_sersic` | double | uJy |  | 0 | Gext HSC band source flux from the Disk+Sersic fit |
| `gal_ebv` | double | mag |  | 0 | Estimated galactic E(B-V) at the source centroid according to the reference Planck map |
| `flux_u_ext_decam_templfit` | double | uJy |  | 0 | Uext DECam band source template fitting flux (TPHOT measurement) |
| `flag_g_ext_decam` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the GextDECam flag image |
| `flux_r_ext_megacam_sersic` | double | uJy |  | 0 | Rext Megacam band source flux from the Sersic fit |
| `fluxerr_r_ext_megacam_4fwhm_aper` | double |  |  | 0 |  |
| `flux_j_4fwhm_aper` | double |  |  | 0 |  |
| `flag_h` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the NIR H flag image |
| `fluxerr_g_ext_hsc_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_z_ext_decam_sersic` | double | uJy |  | 0 | Zext DECam band source flux error from the Sersic fit |
| `flux_u_ext_lsst_sersic` | double | uJy |  | 0 | Uext LSST band source flux from the Sersic fit |
| `fluxerr_g_ext_lsst_sersic` | double | uJy |  | 0 | Gext LSST band source flux error from the Sersic fit |
| `data_set_release_part1` | char |  |  | 0 |  |
| `flag_j` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the NIR J flag image |
| `flux_z_ext_decam_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_j_disk_sersic` | double | uJy |  | 0 | NIR J band source flux error from the Disk+Sersic fit |
| `flux_z_ext_decam_sersic` | double | uJy |  | 0 | Zext DECam band source flux from the Sersic fit |
| `fluxerr_u_ext_decam_sersic` | double | uJy |  | 0 | Uext DECam band source flux error from the Sersic fit |
| `flux_vis_disk_sersic` | double | uJy |  | 0 | VIS band source flux from the Disk+Sersic fit |
| `flag_z_ext_hsc` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Zext HSC flag image |
| `flux_g_ext_lsst_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_g_ext_decam_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_r_ext_decam_templfit` | double | uJy |  | 0 | Rext DECam band source template fitting flux error (TPHOT measurement) |
| `fluxerr_r_ext_lsst_sersic` | double | uJy |  | 0 | Rext LSST band source flux error from the Sersic fit |
| `flux_y_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_u_ext_lsst_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_g_ext_decam_4fwhm_aper` | double |  |  | 0 |  |
| `flux_r_ext_megacam_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_i_ext_lsst_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_detection_total` | double | uJy |  | 0 | VIS or NIR stack band source segmented area flux |
| `fluxerr_h_disk_sersic` | double | uJy |  | 0 | NIR H band source flux error from the Disk+Sersic fit |
| `fluxerr_u_ext_megacam_templfit` | double | uJy |  | 0 | Uext Megacam band source template fitting flux error (TPHOT measurement) |
| `flux_g_ext_jpcam_2fwhm_aper` | double |  |  | 0 |  |
| `flux_y_sersic` | double | uJy |  | 1 | NIR Y band source flux from the Sersic fit |
| `fluxerr_z_ext_decam_1fwhm_aper` | double |  |  | 0 |  |
| `extended_flag` | short | NA |  | 0 | Extended source flag |
| `flux_i_ext_decam_templfit` | double | uJy |  | 0 | Iext DECam band source template fitting flux (TPHOT measurement) |
| `declination_psf_fitting` | double | deg |  | 0 | Source DEC coordinate derived by the PSF-fitting photometry method |
| `flux_nir_stack_4fwhm_aper` | double |  |  | 0 |  |
| `flux_r_ext_decam_4fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_g_ext_lsst_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Gext LSST band (TPHOT measurement) |
| `flux_i_ext_panstarrs_3fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_g_ext_lsst_disk_sersic_err` | double | NA |  | 0 | Gext LSST band Sersic fraction error |
| `flux_r_ext_megacam_1fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_y_disk_sersic_err` | double | NA |  | 0 | NIR Y band Sersic fraction error |
| `fluxerr_y_disk_sersic` | double | uJy |  | 0 | NIR Y band source flux error from the Disk+Sersic fit |
| `sersic_fract_z_ext_lsst_disk_sersic` | double | NA |  | 0 | Zext LSST band Sersic fraction |
| `fluxerr_g_ext_jpcam_disk_sersic` | double | uJy |  | 0 | Gext JPCAM band source flux error from the Disk+Sersic fit |
| `sersic_fract_u_ext_lsst_disk_sersic_err` | double | NA |  | 0 | Uext LSST band Sersic fraction error |
| `fluxerr_u_ext_lsst_sersic` | double | uJy |  | 0 | Uext LSST band source flux error from the Sersic fit |
| `fluxerr_r_ext_decam_1fwhm_aper` | double |  |  | 0 |  |
| `flag_i_ext_decam` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the IextDECam flag image |
| `flux_r_ext_megacam_3fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_hsc_disk_sersic` | double | uJy |  | 0 | Zext HSC band source flux from the Disk+Sersic fit |
| `ellipticity_err` | double | NA |  | 0 | Ellipticity error |
| `fluxerr_z_ext_hsc_4fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_hsc_4fwhm_aper` | double |  |  | 0 |  |
| `flux_j_templfit` | double | uJy |  | 0 | NIR J band source template fitting flux (TPHOT measurement) |
| `variable_flag` | short | NA |  | 0 | Object variability flag |
| `fluxerr_z_ext_lsst_2fwhm_aper` | double |  |  | 0 |  |
| `flag_z_ext_panstarrs` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Zext PS flag image |
| `avg_trans_wave_u_ext_megacam` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the Megacam U band |
| `gaia_id` | long | NA |  | 0 | The associated GAIA source id |
| `fluxerr_h_1fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_z_ext_panstarrs_2fwhm_aper` | double |  |  | 0 |  |
| `segmentation_map_id` | long | NA |  | 0 | Source ID in the associated segmentation map |
| `flux_g_ext_jpcam_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_i_ext_lsst_sersic` | double | uJy |  | 0 | Iext LSST band source flux error from the Sersic fit |
| `fluxerr_g_ext_hsc_sersic` | double | uJy |  | 0 | Gext HSC band source flux error from the Sersic fit |
| `flux_u_ext_decam_disk_sersic` | double | uJy |  | 0 | Uext DECam band source flux from the Disk+Sersic fit |
| `flux_i_ext_lsst_1fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_g_ext_decam_1fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_z_ext_lsst_disk_sersic_err` | double | NA |  | 0 | Zext LSST band Sersic fraction error |
| `fluxerr_vis_2fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_r_ext_decam_disk_sersic` | double | NA |  | 0 | Rext DECam band Sersic fraction |
| `fluxerr_z_ext_hsc_sersic` | double | uJy |  | 0 | Zext HSC band source flux error from the Sersic fit |
| `fluxerr_vis_to_i_ext_panstarrs_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Iext PS band (TPHOT measurement) |
| `flux_z_ext_hsc_1fwhm_aper` | double |  |  | 0 |  |
| `flux_nir_stack_3fwhm_aper` | double |  |  | 0 |  |
| `flux_u_ext_decam_1fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_r_ext_megacam_1fwhm_aper` | double |  |  | 0 |  |
| `avg_trans_wave_g_ext_jpcam` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the JPCAM G band |
| `fluxerr_g_ext_lsst_disk_sersic` | double | uJy |  | 0 | Gext LSST band source flux error from the Disk+Sersic fit |
| `avg_trans_wave_vis` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the VIS band |
| `fluxerr_r_ext_megacam_sersic` | double | uJy |  | 0 | Rext Megacam band source flux error from the Sersic fit |
| `fluxerr_vis_to_r_ext_megacam_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Rext Megacam band (TPHOT measurement) |
| `fluxerr_z_ext_hsc_2fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_lsst_2fwhm_aper` | double |  |  | 0 |  |
| `point_like_flag` | short | NA |  | 0 | Point-like flag : flag set to 1 for VIS detections with (DET_QUALITY_FLAG==0) AND (POINT_LIKE_PROBA&gt;threshold), otherwise set to NaN |
| `sersic_fract_g_ext_hsc_disk_sersic` | double | NA |  | 0 | Gext HSC band Sersic fraction |
| `flux_h_templfit` | double | uJy |  | 0 | NIR H band source template fitting flux (TPHOT measurement) |
| `fluxerr_z_ext_lsst_sersic` | double | uJy |  | 0 | Zext LSST band source flux error from the Sersic fit |
| `flux_u_ext_megacam_disk_sersic` | double | uJy |  | 0 | Uext Megacam band source flux from the Disk+Sersic fit |
| `fluxerr_i_ext_decam_templfit` | double | uJy |  | 0 | Iext DECam band source template fitting flux error (TPHOT measurement) |
| `fluxerr_vis_to_z_ext_panstarrs_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Zext PS band (TPHOT measurement) |
| `tile_index` | long |  |  | 1 |  |
| `fluxerr_g_ext_lsst_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_u_ext_decam_1fwhm_aper` | double |  |  | 0 |  |
| `flux_r_ext_lsst_sersic` | double | uJy |  | 0 | Rext LSST band source flux from the Sersic fit |
| `fluxerr_z_ext_panstarrs_templfit` | double | uJy |  | 0 | Zext PS band source template fitting flux error (TPHOT measurement) |
| `flux_vis_sersic` | double | uJy |  | 1 | VIS band source flux from the Sersic fit |
| `fluxerr_i_ext_decam_1fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_r_ext_decam_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Rext DECam band (TPHOT measurement) |
| `avg_trans_wave_r_ext_lsst` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the LSST R band |
| `fluxerr_z_ext_panstarrs_3fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_r_ext_lsst_disk_sersic_err` | double | NA |  | 0 | Rext LSST band Sersic fraction error |
| `fluxerr_g_ext_jpcam_4fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_panstarrs_2fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_decam_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_r_ext_megacam_templfit` | double | uJy |  | 0 | Rext Megacam band source template fitting flux error (TPHOT measurement) |
| `fluxerr_g_ext_jpcam_1fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_u_ext_megacam_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_z_ext_lsst_1fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_decam_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_u_ext_lsst_disk_sersic` | double | uJy |  | 0 | Uext LSST band source flux error from the Disk+Sersic fit |
| `data_set_release` | char |  |  | 0 |  |
| `fluxerr_r_ext_lsst_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_u_ext_decam_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_y_templfit` | double | uJy |  | 0 | NIR Y band source template fitting flux error (TPHOT measurement) |
| `fluxerr_h_2fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_i_ext_lsst_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Iext LSST band (TPHOT measurement) |
| `flux_z_ext_panstarrs_1fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_u_ext_decam_disk_sersic` | double | NA |  | 0 | Uext DECam band Sersic fraction |
| `flux_z_ext_panstarrs_sersic` | double | uJy |  | 0 | Zext PS band source flux from the Sersic fit |
| `fluxerr_g_ext_decam_3fwhm_aper` | double |  |  | 0 |  |
| `flux_r_ext_megacam_2fwhm_aper` | double |  |  | 0 |  |
| `flag_g_ext_jpcam` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Gext JPCAM flag image |
| `avg_trans_wave_g_ext_decam` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the DECam G band |
| `flux_vis_to_u_ext_decam_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Uext DECam band (TPHOT measurement) |
| `flux_g_ext_lsst_1fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_y_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_h_templfit` | double | uJy |  | 0 | NIR H band source template fitting flux error (TPHOT measurement) |
| `fluxerr_nir_stack_2fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_decam_disk_sersic` | double | uJy |  | 0 | Zext DECam band source flux from the Disk+Sersic fit |
| `flux_vis_to_j_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to NIR J band (TPHOT measurement) |
| `fluxerr_i_ext_panstarrs_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_z_ext_panstarrs_sersic` | double | uJy |  | 0 | Zext PS band source flux error from the Sersic fit |
| `fluxerr_vis_to_j_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to NIR J bandr (TPHOT measurement) |
| `flux_u_ext_lsst_4fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_hsc_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_i_ext_panstarrs_templfit` | double | uJy |  | 0 | Iext PS band source template fitting flux error (TPHOT measurement) |
| `flux_h_2fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_decam_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_z_ext_panstarrs_1fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_decam_3fwhm_aper` | double |  |  | 0 |  |
| `extended_prob` | double | NA |  | 0 | Probability between 0 and 1 that the source is extended |
| `sersic_fract_u_ext_decam_disk_sersic_err` | double | NA |  | 0 | Uext DECam band Sersic fraction error |
| `avg_trans_wave_u_ext_decam` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the DECam U band |
| `kron_radius_err` | double | pix |  | 0 | Error on the major semi-axis (in pixels) of the elliptical aperture used for total (Kron) aperture photometry on the detection image |
| `flag_u_ext_lsst` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Uext LSST flag image |
| `fluxerr_vis_to_g_ext_decam_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Gext DECam band (TPHOT measurement) |
| `flux_g_ext_decam_1fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_decam_disk_sersic` | double | uJy |  | 0 | Iext DECam band source flux from the Disk+Sersic fit |
| `flux_vis_3fwhm_aper` | double |  |  | 0 |  |
| `flux_j_1fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_lsst_disk_sersic` | double | uJy |  | 0 | Gext LSST band source flux from the Disk+Sersic fit |
| `fluxerr_g_ext_lsst_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_u_ext_lsst_2fwhm_aper` | double |  |  | 0 |  |
| `flux_y_disk_sersic` | double | uJy |  | 0 | NIR Y band source flux from the Disk+Sersic fit |
| `fluxerr_y_1fwhm_aper` | double |  |  | 0 |  |
| `flux_u_ext_megacam_3fwhm_aper` | double |  |  | 0 |  |
| `object_id` | long | NA |  | 1 | Euclid unique source identifier |
| `fluxerr_z_ext_panstarrs_4fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_u_ext_lsst_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Uext LSST band (TPHOT measurement) |
| `flux_i_ext_lsst_3fwhm_aper` | double |  |  | 0 |  |
| `flux_r_ext_decam_templfit` | double | uJy |  | 0 | Rext DECam band source template fitting flux (TPHOT measurement) |
| `flux_vis_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_j_sersic` | double | uJy |  | 0 | NIR J band source flux error from the Sersic fit |
| `flux_r_ext_decam_2fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_h_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to NIR H band (TPHOT measurement) |
| `fluxerr_z_ext_decam_2fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_lsst_4fwhm_aper` | double |  |  | 0 |  |
| `parent_id` | long | NA |  | 0 | ID of the parent sources of a deblended object |
| `flux_g_ext_jpcam_sersic` | double | uJy |  | 0 | Gext JPCAM band source flux from the Sersic fit |
| `flux_u_ext_decam_2fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_u_ext_megacam_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Uext Megacam band (TPHOT measurement) |
| `kron_radius` | double | pix |  | 1 | Major semi-axis (in pixels) of the elliptical aperture used for total (Kron) aperture photometry on the detection image |
| `fluxerr_vis_to_g_ext_lsst_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Gext LSST band (TPHOT measurement) |
| `gaia_match_quality` | double | NA |  | 0 | The quality of the GAIA match |
| `fluxerr_u_ext_megacam_3fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_panstarrs_4fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_lsst_1fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_lsst_sersic` | double | uJy |  | 0 | Iext LSST band source flux from the Sersic fit |
| `flag_r_ext_decam` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the RextDECam flag image |
| `sersic_fract_j_disk_sersic_err` | double | NA |  | 0 | NIR J band Sersic fraction error |
| `fluxerr_g_ext_jpcam_3fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_hsc_sersic` | double | uJy |  | 0 | Zext HSC band source flux from the Sersic fit |
| `fluxerr_z_ext_decam_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_vis_to_z_ext_hsc_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Zext HSC band (TPHOT measurement) |
| `sersic_fract_g_ext_decam_disk_sersic_err` | double | NA |  | 0 | Gext DECam band Sersic fraction error |
| `fluxerr_vis_disk_sersic` | double | uJy |  | 0 | VIS band source flux error from the Disk+Sersic fit |
| `flux_nir_stack_2fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_z_ext_lsst_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Zext LSST band (TPHOT measurement) |
| `flux_z_ext_lsst_sersic` | double | uJy |  | 0 | Zext LSST band source flux from the Sersic fit |
| `fluxerr_u_ext_decam_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_j_1fwhm_aper` | double |  |  | 0 |  |
| `spurious_flag` | short | NA |  | 0 | Spurious source flag |
| `fluxerr_i_ext_panstarrs_sersic` | double | uJy |  | 0 | Iext PS band source flux error from the Sersic fit |
| `fluxerr_u_ext_lsst_templfit` | double | uJy |  | 0 | Uext LSST band source template fitting flux error (TPHOT measurement) |
| `flux_segmentation` | double | uJy |  | 0 | VIS or NIR stack band source segmented area flux |
| `flux_j_3fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_z_ext_hsc_disk_sersic_err` | double | NA |  | 0 | Zext HSC band Sersic fraction error |
| `flux_g_ext_jpcam_disk_sersic` | double | uJy |  | 0 | Gext JPCAM band source flux from the Disk+Sersic fit |
| `sersic_fract_i_ext_decam_disk_sersic_err` | double | NA |  | 0 | Iext DECam band Sersic fraction error |
| `flag_y` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the NIR Y flag image |
| `flux_i_ext_decam_sersic` | double | uJy |  | 0 | Iext DECam band source flux from the Sersic fit |
| `fluxerr_i_ext_decam_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_vis_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_u_ext_megacam_1fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_i_ext_panstarrs_3fwhm_aper` | double |  |  | 0 |  |
| `avg_trans_wave_y` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the NIR Y band |
| `flux_i_ext_lsst_disk_sersic` | double | uJy |  | 0 | Iext LSST band source flux from the Disk+Sersic fit |
| `fluxerr_r_ext_megacam_3fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_jpcam_1fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_z_ext_panstarrs_disk_sersic` | double | uJy |  | 0 | Zext PS band source flux error from the Disk+Sersic fit |
| `flux_g_ext_lsst_2fwhm_aper` | double |  |  | 0 |  |
| `flag_u_ext_decam` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the UextDECam flag image |
| `fluxerr_i_ext_panstarrs_1fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_g_ext_hsc_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Gext HSC band (TPHOT measurement) |
| `sersic_fract_z_ext_panstarrs_disk_sersic` | double | NA |  | 0 | Zext PS band Sersic fraction |
| `fluxerr_r_ext_decam_3fwhm_aper` | double |  |  | 0 |  |
| `flux_r_ext_decam_1fwhm_aper` | double |  |  | 0 |  |
| `avg_trans_wave_i_ext_lsst` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the LSST I band |
| `fluxerr_vis_to_u_ext_lsst_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Uext LSST band (TPHOT measurement) |
| `flux_z_ext_hsc_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_g_ext_decam_disk_sersic` | double | uJy |  | 0 | Gext DECam band source flux error from the Disk+Sersic fit |
| `sersic_fract_r_ext_megacam_disk_sersic_err` | double | NA |  | 0 | Rext Megacam band Sersic fraction error |
| `fluxerr_vis_to_z_ext_lsst_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Zext LSST band (TPHOT measurement) |
| `fluxerr_g_ext_lsst_templfit` | double | uJy |  | 0 | Gext LSST band source template fitting flux error (TPHOT measurement) |
| `flag_vis` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the VIS flag image |
| `flux_j_2fwhm_aper` | double |  |  | 0 |  |
| `flux_h_disk_sersic` | double | uJy |  | 0 | NIR H band source flux from the Disk+Sersic fit |
| `flux_g_ext_decam_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_j_2fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_g_ext_hsc_disk_sersic_err` | double | NA |  | 0 | Gext HSC band Sersic fraction error |
| `flux_vis_to_z_ext_decam_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Zext DECam band (TPHOT measurement) |
| `flux_vis_to_y_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to NIR Y band (TPHOT measurement) |
| `flux_g_ext_hsc_2fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_4fwhm_aper` | double |  |  | 0 |  |
| `data_set_release_part3` | int |  |  | 0 |  |
| `fluxerr_i_ext_lsst_3fwhm_aper` | double |  |  | 0 |  |
| `position_angle` | double | deg |  | 0 | Position angle (CCW/x) of the source (SExtractor THETA_IMAGE) range: -90 up to +90 decimal degrees |
| `position_angle_err` | double | deg |  | 0 | Position angle error |
| `right_ascension_psf_fitting` | double | deg |  | 0 | Source RA coordinate derived by the PSF-fitting photometry method |
| `avg_trans_wave_z_ext_lsst` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the LSST Z band |
| `fluxerr_vis_sersic` | double | uJy |  | 0 | VIS band source flux error from the Sersic fit |
| `sersic_fract_u_ext_lsst_disk_sersic` | double | NA |  | 0 | Uext LSST band Sersic fraction |
| `flux_j_sersic` | double | uJy |  | 1 | NIR J band source flux from the Sersic fit |
| `blended_prob` | double | NA |  | 0 | Probability that the source is blended with another source |
| `sersic_fract_u_ext_megacam_disk_sersic_err` | double | NA |  | 0 | Uext Megacam band Sersic fraction error |
| `flag_z_ext_lsst` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Zext LSST flag image |
| `avg_trans_wave_r_ext_decam` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the DECam R band |
| `flux_r_ext_decam_disk_sersic` | double | uJy |  | 0 | Rext DECam band source flux from the Disk+Sersic fit |
| `fluxerr_r_ext_lsst_disk_sersic` | double | uJy |  | 0 | Rext LSST band source flux error from the Disk+Sersic fit |
| `semimajor_axis` | double | pix |  | 0 | Semi-major axis of the source (from Asterism) |
| `fluxerr_z_ext_hsc_disk_sersic` | double | uJy |  | 0 | Zext HSC band source flux error from the Disk+Sersic fit |
| `fluxerr_z_ext_hsc_1fwhm_aper` | double |  |  | 0 |  |
| `flux_r_ext_decam_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_vis_to_g_ext_jpcam_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Gext JPCAM band (TPHOT measurement) |
| `flux_g_ext_decam_sersic` | double | uJy |  | 0 | Gext DECam band source flux from the Sersic fit |
| `fluxerr_z_ext_lsst_disk_sersic` | double | uJy |  | 0 | Zext LSST band source flux error from the Disk+Sersic fit |
| `flux_z_ext_panstarrs_disk_sersic` | double | uJy |  | 0 | Zext PS band source flux from the Disk+Sersic fit |
| `flux_z_ext_decam_1fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_g_ext_decam_disk_sersic` | double | NA |  | 0 | Gext DECam band Sersic fraction |
| `flux_i_ext_panstarrs_2fwhm_aper` | double |  |  | 0 |  |
| `data_set_release_part2` | char |  |  | 0 |  |
| `flux_u_ext_megacam_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_r_ext_megacam_disk_sersic` | double | uJy |  | 0 | Rext Megacam band source flux error from the Disk+Sersic fit |
| `fluxerr_nir_stack_3fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_jpcam_4fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_g_ext_jpcam_disk_sersic_err` | double | NA |  | 0 | Gext JPCAM band Sersic fraction error |
| `deblended_flag` | short | NA |  | 0 | Flag marking if the object was originally blended with another one |
| `sersic_fract_z_ext_decam_disk_sersic_err` | double | NA |  | 0 | Zext DECam band Sersic fraction error |
| `flux_g_ext_hsc_1fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_decam_1fwhm_aper` | double |  |  | 0 |  |
| `flux_r_ext_lsst_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_vis_to_y_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to NIR Y band (TPHOT measurement) |
| `ellipticity` | double | NA |  | 0 | A parametrization of how stretched an object is in the detection band, computed from the minor and major axes of the object itself (directly from SExtractor) |
| `fluxerr_g_ext_hsc_disk_sersic` | double | uJy |  | 0 | Gext HSC band source flux error from the Disk+Sersic fit |
| `fluxerr_vis_psf` | double | uJy |  | 0 | VIS band source PSF-fitting photometry flux error (TPHOT measurement) |
| `fluxerr_u_ext_megacam_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_u_ext_lsst_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_vis_to_h_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to NIR H band (TPHOT measurement) |
| `sersic_fract_i_ext_panstarrs_disk_sersic_err` | double | NA |  | 0 | Iext PS band Sersic fraction error |
| `fluxerr_j_templfit` | double | uJy |  | 0 | NIR J band source template fitting flux error (TPHOT measurement) |
| `flag_g_ext_hsc` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Gext HSC flag image |
| `flux_j_disk_sersic` | double | uJy |  | 0 | NIR J band source flux from the Disk+Sersic fit |
| `fluxerr_i_ext_decam_3fwhm_aper` | double |  |  | 0 |  |
| `mumax_minus_mag` | double | mag/arcsec2 |  | 0 | The difference between MU_MAX and MAG_STARGAL_SEP, valid even for NIR-only sources |
| `flux_z_ext_lsst_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_z_ext_lsst_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_segmentation` | double | uJy |  | 0 | VIS or NIR stack band source total flux (Kron aperture) |
| `fluxerr_vis_to_u_ext_decam_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Uext DECam band (TPHOT measurement) |
| `avg_trans_wave_g_ext_lsst` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the LSST G band |
| `flux_u_ext_lsst_templfit` | double | uJy |  | 0 | Uext LSST band source template fitting flux (TPHOT measurement) |
| `flux_u_ext_lsst_2fwhm_aper` | double |  |  | 0 |  |
| `semimajor_axis_err` | double | pix |  | 0 | Semi-major axis error |
| `flux_z_ext_lsst_4fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_panstarrs_templfit` | double | uJy |  | 0 | Zext PS band source template fitting flux (TPHOT measurement) |
| `fluxerr_i_ext_panstarrs_disk_sersic` | double | uJy |  | 0 | Iext PS band source flux error from the Disk+Sersic fit |
| `sersic_fract_z_ext_panstarrs_disk_sersic_err` | double | NA |  | 0 | Zext PS band Sersic fraction error |
| `fluxerr_g_ext_hsc_templfit` | double | uJy |  | 0 | Gext HSC band source template fitting flux error (TPHOT measurement) |
| `flux_u_ext_lsst_1fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_i_ext_decam_disk_sersic` | double | NA |  | 0 | Iext DECam band Sersic fraction |
| `fluxerr_u_ext_megacam_disk_sersic` | double | uJy |  | 0 | Uext Megacam band source flux error from the Disk+Sersic fit |
| `fluxerr_g_ext_jpcam_sersic` | double | uJy |  | 0 | Gext JPCAM band source flux error from the Sersic fit |
| `avg_trans_wave_g_ext_hsc` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the HSC G band |
| `avg_trans_wave_z_ext_panstarrs` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the PS Z band |
| `fluxerr_nir_stack_4fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_i_ext_lsst_disk_sersic_err` | double | NA |  | 0 | Iext LSST band Sersic fraction error |
| `flux_z_ext_hsc_templfit` | double | uJy |  | 0 | Zext HSC band source template fitting flux (TPHOT measurement) |
| `fluxerr_nir_stack_1fwhm_aper` | double |  |  | 0 |  |
| `binary_flag` | short | NA |  | 0 | Flag for potentially binary stars |
| `flux_i_ext_lsst_templfit` | double | uJy |  | 0 | Iext LSST band source template fitting flux (TPHOT measurement) |
| `fluxerr_r_ext_decam_disk_sersic` | double | uJy |  | 0 | Rext DECam band source flux error from the Disk+Sersic fit |
| `flux_u_ext_megacam_sersic` | double | uJy |  | 0 | Uext Megacam band source flux from the Sersic fit |
| `flag_g_ext_lsst` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Gext LSST flag image |
| `sersic_fract_u_ext_megacam_disk_sersic` | double | NA |  | 0 | Uext Megacam band Sersic fraction |
| `flux_g_ext_lsst_templfit` | double | uJy |  | 0 | Gext LSST band source template fitting flux (TPHOT measurement) |
| `fluxerr_r_ext_decam_4fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_g_ext_hsc_2fwhm_aper` | double |  |  | 0 |  |
| `flux_r_ext_megacam_disk_sersic` | double | uJy |  | 0 | Rext Megacam band source flux from the Disk+Sersic fit |
| `fluxerr_g_ext_hsc_3fwhm_aper` | double |  |  | 0 |  |
| `mag_stargal_sep` | double | mag |  | 0 | Magnitude used to compute POINT_LIKE_PROB |
| `fluxerr_r_ext_decam_2fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_decam_3fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_hsc_templfit` | double | uJy |  | 0 | Gext HSC band source template fitting flux (TPHOT measurement) |
| `flux_z_ext_hsc_2fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_r_ext_decam_sersic` | double | uJy |  | 0 | Rext DECam band source flux error from the Sersic fit |
| `sersic_fract_vis_disk_sersic` | double | NA |  | 0 | VIS band Sersic fraction |
| `fluxerr_i_ext_lsst_1fwhm_aper` | double |  |  | 0 |  |
| `flux_i_ext_panstarrs_disk_sersic` | double | uJy |  | 0 | Iext PS band source flux from the Disk+Sersic fit |
| `she_flag` | short | NA |  | 0 | Flags for objects SHE might want to remove (eg. bright stars) |
| `flag_i_ext_lsst` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Iext LSST flag image |
| `vis_det` | short | NA |  | 1 | Flag to indicate if the source is detected in the VIS mosaic (1) or is only detected in the NIR mosaic (0) |
| `fluxerr_i_ext_panstarrs_4fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_r_ext_decam_disk_sersic_err` | double | NA |  | 0 | Rext DECam band Sersic fraction error |
| `spurious_prob` | double | NA |  | 0 | Probability between 0 and 1 that the source is spurious |
| `flux_z_ext_panstarrs_3fwhm_aper` | double |  |  | 0 |  |
| `flux_vis_to_r_ext_megacam_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Rext Megacam band (TPHOT measurement) |
| `fluxerr_i_ext_lsst_templfit` | double | uJy |  | 0 | Iext LSST band source template fitting flux error (TPHOT measurement) |
| `right_ascension` | double | deg | pos.eq.ra;meta.main | 1 | Source barycenter RA coordinate (SExtractor ALPHA_J2000) decimal degrees |
| `avg_trans_wave_h` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the NIR H band |
| `flux_g_ext_hsc_sersic` | double | uJy |  | 0 | Gext HSC band source flux from the Sersic fit |
| `flux_r_ext_lsst_4fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_jpcam_templfit` | double | uJy |  | 0 | Gext JPCAM band source template fitting flux (TPHOT measurement) |
| `fluxerr_vis_to_u_ext_megacam_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Uext Megacam band (TPHOT measurement) |
| `fluxerr_g_ext_decam_templfit` | double | uJy |  | 0 | Gext DECam band source template fitting flux error (TPHOT measurement) |
| `fluxerr_z_ext_lsst_4fwhm_aper` | double |  |  | 0 |  |
| `patch_id_list` | long |  |  | 1 |  |
| `flux_y_1fwhm_aper` | double |  |  | 0 |  |
| `sersic_fract_g_ext_jpcam_disk_sersic` | double | NA |  | 0 | Gext JPCAM band Sersic fraction |
| `sersic_fract_z_ext_decam_disk_sersic` | double | NA |  | 0 | Zext DECam band Sersic fraction |
| `flux_h_1fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_decam_4fwhm_aper` | double |  |  | 0 |  |
| `basic_download_data_oid` | long |  |  | 1 |  |
| `flux_r_ext_lsst_1fwhm_aper` | double |  |  | 0 |  |
| `flux_z_ext_lsst_disk_sersic` | double | uJy |  | 0 | Zext LSST band source flux from the Disk+Sersic fit |
| `fluxerr_y_4fwhm_aper` | double |  |  | 0 |  |
| `avg_trans_wave_j` | double | Angstrom |  | 0 | Average filter transmission curve wavelength for the NIR J band |
| `gal_ebv_err` | double | mag |  | 0 | Error on galactic E(B-V) according to the reference Planck map |
| `flux_vis_to_z_ext_hsc_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Zext HSC band (TPHOT measurement) |
| `fluxerr_z_ext_hsc_templfit` | double | uJy |  | 0 | Zext HSC band source template fitting flux error (TPHOT measurement) |
| `flux_i_ext_decam_4fwhm_aper` | double |  |  | 0 |  |
| `flux_u_ext_megacam_1fwhm_aper` | double |  |  | 0 |  |
| `flux_u_ext_megacam_templfit` | double | uJy |  | 0 | Uext Megacam band source template fitting flux (TPHOT measurement) |
| `flux_r_ext_lsst_3fwhm_aper` | double |  |  | 0 |  |
| `fluxerr_i_ext_decam_disk_sersic` | double | uJy |  | 0 | Iext DECam band source flux error from the Disk+Sersic fit |
| `flux_vis_to_r_ext_lsst_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Rext LSST band (TPHOT measurement) |
| `fluxerr_r_ext_lsst_3fwhm_aper` | double |  |  | 0 |  |
| `flux_u_ext_lsst_disk_sersic` | double | uJy |  | 0 | Uext LSST band source flux from the Disk+Sersic fit |
| `flag_nir_stack` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the NIR stack flag image |
| `fwhm` | double |  |  | 0 |  |
| `fluxerr_i_ext_lsst_disk_sersic` | double | uJy |  | 0 | Iext LSST band source flux error from the Disk+Sersic fit |
| `sersic_fract_h_disk_sersic_err` | double | NA |  | 0 | NIR H band Sersic fraction error |
| `flux_vis_to_i_ext_panstarrs_templfit` | double | uJy |  | 0 | VIS band source flux on a VIS image PSF-matched to Iext PS band (TPHOT measurement) |
| `fluxerr_u_ext_lsst_1fwhm_aper` | double |  |  | 0 |  |
| `flag_r_ext_lsst` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the Rext LSST flag image |
| `flux_y_3fwhm_aper` | double |  |  | 0 |  |
| `flux_g_ext_decam_templfit` | double | uJy |  | 0 | Gext DECam band source template fitting flux (TPHOT measurement) |
| `flux_h_sersic` | double | uJy |  | 1 | NIR H band source flux from the Sersic fit |
| `sersic_fract_r_ext_megacam_disk_sersic` | double | NA |  | 0 | Rext Megacam band Sersic fraction |
| `sersic_fract_i_ext_lsst_disk_sersic` | double | NA |  | 0 | Iext LSST band Sersic fraction |
| `fluxerr_y_sersic` | double | uJy |  | 0 | NIR Y band source flux error from the Sersic fit |
| `flag_z_ext_decam` | int | NA |  | 0 | Objects flag keeping track of the flagged pixels in the ZextDECam flag image |
| `declination` | double | deg | pos.eq.dec;meta.main | 1 | Source barycenter DEC coordinate (SExtractor DELTA_J2000) decimal degrees |
| `fluxerr_vis_to_i_ext_lsst_templfit` | double | uJy |  | 0 | VIS band source flux error on a VIS image PSF-matched to Iext LSST band (TPHOT measurement) |
| `flux_r_ext_megacam_templfit` | double | uJy |  | 0 | Rext Megacam band source template fitting flux (TPHOT measurement) |
| `calblock_id_list` | char |  |  | 1 |  |
