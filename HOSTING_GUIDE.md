# 🚀 Global Hosting Guide: Vercel + Render Hybrid

To host the **MindfulAI** ecosystem, we use a hybrid strategy because of the heavy AI models (Torch/Transformers) which exceed Vercel's size limits.

## 🏗️ Architecture Overview
*   **Frontend (Next.js)**: Hosted on **Vercel** (Best-in-class performance).
*   **API Gateway (Express)**: Hosted on **Render** or **Railway** (Reliable long-running Node.js).
*   **AI Intelligence (Python)**: Hosted on **Render** (Support for Docker and heavy ML libs).

---

## 🔼 Step 1: Deploy Frontend to Vercel

1.  **Push your code** to a GitHub/GitLab repository.
2.  Go to [Vercel Dashboard](https://vercel.com/new).
3.  Import the repository.
4.  **Crucial Settings**:
    *   **Root Directory**: Set to `frontend`.
    *   **Framework Preset**: Select `Next.js`.
5.  **Environment Variables**: Add the following:
    *   `NEXT_PUBLIC_API_URL`: The URL of your Express Backend (from Step 2).
6.  Click **Deploy**.

---

## 🟢 Step 2: Deploy Express API to Render

1.  Create a new **Web Service** on [Render](https://render.com/).
2.  Connect your repository.
3.  **Settings**:
    *   **Root Directory**: `backend-express`
    *   **Build Command**: `npm install`
    *   **Start Command**: `npm start`
4.  **Environment Variables**:
    *   `MONGODB_URI`: Your MongoDB Atlas connection string.
    *   `JWT_SECRET`: A long random string.
    *   `AI_TEXT_SERVICE_URL`: URL of Text Service (from Step 3).
    *   `AI_VOICE_SERVICE_URL`: URL of Voice Service (from Step 3).
    *   `AI_FACE_SERVICE_URL`: URL of Face Service (from Step 3).

---

## 🤖 Step 3: Deploy AI Microservices (Render Docker)

Since these services use heavy AI libraries, we use Docker.

1.  Create a new **Web Service** on Render for EACH service (`text`, `voice`, `face`).
2.  **Settings**:
    *   **Runtime**: `Docker`
    *   **Docker Context**: `.` (Root)
    *   **Docker File Path**: `backend/text_service/Dockerfile` (adjust for others).
3.  **Environment Variables**:
    *   `MONGODB_URI`: Link to your MongoDB Atlas.

---

## 📡 Cross-Origin Resource Sharing (CORS)
I have already configured the Express backend to accept requests from any origin, but for production, you should update `backend-express/server.js` with your specific Vercel URL once deployed.

---

## 💡 Pro Tip: MongoDB Atlas
Do not use `localhost:27017` for hosting.
1.  Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2.  Whitelist `0.0.0.0/0` (or use specific IPs if preferred).
3.  Use the connection string in your `.env` files.
