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
LATEST=$(curl -fsSL -H "User-Agent: HomeAssistant-NextDNS/1.0.3" --max-time 10 \
    "https://api.github.com/repos/nextdns/nextdns/releases/latest" \
    | jq -r '.tag_name // empty' | tr -d 'v') || true

CACHED=""
[ -f "${VERSION_FILE}" ] && CACHED=$(cat "${VERSION_FILE}")

if [ ! -x "${NEXTDNS_BIN}" ] || { [ -n "${LATEST}" ] && [ "${LATEST}" != "${CACHED}" ]; }; then
    if [ -n "${LATEST}" ]; then
        bashio::log.info "Downloading NextDNS v${LATEST}..."
        curl -fsSL -H "User-Agent: HomeAssistant-NextDNS/1.0.3" --max-time 60 \
            "https://github.com/nextdns/nextdns/releases/download/v${LATEST}/nextdns_${LATEST}_linux_${NEXTDNS_ARCH}.tar.gz" \
            | tar -xz -C /data nextdns \
            && chmod +x "${NEXTDNS_BIN}" \
            && echo "${LATEST}" > "${VERSION_FILE}"
        bashio::log.info "NextDNS v${LATEST} ready."
    else
        bashio::log.fatal "No cached binary and cannot reach GitHub. Cannot start."
        exit 1
    fi
else
    bashio::log.info "NextDNS v${CACHED} is up to date."
fi

# ── Validate config & Build arguments ───────────────────────────────────────
PROFILE_ID=$(bashio::config 'profile_id')
DEVICE_NAME=$(bashio::config 'device_name')

HAS_PROFILES=false
ARGS=(
    "--listen" "0.0.0.0:53"
    "--report-client-info"
    "--bogus-priv"
    "--use-hosts"
)

# ── Add per-device profile rules ─────────────────────────────────────────────
if bashio::config.has_value 'profile_assignments'; then
    _jq() {
        echo "${1}" | base64 --decode | jq -r "${2}"
    }
    for row in $(bashio::config 'profile_assignments' | jq -r '.[]? | @base64'); do
        MATCH=$(_jq "${row}" '.match // empty')
        PROF_ID=$(_jq "${row}" '.profile_id // empty')
        NAME=$(_jq "${row}" '.name // empty')

        if [ -n "${MATCH}" ] && [ -n "${PROF_ID}" ]; then
            if [ -n "${NAME}" ]; then
                TARGET_SPEC="${MATCH}=${PROF_ID}/${NAME}"
            else
                TARGET_SPEC="${MATCH}=${PROF_ID}"
            fi
            ARGS+=("--profile" "${TARGET_SPEC}")
            bashio::log.info "Assigned Profile Rule: ${TARGET_SPEC}"
            HAS_PROFILES=true
        fi
    done
fi


# ── Add default / fallback profile ──────────────────────────────────────────
if bashio::var.is_not_empty "${PROFILE_ID}"; then
    if bashio::var.is_not_empty "${DEVICE_NAME}"; then
        DEFAULT_SPEC="${PROFILE_ID}/${DEVICE_NAME}"
    else
        DEFAULT_SPEC="${PROFILE_ID}"
    fi
    ARGS+=("--profile" "${DEFAULT_SPEC}")
    bashio::log.info "Default Profile: ${DEFAULT_SPEC}"
    HAS_PROFILES=true
fi

if [ "${HAS_PROFILES}" = false ]; then
    bashio::log.fatal "No NextDNS profiles configured. Please set a profile_id or add rules to profile_assignments in Configuration."
    exit 1
fi

bashio::config.true 'log_queries' && ARGS+=("--log-queries")
bashio::config.true 'cache'       && ARGS+=("--cache-size" "10MB")

exec "${NEXTDNS_BIN}" run "${ARGS[@]}"

