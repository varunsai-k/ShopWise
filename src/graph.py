from langgraph.graph import StateGraph, START, END
from src.state import MainAgentState, UserContext
from src.nodes import SubCartAgent, SubOrdersAgent, SubProductsAgent, Supervisor, router
from src.llms import memory 

MultiAgentWorkflow=StateGraph(MainAgentState, context_schema=UserContext)
MultiAgentWorkflow.add_node("Supervisor",Supervisor)
MultiAgentWorkflow.add_node("OrdersAgent",SubOrdersAgent)
MultiAgentWorkflow.add_node("ProductsAgent",SubProductsAgent)
MultiAgentWorkflow.add_node("CartManagementAgent",SubCartAgent)
MultiAgentWorkflow.add_edge(START,"Supervisor")
MultiAgentWorkflow.add_conditional_edges("Supervisor",router, ["OrdersAgent", "ProductsAgent","CartManagementAgent",END])
MultiAgentWorkflow.add_edge("OrdersAgent",END)
MultiAgentWorkflow.add_edge("ProductsAgent",END)
MultiAgentWorkflow.add_edge("CartManagementAgent",END)
MultiAgentWorkflow.add_edge("Supervisor",END)
MultiAgenticGraph=MultiAgentWorkflow.compile()
# display(Image(MultiAgenticGraph.get_graph().draw_mermaid_png()))