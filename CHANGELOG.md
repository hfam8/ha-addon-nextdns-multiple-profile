# Changelog

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
