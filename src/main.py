from src.graph import MultiAgenticGraph
from langchain.messages import HumanMessage
from src.state import UserContext
from PIL import Image
from src.tools import pil_to_bytes
import base64
from fastapi import FastAPI, Body
from typing import Annotated
from uuid import uuid4
from src.utils import init_db

init_db()

thread_id=str(uuid4())
config={
    "configurable": {
                "thread_id": thread_id,
            }
}


# agentEvnets=MultiAgenticGraph.invoke({"messages":[HumanMessage(content="can you show some all my products in cart")]},
#     context=UserContext(userid="USR-2025-001", username="Aakash Sharma"),config=config)

# for event in agentEvnets["messages"]:
#     print(event.pretty_print())

app=FastAPI(title="E-Commerce MultiAgentSystem")

@app.post("/workflows/Agent/run")
async def run_agent(
    messages: Annotated[str,Body(description="User input")],
    username: Annotated[str,Body(description="Username")],
    userid: Annotated[str,Body(description="UserID")],
    file: Annotated[str|None, Body(description="For Image based recommendation")]=None 
):
    if file is not None:
        
        # data=await file.read()
        # encoded = base64.b64encode(data).decode("utf-8")
        agentEvnets=MultiAgenticGraph.invoke({"messages":[HumanMessage(content=messages)],"image_data":file},context=UserContext(userid=userid, username=username),config=config)
        response=agentEvnets["messages"][-1].content
        return {"Human":messages,"Agent":response}
    agentEvnets=MultiAgenticGraph.invoke({"messages":[HumanMessage(content=messages)]},context=UserContext(userid=userid, username=username),config=config)
    response=agentEvnets["messages"][-1].content
    return {"Human":messages,"Agent":response}

