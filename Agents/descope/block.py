from descope import DescopeClient

PROJECT_ID = "P32GTfUg5UE6jTwQNzhPJzQXDhf2"
MANAGEMENT_KEY = "K32JhxcSYnzl4rjqEnHWYiwscYXY0antcHb3AxCZ2vQK9ZseDWe3Jvd2STDv3foXjnLpwSf" 
descope = DescopeClient(project_id=PROJECT_ID, management_key=MANAGEMENT_KEY)

def block(userid):
    try:
        descope.management.user.update_status(userid, "disabled")
        return f"🚫 Permanently blocked user {userid}"
    except Exception as e:
        return f"❌ Failed to block user: {str(e)}"

block("diva22022.it@rmkec.ac.in")