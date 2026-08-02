#!/usr/bin/env bash
# Instagram Business hesabına organik foto yayınlar (Content Publishing API).
# Kullanım: ./publish-instagram-post.sh <image_url> <caption> [--dry-run]
#   --dry-run: container oluşturur, FINISHED durumunu bekler, YAYINLAMADAN durur.

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
DRY_RUN=false
[[ "${3:-}" == "--dry-run" ]] && DRY_RUN=true

if [[ ! -f "$ENV_FILE" ]]; then
  echo "HATA: $ENV_FILE bulunamadı." >&2
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

for var in META_ACCESS_TOKEN META_IG_BUSINESS_ACCOUNT_ID; do
  if [[ -z "${!var:-}" ]]; then
    echo "HATA: $var .env içinde tanımlı değil." >&2
    exit 1
  fi
done

API="https://graph.facebook.com/v21.0"

echo "1/3 Container oluşturuluyor..."
CONTAINER_RESPONSE=$(curl -s -X POST "${API}/${META_IG_BUSINESS_ACCOUNT_ID}/media" \
  --data-urlencode "image_url=${IMAGE_URL}" \
  --data-urlencode "caption=${CAPTION}" \
  --data-urlencode "access_token=${META_ACCESS_TOKEN}")

CONTAINER_ID=$(echo "$CONTAINER_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

if [[ -z "$CONTAINER_ID" ]]; then
  echo "HATA: Container oluşturulamadı (adım 1/3 - POST /media)." >&2
  echo "$CONTAINER_RESPONSE" >&2
  exit 1
fi
echo "   Container ID: $CONTAINER_ID"

echo "2/3 İşlenme durumu bekleniyor (FINISHED bekleniyor)..."
STATUS_CODE=""
for i in $(seq 1 20); do
  STATUS_RESPONSE=$(curl -s "${API}/${CONTAINER_ID}?fields=status_code,status&access_token=${META_ACCESS_TOKEN}")
  STATUS_CODE=$(echo "$STATUS_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status_code',''))")
  [[ "$STATUS_CODE" == "FINISHED" ]] && break
  if [[ "$STATUS_CODE" == "ERROR" ]]; then
    echo "HATA: Container işlenirken hata (adım 2/3 - status ERROR döndü)." >&2
    echo "$STATUS_RESPONSE" >&2
    exit 1
  fi
  sleep 3
done

if [[ "$STATUS_CODE" != "FINISHED" ]]; then
  echo "HATA: Container 60sn içinde FINISHED olmadı (adım 2/3 - son durum: $STATUS_CODE)." >&2
  exit 1
fi
echo "   Durum: FINISHED"

if $DRY_RUN; then
  echo "3/3 --dry-run: yayınlama atlandı. Container hazır ama yayınlanmadı."
  exit 0
fi

echo "3/3 Yayınlanıyor..."
PUBLISH_RESPONSE=$(curl -s -X POST "${API}/${META_IG_BUSINESS_ACCOUNT_ID}/media_publish" \
  --data-urlencode "creation_id=${CONTAINER_ID}" \
  --data-urlencode "access_token=${META_ACCESS_TOKEN}")

POST_ID=$(echo "$PUBLISH_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

if [[ -z "$POST_ID" ]]; then
  echo "HATA: Yayınlama başarısız (adım 3/3 - POST /media_publish)." >&2
  echo "$PUBLISH_RESPONSE" >&2
  exit 1
fi

PERMALINK_RESPONSE=$(curl -s "${API}/${POST_ID}?fields=permalink&access_token=${META_ACCESS_TOKEN}")
PERMALINK=$(echo "$PERMALINK_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('permalink',''))")

echo "Yayınlandı: Post ID $POST_ID"
[[ -n "$PERMALINK" ]] && echo "Link: $PERMALINK"
