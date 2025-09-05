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

import requests

resp = requests.post(
    "http://127.0.0.1:8000/send-email",
    json={"email_id": "kavi22022.ad@rmkec.ac.in", "message": "Tomorrow is holiday"}
)
print(resp.json())
