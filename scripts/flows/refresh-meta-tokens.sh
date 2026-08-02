#!/usr/bin/env bash
# Kısa ömürlü bir Meta user token'ını uzun ömürlüye (60 gün) çevirir, ondan
# Page access token'ı türetir ve .env dosyasını günceller.
# Kullanım: ./refresh-meta-tokens.sh <short_lived_user_token>
#
# Kısa ömürlü token nereden alınır:
#   https://developers.facebook.com/tools/explorer/
#   App seç -> User Token -> izinler: instagram_basic, instagram_content_publish,
#   pages_manage_posts, pages_read_engagement, pages_show_list -> Generate.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [[ $# -lt 1 ]]; then
  echo "Kullanım: $0 <short_lived_user_token>" >&2
  exit 1
fi

SHORT_TOKEN="$1"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "HATA: $ENV_FILE bulunamadı." >&2
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

for var in META_APP_ID META_APP_SECRET META_PAGE_ID; do
  if [[ -z "${!var:-}" ]]; then
    echo "HATA: $var .env içinde tanımlı değil." >&2
    exit 1
  fi
done

API="https://graph.facebook.com/v21.0"

json_get() {
  python3 -c "import sys,json;print(json.load(sys.stdin).get('$1',''))"
}

echo "1/4 Uzun ömürlü user token alınıyor..."
EXCHANGE_RESPONSE=$(curl -s -G "${API}/oauth/access_token" \
  --data-urlencode "grant_type=fb_exchange_token" \
  --data-urlencode "client_id=${META_APP_ID}" \
  --data-urlencode "client_secret=${META_APP_SECRET}" \
  --data-urlencode "fb_exchange_token=${SHORT_TOKEN}")

LONG_TOKEN=$(echo "$EXCHANGE_RESPONSE" | json_get access_token)

if [[ -z "$LONG_TOKEN" ]]; then
  echo "HATA: Token takası başarısız (adım 1/4)." >&2
  echo "$EXCHANGE_RESPONSE" >&2
  exit 1
fi
echo "   Uzun ömürlü user token alındı."

echo "2/4 Page access token türetiliyor (Page ID: ${META_PAGE_ID})..."
ACCOUNTS_RESPONSE=$(curl -s -G "${API}/me/accounts" \
  --data-urlencode "access_token=${LONG_TOKEN}")

PAGE_TOKEN=$(echo "$ACCOUNTS_RESPONSE" | python3 -c "
import sys, json
page_id = '${META_PAGE_ID}'
data = json.load(sys.stdin).get('data', [])
for page in data:
    if page.get('id') == page_id:
        print(page.get('access_token', ''))
        break
")

if [[ -z "$PAGE_TOKEN" ]]; then
  echo "HATA: ${META_PAGE_ID} ID'li sayfa için token bulunamadı (adım 2/4)." >&2
  echo "Token'ın pages_show_list iznine sahip olduğundan emin ol." >&2
  echo "$ACCOUNTS_RESPONSE" >&2
  exit 1
fi
echo "   Page access token alındı."

echo "3/4 Instagram Business hesabı doğrulanıyor..."
IG_RESPONSE=$(curl -s -G "${API}/${META_PAGE_ID}" \
  --data-urlencode "fields=instagram_business_account" \
  --data-urlencode "access_token=${PAGE_TOKEN}")

IG_ID=$(echo "$IG_RESPONSE" | python3 -c "
import sys, json
account = json.load(sys.stdin).get('instagram_business_account') or {}
print(account.get('id', ''))
")

if [[ -z "$IG_ID" ]]; then
  echo "UYARI: Sayfaya bağlı IG Business hesabı okunamadı, mevcut" >&2
  echo "META_IG_BUSINESS_ACCOUNT_ID değeri korunuyor." >&2
  IG_ID="${META_IG_BUSINESS_ACCOUNT_ID:-}"
else
  echo "   IG Business Account ID: $IG_ID"
fi

echo "4/4 .env güncelleniyor..."
BACKUP_FILE="${ENV_FILE}.bak"
cp "$ENV_FILE" "$BACKUP_FILE"

python3 - "$ENV_FILE" "$LONG_TOKEN" "$PAGE_TOKEN" "$IG_ID" <<'PYTHON'
import sys

env_path, user_token, page_token, ig_id = sys.argv[1:5]
updates = {
    'META_ACCESS_TOKEN': user_token,
    'META_PAGE_ACCESS_TOKEN': page_token,
}
if ig_id:
    updates['META_IG_BUSINESS_ACCOUNT_ID'] = ig_id

with open(env_path, encoding='utf-8') as handle:
    lines = handle.readlines()

seen = set()
output = []
for line in lines:
    key = line.split('=', 1)[0].strip()
    if key in updates:
        output.append(f'{key}={updates[key]}\n')
        seen.add(key)
    else:
        output.append(line)

for key, value in updates.items():
    if key not in seen:
        output.append(f'{key}={value}\n')

with open(env_path, 'w', encoding='utf-8') as handle:
    handle.writelines(output)
PYTHON

EXPIRY=$(curl -s -G "${API}/debug_token" \
  --data-urlencode "input_token=${LONG_TOKEN}" \
  --data-urlencode "access_token=${META_APP_ID}|${META_APP_SECRET}" \
  | python3 -c "
import sys, json, datetime
data = json.load(sys.stdin).get('data', {})
expires = data.get('expires_at', 0)
if not data.get('is_valid'):
    print('GEÇERSİZ')
elif expires:
    print(datetime.datetime.fromtimestamp(expires).strftime('%Y-%m-%d %H:%M'))
else:
    print('süresiz')
")

echo "Tamamlandı. .env güncellendi (yedek: ${BACKUP_FILE})"
echo "User token geçerlilik: ${EXPIRY}"
