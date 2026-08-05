# Changelog

## [1.0.6] - 2026-08-04

### Security & UI
- Applied CSS text-security masking (`••••••••`) to the NextDNS API Key field so characters remain visually hidden on screen while preventing browser HTTP password warning popups.

## [1.0.5] - 2026-08-04


### Fixed
- Updated NextDNS API Key input field to suppress browser HTTP insecure login warnings on local network IPs.

## [1.0.4] - 2026-08-04


### Fixed
- Trigger instant NextDNS process reload upon clicking Save & Apply Settings in the Web UI so new profile routing rules take effect immediately.

## [1.0.3] - 2026-08-04


### Fixed
- Fixed GitHub API 403 error during NextDNS binary check by adding custom User-Agent header to curl.
- Fixed socket `Address in use` (OSError 98) in web_server.py by enabling `SO_REUSEADDR` and checking for running instances in run.sh.

## [1.0.2] - 2026-08-04


### Fixed & Improved
- Added `homeassistant_api: true` and `hassio_role: manager` permissions to allow the Web UI to fetch Home Assistant core entity states for device auto-discovery.

## [1.0.1] - 2026-08-04


### Fixed & Improved
- Cleaned up NextDNS Profile selection in Ingress Web UI (removed redundant duplicate profile fields).
- Expanded Home Assistant device scanner to perform deep attribute inspection for Omada Controller entities and network clients.

## [1.0.0] - 2026-08-04



### Added
- Multi-profile support for assigning specific NextDNS profiles to devices by IP address, CIDR subnet, or MAC address.
- Built-in NextDNS Manager Ingress Web UI featuring automatic device discovery for TP-Link Omada and network clients.
- Updated field labels clarifying Default/Fallback profile behavior.

## [0.9.0] - 2026-05-15


> Pre-release. Core functionality is working — DNS traffic is forwarded through NextDNS with device identification.

### Added
- Initial working release of the NextDNS Home Assistant add-on
- Forwards all DNS traffic on port 53 to NextDNS using DNS-over-HTTPS
- Two configuration options:
  - **Profile ID** — your NextDNS profile ID from my.nextdns.io
  - **Device name** — how this device appears in your NextDNS dashboard
- NextDNS client binary is downloaded automatically on first start and updated whenever a new version is released — no add-on update needed to stay current
- Supports all Home Assistant architectures: `aarch64`, `amd64`, `armhf`, `armv7`, `i386`
- Docker images built and published automatically to GHCR via GitHub Actions on every release
- One-click "Add to Home Assistant" button on the GitHub repository page
- Log is cleared on each restart

### Known limitations
- Device name appears in the NextDNS dashboard for the add-on itself only. Individual devices on your network will be identified separately by NextDNS based on their own IP/hostname
