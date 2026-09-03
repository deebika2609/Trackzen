# TrackZen — Frontend Dashboard

React + Tailwind dashboard that talks to the FastAPI backend. Builds cleanly
with `npm run build` (verified — 0 errors).

## Run locally

Make sure the backend is running first (see `../backend/README.md`),
then:

```bash
npm install
npm run dev
```

Open http://localhost:5173

By default it calls `http://localhost:8000`. To point at a deployed backend,
create a `.env` file:

```
VITE_API_BASE=https://your-backend.onrender.com
```

## Pages (tabs)

- **Requests** — pending maintenance tasks (synthetic TMS/SMMS/TDMS feed)
- **Priority Engine** — XGBoost urgency scores with SHAP-based explanations
- **Auction & Coordination** — which department requests got fairly combined into one block, and why
- **Schedule** — the OR-Tools CP-SAT output as a day calendar, colour-coded by department
- **Corridor Impact** — Leaflet map of the corridor network, colour-coded by the digital twin's risk assessment if that corridor is blocked

## Stack

React 18 · Tailwind CSS · react-big-calendar · react-leaflet · axios · Vite

## Next steps to extend (good starting points in Antigravity)

- Wire the "Re-run Optimization" button to a controller approval flow (POST back to the backend to confirm a block)
- Replace fake station coordinates in `CorridorMap.jsx` with real GPS data once available
- Add a weekly/monthly calendar view backed by `/api/plan/weekly`
- Add auth (e.g. Firebase Auth) before deploying beyond a demo
