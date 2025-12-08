from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from src.state import Product, SupervisorState
from src.tools import get_order_info, show_all_orders, place_order, cancel_order, get_products_based_on_category, get_product_recommendation_through_image, view_cart_items, add_product_to_cart,remove_product_from_cart
from langgraph.checkpoint.memory import MemorySaver
from uuid import uuid4
load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
ProductsLLM=llm.with_structured_output(Product)
OrdersAgentLLM=llm.bind_tools([get_order_info, show_all_orders, place_order, cancel_order])
ProductsAgentLLM=llm.bind_tools([get_products_based_on_category, get_product_recommendation_through_image])
CartAgentLLM=llm.bind_tools([view_cart_items,add_product_to_cart,remove_product_from_cart])
SupervisorLLM=llm.with_structured_output(SupervisorState)
memory=MemorySaver()
thread_id=str(uuid4())

config={
    "configurable": {
                "thread_id": thread_id,
            }
}

