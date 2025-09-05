from descope import DescopeClient

PROJECT_ID = "P32GTfUg5UE6jTwQNzhPJzQXDhf2"
descope = DescopeClient(project_id=PROJECT_ID)

# First time user needs to sign up with email + password
resp = descope.password.sign_up(
    login_id="kavirajtechpersonal@gmail.com",
    password="12345678Ab@"
)

print("✅ User signed up:", resp)
