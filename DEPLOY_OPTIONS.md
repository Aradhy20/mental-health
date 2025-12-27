# 🚀 Final Deployment Step (Koyeb)

You have provided your MongoDB Atlas connection string! We are ready to launch.

## ⚠️ CRITICAL STEP: The Password
The connection string you gave has a placeholder: `<db_password>`.
**You MUST replace this with your actual password** inside the Koyeb dashboard.

## 🔗 Your Custom Deployment Link

**[👉 Click Here to Deploy to Koyeb](https://app.koyeb.com/deploy?type=git&repository=github.com/Aradhy20/mental-health&branch=main&env[MONGO_DETAILS]=mongodb%2Bsrv%3A%2F%2Fmentalhealth_db_user%3A%3Cdb_password%3E%40cluster0.8tevbr6.mongodb.net%2F%3FappName%3DCluster0&env[MONGO_DB_NAME]=mental_health_db&env[PORT]=8000)**

### Instructions:
1.  Click the link above.
2.  Login to Koyeb.
3.  Look for the **MONGO_DETAILS** field.
4.  It will say: `mongodb+srv://mentalhealth_db_user:<db_password>@cluster0...`
5.  **DELETE** `<db_password>` and type your **REAL PASSWORD** (the one you set for `mentalhealth_db_user`).
    *   *Example*: if password is `secret123`, it should look like `...user:secret123@cluster0...`
6.  Click **Deploy**.

## 🎤 Verifying Microphone
After deployment, wait 5 minutes.
Visit the URL (e.g., `https://mental-health-app.koyeb.app`).
Ensure it starts with `https://`.
Go to the Assistant/Voice page and allow microphone permissions.
