#!/bin/bash

set -euo pipefail

PROJECT_DIR="/home/ubuntu/svcs"
BACKUP_ROOT="/home/ubuntu/backups/svcs"
WORKSPACE_DIR="${WORKSPACE}"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_PATH="${BACKUP_ROOT}/svcs_${TIMESTAMP}"

echo "========================================"
echo "SVCS Deployment Started"
echo "Timestamp : ${TIMESTAMP}"
echo "Workspace : ${WORKSPACE_DIR}"
echo "========================================"

mkdir -p "${BACKUP_ROOT}"

############################################
# ROLLBACK FUNCTION
############################################

rollback() {

    echo ""
    echo "========================================"
    echo "ROLLBACK INITIATED"
    echo "========================================"

    cd /

    echo "Stopping failed deployment..."
    docker compose -f "${PROJECT_DIR}/docker-compose.yml" down || true

    echo "Cleaning deployment directory..."
    find "${PROJECT_DIR}" \
        -mindepth 1 \
        -maxdepth 1 \
        ! -name '.env' \
        -exec rm -rf {} +

    echo "Restoring backup..."
    rsync -a \
        "${BACKUP_PATH}/" \
        "${PROJECT_DIR}/"

    cd "${PROJECT_DIR}"

    echo "Starting rollback deployment..."

    if ! docker compose up --build -d; then
        echo "Rollback deployment failed."
        exit 1
    fi

    sleep 30

    CONTAINER_ID=$(docker compose ps -q svcs)

    if [ -z "${CONTAINER_ID}" ]; then
        echo "Rollback failed: container not found"
        exit 1
    fi

    STATUS=$(docker inspect \
        --format='{{.State.Status}}' \
        "${CONTAINER_ID}")

    echo "Rollback container status: ${STATUS}"

    if [ "${STATUS}" != "running" ]; then
        echo "Rollback deployment unhealthy"
        exit 1
    fi

    echo ""
    echo "Rollback completed successfully."
    echo ""

    exit 1
}

############################################
# BACKUP CURRENT DEPLOYMENT
############################################

echo "[1/6] Creating backup..."

mkdir -p "${BACKUP_PATH}"

rsync -a \
    --exclude='backup' \
    --exclude='__pycache__' \
    --exclude='.git' \
    "${PROJECT_DIR}/" \
    "${BACKUP_PATH}/"

echo "Backup completed:"
echo "${BACKUP_PATH}"

############################################
# STOP CURRENT DEPLOYMENT
############################################

echo "[2/6] Stopping current containers..."

cd "${PROJECT_DIR}"

docker compose down || true

############################################
# REPLACE APPLICATION FILES
############################################

echo "[3/6] Replacing application files..."

find "${PROJECT_DIR}" \
    -mindepth 1 \
    -maxdepth 1 \
    ! -name '.env' \
    -exec rm -rf {} +

rsync -a \
    --delete \
    --exclude='.env' \
    "${WORKSPACE_DIR}/" \
    "${PROJECT_DIR}/"

############################################
# BUILD + START
############################################

echo "[4/6] Building containers..."

cd "${PROJECT_DIR}"

if ! docker compose up --build -d; then
    echo "Docker build/start failed."
    rollback
fi

############################################
# HEALTH CHECK
############################################

echo "[5/6] Waiting for startup..."

sleep 30

CONTAINER_ID=$(docker compose ps -q svcs)

if [ -z "${CONTAINER_ID}" ]; then
    echo "Container not created."
    rollback
fi

STATUS=$(docker inspect \
    --format='{{.State.Status}}' \
    "${CONTAINER_ID}")

RESTART_COUNT=$(docker inspect \
    --format='{{.RestartCount}}' \
    "${CONTAINER_ID}")

echo "Container Status : ${STATUS}"
echo "Restart Count    : ${RESTART_COUNT}"

if [ "${STATUS}" != "running" ]; then
    echo "Container is not running."
    rollback
fi

if [ "${RESTART_COUNT}" -gt 0 ]; then
    echo "Container is restarting/crashing."
    rollback
fi

############################################
# SUCCESS
############################################

echo "[6/6] Deployment successful"

echo "========================================"
echo "SVCS Deployment Completed Successfully"
echo "========================================"
