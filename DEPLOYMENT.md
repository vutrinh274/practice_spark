# Deployment Guide — spark.practice

## Architecture

```
GitHub (code) ──push──> GitHub Actions ──build──> ghcr.io (Docker image)
                                              └──SSH──> Hetzner VPS
                                                         ├── nginx (port 80)
                                                         ├── api (FastAPI)
                                                         └── spark-connect

Vercel ──auto-deploy──> Next.js frontend
```

---

## Step 0 — Prerequisites

- GitHub account with this repo
- Hetzner account (hetzner.com)
- Cloudflare account (cloudflare.com) with your domain
- Vercel account (vercel.com)

---

## Step 1 — Create Hetzner Server

1. Go to **hetzner.com/cloud** → New Project → "spark-practice"
2. Click **Add Server**:
   - Location: choose closest to your users
   - Image: **Ubuntu 24.04**
   - Type: **CX31** (2 vCPU, 4GB RAM, €15.90/mo) — start here, scale up if needed
   - SSH Keys: Add your SSH public key (`cat ~/.ssh/id_rsa.pub`)
   - Name: `spark-practice`
3. Click **Create & Buy**
4. Note your server **IP address**

---

## Step 2 — Initial Server Setup

SSH into your server:
```bash
ssh root@YOUR_SERVER_IP
```

Run the setup script:
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/practice_spark/main/scripts/setup_server.sh | bash
```

Or manually:
```bash
cd /app
# Script already cloned the repo — just fill in secrets
cp apps/api/.env.prod.example apps/api/.env.prod
nano apps/api/.env.prod  # fill in real values
```

---

## Step 3 — Configure Secrets in `.env.prod`

Edit `/app/apps/api/.env.prod` on the server:

```bash
nano /app/apps/api/.env.prod
```

Fill in:
- `CLERK_SECRET_KEY` — from clerk.com dashboard (use PRODUCTION keys, not test)
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` — from clerk.com
- `STRIPE_SECRET_KEY` — from stripe.com (LIVE keys)
- `ADMIN_SECRET_KEY` — generate: `python3 -c "import secrets; print(secrets.token_hex(32))"`
- `CORS_ORIGINS` — your Vercel frontend URL

---

## Step 4 — Configure Cloudflare

1. Add your domain to Cloudflare (if not already)
2. Go to **DNS** → Add record:
   - Type: **A**
   - Name: `api` (for api.yourdomain.com)
   - Content: your Hetzner server IP
   - Proxy: **ON** (orange cloud) ← important for SSL
3. Add another record for the root domain if needed

---

## Step 5 — Configure GitHub Secrets

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**

Add these secrets:
| Secret | Value |
|---|---|
| `SERVER_IP` | Your Hetzner IP address |
| `SERVER_USER` | `root` |
| `SSH_PRIVATE_KEY` | Contents of `~/.ssh/id_rsa` (private key) |

---

## Step 6 — Deploy Frontend to Vercel

1. Go to **vercel.com** → New Project
2. Import your GitHub repository
3. Configure:
   - Framework: **Next.js**
   - Root directory: `apps/web`
   - Build command: `npm run build`
4. Add Environment Variables:
   - `NEXT_PUBLIC_API_URL` = `https://api.yourdomain.com`
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` = your Clerk publishable key (PRODUCTION)
   - `NEXT_PUBLIC_CLERK_SIGN_IN_URL` = `/sign-in`
   - `NEXT_PUBLIC_CLERK_SIGN_UP_URL` = `/sign-up`
   - `NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL` = `/problems`
   - `NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL` = `/problems`
5. Click **Deploy**

---

## Step 7 — First Deploy

Push to main to trigger CI/CD:
```bash
git push origin main
```

GitHub Actions will:
1. Build the API Docker image
2. Push to `ghcr.io`
3. SSH into Hetzner and pull + restart the API

Watch it: GitHub → Actions tab

---

## Step 8 — Seed Problems on Server

After first deploy, seed the expected.csv files:
```bash
make seed-prod
```

This runs `reference.py` for each problem on the server.

---

## Day-to-Day Operations

```bash
# Deploy new code
git push origin main        # triggers auto-deploy

# View logs
make logs

# Backup database
make backup-db              # saves to backups/

# Restore database
make restore-db FILE=backups/backup_20260509_1200.sql

# SSH into server
ssh root@YOUR_SERVER_IP

# Restart services manually
ssh root@YOUR_SERVER_IP "cd /app && docker compose -f docker-compose.prod.yml restart api"
```

---

## Scaling Up

When you need more resources:
1. Go to Hetzner Cloud → your server → **Rescale**
2. Choose larger instance (CX41 → CX51 etc.)
3. ~2 min downtime
4. Data in volumes is safe

---

## Monitoring

Check server health:
```bash
# Container status
ssh root@YOUR_SERVER_IP "docker compose -f docker-compose.prod.yml ps"

# Resource usage
ssh root@YOUR_SERVER_IP "docker stats --no-stream"

# Disk usage
ssh root@YOUR_SERVER_IP "df -h"
```

---

## Clerk Production Setup

Before going live:
1. Go to clerk.com → your app → **Production** instance
2. Add your domain to allowed origins
3. Copy **Production** API keys (different from test keys)
4. Update `.env.prod` on server with production keys
5. Update Vercel env vars with production publishable key
