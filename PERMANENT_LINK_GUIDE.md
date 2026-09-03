# 🚆 TrackZen RailSync — Permanent Public Link & SIH 2026 Submission Guide

---

## 📌 1. Why Did You See "localhost refused to connect"?

1. **`localhost` is NOT a public internet link** — `localhost` (or `127.0.0.1`) only points inside your current computer.
2. **The local server was turned off** — When you closed the terminal or hadn't started the Python backend, your browser couldn't reach port 8000.
3. **Crucial for SIH 2026**: **Smart India Hackathon judges and evaluators cannot access `localhost`** from their laptops or phones. You must submit **public live HTTPS links** (`https://...`) that stay online 24/7.

---

## 🚀 2. What We Have Built (Unified Single-Server Architecture)

We have unified your entire project into a **single self-contained fullstack server**:
Your backend now serves the built React frontend dashboard directly.

Once deployed on the cloud, **one single permanent domain** gives you all 3 links required for SIH 2026:

| Submission Field | URL Path | What the Evaluators Will See |
| :--- | :--- | :--- |
| **Frontend Dashboard** | `https://your-app-name.onrender.com/` | Full interactive UI with corridor maps, schedule calendar, priority engine & auction panels. |
| **Backend API Docs** | `https://your-app-name.onrender.com/docs` | Interactive Swagger UI where judges can test live endpoints in real time. |
| **Backend API Base** | `https://your-app-name.onrender.com/api` | JSON health, endpoints directory, and status payload. |

---

## 🌐 3. How to Get Your Free Permanent 24/7 Cloud Link (2 Minutes)

Follow these simple steps to host your prototype permanently on **Render.com** (100% Free, no credit card needed, stays live 24/7):

### Step 1: Push Your Code to GitHub
1. Create a new repository on [GitHub](https://github.com/new) named `railsync-prototype` (or `trackzen`).
2. In your project folder, run:
```bash
git init
git add .
git commit -m "TrackZen RailSync SIH 2026 Prototype"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/railsync-prototype.git
git push -u origin main
```

---

### Step 2: Deploy on Render.com (1-Click Free Hosting)
1. Sign up / Log in to [Render.com](https://render.com) (Log in with GitHub).
2. Click **New +** → **Web Service**.
3. Select your GitHub repository (`railsync-prototype`).
4. Fill in the settings:
   - **Name**: `trackzen-railsync` (or any custom name you prefer)
   - **Region**: `Singapore` or `Oregon`
   - **Runtime**: `Python`
   - **Build Command**:
     ```bash
     cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: `Free`
5. Click **Create Web Service**.

Render will automatically build your React frontend, install your Python packages, and launch the unified server.

---

### Step 3: Copy Your Permanent Links for SIH 2026 Submission
Once deployment completes (takes ~2 minutes), Render gives you a permanent HTTPS URL like:
`https://trackzen-railsync.onrender.com`

You can now submit these 3 permanent URLs in your SIH 2026 submission form:
1. **Frontend Prototype URL**:
   `https://trackzen-railsync.onrender.com/`
2. **Interactive API Documentation (Swagger)**:
   `https://trackzen-railsync.onrender.com/docs`
3. **Backend Base URL**:
   `https://trackzen-railsync.onrender.com/api`

---

## ⚡ 4. Alternative 1-Click Free Hosting Options

If you prefer other platforms, your project is already pre-configured for:

### Option B: Railway.app (Automatic via Dockerfile)
1. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub Repo**.
2. Railway detects the `Dockerfile` automatically and deploys both frontend & backend.

### Option C: Koyeb.com
1. Go to [koyeb.com](https://koyeb.com) → **Create App** → Select GitHub Repo.
2. Uses the included `Dockerfile` with free tier.

---

## 💻 5. How to Run Locally on Your Computer (Without Any Errors)

We created two 1-click batch files in your project root:

1. **`START_LOCAL.bat`** (Recommended):
   - Double-click this file to start the unified production server.
   - It will automatically launch on `http://localhost:8000` and open your browser.
2. **`START_DEV.bat`**:
   - Double-click this file for development mode with hot reloading on `http://localhost:5173`.
