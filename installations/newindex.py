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
IPERF_PATH = "./iperf3.exe"
SERVER = "65.0.7.155"
PORT = 5201
ADAPTER_NAME = "WiFi"  # leave blank "" for auto-detect

TCP_DURATION = 10
UDP_DURATION = 10
UDP_BANDWIDTH = "50M"
PING_COUNT = 5
INTERVAL = 30
WAN_TARGET = "8.8.8.8"

# ===============================
# LOG PATH SETUP
# ===============================
LOG_DIR = "C:\\temp"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "Full_Network_Diagnostics_Py.csv")

# ===============================
# HELPER FUNCTIONS
# ===============================

def detect_active_adapter():
    """Automatically detect active network adapter"""
    stats = psutil.net_if_stats()
    for name, s in stats.items():
        if s.isup and name.lower() != "loopback":
            return name
    return None


def get_default_gateway():
    try:
        output = subprocess.check_output(["route", "print", "0.0.0.0"], text=True)
        for line in output.splitlines():
            if "0.0.0.0" in line and "Active Routes" not in line:
                parts = line.split()
                if len(parts) >= 3:
                    return parts[2]
    except:
        pass
    return None


def run_ping(target):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = ['ping', param, str(PING_COUNT), target]

    try:
        output = subprocess.check_output(cmd, text=True)

        if "Average =" in output:
            avg = float(output.split("Average =")[-1].replace("ms", "").strip())
            return {"Latency": avg, "Loss": 0}

    except subprocess.CalledProcessError:
        return {"Latency": 0, "Loss": 100}

    return {"Latency": 0, "Loss": 100}


def get_nic_stats(adapter):
    counters = psutil.net_io_counters(pernic=True)
    return counters.get(adapter)


def calculate_stats(data):
    if not data:
        return {"Min": 0, "Max": 0, "Avg": 0}

    return {
        "Min": round(min(data), 2),
        "Max": round(max(data), 2),
        "Avg": round(sum(data) / len(data), 2)
    }


def run_iperf(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return json.loads(result.stdout)
    except:
        return None


# ===============================
# INITIALIZATION
# ===============================

if not os.path.exists(IPERF_PATH):
    print("ERROR: iperf3.exe not found:", IPERF_PATH)
    exit()

if not ADAPTER_NAME:
    ADAPTER_NAME = detect_active_adapter()

print("Using Network Adapter:", ADAPTER_NAME)

headers = [
    "Timestamp","TCP_Down_Mbps","TCP_Up_Mbps","UDP_Loss%","UDP_Jitter_ms",
    "NIC_Down_Mbps","GW_Lat_ms","GW_Loss%","WAN_Lat_ms",
    "iPerf_Down_Min","iPerf_Down_Max","iPerf_Down_Avg","Retransmission%"
]

if not os.path.exists(log_file):
    with open(log_file,'w',newline='') as f:
        csv.writer(f).writerow(headers)

trend_iperf_down = []

gateway = get_default_gateway()

# ===============================
# MAIN LOOP
# ===============================

try:

    while True:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        gw_ping = run_ping(gateway) if gateway else {"Latency":0,"Loss":100}
        wan_ping = run_ping(WAN_TARGET)

        # ---------------------------
        # TCP DOWNLOAD TEST
        # ---------------------------

        nic_before = get_nic_stats(ADAPTER_NAME)
        t1 = time.time()

        cmd_down = [IPERF_PATH,"-c",SERVER,"-p",str(PORT),"-t",str(TCP_DURATION),"-J","-R"]
        down_data = run_iperf(cmd_down)

        t2 = time.time()
        nic_after = get_nic_stats(ADAPTER_NAME)

        nic_down = 0

        if nic_before and nic_after:
            delta = nic_after.bytes_recv - nic_before.bytes_recv
            nic_down = round(((delta * 8)/(t2-t1))/1e6,2)

        tcp_down = 0
        retrans_rate = 0

        if down_data:
            try:
                tcp_down = round(down_data['end']['sum_received']['bits_per_second']/1e6,2)

                retrans = down_data['end']['sum_sent'].get('retransmits',0)
                bytes_sent = down_data['end']['sum_sent']['bytes']
                mss = down_data['start']['test_start'].get('mss',1460)

                packets = bytes_sent/mss if mss else 0

                if packets>0:
                    retrans_rate = (retrans/packets)*100

            except:
                pass

        # ---------------------------
        # TCP UPLOAD
        # ---------------------------

        tcp_up = 0

        cmd_up = [IPERF_PATH,"-c",SERVER,"-p",str(PORT),"-t",str(TCP_DURATION),"-J"]
        up_data = run_iperf(cmd_up)

        if up_data:
            try:
                tcp_up = round(up_data['end']['sum_sent']['bits_per_second']/1e6,2)
            except:
                pass

        # ---------------------------
        # UDP TEST
        # ---------------------------

        udp_loss = 0
        udp_jitter = 0

        cmd_udp = [IPERF_PATH,"-c",SERVER,"-p",str(PORT),"-u","-b",UDP_BANDWIDTH,"-t",str(UDP_DURATION),"-J"]
        udp_data = run_iperf(cmd_udp)

        if udp_data:
            try:
                udp_loss = round(udp_data['end']['sum']['lost_percent'],2)
                udp_jitter = round(udp_data['end']['sum']['jitter_ms'],2)
            except:
                pass

        # ---------------------------
        # TREND STATS
        # ---------------------------

        trend_iperf_down.append(tcp_down)
        stats = calculate_stats(trend_iperf_down)

        # ---------------------------
        # LOGGING
        # ---------------------------

        row = [
            timestamp,tcp_down,tcp_up,udp_loss,udp_jitter,
            nic_down,gw_ping['Latency'],gw_ping['Loss'],wan_ping['Latency'],
            stats['Min'],stats['Max'],stats['Avg'],round(retrans_rate,4)
        ]

        with open(log_file,'a',newline='') as f:
            csv.writer(f).writerow(row)

        # ---------------------------
        # DASHBOARD
        # ---------------------------

        os.system('cls' if os.name=='nt' else 'clear')

        print("===== FULL NETWORK DIAGNOSTICS =====")
        print("Time:",timestamp)

        print("\n--- Throughput ---")
        print("TCP Down:",tcp_down,"Mbps")
        print("TCP Up  :",tcp_up,"Mbps")
        print("NIC Down:",nic_down,"Mbps")

        print("\n--- UDP ---")
        print("Loss  :",udp_loss,"%")
        print("Jitter:",udp_jitter,"ms")

        print("\n--- Latency ---")
        print("Gateway:",gw_ping['Latency'],"ms")
        print("Internet:",wan_ping['Latency'],"ms")

        print("\n--- Trend (Download) ---")
        print("Min:",stats['Min'],"Max:",stats['Max'],"Avg:",stats['Avg'])

        status = "OK" if retrans_rate <=1 else "WARNING"
        print("\nRetransmission Rate:",round(retrans_rate,4),"%",status)

        print("\nLogging:",log_file)

        time.sleep(INTERVAL)

except KeyboardInterrupt:

    print("\nMonitoring stopped.")