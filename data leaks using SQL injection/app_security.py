import os
import sqlite3
import base64
from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 1. Force absolute path discovery
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# 2. Automatically create the templates folder if it doesn't exist
if not os.path.exists(TEMPLATE_DIR):
    os.makedirs(TEMPLATE_DIR)

# 3. Premium HTML Content string to auto-inject if missing
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud-Native SQL Injection Leak Prevention System</title>
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #020617 0%, #0f172a 100%);
            --panel-bg: rgba(30, 41, 59, 0.7);
            --accent-blue: #38bdf8;
            --accent-red: #ef4444;
            --accent-green: #10b981;
            --text-light: #f8fafc;
            --border-color: rgba(255,255,255,0.1);
        }
        body { 
            font-family: 'Segoe UI', system-ui, sans-serif; 
            background: var(--bg-gradient); 
            margin: 0; padding: 20px; 
            color: var(--text-light);
            min-height: 100vh;
            display: flex; align-items: center; justify-content: center;
        }
        .container { width: 1050px; max-width: 95%; display: grid; grid-template-columns: 1fr 1.2fr; gap: 25px; }
        @media(max-width: 850px) { .container { grid-template-columns: 1fr; } }
        .panel {
            background: var(--panel-bg); padding: 30px; border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5); border: 1px solid var(--border-color);
            backdrop-filter: blur(12px); display: flex; flex-direction: column; gap: 20px;
        }
        .full-width { grid-column: 1 / -1; }
        h1, h2 { margin: 0; color: #fff; font-weight: 700; }
        h1 { font-size: 24px; border-bottom: 1px solid var(--border-color); padding-bottom: 15px; }
        h2 { font-size: 18px; color: var(--accent-blue); }
        .system-badge { background: rgba(56, 189, 248, 0.15); color: var(--accent-blue); padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; text-transform: uppercase; }
        .input-group { display: flex; flex-direction: column; gap: 8px; }
        label { font-size: 13px; font-weight: 600; color: #94a3b8; text-transform: uppercase; }
        input { 
            width: 100%; padding: 14px; background: rgba(15, 23, 42, 0.6); 
            border: 1px solid var(--border-color); border-radius: 10px; 
            box-sizing: border-box; color: #fff; font-size: 14px; outline: none;
        }
        .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .btn { padding: 14px; border-radius: 10px; font-weight: 700; font-size: 14px; cursor: pointer; text-align: center; transition: all 0.2s; }
        .btn-secure { background: var(--accent-green); color: #fff; box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3); }
        .btn-bypass { background: var(--accent-red); color: #fff; box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3); }
        .console-box { background: #020617; border: 1px solid var(--border-color); border-radius: 12px; padding: 15px; font-family: monospace; font-size: 13px; color: #cbd5e1; }
        .payload-card { background: rgba(255,255,255,0.03); border: 1px dashed var(--border-color); border-radius: 10px; padding: 15px; font-size: 13px; color: #94a3b8; }
        .payload-token { background: rgba(239, 68, 68, 0.1); color: var(--accent-red); padding: 2px 6px; border-radius: 4px; font-family: monospace; font-weight: 600; }
        .results-scroll { display: flex; flex-direction: column; gap: 15px; overflow-y: auto; max-height: 380px; }
        .user-card { background: rgba(15, 23, 42, 0.8); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px; border-left: 4px solid var(--accent-blue); }
        .user-card.breached { border-left-color: var(--accent-red); }
        .meta-row { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 8px; }
        .crypto-block { background: rgba(255,255,255,0.02); padding: 10px; border-radius: 6px; font-size: 12px; display: flex; flex-direction: column; gap: 4px; margin-top: 8px; }
        .crypto-lbl { text-transform: uppercase; font-size: 10px; font-weight: 700; color: #64748b; }
        .crypto-str { font-family: monospace; word-break: break-all; color: #94a3b8; }
    </style>
</head>
<body>
<div class="container">
    <div class="panel full-width">
        <h1>🔒 Mitigating Cloud Data Leaks via Double-Layer Security Protocol</h1>
        <div style="display: flex; gap: 20px; flex-wrap: wrap; font-size: 14px; color: #94a3b8;">
            <div>• Cryptographic Core: <span style="color: var(--accent-green); font-weight: 700;">AES-256-CBC Active</span></div>
            <div>• Vulnerability Defense: <span style="color: var(--accent-blue); font-weight: 700;">SQL Parameterization Isolation</span></div>
        </div>
    </div>
    <div class="panel">
        <h2>Gateway Controller Terminal</h2>
        <div class="input-group">
            <label for="usernameInput">Target Search Query (Username)</label>
            <input type="text" id="usernameInput" value="admin">
        </div>
        <div class="btn-grid">
            <div class="btn btn-secure" onclick="dispatchQuery('secure')">Secure Execution</div>
            <div class="btn btn-bypass" onclick="dispatchQuery('vulnerable')">Bypass Isolation</div>
        </div>
        <div class="input-group">
            <label>Evaluated SQL Statement Engine Text</label>
            <div class="console-box" id="sqlConsole">SELECT username, encrypted_email FROM vault_users WHERE username = ?</div>
        </div>
        <div class="payload-card">
            <strong>💡 Testing Injection Vulnerability:</strong><br><br>
            Paste this custom payload to test the leak: <span class="payload-token">' OR '1'='1</span>
        </div>
    </div>
    <div class="panel">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2>Vault Records Extraction Manifest</h2>
            <span class="system-badge" id="modeBadge">Idle Ready</span>
        </div>
        <div class="results-scroll" id="resultsContainer">
            <div style="color: #64748b; text-align: center; font-style: italic; margin-top: 40px;">Execute search to view output profile diagnostics.</div>
        </div>
    </div>
</div>
<script>
    async function dispatchQuery(selectedMode) {
        const queryVal = document.getElementById('usernameInput').value.trim();
        const badge = document.getElementById('modeBadge');
        if(!queryVal) return;
        if(selectedMode === 'secure') {
            badge.innerText = "Secure Parameterized Protocol"; badge.style.color = "var(--accent-green)";
        } else {
            badge.innerText = "Unsafe Direct String Concat"; badge.style.color = "var(--accent-red)";
        }
        try {
            const response = await fetch('/query_vault', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: queryVal, mode: selectedMode })
            });
            const data = await response.json();
            document.getElementById('sqlConsole').innerText = data.query;
            const container = document.getElementById('resultsContainer');
            container.innerHTML = "";
            if (!data.success && data.database_error) {
                container.innerHTML = `<div style="color:var(--accent-red); font-family:monospace;">⚠️ Error: ${data.database_error}</div>`;
                return;
            }
            data.results.forEach(row => {
                const card = document.createElement('div');
                card.className = `user-card ${selectedMode === 'vulnerable' ? 'breached' : ''}`;
                card.innerHTML = `
                    <div class="meta-row"><strong>Identity:</strong> <span style="color:var(--accent-blue); font-family:monospace;">${row.username}</span></div>
                    <div class="crypto-block">
                        <span class="crypto-lbl">Decrypted Email (Plaintext)</span><span style="color:#fff;">${row.decrypted_email}</span>
                        <span class="crypto-lbl">AES-256 Storage Ciphertext</span><span class="crypto-str">${row.raw_email}</span>
                    </div>
                    <div class="crypto-block">
                        <span class="crypto-lbl">Decrypted Secret Token</span><span style="color:var(--accent-blue);">${row.decrypted_secret}</span>
                        <span class="crypto-lbl">AES-256 Storage Ciphertext</span><span class="crypto-str">${row.raw_secret}</span>
                    </div>`;
                container.appendChild(card);
            });
        } catch (error) { alert("Handshake error."); }
    }
</script>
</body>
</html>"""

# 4. Write the file automatically if missing or mismatched
html_target_path = os.path.join(TEMPLATE_DIR, 'security_index.html')
with open(html_target_path, 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)

print("\n" + "="*60)
print(f"✅ AUTO-CONFIGURED SUCCESSFUL:")
print(f"   Created HTML view right at: {html_target_path}")
print("="*60 + "\n")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
DB_PATH = os.path.join(BASE_DIR, "secure_vault.db")
AES_KEY = b'CodeAlphaSecureEncryptionKey2026' 
IV_STATIC = b'StaticInitVector'

def encrypt_data(plain_text):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, IV_STATIC)
    padded_data = pad(plain_text.encode('utf-8'), AES.block_size)
    return base64.b64encode(cipher.encrypt(padded_data)).decode('utf-8')

def decrypt_data(cipher_text):
    try:
        cipher = AES.new(AES_KEY, AES.MODE_CBC, IV_STATIC)
        return unpad(cipher.decrypt(base64.b64decode(cipher_text)), AES.block_size).decode('utf-8')
    except Exception:
        return "[Decryption Error]"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vault_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE,
            encrypted_email TEXT NOT NULL, encrypted_secret TEXT NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM vault_users")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO vault_users (username, encrypted_email, encrypted_secret) VALUES (?, ?, ?)",
            ("admin", encrypt_data("admin@enterprise.cloud"), encrypt_data("FLAG{AES_256_VAULT_SUCCESS}"))
        )
        conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('security_index.html')

@app.route('/query_vault', methods=['POST'])
def query_vault():
    data = request.json or {}
    user_input = data.get("username", "").strip()
    execution_mode = data.get("mode", "secure")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    records, constructed_query, error_raised = [], "", None
    try:
        if execution_mode == "vulnerable":
            constructed_query = f"SELECT username, encrypted_email, encrypted_secret FROM vault_users WHERE username = '{user_input}'"
            cursor.execute(constructed_query)
        else:
            constructed_query = "SELECT username, encrypted_email, encrypted_secret FROM vault_users WHERE username = ?"
            cursor.execute(constructed_query, (user_input,))
        rows = cursor.fetchall()
        for row in rows:
            records.append({
                "username": row[0], "raw_email": row[1], "raw_secret": row[2],
                "decrypted_email": decrypt_data(row[1]), "decrypted_secret": decrypt_data(row[2])
            })
    except sqlite3.Error as e:
        error_raised = str(e)
    finally:
        conn.close()
    return jsonify({"success": True if not error_raised else False, "query": constructed_query, "results": records, "database_error": error_raised})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5002)