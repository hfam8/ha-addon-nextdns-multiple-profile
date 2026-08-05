#!/usr/bin/env python3
import json
import os
import re
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8080
OPTIONS_FILE = "/data/options.json"

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NextDNS Profile Manager</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: rgba(30, 41, 59, 0.7);
            --border-color: rgba(255, 255, 255, 0.1);
            --accent-primary: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-gradient: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --success: #10b981;
            --danger: #ef4444;
            --radius-lg: 16px;
            --radius-md: 10px;
            --radius-sm: 6px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 2rem 1.5rem;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(59, 130, 246, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.15) 0%, transparent 40%);
            background-attachment: fixed;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--border-color);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .brand-icon {
            width: 42px;
            height: 42px;
            background: var(--accent-gradient);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.2rem;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }

        .brand-title h1 {
            font-size: 1.4rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .brand-title p {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: var(--success);
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--success);
        }

        .card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
        }

        .card-title {
            font-size: 1.1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .card-description {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        label {
            font-size: 0.825rem;
            font-weight: 500;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        input[type="text"], input[type="password"], select {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 0.65rem 0.9rem;
            color: var(--text-primary);
            font-size: 0.925rem;
            outline: none;
            transition: all 0.2s ease;
        }

        input[type="text"]:focus, input[type="password"]:focus, select:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        }

        select option {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.65rem 1.25rem;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            border: none;
            transition: all 0.2s ease;
        }

        .btn-primary {
            background: var(--accent-gradient);
            color: white;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
        }

        .btn-primary:hover {
            opacity: 0.95;
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.15);
        }

        .btn-danger {
            background: rgba(239, 68, 68, 0.15);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.3);
            padding: 0.4rem 0.75rem;
            font-size: 0.8rem;
        }

        .btn-danger:hover {
            background: var(--danger);
            color: white;
        }

        .rule-item {
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1rem;
            margin-bottom: 0.75rem;
            display: grid;
            grid-template-columns: 2fr 2fr 1.5fr 40px;
            gap: 1rem;
            align-items: center;
            transition: border-color 0.2s ease;
        }

        .rule-item:hover {
            border-color: rgba(59, 130, 246, 0.4);
        }

        .rule-info {
            display: flex;
            flex-direction: column;
        }

        .rule-title {
            font-weight: 600;
            font-size: 0.95rem;
        }

        .rule-sub {
            font-size: 0.8rem;
            color: var(--text-secondary);
            font-family: monospace;
        }

        .badge-chip {
            display: inline-block;
            background: rgba(139, 92, 246, 0.15);
            color: #c084fc;
            border: 1px solid rgba(139, 92, 246, 0.3);
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            font-family: monospace;
        }

        .empty-state {
            text-align: center;
            padding: 2.5rem 1rem;
            color: var(--text-muted);
        }

        .toast {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #10b981;
            color: white;
            padding: 0.9rem 1.5rem;
            border-radius: var(--radius-md);
            font-weight: 600;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            display: none;
            z-index: 1000;
            animation: slideUp 0.3s ease;
        }

        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="brand">
                <div class="brand-icon">NX</div>
                <div class="brand-title">
                    <h1>NextDNS Manager</h1>
                    <p>Per-Device NextDNS Profile Routing for Home Assistant</p>
                </div>
            </div>
            <div class="status-badge">
                <span class="status-dot"></span>
                <span>Active</span>
            </div>
        </header>

        <!-- API Key Card -->
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">NextDNS Account Integration (Optional)</div>
                    <div class="card-description">Enter your NextDNS API Key (from my.nextdns.io → Account tab) to auto-populate your profiles.</div>
                </div>
            </div>
            <div class="form-grid" style="grid-template-columns: 3fr auto; align-items: end;">
                <div class="form-group">
                    <label for="api_key_input">NextDNS API Key</label>
                    <input type="password" id="api_key_input" placeholder="e.g. 4a8b... (Optional)">
                </div>
                <button class="btn btn-secondary" onclick="fetchNextDNSProfiles()">Fetch NextDNS Profiles</button>
            </div>
        </div>

        <!-- Default Profile Card -->
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">Default Fallback Profile</div>
                    <div class="card-description">Applied to any device on your network that is not specifically assigned below.</div>
                </div>
            </div>
            <div class="form-grid">
                <div class="form-group" id="default_profile_select_group" style="display:none;">
                    <label for="default_profile_select">Select NextDNS Profile</label>
                    <select id="default_profile_select" onchange="onDefaultProfileSelect()">
                        <option value="">-- Choose Profile --</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="default_profile_id">NextDNS Profile ID</label>
                    <input type="text" id="default_profile_id" placeholder="e.g. 3ee52c">
                </div>
                <div class="form-group">
                    <label for="default_device_name">Default Device Label</label>
                    <input type="text" id="default_device_name" placeholder="home-assistant">
                </div>
            </div>
        </div>

        <!-- Add Device Assignment Card -->
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">Add Device Profile Assignment</div>
                    <div class="card-description">Select a discovered network device (Omada / HA) or manually enter an IP / MAC.</div>
                </div>
            </div>

            <div class="form-grid">
                <div class="form-group">
                    <label for="device_select">Discovered Device (Omada / HA)</label>
                    <select id="device_select" onchange="onDeviceSelect()">
                        <option value="">-- Choose Discovered Device --</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="target_match">Target (IP / Subnet / MAC)</label>
                    <input type="text" id="target_match" placeholder="192.168.1.50">
                </div>
                <div class="form-group" id="profile_select_group" style="display:none;">
                    <label for="profile_select">NextDNS Profile Dropdown</label>
                    <select id="profile_select" onchange="onProfileSelect()">
                        <option value="">-- Choose NextDNS Profile --</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="target_profile">NextDNS Profile ID</label>
                    <input type="text" id="target_profile" placeholder="e.g. kids123">
                </div>
                <div class="form-group">
                    <label for="target_name">Device Label</label>
                    <input type="text" id="target_name" placeholder="e.g. Kids Tablet">
                </div>
            </div>
            <div style="margin-top: 1.25rem; display: flex; justify-content: flex-end;">
                <button class="btn btn-secondary" onclick="addRule()">+ Add Assignment Rule</button>
            </div>
        </div>

        <!-- Rules List Card -->
        <div class="card">
            <div class="card-header">
                <div>
                    <div class="card-title">Active Device Assignments</div>
                    <div class="card-description">Specific profile rules evaluated in top-to-bottom order.</div>
                </div>
            </div>
            <div id="rules_container">
                <div class="empty-state">No per-device rules added yet.</div>
            </div>
        </div>

        <div style="display: flex; justify-content: flex-end; margin-top: 2rem;">
            <button class="btn btn-primary" onclick="saveConfig()">Save & Apply Settings</button>
        </div>
    </div>

    <div id="toast" class="toast">Settings saved & NextDNS reloaded!</div>

    <script>
        let currentRules = [];
        let discoveredDevices = [];
        let nextdnsProfiles = [];

        async function loadAll() {
            try {
                const [devicesRes, configRes] = await Promise.all([
                    fetch('./api/devices'),
                    fetch('./api/config')
                ]);
                
                discoveredDevices = await devicesRes.json();
                const config = await configRes.json();

                populateDeviceDropdown();
                populateConfig(config);

                if (config.api_key) {
                    await fetchNextDNSProfiles();
                }
            } catch (err) {
                console.error("Failed to load setup:", err);
            }
        }

        async function fetchNextDNSProfiles() {
            const apiKey = document.getElementById('api_key_input').value.trim();
            try {
                const res = await fetch('./api/nextdns_profiles?api_key=' + encodeURIComponent(apiKey));
                if (res.ok) {
                    nextdnsProfiles = await res.json();
                    populateNextDNSProfileDropdowns();
                }
            } catch (err) {
                console.warn("Could not fetch NextDNS profiles:", err);
            }
        }

        function populateNextDNSProfileDropdowns() {
            if (!nextdnsProfiles || nextdnsProfiles.length === 0) return;

            const defSelect = document.getElementById('default_profile_select');
            const ruleSelect = document.getElementById('profile_select');

            defSelect.innerHTML = '<option value="">-- Choose Profile --</option>';
            ruleSelect.innerHTML = '<option value="">-- Choose NextDNS Profile --</option>';

            nextdnsProfiles.forEach(p => {
                const opt1 = document.createElement('option');
                opt1.value = p.id;
                opt1.textContent = `${p.name} (${p.id})`;
                defSelect.appendChild(opt1);

                const opt2 = document.createElement('option');
                opt2.value = p.id;
                opt2.textContent = `${p.name} (${p.id})`;
                ruleSelect.appendChild(opt2);
            });

            document.getElementById('default_profile_select_group').style.display = 'flex';
            document.getElementById('profile_select_group').style.display = 'flex';
        }

        function onDefaultProfileSelect() {
            const val = document.getElementById('default_profile_select').value;
            if (val) {
                document.getElementById('default_profile_id').value = val;
            }
        }

        function onProfileSelect() {
            const val = document.getElementById('profile_select').value;
            if (val) {
                document.getElementById('target_profile').value = val;
            }
        }

        function populateDeviceDropdown() {
            const select = document.getElementById('device_select');
            select.innerHTML = '<option value="">-- Choose Discovered Device (Omada / HA) --</option>';
            
            discoveredDevices.forEach((dev, idx) => {
                const opt = document.createElement('option');
                opt.value = idx;
                opt.textContent = `${dev.name} (${dev.ip || dev.mac || 'No IP'})`;
                select.appendChild(opt);
            });
        }

        function onDeviceSelect() {
            const select = document.getElementById('device_select');
            const idx = select.value;
            if (idx === "") return;

            const dev = discoveredDevices[idx];
            document.getElementById('target_match').value = dev.ip || dev.mac || '';
            document.getElementById('target_name').value = dev.name;
        }

        function populateConfig(config) {
            document.getElementById('api_key_input').value = config.api_key || '';
            document.getElementById('default_profile_id').value = config.profile_id || '';
            document.getElementById('default_device_name').value = config.device_name || 'home-assistant';

            currentRules = config.profile_assignments || [];
            renderRules();
        }

        function renderRules() {
            const container = document.getElementById('rules_container');
            if (currentRules.length === 0) {
                container.innerHTML = '<div class="empty-state">No per-device rules added yet. Select a device above to create a rule.</div>';
                return;
            }

            container.innerHTML = '';
            currentRules.forEach((rule, idx) => {
                const div = document.createElement('div');
                div.className = 'rule-item';
                div.innerHTML = `
                    <div class="rule-info">
                        <span class="rule-title">${escapeHtml(rule.name || 'Unnamed Device')}</span>
                        <span class="rule-sub">Target: ${escapeHtml(rule.match)}</span>
                    </div>
                    <div>
                        <span class="badge-chip">Profile: ${escapeHtml(rule.profile_id)}</span>
                    </div>
                    <div></div>
                    <button class="btn btn-danger" onclick="deleteRule(${idx})">✕</button>
                `;
                container.appendChild(div);
            });
        }

        function addRule() {
            const match = document.getElementById('target_match').value.trim();
            const profile_id = document.getElementById('target_profile').value.trim();
            const name = document.getElementById('target_name').value.trim();

            if (!match || !profile_id) {
                alert("Please enter both a Target (IP/MAC) and a NextDNS Profile ID.");
                return;
            }

            currentRules.push({ match, profile_id, name });
            renderRules();

            document.getElementById('target_match').value = '';
            document.getElementById('target_profile').value = '';
            document.getElementById('target_name').value = '';
            document.getElementById('device_select').value = '';
            document.getElementById('profile_select').value = '';
        }

        function deleteRule(idx) {
            currentRules.splice(idx, 1);
            renderRules();
        }

        async function saveConfig() {
            const payload = {
                api_key: document.getElementById('api_key_input').value.trim(),
                profile_id: document.getElementById('default_profile_id').value.trim(),
                device_name: document.getElementById('default_device_name').value.trim() || 'home-assistant',
                profile_assignments: currentRules
            };

            try {
                const res = await fetch('./api/config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                if (res.ok) {
                    showToast();
                } else {
                    alert("Error saving configuration.");
                }
            } catch (err) {
                alert("Failed to connect to server: " + err);
            }
        }

        function showToast() {
            const toast = document.getElementById('toast');
            toast.style.display = 'block';
            setTimeout(() => { toast.style.display = 'none'; }, 3000);
        }

        function escapeHtml(str) {
            return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
        }

        window.onload = loadAll;
    </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        clean_path = self.path.split('?')[0]
        query_str = self.path.split('?')[1] if '?' in self.path else ''
        
        if clean_path in ["/", "/index.html", ""]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode('utf-8'))
        elif clean_path.endswith("/api/devices") or clean_path == "/api/devices":
            devices = self.get_ha_devices()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(devices).encode('utf-8'))
        elif clean_path.endswith("/api/nextdns_profiles") or clean_path == "/api/nextdns_profiles":
            api_key = ""
            for param in query_str.split('&'):
                if param.startswith('api_key='):
                    api_key = urllib.parse.unquote(param.split('api_key=')[1])
            if not api_key:
                config = self.get_config()
                api_key = config.get("api_key", "")

            profiles = self.get_nextdns_profiles(api_key)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(profiles).encode('utf-8'))
        elif clean_path.endswith("/api/config") or clean_path == "/api/config":
            config = self.get_config()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(config).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        clean_path = self.path.split('?')[0]
        if clean_path.endswith("/api/config") or clean_path == "/api/config":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
                self.save_config(data)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def get_nextdns_profiles(self, api_key):
        if not api_key:
            return []
        
        url = "https://api.nextdns.io/profiles"
        req = urllib.request.Request(url, headers={"X-Api-Key": api_key, "User-Agent": "HomeAssistant-NextDNS/0.9.3"})
        profiles = []

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    for p in data.get("data", []):
                        profiles.append({
                            "id": p.get("id", ""),
                            "name": p.get("name", "")
                        })
        except Exception as err:
            print(f"Error querying NextDNS API: {err}")

        return profiles

    def get_ha_devices(self):
        token = os.environ.get("SUPERVISOR_TOKEN") or os.environ.get("HASSIO_TOKEN")
        if not token:
            return []

        url = "http://supervisor/core/api/states"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        devices = []

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    states = json.loads(response.read().decode('utf-8'))
                    for entity in states:
                        entity_id = entity.get("entity_id", "")
                        if entity_id.startswith("device_tracker."):
                            attrs = entity.get("attributes", {})
                            ip = attrs.get("ip") or attrs.get("ip_address") or ""
                            mac = attrs.get("mac") or attrs.get("mac_address") or ""
                            name = attrs.get("friendly_name") or entity_id.replace("device_tracker.", "").replace("_", " ").title()

                            devices.append({
                                "entity_id": entity_id,
                                "name": name,
                                "ip": ip,
                                "mac": mac
                            })
        except Exception as err:
            print(f"Error querying HA states: {err}")

        return devices

    def get_config(self):
        if os.path.exists(OPTIONS_FILE):
            try:
                with open(OPTIONS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading options.json: {e}")
        return {"api_key": "", "profile_id": "", "device_name": "home-assistant", "profile_assignments": []}

    def save_config(self, new_data):
        current = self.get_config()
        current.update(new_data)
        with open(OPTIONS_FILE, 'w') as f:
            json.dump(current, f, indent=2)

def run_server():
    server = HTTPServer(('0.0.0.0', PORT), RequestHandler)
    print(f"Starting NextDNS Ingress Web UI on port {PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
