#!/bin/bash
# Script untuk restart Odoo dan update module list

cd "d:\bebas lah terserah kamu\port-pak-mada\Portofolio-Pak-Dosen"

echo "=== Stopping Odoo container ==="
docker-compose down

echo "=== Waiting 5 seconds ==="
sleep 5

echo "=== Starting Odoo container ==="
docker-compose up -d

echo "=== Waiting for Odoo to start (30 seconds) ==="
sleep 30

echo "=== Checking Odoo logs ==="
docker-compose logs odoo | tail -50

echo "Done! Module should be available now."
