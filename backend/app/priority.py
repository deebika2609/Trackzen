"""
AI Priority Engine.

Trains a small XGBoost regressor on synthetic historical maintenance
outcomes to predict an urgency score (0-100) for each pending task, then
uses SHAP to explain *why* a task received its score — this explainability
is what a controller/engineer actually needs to trust the recommendation.

Weather risk (monsoon / heatwave) is folded in as an extra feature so that
seasonal signals genuinely move the score, not just decorate it.
"""
import random
import numpy as np
import pandas as pd
import xgboost as xgb
import shap

random.seed(7)
np.random.seed(7)

FEATURES = [
    "criticality", "historical_defects", "asset_age_years",
    "traffic_load", "due_in_days", "weather_risk",
]


def _synthetic_training_set(n=800) -> pd.DataFrame:
    """Generates plausible historical (task -> eventual severity) pairs so
    the model learns a sensible, monotonic relationship instead of random
    noise. In production this table is replaced by real closed-work-order
    history from TMS/SMMS/TDMS."""
    df = pd.DataFrame({
        "criticality": np.random.randint(1, 11, n),
        "historical_defects": np.random.randint(0, 16, n),
        "asset_age_years": np.random.randint(1, 31, n),
        "traffic_load": np.random.randint(10, 50, n),
        "due_in_days": np.random.randint(1, 31, n),
        "weather_risk": np.random.randint(0, 2, n),
    })
    # ground-truth urgency generator (nonlinear, with noise) that the model must learn
    urgency = (
        6.5 * df.criticality
        + 1.8 * df.historical_defects
        + 0.6 * df.asset_age_years
        + 0.35 * df.traffic_load
        - 1.1 * df.due_in_days
        + 14 * df.weather_risk
        + np.random.normal(0, 6, n)
    )
    df["urgency_label"] = np.clip(urgency, 0, 130)
    return df


class PriorityEngine:
    def __init__(self):
        train = _synthetic_training_set()
        X, y = train[FEATURES], train["urgency_label"]
        self.model = xgb.XGBRegressor(
            n_estimators=120, max_depth=4, learning_rate=0.08,
            subsample=0.9, colsample_bytree=0.9, random_state=7,
        )
        self.model.fit(X, y)
        self.explainer = shap.TreeExplainer(self.model)
        self._max_label = float(train["urgency_label"].max())

    def weather_risk_flag(self, department: str, month: int) -> int:
        """Monsoon (Jun-Sep) raises TRD/Engineering risk; heatwave (Apr-Jun)
        raises Engineering (rail buckling) risk."""
        monsoon = month in (6, 7, 8, 9) and department in ("TRD", "Engineering")
        heat = month in (4, 5, 6) and department == "Engineering"
        return int(monsoon or heat)

    def score(self, task: dict, month: int) -> dict:
        weather_risk = self.weather_risk_flag(task["department"], month)
        row = pd.DataFrame([{
            "criticality": task["criticality"],
            "historical_defects": task["historical_defects"],
            "asset_age_years": task["asset_age_years"],
            "traffic_load": task["traffic_load"],
            "due_in_days": task["due_in_days"],
            "weather_risk": weather_risk,
        }])
        raw = float(self.model.predict(row)[0])
        score_0_100 = round(float(np.clip(raw / self._max_label * 100, 0, 100)), 1)

        shap_values = self.explainer.shap_values(row)[0]
        contributions = sorted(
            zip(FEATURES, shap_values), key=lambda x: -abs(x[1])
        )
        reasons = []
        label_map = {
            "criticality": "Criticality rating",
            "historical_defects": "History of recurring defects",
            "asset_age_years": "Asset age",
            "traffic_load": "Corridor traffic load",
            "due_in_days": "Time remaining before due date",
            "weather_risk": "Seasonal weather risk (monsoon/heat)",
        }
        for feat, val in contributions[:3]:
            direction = "increases" if val > 0 else "decreases"
            reasons.append(f"{label_map[feat]} {direction} urgency (impact {val:+.1f})")

        return {
            "task_id": task["id"],
            "urgency_score": score_0_100,
            "weather_risk_flag": bool(weather_risk),
            "top_reasons": reasons,
        }

    def score_all(self, tasks: list, month: int) -> list:
        scored = [self.score(t, month) for t in tasks]
        scored.sort(key=lambda s: -s["urgency_score"])
        return scored
