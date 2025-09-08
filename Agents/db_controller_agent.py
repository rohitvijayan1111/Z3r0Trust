from phi.agent import Agent
from phi.tools.sql import SQLTools
import os
from phi.model.groq import Groq
from dotenv import load_dotenv
from descope import DescopeClient
load_dotenv()

descope = DescopeClient(project_id=os.getenv("DESCOPE_PROJECT_ID"))


def db_controller_agent(prompt,access_key):
    token = descope.exchange_access_key(access_key=access_key).get('sessionToken', {}).get('jwt')
    if not token:
        return "Access Key Not Valid"
    "This agent only do the modification in the database, but not fetch and show anything, it is for purpose"
    model_id=os.getenv("GROQ_MODEL_1")
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    db_url = "mysql+pymysql://root:ZeroTrust%40123@34.93.101.129:3306/zerotrust"

    agent = Agent(
        name="DB agent",
        role="Connect and do operations with mysql database",
        model=Groq(id=model_id, api_key=groq_api_key),
        tools=[SQLTools(db_url=db_url)],
        markdown=True
        )

    agent.print_response(prompt)
    return "statues from DBController : Successfully executed"