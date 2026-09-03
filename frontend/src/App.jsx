import React, { useEffect, useState } from "react";
import axios from "axios";
import TaskTable from "./components/TaskTable.jsx";
import PriorityPanel from "./components/PriorityPanel.jsx";
import AuctionPanel from "./components/AuctionPanel.jsx";
import ScheduleCalendar from "./components/ScheduleCalendar.jsx";
import CorridorMap from "./components/CorridorMap.jsx";

// If VITE_API_BASE is set, use it; otherwise use empty string for same-origin requests
const API_BASE = (import.meta.env.VITE_API_BASE || "").replace(/\/$/, "");

const TABS = ["Requests", "Priority Engine", "Auction & Coordination", "Schedule", "Corridor Impact"];

export default function App() {
  const [plan, setPlan] = useState(null);
  const [network, setNetwork] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tab, setTab] = useState(TABS[0]);

  const docsUrl = API_BASE ? `${API_BASE}/docs` : "/docs";
  const apiUrl = API_BASE ? `${API_BASE}/api` : "/api";

  const runPipeline = async () => {
    setLoading(true);
    setError(null);
    try {
      const [planRes, netRes] = await Promise.all([
        axios.post(`${API_BASE}/api/plan/full`, { num_tasks: 10 }),
        axios.get(`${API_BASE}/api/network`),
      ]);
      setPlan(planRes.data);
      setNetwork(netRes.data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runPipeline();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      {/* Top Banner & Header */}
      <header className="bg-navy text-white px-6 py-4 flex flex-wrap items-center justify-between gap-4 shadow-lg border-b border-blue-900">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber flex items-center justify-center text-navy font-bold text-2xl shadow">
            🚆
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight">TrackZen — RailSync Intelligent Block Planning</h1>
              <span className="bg-blue-800 text-blue-200 text-xs px-2.5 py-0.5 rounded-full font-semibold border border-blue-600">
                SIH 2026
              </span>
            </div>
            <p className="text-xs text-blue-200 mt-0.5">
              FastAPI · XGBoost + SHAP · OR-Tools CP-SAT · NetworkX Digital Twin
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Quick links to Swagger Docs & API Base */}
          <a
            href={docsUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-semibold px-3.5 py-2 rounded-lg border border-blue-700 transition shadow-sm"
            title="Open Interactive FastAPI Swagger Documentation"
          >
            <span>📘</span> API Docs (/docs)
          </a>
          <a
            href={apiUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-semibold px-3.5 py-2 rounded-lg border border-blue-700 transition shadow-sm"
            title="Open Raw Backend API Root"
          >
            <span>⚡</span> Backend API (/api)
          </a>

          {/* Status badge */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-950 border border-blue-800">
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                loading ? "bg-amber animate-ping" : error ? "bg-rose-500" : "bg-emerald-400"
              }`}
            />
            <span className={error ? "text-rose-300" : "text-emerald-300"}>
              {loading ? "Optimizing..." : error ? "API Disconnected" : "API Live"}
            </span>
          </div>

          <button
            onClick={runPipeline}
            disabled={loading}
            className="bg-amber text-navy font-bold px-4 py-2 rounded-lg hover:brightness-105 active:scale-95 disabled:opacity-50 transition shadow"
          >
            {loading ? "Running Pipeline…" : "Re-run Optimization"}
          </button>
        </div>
      </header>

      {/* Tabs */}
      <nav className="flex gap-2 px-6 pt-3 bg-white border-b border-gray-200 shadow-sm overflow-x-auto">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2.5 text-sm font-semibold rounded-t-lg transition border-b-2 ${
              tab === t
                ? "bg-slate-100 text-navy border-amber"
                : "text-gray-500 hover:text-navy border-transparent hover:bg-gray-50"
            }`}
          >
            {t}
          </button>
        ))}
      </nav>

      {/* Error state */}
      {error && (
        <div className="mx-6 mt-6 p-4 bg-rose-50 border border-rose-200 rounded-xl flex items-center justify-between text-rose-800">
          <div>
            <p className="font-bold text-sm">Unable to connect to TrackZen Backend API</p>
            <p className="text-xs text-rose-600 mt-1">
              Ensure the backend is running. If running locally, launch the backend on port 8000.
            </p>
          </div>
          <button
            onClick={runPipeline}
            className="bg-rose-600 text-white font-semibold text-xs px-3 py-1.5 rounded-lg hover:bg-rose-700 transition"
          >
            Retry Connection
          </button>
        </div>
      )}

      {/* Main Content Area */}
      <main className="p-6 flex-1 max-w-7xl w-full mx-auto">
        {!plan && !error ? (
          <div className="bg-white rounded-2xl p-12 shadow-sm border border-gray-100 text-center flex flex-col items-center justify-center">
            <div className="w-12 h-12 border-4 border-navy border-t-amber rounded-full animate-spin mb-4" />
            <p className="font-semibold text-gray-700">Loading TrackZen Pipeline Output…</p>
            <p className="text-xs text-gray-400 mt-1">Running synthetic generation, priority engine & CP-SAT solver</p>
          </div>
        ) : (
          plan && (
            <>
              {tab === "Requests" && <TaskTable tasks={plan.tasks} />}
              {tab === "Priority Engine" && <PriorityPanel scores={plan.priority_scores} />}
              {tab === "Auction & Coordination" && (
                <AuctionPanel groups={plan.auction_groups} tasks={plan.tasks} />
              )}
              {tab === "Schedule" && <ScheduleCalendar schedule={plan.schedule} />}
              {tab === "Corridor Impact" && network && (
                <CorridorMap network={network} impact={plan.network_impact} />
              )}
            </>
          )
        )}
      </main>

      {/* Footer with Submission Metadata */}
      <footer className="bg-white border-t border-gray-200 px-6 py-4 text-xs text-gray-500 flex flex-wrap items-center justify-between gap-2 mt-auto">
        <div>
          <span className="font-semibold text-navy">TrackZen RailSync Prototype</span> — Smart India Hackathon (SIH) 2026
        </div>
        <div className="flex gap-4">
          <a href={docsUrl} target="_blank" rel="noopener noreferrer" className="hover:text-navy underline">
            Swagger API Docs (/docs)
          </a>
          <a href={apiUrl} target="_blank" rel="noopener noreferrer" className="hover:text-navy underline">
            Backend Root (/api)
          </a>
          <a href={API_BASE ? `${API_BASE}/api/health` : "/api/health"} target="_blank" rel="noopener noreferrer" className="hover:text-navy underline">
            Health Check (/api/health)
          </a>
        </div>
      </footer>
    </div>
  );
}

