#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 5 ]; then
  echo "Usage: PGPASSWORD=... $0 <host> <port> <database> <user> <sql_file>" >&2
  exit 1
fi

if [ -z "${PGPASSWORD:-}" ]; then
  echo "PGPASSWORD must be set" >&2
  exit 1
fi

PGHOST="$1"
PGPORT="$2"
PGDATABASE="$3"
PGUSER="$4"
SQL_FILE="$5"

export PGPASSWORD

CONN="host=${PGHOST} port=${PGPORT} dbname=${PGDATABASE} user=${PGUSER} sslmode=require"

resolve_psql() {
  if command -v psql >/dev/null 2>&1; then
    echo "psql"
    return
  fi

  for candidate in \
    /opt/homebrew/opt/libpq/bin/psql \
    /usr/local/opt/libpq/bin/psql; do
    if [ -x "$candidate" ]; then
      echo "$candidate"
      return
    fi
  done

  if command -v docker >/dev/null 2>&1; then
    echo "docker"
    return
  fi

  echo "psql not found. Install a client (brew install libpq) or ensure Docker is available." >&2
  exit 1
}

PSQL_MODE="$(resolve_psql)"

run_psql() {
  if [ "$PSQL_MODE" = "docker" ]; then
    docker run --rm -i -e PGPASSWORD postgres:16-alpine \
      psql "$CONN" "$@"
    return
  fi

  "$PSQL_MODE" "$CONN" "$@"
}

LAST_ERR=""
for attempt in $(seq 1 30); do
  if err="$(run_psql -c "SELECT 1" 2>&1)"; then
    break
  fi
  LAST_ERR="$err"

  if [ "$attempt" -eq 30 ]; then
    echo "RDS not reachable after 30 attempts" >&2
    if [ -n "$LAST_ERR" ]; then
      echo "$LAST_ERR" >&2
    fi
    exit 1
  fi

  sleep 10
done

if run_psql -tAc "SELECT to_regclass('public.meals')" | grep -q meals; then
  echo "Schema already applied, skipping init.sql"
  exit 0
fi

if [ "$PSQL_MODE" = "docker" ]; then
  docker run --rm -i -e PGPASSWORD -v "${SQL_FILE}:/init.sql:ro" postgres:16-alpine \
    psql "$CONN" -v ON_ERROR_STOP=1 -f /init.sql
else
  run_psql -v ON_ERROR_STOP=1 -f "$SQL_FILE"
fi

echo "Schema applied successfully"
