# import asyncio
# from fastmcp import Client
# from descope import DescopeClient
# import os
# from dotenv import load_dotenv

# load_dotenv()

# async def test_server():

#     async with Client("http://localhost:8080/mcp") as client:
#         # ✅ Call authenticator
#         # auth_result = await client.call_tool("authenticator", {"token": token})

#         tools = await client.list_tools()
#         for tool in tools:
#             print(f">>> Tool found: {tool.name}")
#         # Call add tool
#         result=await client.call_tool("authenticator",{"access_key":os.getenv("DESCOPE_ACCESS_KEY")})
#         print(result[0])

#         result = await client.call_tool("send_email_to_employees", {"email_id":"kavi22022.ad@rmkec.ac.in", "message":"tomorrow is declared as an holiday for exam preparation, send this mail to kavi22022.ad@rmkec.ac.in"})
#         print(f"<<< Result: {result[0].text}")

# if __name__ == "__main__":
#     asyncio.run(test_server())

import asyncio
from fastmcp import Client
import os
from dotenv import load_dotenv
import sys

load_dotenv()

async def test_server(email_id, message):
    async with Client("http://localhost:8080/mcp") as client:
        tools = await client.list_tools()
        for tool in tools:
            print(f">>> Tool found: {tool.name}")

        # Call authenticator
        result = await client.call_tool("authenticator", {"access_key": os.getenv("DESCOPE_ACCESS_KEY")})
        print(result[0])

        # Send email
        result = await client.call_tool(
            "send_email_to_employees", 
            {"email_id": email_id, "message": message}
        )
        print(f"<<< Result: {result[0].text}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python send_email.py <email_id> <message>")
        sys.exit(1)

    email_arg = sys.argv[1]
    message_arg = sys.argv[2]

    asyncio.run(test_server(email_arg, message_arg))
