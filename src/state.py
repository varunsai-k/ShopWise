from dataclasses import dataclass
from pydantic import BaseModel
from typing import Annotated, Optional, Literal
from langchain.messages import AnyMessage
from langgraph.graph import add_messages

class MainState(BaseModel):
    messages: Annotated[list[AnyMessage],add_messages]
    image_data: Optional[str]=None

@dataclass
class UserContext:
    userid: str
    username: str

class Product(BaseModel):
    category: Literal["Electronics","Audio","Computers","Footwear","Apparel","Printers","Wearables","Accessories","Home Appliances","Kitchen", "None"]

class SupervisorState(BaseModel):
    agent: Literal["OrdersAgent", "ProductsAgent","CartManagementAgent"]

class MainAgentState(BaseModel):
    messages: Annotated[list[AnyMessage],add_messages]
    agent: Optional[str]=None
    image_data: Optional[str]=None
