#!/usr/bin/env bash
# Facebook Page'e foto paylaşır (Graph API /{page-id}/photos).
# Kullanım: ./publish-facebook-post.sh <image_url> <caption> [--dry-run]
#   --dry-run: published=false ile taslak oluşturur, herkese açık YAYINLANMAZ.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [[ $# -lt 2 ]]; then
  echo "Kullanım: $0 <image_url> <caption> [--dry-run]" >&2
  exit 1
fi

IMAGE_URL="$1"
CAPTION="$2"
PUBLISHED=true
[[ "${3:-}" == "--dry-run" ]] && PUBLISHED=false

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

echo "1/1 Sayfaya paylaşılıyor (published=${PUBLISHED})..."
RESPONSE=$(curl -s -X POST "${API}/${META_PAGE_ID}/photos" \
  --data-urlencode "url=${IMAGE_URL}" \
  --data-urlencode "caption=${CAPTION}" \
  --data-urlencode "published=${PUBLISHED}" \
  --data-urlencode "access_token=${META_PAGE_ACCESS_TOKEN}")

POST_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('post_id', d.get('id','')))")

if [[ -z "$POST_ID" ]]; then
  echo "HATA: Paylaşım başarısız (POST /{page-id}/photos)." >&2
  echo "$RESPONSE" >&2
  exit 1
fi

echo "Post ID: $POST_ID"
if [[ "$PUBLISHED" == "true" ]]; then
  echo "Link: https://www.facebook.com/${POST_ID}"
else
  echo "--dry-run: taslak olarak kaydedildi, yayınlanmadı."
fi
