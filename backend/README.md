# TrackZen — Backend API

Real, working implementation of the pipeline: synthetic data → AI priority
scoring (XGBoost + SHAP) → auction negotiation → OR-Tools safety scheduling →
NetworkX digital-twin impact check.

Every module here actually runs — this isn't pseudocode. Tested end-to-end
during development: XGBoost trains on startup, SHAP explains every score,
OR-Tools CP-SAT returns a real optimal/feasible schedule, NetworkX correctly
detects when a corridor has no safe alternate route.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then open http://localhost:8000/docs for interactive Swagger docs, or hit:

```bash
curl -X POST http://localhost:8000/api/plan/full \
  -H "Content-Type: application/json" \
  -d '{"num_tasks": 10}'
```

## Endpoints

| Method | Path | What it does |
|---|---|---|
| GET | `/api/health` | Liveness check |
| GET | `/api/network` | Returns the corridor network graph (stations + edges) |
| POST | `/api/plan/full` | Runs the full pipeline once: generate tasks → score → negotiate → schedule → simulate impact |
| GET | `/api/plan/weekly` | Runs the pipeline once per day for 7 days and returns a weekly view |

## Module map

- `app/synthetic_data.py` — stand-in for TMS/SMMS/TDMS/COA feeds (swap for real DB/API calls in production)
- `app/priority.py` — XGBoost regressor trained on synthetic historical outcomes + SHAP TreeExplainer for per-task reasoning; folds in monsoon/heatwave seasonal risk
- `app/auction.py` — groups same-corridor requests, picks a priority anchor, explains the combination in plain language
- `app/scheduler.py` — Google OR-Tools CP-SAT model: hard no-double-booking-per-department constraint, soft objective pulls urgent tasks earlier and same-corridor tasks into a compact combined window
- `app/digital_twin.py` — NetworkX graph of the corridor network; simulates where diverted traffic goes if a corridor is blocked and flags when an alternate route would be pushed over capacity

## Deploying free-tier (Render)

1. Push this folder to a GitHub repo.
2. On Render: New → Web Service → connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Copy the deployed URL into the frontend's `VITE_API_BASE` env var.

## Next steps to extend (good starting points in Antigravity)

- Replace `synthetic_data.py` with real TMS/SMMS/TDMS/COA connectors once available
- Replace the synthetic XGBoost training set in `priority.py` with real closed-work-order history
- Add a persistence layer (PostgreSQL via SQLAlchemy) so plans survive restarts
- Extend `digital_twin.py` with a full GNN (PyTorch Geometric) for larger networks
- Add authentication + a controller "approve/reject" endpoint before a block is finalized
