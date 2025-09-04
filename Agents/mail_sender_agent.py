# agent.py
import os
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from agno.models.openai import OpenAIChat

GROQ_BASE = "https://api.groq.com/openai/v1"

async def main():
    # Launch your MCP server as a subprocess via stdio
    # (adjust the command if your server file is not main.py)
    async with MCPTools(command="python mail_mcp_server/main.py", timeout_seconds=60) as mcp_tools:
        agent = Agent(
            # Pick a Groq model; example: Llama 3.3 70B versatile
            model= OpenAIChat(
                id="llama-3.3-70b-versatile",   # Groq model name
                base_url="https://api.groq.com/openai/v1",
                api_key=os.environ["GROQ_API_KEY"],
            )
,
            tools=[mcp_tools],
            markdown=True,
        )

        # Ask the agent to use your MCP tools
        prompt = (
            "send the mail to kavi22022.ad@rmkec.ac.in this mailid that he has reached the free limit of using his trial bus ticket card "
        )
        await agent.aprint_response(prompt, stream=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

