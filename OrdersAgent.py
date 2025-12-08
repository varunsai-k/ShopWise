from langgraph.graph import StateGraph, START, END
from typing import Literal, Optional, Annotated, Union
from src.state import MainState, UserContext
from langgraph.prebuilt import ToolNode, ToolRuntime
from langgraph.runtime import Runtime
from src.llms import OrdersAgentLLM, memory
from src.prompts import OrderAgentPrompt
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from src.tools import get_order_info, show_all_orders, place_order, cancel_order, get_products_based_on_category, get_product_recommendation_through_image, view_cart_items, add_product_to_cart,remove_product_from_cart 


def OrdersAgentNode(state: MainState, runtime: Runtime[UserContext]):
    uname=runtime.context.username
    
    response=OrdersAgentLLM.invoke(

        [
            SystemMessage(content=OrderAgentPrompt.format(uname))
        ] + state.messages
    )
    if isinstance(response.content,list):
        if "text" in response.content[0]:
            return {"messages":AIMessage(content=response.content[0]["text"])}
        return {"messages":AIMessage(content="")}
    return {"messages":response}



         

def handle_tool_error(e: ValueError) -> str:
    return f"Invalid input provided, {e}"

orders_tool_node=ToolNode([get_order_info, show_all_orders, place_order, cancel_order], handle_tool_errors=handle_tool_error)

def OrdersAgentToolsCondition(state: MainState) -> Literal["OrdersAgentTools",END]:
    if state.messages[-1].tool_calls:
        return "OrdersAgentTools"
    return END

OrdersWorkflow=StateGraph(MainState, context_schema=UserContext)
OrdersWorkflow.add_node("OrdersAgent",OrdersAgentNode)
OrdersWorkflow.add_node("OrdersAgentTools",orders_tool_node)
OrdersWorkflow.add_edge(START,"OrdersAgent")
OrdersWorkflow.add_conditional_edges("OrdersAgent",OrdersAgentToolsCondition,["OrdersAgentTools",END])
OrdersWorkflow.add_edge("OrdersAgentTools","OrdersAgent")
OrdersWorkflow.add_edge("OrdersAgent",END)

OrdersGraph=OrdersWorkflow.compile(checkpointer=memory)

#display(Image(OrdersGraph.get_graph().draw_mermaid_png()))