# ===============================
# pip install psutil
# ===============================

import os
import time
import json
import csv
import subprocess
import platform
import psutil
from datetime import datetime

# ===============================
# CONFIGURATION
# ===============================
IPERF_PATH ="./iperf3.exe"
SERVER = "65.0.7.155"
PORT = 5201
ADAPTER_NAME = "WiFi"  # Note: On Linux/Mac, this might be 'eth0' or 'en0'
TCP_DURATION = 10
UDP_DURATION = 10
UDP_BANDWIDTH = "50M"
PING_COUNT = 5
INTERVAL = 30
WAN_TARGET = "8.8.8.8"

# Setup Log Path
# desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
log_file = os.path.join("C:\\temp\\", "Full_Network_Diagnostics_Py.csv")

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------

def get_default_gateway():
    """Detects the default gateway IP by parsing 'route print'."""
    try:
        # Run the Windows 'route print' command
        output = subprocess.check_output(["route", "print", "0.0.0.0"], universal_newlines=True)
        # Look for the Gateway column in the Active Routes table
        for line in output.splitlines():
            if "0.0.0.0" in line and "Active Routes" not in line:
                parts = line.split()
                if len(parts) >= 3:
                    # The gateway is usually the 3rd column in 'route print'
                    return parts[2]
    except Exception:
        return None
    return None

def run_ping(target):
    """Replicates Test-Connection for Latency and Loss."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(PING_COUNT), target]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        # Parse output for average latency (this regex is basic; handles Windows format)
        if "Average =" in output:
            avg_lat = float(output.split("Average =")[-1].replace("ms", "").strip())
            return {"Latency": avg_lat, "Loss": 0}
    except subprocess.CalledProcessError:
        return {"Latency": 0, "Loss": 100}
    return {"Latency": 0, "Loss": 100}

def get_nic_stats(adapter):
    """Gets current Sent/Received bytes for a specific adapter."""
    counters = psutil.net_io_counters(pernic=True)
    if adapter in counters:
        return counters[adapter]
    return None

def calculate_stats(data_list):
    """Replicates the PowerShell Stats function."""
    if not data_list:
        return {"Min": 0, "Max": 0, "Avg": 0}
    return {
        "Min": round(min(data_list), 2),
        "Max": round(max(data_list), 2),
        "Avg": round(sum(data_list) / len(data_list), 2)
    }

# -------------------------------
# MAIN MONITORING LOOP
# -------------------------------

# Initialize CSV
headers = [
    "Timestamp", "TCP_Down_Mbps", "TCP_Up_Mbps", "UDP_Loss%", "UDP_Jitter_ms", 
    "NIC_Down_Mbps", "NIC_Up_Mbps", "GW_Lat_ms", "GW_Loss%", "WAN_Lat_ms",
    "iPerf_Down_Min", "iPerf_Down_Max", "iPerf_Down_Avg"
]

if not os.path.exists(log_file):
    with open(log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

# Trend Trackers
trend_iperf_down, trend_iperf_up = [], []
trend_nic_down, trend_nic_up = [], []

gateway = get_default_gateway()

try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. PING TESTS
        gw_ping = run_ping(gateway) if gateway else {"Latency": 0, "Loss": 100}
        wan_ping = run_ping(WAN_TARGET)

        # 2. TCP DOWNLOAD & NIC STATS
        nic_before = get_nic_stats(ADAPTER_NAME)
        t1 = time.time()
        
        # Run iPerf3 Download (-R for reverse/down)
        cmd_down = [IPERF_PATH, "-c", SERVER, "-p", str(PORT), "-t", str(TCP_DURATION), "-J", "-R"]
        res_down = subprocess.run(cmd_down, capture_output=True, text=True)
        
        t2 = time.time()
        nic_after = get_nic_stats(ADAPTER_NAME)
        
        # Calculate NIC Bandwidth
        delta_recv = nic_after.bytes_recv - nic_before.bytes_recv
        nic_down_mbps = round(((delta_recv * 8) / (t2 - t1)) / 1e6, 2)
        
        # Parse iPerf Download
        try:
            data_down = json.loads(res_down.stdout)
            tcp_down = round(data_down['end']['sum_received']['bits_per_second'] / 1e6, 2)
        except: tcp_down = 0

        # 3. TCP UPLOAD
        cmd_up = [IPERF_PATH, "-c", SERVER, "-p", str(PORT), "-t", str(TCP_DURATION), "-J"]
        res_up = subprocess.run(cmd_up, capture_output=True, text=True)
        try:
            data_up = json.loads(res_up.stdout)
            tcp_up = round(data_up['end']['sum_sent']['bits_per_second'] / 1e6, 2)
        except: tcp_up = 0

        # 4. UDP TEST
        cmd_udp = [IPERF_PATH, "-c", SERVER, "-p", str(PORT), "-u", "-b", UDP_BANDWIDTH, "-t", str(UDP_DURATION), "-J"]
        res_udp = subprocess.run(cmd_udp, capture_output=True, text=True)
        try:
            data_udp = json.loads(res_udp.stdout)
            udp_loss = round(data_udp['end']['sum']['lost_percent'], 2)
            udp_jitter = round(data_udp['end']['sum']['jitter_ms'], 2)
        except: udp_loss, udp_jitter = 0, 0

        # Update Trends
        trend_iperf_down.append(tcp_down)
        trend_nic_down.append(nic_down_mbps)
        sIPDown = calculate_stats(trend_iperf_down)
        
        # Parse iPerf Download & Retransmissions
        retransmission_rate = 0
        tcp_retrans = 0
        try:
            data_down = json.loads(res_down.stdout)
            tcp_down = round(data_down['end']['sum_received']['bits_per_second'] / 1e6, 2)
            
            # Logic for Retransmission Rate
            tcp_retrans = data_down['end']['sum_sent'].get('retransmits', 0)
            total_bytes = data_down['end']['sum_sent']['bytes']
            mss = data_down['start']['test_start'].get('mss', 1460)
            
            total_packets = total_bytes / mss
            if total_packets > 0:
                retransmission_rate = (tcp_retrans / total_packets) * 100
        except:
            tcp_down = 0

        # 5. LOGGING
        log_data = [timestamp, tcp_down, tcp_up, udp_loss, udp_jitter, nic_down_mbps, 0, gw_ping['Latency'], gw_ping['Loss'], wan_ping['Latency'], sIPDown['Min'], sIPDown['Max'], sIPDown['Avg']]
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(log_data)

        # 6. DASHBOARD (Console Output)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"--- FULL NETWORK DIAGNOSTICS ({timestamp}) ---")
        print(f"TCP Down: {tcp_down} Mbps | TCP Up: {tcp_up} Mbps")
        print(f"UDP Loss: {udp_loss}% | Jitter: {udp_jitter} ms")
        print(f"NIC Down: {nic_down_mbps} Mbps")
        print(f"GW Ping: {gw_ping['Latency']} ms | WAN Ping: {wan_ping['Latency']} ms")
        print(f"\nTrend (IPerf Down): Min: {sIPDown['Min']} | Max: {sIPDown['Max']} | Avg: {sIPDown['Avg']}")
        print(f"Logging to: {log_file}")
        # Color coding logic for retransmission rate
        retrans_status = "OK" if retransmission_rate <= 1 else "HIGH WARNING"
        print(f"Retransmission Rate: {retransmission_rate:.4f}% ({retrans_status})")
        print(f"WAN Latency: {wan_ping['Latency']} ms")

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\nDiagnostics stopped by user.")