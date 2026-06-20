import os
import sqlite3
import random
import time
from flask import Flask, render_template, request, jsonify

# 1. Dynamically discover path to ensure Flask finds the template folder
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

print("\n" + "="*60)
print(f"👉 CRITICAL DIAGNOSTIC CHECK:")
print(f"   Looking for 'bus_index.html' inside: {template_dir}")
print(f"   Does templates folder exist? {os.path.exists(template_dir)}")
if os.path.exists(template_dir):
    print(f"   Files inside templates folder: {os.listdir(template_dir)}")
print("="*60 + "\n")

app = Flask(__name__, template_folder=template_dir)
DB_NAME = os.path.join(base_dir, "bus_pass.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            passenger_name TEXT NOT NULL,
            route TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

ROUTE_PRICING = {
    "Route A (Downtown - Campus)": 15.00,
    "Route B (Suburbs - Terminal)": 25.50,
    "Route C (Express - Airport)": 40.00
}

def check_server_load():
    simulated_traffic = random.randint(50, 150) 
    active_servers = 1 if simulated_traffic <= 90 else 3
    status = "Normal Traffic." if active_servers == 1 else "High Traffic Detected! Autoscale Triggered: Provisioned +2 instances."
    return {"traffic": simulated_traffic, "servers": active_servers, "status": status}

@app.route('/')
def home():
    load_metrics = check_server_load()
    return render_template('bus_index.html', routes=ROUTE_PRICING, metrics=load_metrics)

@app.route('/book_pass', methods=['POST'])
def book_pass():
    start_time = time.time()
    data = request.json
    name = data.get("name", "").strip()
    route = data.get("route", "")

    if not name or route not in ROUTE_PRICING:
        return jsonify({"success": False, "message": "Invalid inputs."}), 400

    verified_price = ROUTE_PRICING[route]
    secure_ticket_id = f"CA-PASS-{random.randint(100000, 999999)}"
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tickets (ticket_id, passenger_name, route, price, timestamp, status) VALUES (?, ?, ?, ?, ?, ?)",
            (secure_ticket_id, name, route, verified_price, current_time, "VERIFIED_ACTIVE")
        )
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"success": False, "message": "Database error."}), 500

    compute_latency = round((time.time() - start_time) * 1000, 2)
    load_info = check_server_load()

    return jsonify({
        "success": True,
        "ticket_id": secure_ticket_id,
        "price": verified_price,
        "time": current_time,
        "latency": f"{compute_latency}ms",
        "scale_status": load_info["status"]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)