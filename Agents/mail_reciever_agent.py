# # agent.py
# import os
# from agno.agent import Agent
# from agno.tools.mcp import MCPTools
# from agno.models.openai import OpenAIChat

# GROQ_BASE = "https://api.groq.com/openai/v1"

# async def main():
#     # Launch your MCP server as a subprocess via stdio
#     # (adjust the command if your server file is not main.py)
#     async with MCPTools(command="python mail_mcp_server/main.py", timeout_seconds=60) as mcp_tools:
#         agent = Agent(
#             # Pick a Groq model; example: Llama 3.3 70B versatile
#             model= OpenAIChat(
#                 id="llama-3.3-70b-versatile",   # Groq model name
#                 base_url="https://api.groq.com/openai/v1",
#                 api_key=os.environ["GROQ_API_KEY"],
#             )
# ,
#             tools=[mcp_tools],
#             markdown=True,
#         )

#         # Ask the agent to use your MCP tools
#         prompt = (
#             "show the last 5 recent mails for the mail id kavirajmetech@gmail.com"
#         )
#         await agent.aprint_response(prompt, stream=True)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())


import asyncio
from fastmcp import Client
from descope import DescopeClient

# ✅ Init Descope client
descope = DescopeClient(project_id="P32GTfUg5UE6jTwQNzhPJzQXDhf2")

def get_token():
    # Replace with your real login flow
    resp = descope.password.sign_in(
        login_id="kavirajtechpersonal@gmail.com",
        password="12345678Ab@"  # (fix: 'code' → 'password')
    )
    return resp["sessionToken"]

token = get_token()
print(token['jwt'])


async def test_server():

   
    

    async with Client("http://localhost:8080/mcp") as client:
        # ✅ Call authenticator
        # auth_result = await client.call_tool("authenticator", {"token": token})

        tools = await client.list_tools()
        for tool in tools:
            print(f">>> Tool found: {tool.name}")
        # Call add tool
        print(">>>  Calling add tool for 1 + 2")
        result = await client.call_tool("add", {"a": 1, "b": 2, "token": token['jwt']})
        print(f"<<<  Result: {result[0].text}")
        # Call subtract tool
        print(">>>  Calling subtract tool for 10 - 3")
        result = await client.call_tool("subtract", {"a": 10, "b": 3, "token": token['jwt']})
        print(f"<<< Result: {result[0].text}")
        # print("Auth result:", auth_result[0].text)


if __name__ == "__main__":
    asyncio.run(test_server())

