#!/bin/bash
# Run once on a fresh Hetzner Ubuntu 24.04 server
# Usage: bash scripts/setup_server.sh

set -e

echo "=== spark.practice server setup ==="

# 1. Update system
apt-get update && apt-get upgrade -y

# 2. Install dependencies
apt-get install -y docker-compose-plugin make git curl

# 3. Install Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker

# 4. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# 5. Configure firewall
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# 6. Clone repo
mkdir -p ~/practice_spark
cd ~/practice_spark
git clone https://github.com/vutrinh274/practice_spark.git .

# 7. Install Python dependencies
cd apps/api && uv sync && cd ../..

# 8. Copy env template
cp apps/api/.env.prod.example apps/api/.env.prod

echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  1. nano apps/api/.env.prod       — fill in real secrets"
echo "  2. Add deploy key:               echo 'YOUR_DEPLOY_KEY' >> ~/.ssh/authorized_keys"
echo "  3. Add GitHub secrets:           SERVER_IP, SERVER_USER, SSH_PRIVATE_KEY"
echo "  4. git push origin main          — triggers first auto-deploy"
echo "  5. make seed                     — seed problem datasets"
