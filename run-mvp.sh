#!/bin/bash
# Launcher script for MVP Streamlit from project root

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 SaaS Planz MVP Streamlit${NC}"
echo ""
echo "Forwarding to apps/mvp-streamlit/docker-dev.sh..."
echo ""

cd apps/mvp-streamlit
./docker-dev.sh "$@"
