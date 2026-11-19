#!/usr/bin/env bash
# PolyglotDesk — Detaylı Çevir için yalnız okuma rolü (isteğe bağlı yardımcı; aynı işin düz SQL hâli
# doc/detailed-setup.md'de).
#
# Kullanım (kendi kullanıcınızla; yönetici bağlantısı standart PG* ortam değişkenleriyle verilir):
#     PGHOST=127.0.0.1 PGUSER=postgres veritabani/okur_rol.sh
# Yönetici rolü süper kullanıcı olmalı (ya da CREATEROLE yetkili ve veritabanının sahibi).
#
# Ayarlar (ortam değişkenleri; uygulamanın kullandıklarıyla aynı):
#     POLYGLOTDESK_PG_DB     veritabanı           (varsayılan cevirmen; önceden oluşturulmuş olmalı)
#     POLYGLOTDESK_PG_USER   yalnız okuma rolü     (varsayılan cevirmen_okur)
#     POLYGLOTDESK_PG_HOST / POLYGLOTDESK_PG_PORT  ~/.pgpass satırı için (varsayılan 127.0.0.1 / 5432)
#
# - Rol: LOGIN; süper kullanıcı değil, veritabanı/rol açamaz; varsayılan işlemi salt okunur; yalnız bu veritabanına
#   CONNECT. Tablo okuma (SELECT) yetkisini yükleme betiği verir (veritabani/yukle.py, her yüklemede yeniden).
# - Şifre rastgele üretilir, istemci tarafında SCRAM-SHA-256'ya çevrilir; düz hâli yalnız betiği çalıştıran
#   kullanıcının ~/.pgpass dosyasına (izin 600) yazılır. Ekrana ve günlüğe düşmez.
# - Tekrar çalıştırılabilir: rol varsa şifreye dokunmaz.
set -Eeuo pipefail
umask 077
export LC_ALL=C.UTF-8
unset PGSERVICE || true

ROL="${POLYGLOTDESK_PG_USER:-cevirmen_okur}"
VT="${POLYGLOTDESK_PG_DB:-cevirmen}"
SUNUCU="${POLYGLOTDESK_PG_HOST:-127.0.0.1}"
PORT="${POLYGLOTDESK_PG_PORT:-5432}"
PGPASS_DOSYA="${PGPASSFILE:-$HOME/.pgpass}"
export PGDATABASE="${PGDATABASE:-postgres}"

hata() { printf 'HATA: %s\n' "$*" >&2; exit 1; }
sql() { psql -X -q -v ON_ERROR_STOP=1 "$@"; }
deger() { psql -X -A -t -q -v ON_ERROR_STOP=1 "$@"; }

[[ "$(deger -v v="$VT" <<<"SELECT count(*) FROM pg_database WHERE datname = :'v'")" == 1 ]] \
    || hata "$VT veritabanı yok; önce doc/detailed-setup.md'deki adımlarla oluşturun"

if [[ "$(deger -v r="$ROL" <<<"SELECT count(*) FROM pg_roles WHERE rolname = :'r'")" == 0 ]]; then
    yeni=$(mktemp "$HOME/.pgpass.yeni.XXXXXX")
    trap 'rm -f -- "$yeni"' EXIT
    dogrulayici=$(python3 - "$ROL" "$PGPASS_DOSYA" "$yeni" "$SUNUCU" "$PORT" <<'PY'
import base64, hashlib, hmac, os, secrets, sys
rol, eski, yeni, sunucu, port = sys.argv[1:6]
sifre = secrets.token_urlsafe(32)
tuz = secrets.token_bytes(16); tur = 4096
tuzlu = hashlib.pbkdf2_hmac("sha256", sifre.encode(), tuz, tur)
istemci = hmac.new(tuzlu, b"Client Key", hashlib.sha256).digest()
saklanan = hashlib.sha256(istemci).digest()
sunucu_anahtari = hmac.new(tuzlu, b"Server Key", hashlib.sha256).digest()
b = lambda x: base64.b64encode(x).decode()
onek = f"{sunucu}:{port}:*:{rol}:"
satirlar = []
if os.path.exists(eski):
    with open(eski) as f:
        satirlar = [s for s in f.read().splitlines() if not s.startswith(onek)]
satirlar.append(onek + sifre)
with open(yeni, "w") as f:
    f.write("\n".join(satirlar) + "\n")
os.chmod(yeni, 0o600)
print(f"SCRAM-SHA-256${tur}:{b(tuz)}${b(saklanan)}:{b(sunucu_anahtari)}")
PY
)
    # Doğrulayıcı komut satırından değil stdin'den gider (ps çıktısında görünmez).
    { printf '%s\n' "\\set d '$dogrulayici'"; cat <<'SQL'; } | sql -v r="$ROL"
SELECT format('CREATE ROLE %I LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD %L',
              :'r', :'d') \gexec
SQL
    mv -f -- "$yeni" "$PGPASS_DOSYA"; chmod 600 "$PGPASS_DOSYA"
    printf 'Rol oluşturuldu: %s (şifre %s içinde, %s:%s:*:%s)\n' "$ROL" "$PGPASS_DOSYA" "$SUNUCU" "$PORT" "$ROL"
else
    printf 'Rol zaten var: %s (şifre değiştirilmedi)\n' "$ROL"
fi

sql -v r="$ROL" -v v="$VT" <<'SQL'
SELECT format('ALTER ROLE %I SET default_transaction_read_only = on', :'r') \gexec
SELECT format('GRANT CONNECT ON DATABASE %I TO %I', :'v', :'r') \gexec
SQL
printf 'Tamam: %s, %s veritabanına bağlanabilir (salt okunur); tablo okuma yetkisini yukle.py verir.\n' "$ROL" "$VT"
