#!/command/with-contenv bashio
# shellcheck shell=bash

NEXTDNS_BIN="/data/nextdns"
VERSION_FILE="/data/nextdns.version"

printf '\033c'
bashio::log.info "Starting NextDNS add-on..."

# ── Start Ingress Web UI Server ────────────────────────────────────────────────
if ! pgrep -f "web_server.py" >/dev/null 2>&1; then
    bashio::log.info "Starting NextDNS Manager Ingress Web UI..."
    python3 /etc/services.d/nextdns/web_server.py &
fi

# ── Map HA arch to NextDNS release arch ───────────────────────────────────────
case "${BUILD_ARCH}" in
    aarch64) NEXTDNS_ARCH="arm64" ;;
    amd64)   NEXTDNS_ARCH="amd64" ;;
    armhf)   NEXTDNS_ARCH="armv6" ;;
    armv7)   NEXTDNS_ARCH="armv7" ;;
    i386)    NEXTDNS_ARCH="386" ;;
    *)
        bashio::log.fatal "Unsupported architecture: ${BUILD_ARCH}"
        exit 1
        ;;
esac

# ── Download latest NextDNS if needed ─────────────────────────────────────────
CACHED=""
[ -f "${VERSION_FILE}" ] && CACHED=$(cat "${VERSION_FILE}")

LATEST=$(curl -fsSL -H "User-Agent: Mozilla/5.0" -w "%{url_effective}" -o /dev/null --max-time 10 "https://github.com/nextdns/nextdns/releases/latest" | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | tr -d 'v' || true)

if [ -z "${LATEST}" ]; then
    LATEST=$(curl -fsSL -H "User-Agent: HomeAssistant-NextDNS/1.0.6" --max-time 10 \
        "https://api.github.com/repos/nextdns/nextdns/releases/latest" \
        | jq -r '.tag_name // empty' | tr -d 'v' || true)
fi

if [ -z "${LATEST}" ]; then
    if [ -n "${CACHED}" ]; then
        LATEST="${CACHED}"
    else
        LATEST="1.43.0"
    fi
fi

if [ ! -x "${NEXTDNS_BIN}" ] || [ "${LATEST}" != "${CACHED}" ]; then
    bashio::log.info "Downloading NextDNS v${LATEST}..."
    if curl -fsSL -H "User-Agent: Mozilla/5.0" --max-time 60 \
        "https://github.com/nextdns/nextdns/releases/download/v${LATEST}/nextdns_${LATEST}_linux_${NEXTDNS_ARCH}.tar.gz" \
        | tar -xz -C /data nextdns \
        && chmod +x "${NEXTDNS_BIN}" \
        && echo "${LATEST}" > "${VERSION_FILE}"; then
        bashio::log.info "NextDNS v${LATEST} ready."
    elif [ -x "${NEXTDNS_BIN}" ]; then
        bashio::log.warning "Could not fetch new version from GitHub. Using existing NextDNS binary v${CACHED}."
    else
        bashio::log.fatal "Could not download NextDNS binary from GitHub."
        exit 1
    fi
else
    bashio::log.info "NextDNS v${CACHED} is up to date."
fi


# ── Validate config & Build arguments loop ──────────────────────────────────────
run_nextdns() {
    HAS_PROFILES=false
    ARGS=(
        "--listen" "0.0.0.0:53"
        "--report-client-info"
        "--bogus-priv"
        "--use-hosts"
    )

    if [ -f "/data/options.json" ]; then
        while IFS= read -r line; do
            if [ -n "${line}" ]; then
                ARGS+=("--profile" "${line}")
                bashio::log.info "Configured Profile Rule: ${line}"
                HAS_PROFILES=true
            fi
        done < <(python3 -c '
import json, sys
try:
    with open("/data/options.json", "r") as f:
        data = json.load(f)
    assignments = data.get("profile_assignments", [])
    if isinstance(assignments, list):
        for item in assignments:
            if isinstance(item, dict):
                match = str(item.get("match") or "").strip()
                prof_id = str(item.get("profile_id") or "").strip()
                name = str(item.get("name") or "").strip()
                if match and prof_id:
                    spec = f"{match}={prof_id}/{name}" if name else f"{match}={prof_id}"
                    print(spec)
    default_prof = str(data.get("profile_id") or "").strip()
    default_dev = str(data.get("device_name") or "").strip()
    if default_prof:
        spec = f"{default_prof}/{default_dev}" if default_dev else f"{default_prof}"
        print(spec)
except Exception as e:
    pass
')
    fi

    if [ "${HAS_PROFILES}" = false ]; then
        bashio::log.warning "No NextDNS profiles configured yet. Waiting for configuration from Web UI or HA Config..."
        sleep 5
        return 0
    fi

    if python3 -c 'import json; data=json.load(open("/data/options.json")); sys.exit(0 if data.get("log_queries") else 1)' 2>/dev/null; then
        ARGS+=("--log-queries")
    fi
    if python3 -c 'import json; data=json.load(open("/data/options.json")); sys.exit(0 if data.get("cache") else 1)' 2>/dev/null; then
        ARGS+=("--cache-size" "10MB")
    fi

    bashio::log.info "Starting NextDNS binary..."
    "${NEXTDNS_BIN}" run "${ARGS[@]}"
}

while true; do
    run_nextdns
    bashio::log.info "NextDNS process stopped or requested reload. Re-evaluating configuration..."
    sleep 2
done

