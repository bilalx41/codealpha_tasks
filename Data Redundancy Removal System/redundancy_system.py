import asyncio
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Set

class WorldClassRedundancyEngine:
    def __init__(self):
        # Simulated high-performance persistent NoSQL cloud storage
        self.cloud_database: Dict[str, Dict[str, Any]] = {}
        # In-memory ultra-fast SHA-256 fingerprint lookup set
        self.fingerprint_cache: Set[str] = set()
        
        # System tracking metrics
        self.metrics = {"processed": 0, "unique": 0, "redundant": 0, "false_positive": 0}

    def generate_fingerprint(self, payload: Dict[str, Any]) -> str:
        """Generates a deterministic SHA-256 hash by sorting keys strictly."""
        normalized_str = json.dumps(payload, sort_keys=True).encode('utf-8')
        return hashlib.sha256(normalized_str).hexdigest()

    def validate_contract(self, packet: Dict[str, Any]) -> Tuple[str, str]:
        """Strict Data Contract Layer to catch anomalies and False Positives."""
        if not isinstance(packet, dict) or "transaction_id" not in packet or "payload" not in packet:
            return "FALSE_POSITIVE", "Missing core structural wrappers"
            
        payload = packet["payload"]
        if not isinstance(payload, dict):
            return "FALSE_POSITIVE", "Payload field must be an object map"
            
        # Metric type checks
        val = payload.get("reading_value")
        if val is None:
            return "FALSE_POSITIVE", "Missing required field: 'reading_value'"
        if not isinstance(val, (int, float)):
            return "FALSE_POSITIVE", f"Type violation: expected number, got '{type(val).__name__}'"
            
        # Device identity checks
        device_id = payload.get("device_id")
        if not device_id or len(str(device_id).strip()) < 3:
            return "FALSE_POSITIVE", "Validation constraint error: 'device_id' missing or too short"

        return "VALID", ""

    async def ingest_packet(self, raw_packet: Dict[str, Any]) -> Tuple[str, str]:
        """Asynchronous execution channel handling stream ingestion and sorting."""
        self.metrics["processed"] += 1
        
        # Step 1: Validate Contract (Identify False Positives)
        validation_status, error_msg = self.validate_contract(raw_packet)
        if validation_status == "FALSE_POSITIVE":
            self.metrics["false_positive"] += 1
            return "FALSE_POSITIVE", error_msg

        txn_id = raw_packet["transaction_id"]
        payload = raw_packet["payload"]

        # Step 2: Compute Unique Signature Cryptographic Fingerprint
        fingerprint = self.generate_fingerprint(payload)

        # Step 3: Fast Deduplication Lookup (Identify Redundancy)
        if fingerprint in self.fingerprint_cache:
            self.metrics["redundant"] += 1
            return "REDUNDANT", f"Dropped exact match data duplicate."

        # Step 4: Commit Unique and Verified Records
        db_record = dict(payload)
        db_record["_committed_at_utc"] = datetime.now(timezone.utc).isoformat()
        
        self.cloud_database[txn_id] = db_record
        self.fingerprint_cache.add(fingerprint)
        self.metrics["unique"] += 1
        
        return "SUCCESS", f"Stored securely under Transaction Reference: {txn_id}"


# --- Interactive Terminal Animation Assets ---
async def play_spinner_animation(duration: float, step_label: str):
    """Renders a beautiful live frame loading spinner inside the console terminal line."""
    spin_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    iterations = int(duration / 0.08)
    for i in range(iterations):
        frame = spin_frames[i % len(spin_frames)]
        sys.stdout.write(f"\r  {frame} \033[36m{step_label}...\033[0m")
        sys.stdout.flush()
        await asyncio.sleep(0.08)
    sys.stdout.write("\r" + " " * 70 + "\r") # Clear the animation trace line cleanly


async def run_live_pipeline():
    # Setup fresh dashboard viewing window 
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\033[95m" + "=" * 80)
    print("      ⚡ HIGH-THROUGHPUT REAL-TIME INGESTION DASHBOARD v5.0 (ANIMATED) ⚡      ")
    print("=" * 80 + "\033[0m\n")

    engine = WorldClassRedundancyEngine()

    # Varied streaming network traffic packets
    data_stream = [
        {"transaction_id": "TXN-701", "payload": {"device_id": "MAIN_FRAME_A", "reading_value": 89.4}},
        {"transaction_id": "TXN-702", "payload": {"device_id": "MAIN_FRAME_A", "reading_value": 89.4}}, # Duplicate
        {"transaction_id": "TXN-703", "payload": {"device_id": "MAIN_FRAME_B", "reading_value": "MALFORMED_STR"}}, # FP Bad Type
        {"transaction_id": "TXN-704", "payload": {"device_id": "", "reading_value": 14.2}}, # FP Empty ID
        {"transaction_id": "TXN-705", "payload": {"device_id": "MAIN_FRAME_C", "reading_value": 55.1}},
        {"transaction_id": "TXN-706", "payload": {"device_id": "MAIN_FRAME_A", "reading_value": 89.4}}, # Duplicate again
        {"transaction_id": "TXN-707", "payload": {"device_id": "MAIN_FRAME_B", "reading_value": 102.7}}
    ]

    for index, raw_packet in enumerate(data_stream, start=1):
        txn_display = raw_packet.get("transaction_id", "UNKNOWN")
        print(f"\033[1m▶ [INBOUND] Processing Stream Packet #{index} (ID: {txn_display})\033[0m")
        
        # Play concurrent step animations to represent cloud network processing latency
        await play_spinner_animation(0.4, "Parsing data contract boundaries")
        await play_spinner_animation(0.5, "Running cryptographic signature lookups")

        # Execute processing engine logic
        status, message = await engine.ingest_packet(raw_packet)

        # Output dynamic beautifully colored status block matrices
        if status == "SUCCESS":
            print(f"  ┗━━ 🟢 \033[92m[UNIQUE COMMITTED]\033[0m {message}\n")
        elif status == "REDUNDANT":
            print(f"  ┗━━ 🟡 \033[93m[REDUNDANT IGNORED]\033[0m {message}\n")
        else:
            print(f"  ┗━━ 🔴 \033[91m[FALSE POSITIVE REJECTED]\033[0m {message}\n")
            
        await asyncio.sleep(0.3) # Natural visual pause interval between items

    # Render persistent storage metrics state
    print("\033[95m" + "=" * 80)
    print("  📊 LIVE REAL-TIME METRICS COMPILATION SUMMARY")
    print("=" * 80 + "\033[0m")
    print(f"  • Total Evaluated Streams : {engine.metrics['processed']}")
    print(f"  • Unique Saved Base Logs : \033[92m{engine.metrics['unique']}\033[0m")
    print(f"  • Intercepted Redundancies: \033[93m{engine.metrics['redundant']}\033[0m")
    print(f"  • Deflected False Positives: \033[91m{engine.metrics['false_positive']}\033[0m")
    print("\033[95m" + "=" * 80 + "\033[0m\n")

    print("\033[1m📦 TARGET CLOUD STORAGE DATABASE DUMP:\033[0m")
    print(json.dumps(engine.cloud_database, indent=4))

if __name__ == "__main__":
    # Launch the async loop environment natively inside Python
    asyncio.run(run_live_pipeline())