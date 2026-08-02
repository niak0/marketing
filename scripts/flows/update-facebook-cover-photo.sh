#!/usr/bin/env bash
# Facebook Page kapak görselini günceller (2 adım: foto yükle -> cover olarak set et).
# Kullanım: ./update-facebook-cover-photo.sh <image_url> [offset_y]
#   offset_y: 0-100 arası dikey konum, varsayılan 50 (ortalanmış)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [[ $# -lt 1 ]]; then
  echo "Kullanım: $0 <image_url> [offset_y]" >&2
  exit 1
fi

IMAGE_URL="$1"
OFFSET_Y="${2:-50}"

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

echo "1/2 Görsel Page albümüne yükleniyor (feed'e düşmeden)..."
UPLOAD_RESPONSE=$(curl -s -X POST "${API}/${META_PAGE_ID}/photos" \
  --data-urlencode "url=${IMAGE_URL}" \
  --data-urlencode "published=false" \
  --data-urlencode "no_feed_story=true" \
  --data-urlencode "access_token=${META_PAGE_ACCESS_TOKEN}")

PHOTO_ID=$(echo "$UPLOAD_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

if [[ -z "$PHOTO_ID" ]]; then
  echo "HATA: Görsel yüklenemedi (adım 1/2 - POST /{page-id}/photos)." >&2
  echo "$UPLOAD_RESPONSE" >&2
  exit 1
fi
echo "   Photo ID: $PHOTO_ID"

echo "2/2 Kapak görseli olarak set ediliyor..."
COVER_RESPONSE=$(curl -s -X POST "${API}/${META_PAGE_ID}" \
  --data-urlencode "cover=${PHOTO_ID}" \
  --data-urlencode "offset_y=${OFFSET_Y}" \
  --data-urlencode "access_token=${META_PAGE_ACCESS_TOKEN}")

SUCCESS=$(echo "$COVER_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('success', False))")

if [[ "$SUCCESS" != "True" ]]; then
  echo "HATA: Kapak görseli set edilemedi (adım 2/2 - POST /{page-id})." >&2
  echo "$COVER_RESPONSE" >&2
  exit 1
fi

echo "Kapak görseli güncellendi."
