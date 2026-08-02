#!/usr/bin/env bash
# Instagram Business hesabına Story yayınlar (foto veya video).
# Kullanım: ./publish-instagram-story.sh <media_url> <media_type> [--dry-run]
#   <media_type>: IMAGE veya VIDEO
#   --dry-run: container oluşturur, FINISHED durumunu bekler, YAYINLAMADAN durur.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [[ $# -lt 2 ]]; then
  echo "Kullanım: $0 <media_url> <media_type: IMAGE|VIDEO> [--dry-run]" >&2
  exit 1
fi

MEDIA_URL="$1"
MEDIA_TYPE="$2"
DRY_RUN=false
[[ "${3:-}" == "--dry-run" ]] && DRY_RUN=true

if [[ "$MEDIA_TYPE" != "IMAGE" && "$MEDIA_TYPE" != "VIDEO" ]]; then
  echo "HATA: media_type IMAGE veya VIDEO olmalı, verilen: $MEDIA_TYPE" >&2
  exit 1
fi

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
URL_FIELD="image_url"
[[ "$MEDIA_TYPE" == "VIDEO" ]] && URL_FIELD="video_url"

echo "1/3 Story container oluşturuluyor (media_type=STORIES, ${URL_FIELD})..."
CONTAINER_RESPONSE=$(curl -s -X POST "${API}/${META_IG_BUSINESS_ACCOUNT_ID}/media" \
  --data-urlencode "media_type=STORIES" \
  --data-urlencode "${URL_FIELD}=${MEDIA_URL}" \
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
for i in $(seq 1 30); do
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
  echo "HATA: Container 90sn içinde FINISHED olmadı (adım 2/3 - son durum: $STATUS_CODE)." >&2
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

echo "Yayınlandı: Story ID $POST_ID (24 saat sonra otomatik kaybolur)"
