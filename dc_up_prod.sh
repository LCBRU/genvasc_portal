#!/usr/bin/env bash
. ./production_environment
docker-compose -f docker-compose.yml -f production.yml up -d