#!/usr/bin/env bash
# çevirmen başlatıcı
cd "$(dirname "$(readlink -f "$0")")" && exec python3 -m cevirmen "$@"
