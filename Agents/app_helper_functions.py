def apply_policy(alert):
    try:
        score = int(alert.get("confidence_score", 0))
    except ValueError:
        score = 0

    if 0 <= score <= 40:
        alert["status"] = "logged"
    elif 61 <= score <= 80:
        alert["status"] = "temporary_block"
    elif 81 <= score <= 100:
        alert["status"] = "permanent_block"
    else:
        alert["status"] = "unknown"
    return alert


