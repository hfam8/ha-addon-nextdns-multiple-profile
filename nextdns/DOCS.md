# NextDNS Add-on Documentation

## Setup

1. Install the add-on from the Add-on Store.
2. Click **Start** to launch the add-on (the Web UI runs inside the active container).
3. Click **OPEN WEB UI** (or select **NextDNS Manager** in the Home Assistant sidebar) to configure your default profile and assign NextDNS profiles to discovered devices.
4. Point your router's DNS (e.g. TP-Link Omada DHCP DNS) to your Home Assistant IP address.

> **Note**: Always **Start** the add-on first so the web server activates before clicking **OPEN WEB UI**.


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

## Smartphone & Mobile Device Setup Tips

Smartphones (iPhones & Androids) have default privacy features that can cause them to fall back to your Default Profile:

### 1. On Home Wi-Fi (Omada Router)
- **Turn off Private Wi-Fi Address**: In your phone's Wi-Fi network settings, disable **"Private Wi-Fi Address"** (iOS) or **"Randomized MAC"** (Android) for your home network.
- **Reserve Static IP in Omada**: In your TP-Link Omada Controller under **Clients**, select the phone and click **Reserve IP** (e.g. `192.168.50.103`).
- **Add Rule in NextDNS Manager**: Add a rule matching the phone's reserved IP address or MAC address.

### 2. Away from Home (Cellular 5G/LTE)
When smartphones leave your home network, they send DNS directly to cellular towers. You can configure NextDNS directly on the phone for 24/7 protection:

- **Android (Private DNS)**: Go to **Settings → Network & internet → Private DNS** → select **Private DNS provider hostname** and enter:
  `Holly--Phone-9867f6.dns.nextdns.io` *(replace `9867f6` with your profile ID)*
- **iPhone / iOS**: Open Safari on your iPhone, visit **[apple.nextdns.io](https://apple.nextdns.io)**, enter your Profile ID (`9867f6`), and install the iOS profile in **Settings → Profile Downloaded**.

## NextDNS Updates

The NextDNS client is downloaded automatically on startup and updated whenever a new version is released — no add-on update required.


