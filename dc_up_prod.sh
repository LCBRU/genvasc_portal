#!/usr/bin/env bash
. ./environment
docker-compose -f docker-compose.yml -f production.yml up -d