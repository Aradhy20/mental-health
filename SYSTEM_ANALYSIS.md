# 📊 System Analysis & Best Deployment Strategy

## 🧐 Architecture Analysis

Your project is a complex **AI-powered Web Application** with two distinct resource profiles:

1.  **Frontend (Next.js 15)**: 
    *   **Nature**: User Interface, Interactive Dashboards.
    *   **Resource Needs**: Low computational power, fast edge delivery.
    *   **Ideal Host**: **Vercel** (Creators of Next.js). It allows for global edge caching and instant static page loads.

2.  **Backend (FastAPI + AI Models)**:
    *   **Nature**: Heavy computation (PyTorch, Transformers, OpenCV).
    *   **Resource Needs**: 
        *   **RAM**: High (>1GB for loading models).
        *   **Disk**: Large (>500MB+ for library dependencies like Torch).
        *   **Time**: Long running processes (Inference might take seconds).
    *   **Constraint Warning**: **Vercel Serverless Functions (Free Tier)** have a hard limit of **250MB** unzipped code size. Your backend (with PyTorch and Transformers) is likely **>1GB**. Deploying the full AI backend to Vercel will almost certainly fail with `Function Size Error`.

## 🚀 The "Best Way" Deployment Strategy (Free Tier)

To achieve a **Single URL** experience without paying for resources, you need a **Hybrid Architecture**.

### The Plan:
1.  **Backend on Render (Free Tier)**: Render allows Docker container deployments. Docker is the *only* stable way to host your heavy AI dependencies on a free tier.
2.  **Frontend on Vercel**: Hosting the Next.js app.
3.  **"Single URL" Glue**: We use **Next.js Rewrites** to proxy `/api` requests from Vercel to Render. The user never sees `render.com`; they only see your domain.

---

## 🛠️ Step-by-Step Deployment Instructions

### Phase 1: Deploy Backend (Render)
1.  Sign up at [Render.com](https://render.com/).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  **Crucial Configuration**:
    *   **Runtime**: Docker
    *   **Region**: Closest to you (e.g., Singapore/Oregon for India optimization).
    *   **Instance Type**: Free
    *   **Environment Variables**:
        *   `MONGO_DETAILS`: *Your MongoDB connection string*
        *   `MONGO_DB_NAME`: `mental_health_db`
5.  Click **Deploy**.
6.  **Wait**: The first build will take 10-15 minutes because it installs PyTorch.
7.  **Result**: You will get a URL like `https://mental-health-backend.onrender.com`. **Copy this.**

### Phase 2: Deploy Frontend (Vercel)
1.  Sign up at [Vercel.com](https://vercel.com/).
2.  Import your GitHub repository.
3.  **Available Optimizations**: Vercel will auto-detect Next.js.
4.  **Environment Variables**:
    *   `BACKEND_URL`: *Paste your Render URL here (e.g., https://mental-health-backend.onrender.com)*
    *   *Do NOT add a trailing slash (e.g., use `.com`, not `.com/`)*
5.  Click **Deploy**.

### Phase 3: Validation
1.  Visit your **Vercel URL** (e.g., `https://mental-health-app.vercel.app`).
2.  This is your **Single URL**.
3.  Try logging in or running an analysis.
    *   The request goes: `User` -> `Vercel (Frontend)` -> `(Proxy)` -> `Render (Backend)` -> `MongoDB`.

## ⚠️ Important Free Tier Limitations
-   **Cold Starts**: Render's free instances "sleep" after inactivity. The first request might take 50 seconds to wake up. This is unavoidable on free tiers.
-   **Memory**: Render Free gives 512MB RAM. Large AI models might crash the server. If this happens, you may need to use smaller models or external APIs (HuggingFace Inference API) instead of running them locally.

## ✅ Files Prepared for You
-   **`Dockerfile`**: Created at root to enable Render deployment.
-   **`next.config.js`**: Updated to handle the URL rewriting (Proxying).
-   **`backend/requirements.txt`**: Optimized for Mongo.
-   **`backend/requirements_all.txt`**: Includes all AI libs for the Docker container.
