from descope import DescopeClient

PROJECT_ID = "P32GTfUg5UE6jTwQNzhPJzQXDhf2"
descope = DescopeClient(project_id=PROJECT_ID)

# Sign in with email + password
resp = descope.password.sign_in(
    login_id="kavirajtechpersonal@gmail.com",
    password="12345678Ab@"
)

# Extract session token
token = resp["sessionToken"]
print("✅ Got session token:", token)
