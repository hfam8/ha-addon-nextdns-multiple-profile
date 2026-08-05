# NextDNS Home Assistant Add-on

Run the [NextDNS](https://nextdns.io) DNS client as a Home Assistant add-on for network-wide DNS filtering, security, and privacy.

[![Add to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fhfam8%2Fha-addon-nextdns-multiple-profile)

## Installation

1. Click the button above, or manually add this repository in Home Assistant:
   **Settings → Add-ons → Add-on Store → ⋮ → Repositories**
   ```
   https://github.com/hfam8/ha-addon-nextdns-multiple-profile
   ```

2. Find **NextDNS** in the add-on store and click **Install**.
3. Go to the **Configuration** tab and enter your **NextDNS Profile ID** from [my.nextdns.io](https://my.nextdns.io) → Setup tab.
4. Click **Start**.

## Configuration

| Option | Description |
|---|---|
| `profile_id` | Fallback / default NextDNS profile ID (e.g. `3ee52c`) — found on the Setup tab at my.nextdns.io |
| `device_name` | Default device name as it appears in your NextDNS dashboard (default: `home-assistant`) |
| `profile_assignments` | List of rules mapping specific IP addresses, subnets, or MAC addresses to specific NextDNS profiles |

### Multiple Profiles & Per-Device Assignments

Assign different profiles to specific family members or devices (e.g., kids' tablets, spouse's laptop, guest network):

```yaml
profile_assignments:
  - match: "192.168.1.50"
    profile_id: "kids_prof_id"
    name: "Kids-Tablet"
  - match: "192.168.1.60"
    profile_id: "husband_prof_id"
    name: "Husband-Laptop"
```

## Network-wide DNS

Point your router's primary DNS server (DHCP DNS) to your Home Assistant IP address. The add-on listens on port 53.

## Supported Architectures

`aarch64` · `amd64` · `armhf` · `armv7` · `i386`

## Credits & Acknowledgements

This add-on is an enhanced multi-profile version based on the original [ha-addon-nextdns](https://github.com/billytkid/ha-addon-nextdns) created by [@billytkid](https://github.com/billytkid).


