# from descope import DescopeClient

# PROJECT_ID = "P32GTfUg5UE6jTwQNzhPJzQXDhf2"
# MANAGEMENT_KEY = "K32P65VkpsOheH1tZ6VGBPYATjyA8DXBOozttLc38DfRVOck8g6bB6BElB2qLjpXGa5W7GX"

# # Initialize Descope client
# descope = DescopeClient(project_id=PROJECT_ID, management_key=MANAGEMENT_KEY)

# print("hello")

# def block(userid: str):
#     try:
#         # Use the appropriate status string expected by the SDK/API
#         response = descope.management.user.update_status(userid, "Inactive")
#         # Check if operation succeeded
#         if hasattr(response, 'ok') and not response.ok:
#             return f"❌ Failed to block user {userid}: {response.error if hasattr(response, 'error') else response}"
#         return f"🚫 Successfully set status to Inactive for user {userid}"
#     except Exception as e:
#         return f"❌ Failed to block user {userid}: {str(e)}"

# # Example usage
# print(block("kavi22022.ad@rmkec.ac.in"))
from descope import DescopeClient

PROJECT_ID = "P32GTfUg5UE6jTwQNzhPJzQXDhf2"
MANAGEMENT_KEY = "K32P65VkpsOheH1tZ6VGBPYATjyA8DXBOozttLc38DfRVOck8g6bB6BElB2qLjpXGa5W7GX"

# Initialize Descope client with management key
descope = DescopeClient(project_id=PROJECT_ID, management_key=MANAGEMENT_KEY)

print("hello")

def login(userid):
        
    PROJECT_ID = "P32GTfUg5UE6jTwQNzhPJzQXDhf2"
    descope = DescopeClient(project_id=PROJECT_ID)

    # Sign in with email + password
    resp = descope.password.sign_in(
        login_id=userid,
        password="12345678Ab@"
    )

    # Extract session token
    token = resp["sessionToken"]
    print("✅ Got session token:", token)

def signup(userid):
    PROJECT_ID = "P32GTfUg5UE6jTwQNzhPJzQXDhf2"
    descope = DescopeClient(project_id=PROJECT_ID)

    # First time user needs to sign up with email + password
    resp = descope.password.sign_up(
        login_id=userid,
        password="12345678Ab@"
    )

    print("✅ User signed up:", resp)

def block(userid: str):
    try:
        # Update status directly via `descope.user`
        descope.mgmt.user.deactivate(userid)   # or "Disabled" if supported
        return f"🚫 Permanently blocked user {userid}"
    except Exception as e:
        return f"❌ Failed to block user {userid}: {str(e)}"

# Example usage
print(signup("abc.it@rmkec.ac.in"))
# print(login("kavi22022.ad@rmkec.ac.in"))
# print(block("kavi22022.ad@rmkec.ac.in"))
