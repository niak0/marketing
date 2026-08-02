#!/usr/bin/env bash
# Facebook Page profil resmini günceller.
# Kullanım: ./update-facebook-profile-picture.sh <image_url>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [[ $# -lt 1 ]]; then
  echo "Kullanım: $0 <image_url>" >&2
  exit 1
fi

IMAGE_URL="$1"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "HATA: $ENV_FILE bulunamadı." >&2
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

for var in META_PAGE_ACCESS_TOKEN META_PAGE_ID; do
  if [[ -z "${!var:-}" ]]; then
    echo "HATA: $var .env içinde tanımlı değil." >&2
    exit 1
  fi
done

API="https://graph.facebook.com/v21.0"

echo "1/1 Profil resmi güncelleniyor..."
RESPONSE=$(curl -s -X POST "${API}/${META_PAGE_ID}/picture" \
  --data-urlencode "picture=${IMAGE_URL}" \
  --data-urlencode "access_token=${META_PAGE_ACCESS_TOKEN}")

SUCCESS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('success', False))")

if [[ "$SUCCESS" != "True" ]]; then
  echo "HATA: Profil resmi güncellenemedi (POST /{page-id}/picture)." >&2
  echo "$RESPONSE" >&2
  exit 1
fi

echo "Profil resmi güncellendi."
