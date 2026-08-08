# Deployment configuration

NUTU's frontend and backend are separate services. The browser must call the
backend through its public HTTPS URL; `127.0.0.1` only works on the computer
running the backend locally.

## Frontend

Set this environment variable in the production frontend host (for example,
Vercel), then redeploy so Vite includes it in the new build:

```text
VITE_API_BASE_URL=https://your-backend.example.com
```

Do not use `http://127.0.0.1:8000` in a hosted deployment.

## Backend

Set `CORS_ORIGINS` on the backend host to a comma-separated list of any
non-Vercel frontend origins, for example:

```text
CORS_ORIGINS=https://your-frontend.example.com,https://nutu-ai-yassin.vercel.app
```

Vercel preview and production `*.vercel.app` origins are already supported.
