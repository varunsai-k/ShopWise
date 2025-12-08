from langgraph.graph import StateGraph, START, END
from typing import Literal, Optional, Annotated, Union
from src.state import MainState, UserContext
from langgraph.prebuilt import ToolNode, ToolRuntime
from langgraph.runtime import Runtime
from src.llms import CartAgentLLM, memory
from src.prompts import CartManagementAgentPrompt
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from src.tools import get_order_info, show_all_orders, place_order, cancel_order, get_products_based_on_category, get_product_recommendation_through_image, view_cart_items, add_product_to_cart,remove_product_from_cart, handle_tool_error

def CartManagementAgentNode(state: MainState, runtime: Runtime[UserContext]):
    uname=runtime.context.username
    
    response=CartAgentLLM.invoke(

        [
            SystemMessage(content=CartManagementAgentPrompt.format(uname))
        ] + state.messages
    )
    if isinstance(response.content,list):
        if "text" in response.content[0]:
            return {"messages":AIMessage(content=response.content[0]["text"])}
        return {"messages":AIMessage(content="")}
    return {"messages":response}


cart_tools_node=ToolNode([view_cart_items,add_product_to_cart,remove_product_from_cart], handle_tool_errors=handle_tool_error)

def cart_tools_condition(state: MainState) -> Literal["CartManagementAgent",END]:
    if state.messages[-1].tool_calls:
        return "CartTools"
    return END 
    
cart_Workflow=StateGraph(MainState, context_schema=UserContext)
cart_Workflow.add_node("CartManagementAgent",CartManagementAgentNode)
cart_Workflow.add_node("CartTools",cart_tools_node)
cart_Workflow.add_edge(START,"CartManagementAgent")
cart_Workflow.add_conditional_edges("CartManagementAgent",cart_tools_condition,["CartTools",END])
cart_Workflow.add_edge("CartTools","CartManagementAgent")
cart_Workflow.add_edge("CartManagementAgent",END)

CartGraph=cart_Workflow.compile(checkpointer=memory)
#display(Image(CartGraph.get_graph().draw_mermaid_png()))