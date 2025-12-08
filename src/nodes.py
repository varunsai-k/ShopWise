from langgraph.prebuilt import ToolNode, ToolRuntime
from langgraph.runtime import Runtime
from src.state import MainAgentState, UserContext
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from src.prompts import SupervisorPrompt
from src.llms import SupervisorLLM
from langgraph.graph import START, StateGraph, END
from src.agents.OrdersAgent import OrdersGraph
from src.agents.ProductsAgent import ProductsGraph
from src.agents.CartManagementAgent import CartGraph
from typing import Literal, Optional, Union
from langchain_core.runnables.config import RunnableConfig


def Supervisor(state: MainAgentState, runtime: Runtime[UserContext]):
    last_message=state.messages[-1].content
    decision=SupervisorLLM.invoke(SupervisorPrompt.format(last_message))
    agent=decision.agent
    state.agent=agent
    print(f"CALLING AGENT: {agent}")
    return state


def router(state: MainAgentState, runtime: Runtime[UserContext]) -> Literal["OrdersAgent", "ProductsAgent","CartManagementAgent", END]:
    if state.agent:
        return state.agent
    return END


def SubOrdersAgent(state: MainAgentState, runtime: Runtime[UserContext], config: RunnableConfig):
    uid=runtime.context.userid
    uname=runtime.context.username
    print(runtime.context)
    # config = runtime.get_config()
    print(config)
    last_message=state.messages[-1].content
    order_events=OrdersGraph.invoke({"messages":[HumanMessage(content=last_message)]},
    context=UserContext(userid=uid, username=uname),config=config)
    response=order_events["messages"][-1]
    return {"messages":response}

def SubProductsAgent(state: MainAgentState, runtime: Runtime[UserContext], config: RunnableConfig):
    uid=runtime.context.userid
    uname=runtime.context.username
    print(runtime.context)
    #config = runtime.get_config()
    print(config)
    last_message=state.messages[-1].content
    img_bytes=state.image_data
    product_events=ProductsGraph.invoke({"messages":[HumanMessage(content=last_message)],"image_data":img_bytes},
    context=UserContext(userid=uid, username=uname),config=config)
    response=product_events["messages"][-1]
    return {"messages":response}

def SubCartAgent(state: MainAgentState, runtime: Runtime[UserContext], config: RunnableConfig):
    uid=runtime.context.userid
    uname=runtime.context.username
    #config = runtime.get_config()
    print(config)
    last_message=state.messages[-1].content
    print(last_message)
    cart_events=CartGraph.invoke({"messages":[HumanMessage(content=last_message)]},
    context=UserContext(userid=uid, username=uname),config=config)
    print(cart_events)
    response=cart_events["messages"][-1]
    print(response)
    return {"messages":response}