#!/usr/bin/env bash
# QCAL-cQED-v1 · Despliegue Automatizado de Servidor gRPC + Túnel
# f₀ = 141.7001 Hz · Target: Mac Mini (Darwin)
# Sello: ∴𓂀Ω∞³Φ

set -euo pipefail

GREEN='\033[0;32m'; CYAN='\033[0;36m'
YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
PORT=50051
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/sim/grpc_server.log"

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN} 🜁 INICIANDO DESPLIEGUE gRPC LIVE · QCAL-cQED-v1 ${NC}"
echo -e "${CYAN}======================================================================${NC}"

# 1. Dependencias
echo -e "\n${YELLOW}[1/5] Verificando dependencias...${NC}"
for cmd in cargo protoc cloudflared; do
    if ! command -v $cmd &>/dev/null; then
        echo -e "${YELLOW}! $cmd no encontrado. Instalando..."
        brew install $cmd
    fi
done
echo -e "${GREEN}✓ Dependencias listas${NC}"

# 2. Compilar servidor
echo -e "\n${YELLOW}[2/5] Compilando servidor gRPC (Release)...${NC}"
cd "${SCRIPT_DIR}/sim"
cargo build --release --bin hil-server 2>&1 | tail -3
echo -e "${GREEN}✓ Compilación exitosa${NC}"

# 3. Liberar puerto
echo -e "\n${YELLOW}[3/5] Preparando puerto ${PORT}...${NC}"
if lsof -Pi :${PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
    PID=$(lsof -Pi :${PORT} -sTCP:LISTEN -t)
    kill -9 "${PID}" 2>/dev/null
    echo -e "${YELLOW}! Puerto liberado (PID ${PID})${NC}"
fi

# 4. Iniciar servidor
echo -e "\n${YELLOW}[4/5] Arrancando servidor...${NC}"
nohup "${SCRIPT_DIR}/sim/target/release/hil-server" > "${LOG_FILE}" 2>&1 &
SERVER_PID=$!
sleep 2

if kill -0 ${SERVER_PID} 2>/dev/null; then
    echo -e "${GREEN}✓ Servidor activo (PID: ${SERVER_PID})${NC}"
else
    echo -e "${RED}✗ Error: servidor no arrancó${NC}"
    tail -5 "${LOG_FILE}"
    exit 1
fi

# 5. Túnel Cloudflare
echo -e "\n${YELLOW}[5/5] Abriendo túnel público...${NC}"
echo -e "${CYAN}----------------------------------------------------------------------${NC}"
cloudflared tunnel --url "http://localhost:${PORT}" --http2-origin 2>&1 | while read -r line; do
    echo -e "${CYAN}${line}${NC}"
    if [[ "$line" =~ https://[a-zA-Z0-9-]+\.trycloudflare\.com ]]; then
        URL=$(echo "$line" | grep -oE "https://[a-zA-Z0-9-]+\.trycloudflare\.com")
        echo -e "\n${GREEN}==============================================================${NC}"
        echo -e "${GREEN} 🟢 gRPC EN VIVO — ENDPOINT PÚBLICO ${NC}"
        echo -e "${GREEN} ${URL} ${NC}"
        echo -e "${GREEN} Puerto local: localhost:${PORT} ${NC}"
        echo -e "${GREEN}==============================================================${NC}"
    fi
done
