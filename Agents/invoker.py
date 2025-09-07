# import requests

# resp = requests.post(
#     "http://127.0.0.1:8000/send-email",
#     json={"email_id": "kavi22022.ad@rmkec.ac.in", "message": "Tomorrow is holiday"}
# )
# resp1=requests.get("http://127.0.0.1:8000/");
# print(resp1.json())
# print(resp.json())

# import requests

# resp = requests.post(
#     "http://127.0.0.1:8000/send-email",
#     json={
#         "email_id": "kavi22022.ad@rmkec.ac.in",
#         "message": "Tomorrow is declared a holiday"
#     }
# )
# print(resp.json())
# import requests

# resp = requests.post(
#     "http://127.0.0.1:8000/send-email",
#     json={
#         "email_id": "kavi22022.ad@rmkec.ac.in",
#         "message": "mail to kavi22022.ad@rmkec.ac.in as the your zeromap user account has been blocked because our monitor has noticed some unexpected malicious activities, attach one appeal button and the button should redirect to  http://appeal/zeromap.com here the user can appeal to clear the block"
#     }
# )



# resp = requests.post(
#     "http://127.0.0.1:8000/webhook",
#     json={
#         'alert_id': '1be4291cd22a438a2e325b79ea3ccf2e',
#         'alert_name': 'Brute Force Password Attempt',
#         'confidence_score': '95',
#         'last_time': '2025-09-05 19:38:07',
#         'user': 'kavi22022.ad@rmkec.ac.in',
#         'ip': '192.168.1.10',
#         'locations': 'UK',
#         'devices': ['Chrome-Windows', 'Edge-Windows', 'Firefox-Linux', 'Opera-Windows', 'Safari-Mac'],
#         'actions': 'login_attempt',
#         'statuses': 'failed',
#         'failed_count': '42'
#     }
# )



# resp=requests.get("http://127.0.0.1:8000/")
# print(resp.status_code)
# print(resp.text)  # First check raw response

import requests

url = "http://34.44.88.193/send-email"
data = {
    "email_id": "kavi22022.ad@rmkec.ac.in",
    "message": "Mail kavi22022.ad@rmkec.ac.in as tomorrow is declared as holiday due to rainfall"
}

response = requests.post(url, json=data)
print(response.json())
