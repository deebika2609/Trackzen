import React from "react";

export default function PriorityPanel({ scores }) {
  return (
    <div className="bg-white rounded-xl shadow p-4">
      <h2 className="font-bold text-navy mb-1">AI Priority Engine — XGBoost + SHAP</h2>
      <p className="text-sm text-gray-500 mb-4">
        Ranked by predicted urgency. Each score is explained by the top contributing factors, including seasonal weather risk.
      </p>
      <div className="space-y-3">
        {scores.map((s) => (
          <div key={s.task_id} className="border rounded-lg p-3">
            <div className="flex items-center justify-between mb-2">
              <span className="font-mono text-sm font-semibold">{s.task_id}</span>
              <div className="flex items-center gap-2">
                {s.weather_risk_flag && (
                  <span className="text-xs bg-amber/20 text-amber-700 px-2 py-0.5 rounded-full">
                    Seasonal risk
                  </span>
                )}
                <div className="w-40 bg-gray-100 rounded-full h-2.5">
                  <div
                    className="bg-navy h-2.5 rounded-full"
                    style={{ width: `${s.urgency_score}%` }}
                  />
                </div>
                <span className="text-sm font-bold w-12 text-right">{s.urgency_score}</span>
              </div>
            </div>
            <ul className="text-xs text-gray-600 list-disc pl-5">
              {s.top_reasons.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
