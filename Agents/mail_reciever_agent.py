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
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Init Descope client



async def test_server():

   
    

    async with Client("http://localhost:8080/mcp") as client:
        # ✅ Call authenticator
        # auth_result = await client.call_tool("authenticator", {"token": token})

        tools = await client.list_tools()
        for tool in tools:
            print(f">>> Tool found: {tool.name}")
        # Call add tool
        result=await client.call_tool("authenticator",{"access_key":os.getenv("DESCOPE_ACCESS_KEY")})
        print(result[0])

        print(">>>  Calling add tool for 1 + 2")
        result = await client.call_tool("add", {"a": 1, "b": 2})
        print(f"<<<  Result: {result[0].text}")
        # Call subtract tool
        print(">>>  Calling subtract tool for 10 - 3")
        result = await client.call_tool("subtract", {"a": 10, "b": 3})
        print(f"<<< Result: {result[0].text}")
        # print("Auth result:", auth_result[0].text)

        result = await client.call_tool("send_email_to_employees", {"email_id":"kavi22022.ad@rmkec.ac.in", "message":"tomorrow is declared as an holiday for exam preparation, send this mail to kavi22022.ad@rmkec.ac.in"})
        print(f"<<< Result: {result[0].text}")

if __name__ == "__main__":
    asyncio.run(test_server())

