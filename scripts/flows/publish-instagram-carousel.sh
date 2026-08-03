#!/usr/bin/env bash
# Instagram Business hesabına çok görselli (carousel) post yayınlar.
# Kullanım: ./publish-instagram-carousel.sh <caption> <url1> <url2> ... [--dry-run]
#   2-10 arası görsel URL'i verilebilir.
#   --dry-run: carousel container'ı hazırlar, YAYINLAMADAN durur.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [[ $# -lt 3 ]]; then
  echo "Kullanım: $0 <caption> <url1> <url2> ... [--dry-run]" >&2
  exit 1
fi

CAPTION="$1"
shift

DRY_RUN=false
URLS=()
for arg in "$@"; do
  if [[ "$arg" == "--dry-run" ]]; then
    DRY_RUN=true
  else
    URLS+=("$arg")
  fi
done

if [[ ${#URLS[@]} -lt 2 || ${#URLS[@]} -gt 10 ]]; then
  echo "HATA: Carousel için 2-10 görsel gerekir (verilen: ${#URLS[@]})." >&2
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

json_get() {
  python3 -c "import sys,json; print(json.load(sys.stdin).get('$1',''))"
}

echo "1/4 ${#URLS[@]} slayt için container oluşturuluyor..."
CHILDREN=()
for index in "${!URLS[@]}"; do
  RESPONSE=$(curl -s -X POST "${API}/${META_IG_BUSINESS_ACCOUNT_ID}/media" \
    --data-urlencode "image_url=${URLS[$index]}" \
    --data-urlencode "is_carousel_item=true" \
    --data-urlencode "access_token=${META_ACCESS_TOKEN}")

  CHILD_ID=$(echo "$RESPONSE" | json_get id)
  if [[ -z "$CHILD_ID" ]]; then
    echo "HATA: Slayt $((index + 1)) container'ı oluşturulamadı." >&2
    echo "$RESPONSE" >&2
    exit 1
  fi
  CHILDREN+=("$CHILD_ID")
  echo "   slayt $((index + 1))/${#URLS[@]}: $CHILD_ID"
done

CHILDREN_CSV=$(IFS=,; echo "${CHILDREN[*]}")

echo "2/4 Carousel container oluşturuluyor..."
CAROUSEL_RESPONSE=$(curl -s -X POST "${API}/${META_IG_BUSINESS_ACCOUNT_ID}/media" \
  --data-urlencode "media_type=CAROUSEL" \
  --data-urlencode "children=${CHILDREN_CSV}" \
  --data-urlencode "caption=${CAPTION}" \
  --data-urlencode "access_token=${META_ACCESS_TOKEN}")

CAROUSEL_ID=$(echo "$CAROUSEL_RESPONSE" | json_get id)
if [[ -z "$CAROUSEL_ID" ]]; then
  echo "HATA: Carousel container oluşturulamadı (adım 2/4)." >&2
  echo "$CAROUSEL_RESPONSE" >&2
  exit 1
fi
echo "   Carousel ID: $CAROUSEL_ID"

echo "3/4 İşlenme durumu bekleniyor (FINISHED bekleniyor)..."
STATUS_CODE=""
for _ in $(seq 1 20); do
  STATUS_RESPONSE=$(curl -s "${API}/${CAROUSEL_ID}?fields=status_code&access_token=${META_ACCESS_TOKEN}")
  STATUS_CODE=$(echo "$STATUS_RESPONSE" | json_get status_code)
  [[ "$STATUS_CODE" == "FINISHED" ]] && break
  if [[ "$STATUS_CODE" == "ERROR" ]]; then
    echo "HATA: Carousel işlenirken hata (adım 3/4)." >&2
    echo "$STATUS_RESPONSE" >&2
    exit 1
  fi
  sleep 3
done

if [[ "$STATUS_CODE" != "FINISHED" ]]; then
  echo "HATA: Carousel 60sn içinde FINISHED olmadı (son durum: $STATUS_CODE)." >&2
  exit 1
fi
echo "   Durum: FINISHED"

if $DRY_RUN; then
  echo "4/4 --dry-run: yayınlama atlandı. Carousel hazır ama yayınlanmadı."
  exit 0
fi

echo "4/4 Yayınlanıyor..."
PUBLISH_RESPONSE=$(curl -s -X POST "${API}/${META_IG_BUSINESS_ACCOUNT_ID}/media_publish" \
  --data-urlencode "creation_id=${CAROUSEL_ID}" \
  --data-urlencode "access_token=${META_ACCESS_TOKEN}")

POST_ID=$(echo "$PUBLISH_RESPONSE" | json_get id)
if [[ -z "$POST_ID" ]]; then
  echo "HATA: Yayınlama başarısız (adım 4/4)." >&2
  echo "$PUBLISH_RESPONSE" >&2
  exit 1
fi

PERMALINK=$(curl -s "${API}/${POST_ID}?fields=permalink&access_token=${META_ACCESS_TOKEN}" | json_get permalink)

echo "Yayınlandı: Post ID $POST_ID"
[[ -n "$PERMALINK" ]] && echo "Link: $PERMALINK"
