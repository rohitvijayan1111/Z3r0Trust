from descope import DescopeClient

PROJECT_ID = "P32GTfUg5UE6jTwQNzhPJzQXDhf2"
descope_client = DescopeClient(project_id=PROJECT_ID)
def get_service_jwt():
    jwt_response = descope_client.exchange_access_key("K32HJodFRFkmcQHY2jRzssfYN7KbuyH28de5AcbE8O3tukkipplW6Jdpkr88iff1YIaZ2o8")
    print("JWT Response:", jwt_response)  # Debug
    # Extract the JWT from nested 'sessionToken' object
    token = jwt_response.get('sessionToken', {}).get('jwt')
    if not token:
        return False
    return token
print(get_service_jwt())