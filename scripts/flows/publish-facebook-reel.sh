#!/usr/bin/env bash
# Facebook Page'e Reel yayınlar (Video API resumable upload, file_url ile).
# Video specs: 9:16, 540x960-1080x1920px, 3-90sn, 24-60fps.
# Kullanım: ./publish-facebook-reel.sh <video_url> <description> [--dry-run]
#   --dry-run: video'yu yükler, işlenmesini bekler, YAYINLAMADAN (finish) durur.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [[ $# -lt 2 ]]; then
  echo "Kullanım: $0 <video_url> <description> [--dry-run]" >&2
  exit 1
fi

VIDEO_URL="$1"
DESCRIPTION="$2"
DRY_RUN=false
[[ "${3:-}" == "--dry-run" ]] && DRY_RUN=true

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

echo "1/4 Upload session başlatılıyor..."
START_RESPONSE=$(curl -s -X POST "${API}/${META_PAGE_ID}/video_reels" \
  --data-urlencode "upload_phase=start" \
  --data-urlencode "access_token=${META_PAGE_ACCESS_TOKEN}")

VIDEO_ID=$(echo "$START_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('video_id',''))")

if [[ -z "$VIDEO_ID" ]]; then
  echo "HATA: Upload session başlatılamadı (adım 1/4 - upload_phase=start)." >&2
  echo "$START_RESPONSE" >&2
  exit 1
fi
echo "   Video ID: $VIDEO_ID"

echo "2/4 Video URL'den yükleniyor..."
UPLOAD_RESPONSE=$(curl -s -X POST "https://rupload.facebook.com/video-upload/v21.0/${VIDEO_ID}" \
  -H "Authorization: OAuth ${META_PAGE_ACCESS_TOKEN}" \
  -H "file_url: ${VIDEO_URL}")

UPLOAD_SUCCESS=$(echo "$UPLOAD_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('success', False))")

if [[ "$UPLOAD_SUCCESS" != "True" ]]; then
  echo "HATA: Video yüklenemedi (adım 2/4 - rupload file_url)." >&2
  echo "$UPLOAD_RESPONSE" >&2
  exit 1
fi

echo "3/4 Upload tamamlanma durumu bekleniyor (uploading_phase=complete bekleniyor)..."
# Not: processing_phase, upload_phase=finish çağrılmadan "not_started" kalır —
# finish öncesi asıl bekleneni gösteren alan uploading_phase.
UPLOADING_STATUS=""
for i in $(seq 1 60); do
  STATUS_RESPONSE=$(curl -s "${API}/${VIDEO_ID}?fields=status&access_token=${META_PAGE_ACCESS_TOKEN}")
  UPLOADING_STATUS=$(echo "$STATUS_RESPONSE" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('status', {}).get('uploading_phase', {}).get('status', ''))
")
  [[ "$UPLOADING_STATUS" == "complete" ]] && break
  if echo "$UPLOADING_STATUS" | grep -qi "error"; then
    echo "HATA: Video yüklenirken hata (adım 3/4 - uploading_phase status: $UPLOADING_STATUS)." >&2
    echo "$STATUS_RESPONSE" >&2
    exit 1
  fi
  sleep 5
done

if [[ "$UPLOADING_STATUS" != "complete" ]]; then
  echo "HATA: Video 5dk içinde upload'ı tamamlamadı (adım 3/4 - son durum: $UPLOADING_STATUS)." >&2
  exit 1
fi
echo "   Durum: complete"

if $DRY_RUN; then
  echo "4/4 --dry-run: yayınlama (finish) atlandı. Video yüklendi ama yayınlanmadı."
  echo "   Video ID: $VIDEO_ID (bu ID ile daha sonra upload_phase=finish çağrılabilir)"
  exit 0
fi

echo "4/4 Yayınlanıyor (upload_phase=finish)..."
FINISH_RESPONSE=$(curl -s -X POST "${API}/${META_PAGE_ID}/video_reels" \
  --data-urlencode "video_id=${VIDEO_ID}" \
  --data-urlencode "upload_phase=finish" \
  --data-urlencode "video_state=PUBLISHED" \
  --data-urlencode "description=${DESCRIPTION}" \
  --data-urlencode "access_token=${META_PAGE_ACCESS_TOKEN}")

FINISH_SUCCESS=$(echo "$FINISH_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('success', False))")

if [[ "$FINISH_SUCCESS" != "True" ]]; then
  echo "HATA: Yayınlama başarısız (adım 4/4 - upload_phase=finish)." >&2
  echo "$FINISH_RESPONSE" >&2
  exit 1
fi

echo "Yayınlandı: Video ID $VIDEO_ID"
echo "Link: https://www.facebook.com/reel/${VIDEO_ID}"
