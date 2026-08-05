# NextDNS Add-on Documentation

## Setup

1. Sign up at [my.nextdns.io](https://my.nextdns.io) and create a configuration.
2. Copy your **Profile ID** from the Setup tab (e.g. `3ee52c`).
3. In the add-on **Configuration** tab, enter your Profile ID and optionally a device name.
4. Start the add-on.
5. Point your router's DNS to your Home Assistant IP address.

## Configuration Options

| Option | Description |
|---|---|
| `api_key` | (Optional) NextDNS API Key from my.nextdns.io → Account tab. Auto-populates your NextDNS profiles into dropdowns in the Ingress Web UI. |
| `profile_id` | Fallback / default NextDNS profile ID from my.nextdns.io (e.g. `3ee52c`). Optional if `profile_assignments` is configured. |
| `device_name` | Fallback device name shown in your NextDNS dashboard (default: `home-assistant`). |
| `profile_assignments` | List of rules mapping specific IP addresses, subnets, or MAC addresses to specific NextDNS profiles. |
| `log_queries` | Log every DNS query in the add-on log. Off by default — useful for troubleshooting blocked sites. |
| `cache` | Cache DNS responses locally (10 MB). Speeds up repeated lookups, reduces round-trips to NextDNS. |


## NextDNS Manager (Ingress Web UI)

This add-on includes a built-in **Ingress Web UI** ("NextDNS Manager") accessible directly from Home Assistant's sidebar or the add-on page:

1. Click **OPEN WEB UI** or select **NextDNS Manager** in the Home Assistant sidebar.
2. The Web UI automatically discovers all network devices registered in Home Assistant (such as **TP-Link Omada** client trackers).
3. Select any discovered device from the dropdown menu, assign a NextDNS profile, and click **Save & Apply**.
4. No manual IP address typing or tracking required!

In the **Configuration** tab, you can also add entries manually under **Profile Assignments per Device**:


```yaml
profile_assignments:
  - match: "192.168.1.50"
    profile_id: "kids_prof_id"
    name: "Kids-Tablet"
  - match: "192.168.1.51"
    profile_id: "kids_prof_id"
    name: "Kids-iPad"
  - match: "192.168.1.60"
    profile_id: "husband_prof_id"
    name: "Husband-Laptop"
  - match: "10.0.4.0/24"
    profile_id: "guest_prof_id"
    name: "Guest-Subnet"
```

- **Target (`match`)**: Single IP (`192.168.1.50`), CIDR subnet (`192.168.1.0/24`), or MAC address (`00:1c:42:2e:60:4a`).
- **Profile ID (`profile_id`)**: The NextDNS profile ID from my.nextdns.io.
- **Label (`name`)**: (Optional) Name that will appear in your NextDNS logs/analytics.

Queries not matching any assigned rule will fall back to your main `profile_id`.

## Router Configuration (e.g., TP-Link Omada / UniFi / OpenWrt)

Set your router's primary DNS server (DHCP DNS) to your Home Assistant IP address. The add-on listens on port 53.
With router DHCP handing out Home Assistant's IP as DNS, NextDNS automatically sees client source IPs/MACs and applies the designated NextDNS profile to each device.

## NextDNS Updates

The NextDNS client is downloaded automatically on startup and updated whenever a new version is released — no add-on update required.

