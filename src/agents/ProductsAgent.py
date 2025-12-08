from langgraph.graph import StateGraph, START, END
from typing import Literal, Optional, Annotated, Union
from src.state import MainState, UserContext
from langgraph.prebuilt import ToolNode, ToolRuntime
from langgraph.runtime import Runtime
from src.llms import ProductsAgentLLM, memory
from src.prompts import ProductsAgentPrompt
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from src.tools import get_order_info, show_all_orders, place_order, cancel_order, get_products_based_on_category, get_product_recommendation_through_image, view_cart_items, add_product_to_cart,remove_product_from_cart 

def ProductsAgentNode(state: MainState, runtime: Runtime[UserContext]):
    uname=runtime.context.username
    
    response=ProductsAgentLLM.invoke(

        [
            SystemMessage(content=ProductsAgentPrompt.format(uname))
        ] + state.messages
    )
    if isinstance(response.content,list):
        if "text" in response.content[0]:
            return {"messages":AIMessage(content=response.content[0]["text"])}
        return {"messages":AIMessage(content="")}
    return {"messages":response}



         

def handle_tool_error(e: ValueError) -> str:
    return f"Invalid input provided, {e}"

products_tool_node=ToolNode([get_products_based_on_category,get_product_recommendation_through_image], handle_tool_errors=handle_tool_error)

def product_tools_condition(state: MainState) -> Literal["ProductsAgent",END]:
    if state.messages[-1].tool_calls:
        return "ProductAgentTools"
    return END


products_Workflow=StateGraph(MainState, context_schema=UserContext)
products_Workflow.add_node("ProductsAgent",ProductsAgentNode)
products_Workflow.add_node("ProductAgentTools",products_tool_node)
products_Workflow.add_edge(START,"ProductsAgent")
products_Workflow.add_conditional_edges("ProductsAgent",product_tools_condition,["ProductAgentTools",END])
products_Workflow.add_edge("ProductAgentTools","ProductsAgent")
products_Workflow.add_edge("ProductsAgent",END)

ProductsGraph=products_Workflow.compile(checkpointer=memory)
#display(Image(ProductsGraph.get_graph().draw_mermaid_png()))