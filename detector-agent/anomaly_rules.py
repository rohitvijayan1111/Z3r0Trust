from datetime import datetime, timedelta
from collections import defaultdict


failed_attempts = defaultdict(list)
user_locations = defaultdict(list)
user_ips = defaultdict(list)

def detect_anomalies(event: dict):
    username = event.get("username")
    location = event.get("location")
    ip = event.get("ip")
    req_type = event.get("request_type")
    response = event.get("response")
    ts = datetime.fromisoformat(event["timestamp"])

    anomalies = []

    # Rule 1: Brute force login attempts
    if response == "fail":
        failed_attempts[username].append(ts)
        failed_attempts[username] = [t for t in failed_attempts[username] if t > ts - timedelta(minutes=5)]
        if len(failed_attempts[username]) > 5:
            anomalies.append("Brute force attempt: multiple failed logins in short time")

    # Rule 2: Impossible travel (location change too fast)
    if username and location:
        last_locations = user_locations[username]
        if last_locations:
            prev_loc, prev_ts = last_locations[-1]
            if prev_loc != location and (ts - prev_ts).seconds < 600:
                anomalies.append(f"Impossible travel: {prev_loc} → {location} in <10 mins")
        user_locations[username].append((location, ts))


    # Rule 4: Multiple IPs in short time
    if username and ip:
        user_ips[username].append((ip, ts))
        recent_ips = [i for i, t in user_ips[username] if t > ts - timedelta(minutes=10)]
        if len(set(recent_ips)) > 3:
            anomalies.append("Suspicious behavior: user logged in from multiple IPs in short time")

    return anomalies
