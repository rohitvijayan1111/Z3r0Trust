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

        result = await client.call_tool("send_email_to_employees", {"email_id":"diva22022.it@rmkec.ac.in", "message":"tomorrow is declared as an holiday for exam preparation, send this mail to diva22022.it@rmkec.ac.in"})
        print(f"<<< Result: {result[0].text}")

if __name__ == "__main__":
    asyncio.run(test_server())

