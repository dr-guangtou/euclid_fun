"""bubbletea's frozen Gaia point-source logistic selector (v1), applied from its JSON manifest.

The model is a median imputer with missing-value indicators, a standard scaler and a logistic regression. It is
evaluated here directly from the stored statistics and coefficients, so scikit-learn is not needed. Feature
definitions follow bubbletea `scripts/utils/point_source_selector.py` exactly; stage 0 checks the scores against
bubbletea's own stored scores.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

selector_version = "point_source_logistic_model_v1"
minimum_g_magnitude = 11.26291847229004
maximum_g_magnitude = 21.75798797607422
raw_gaia_columns = [
    "source_id",
    "ra",
    "dec",
    "phot_g_mean_mag",
    "phot_bp_mean_mag",
    "phot_rp_mean_mag",
    "phot_bp_rp_excess_factor",
    "astrometric_excess_noise",
    "astrometric_excess_noise_sig",
    "parallax",
    "parallax_error",
    "pmra",
    "pmra_error",
    "pmdec",
    "pmdec_error",
    "pmra_pmdec_corr",
    "ruwe",
    "ipd_frac_multi_peak",
    "ipd_frac_odd_win",
]


def add_model_features(rows: pd.DataFrame) -> pd.DataFrame:
    """Derive the nine model features; missing inputs stay missing."""
    rows = rows.copy()
    rows["bp_rp"] = rows["phot_bp_mean_mag"] - rows["phot_rp_mean_mag"]
    rows["absolute_parallax_zero_significance"] = rows["parallax"].abs() / rows["parallax_error"].where(
        rows["parallax_error"].gt(0)
    )
    standardized_pmra = rows["pmra"] / rows["pmra_error"]
    standardized_pmdec = rows["pmdec"] / rows["pmdec_error"]
    correlation = rows["pmra_pmdec_corr"]
    valid_motion = (
        rows["pmra_error"].gt(0)
        & rows["pmdec_error"].gt(0)
        & np.isfinite(standardized_pmra)
        & np.isfinite(standardized_pmdec)
        & np.isfinite(correlation)
        & correlation.abs().lt(1)
    )
    squared_significance = (
        np.square(standardized_pmra)
        + np.square(standardized_pmdec)
        - 2 * correlation * standardized_pmra * standardized_pmdec
    ) / (1 - np.square(correlation))
    rows["proper_motion_zero_significance"] = np.sqrt(squared_significance.clip(lower=0).where(valid_motion))
    rows["log1p_astrometric_excess_noise"] = np.log1p(rows["astrometric_excess_noise"].clip(lower=0))
    rows["log1p_astrometric_excess_noise_sig"] = np.log1p(rows["astrometric_excess_noise_sig"].clip(lower=0))
    rows["log_ruwe"] = np.log(rows["ruwe"].where(rows["ruwe"].gt(0)))
    for source in (
        "ipd_frac_multi_peak",
        "ipd_frac_odd_win",
        "absolute_parallax_zero_significance",
        "proper_motion_zero_significance",
    ):
        rows[f"log1p_{source}"] = np.log1p(rows[source].clip(lower=0))
    return rows


class FrozenSelector:
    def __init__(self, manifest_path: Path):
        manifest = json.loads(Path(manifest_path).read_text())
        if manifest["model_version"] != selector_version:
            raise RuntimeError(f"unexpected selector version {manifest['model_version']}")
        self.features = manifest["input_features"]
        self.threshold = float(manifest["threshold"])
        self.imputer_values = np.array([manifest["imputer_statistics"][name] for name in self.features])
        self.indicator_indices = manifest["missing_indicator_input_indices"]
        transformed = manifest["transformed_features"]
        self.scaler_mean = np.array([manifest["scaler_mean"][name] for name in transformed])
        self.scaler_scale = np.array([manifest["scaler_scale"][name] for name in transformed])
        self.coefficients = np.array([manifest["coefficients"][name] for name in transformed])
        self.intercept = float(manifest["intercept"])

    def score(self, rows: pd.DataFrame) -> pd.DataFrame:
        """All input rows with the frozen probability, the decision and whether G is in the valid range."""
        scored = add_model_features(rows)
        values = scored[self.features].to_numpy(dtype=float)
        missing = ~np.isfinite(values)
        filled = np.where(missing, self.imputer_values, values)
        design = np.hstack([filled, missing[:, self.indicator_indices].astype(float)])
        logit = ((design - self.scaler_mean) / self.scaler_scale) @ self.coefficients + self.intercept
        scored["selector_probability"] = 1.0 / (1.0 + np.exp(-logit))
        scored["selector_selected"] = scored["selector_probability"] >= self.threshold
        scored["selector_in_valid_g_range"] = scored["phot_g_mean_mag"].between(
            minimum_g_magnitude, maximum_g_magnitude
        )
        return scored
