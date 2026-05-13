#!/bin/bash
# Run once on a fresh Hetzner Ubuntu 24.04 server
# Assumes repo is already cloned to /app
# Usage: cd /app && bash scripts/setup_server.sh <deploy_public_key>
# Example: bash scripts/setup_server.sh "ssh-ed25519 AAAA..."

set -e

DEPLOY_PUBLIC_KEY=${1:?"Usage: bash scripts/setup_server.sh <deploy_public_key>"}

echo "=== spark.practice server setup ==="

# 1. Update system
apt-get update && apt-get upgrade -y

# 2. Install Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker

# 3. Install Docker Compose v2
apt-get install -y docker-compose-plugin

# 4. Configure firewall
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP (Cloudflare proxies this)
ufw --force enable

# 5. Add deploy public key for GitHub Actions
echo "$DEPLOY_PUBLIC_KEY" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo "✓ Deploy key added"

# 6. Copy env template
cp apps/api/.env.prod.example apps/api/.env.prod
echo "✓ Env template copied"

echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  1. nano apps/api/.env.prod  — fill in real secrets"
echo "  2. Add GitHub secrets: SERVER_IP, SERVER_USER, SSH_PRIVATE_KEY"
echo "  3. git push origin main  — triggers first auto-deploy"
echo "  4. make seed-prod  — seed problem datasets"
