#!/bin/bash
echo "Removing services"
docker compose down || true
echo "Removing images"
docker image rm -f rabnmgr7/drawer-flask-app:latest || true
docker image rm -f rabnmgr7/drawer-mysql-db:latest || true
echo "Creating docker compose services"
docker compose up -d
