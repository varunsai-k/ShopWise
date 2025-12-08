import streamlit as st
from PIL import Image
import os
APP_TITLE="ShopWise"

APP_ICON=Image.open(f"{os.getcwd()}/assets/chaticon3.png")

st.set_page_config(page_title=APP_TITLE,page_icon=APP_ICON)

with st.sidebar:
    # st.markdown("### 📂 Navigation")
    # st.page_link("app.py", label="🏠 Home")
    # st.page_link("pages/guest.py", label="👤 Guest Login")
    # st.page_link("pages/chat.py", label="💬 ShopWise")
    # st.page_link("pages/faqs.py", label="❓ FAQs")
        
    st.caption("Made with :material/favorite: by [Varun](https://www.linkedin.com/in/varun-sai-kanuri-089b34226/)")

st.markdown("#### FAQs")
with st.expander("1. 🛍️ What is ShopWise?", expanded=False):
    st.markdown("""
        **ShopWise** is an AI-driven e-commerce assistant that helps you ***discover products, get image-based recommendations, manage your cart, and handle orders*** through natural language.It acts as a smart conversational shopping companion, offering fast, accurate, and personalized support.
    
    """)


with st.expander("🚀 How do I get started with ShopWise?"):
    st.markdown("""
Click the **Guest Login** button, select any available guest account, and begin using the assistant. No registration, setup, or authentication required.""")

with st.expander("💡 What example prompts can I use?"):
    st.markdown("""

    Here are some prompts to help you get started:

    📦 Order Management
        
        “Show me a list of all my orders.”
        
        “What’s the status of my order with ID <ORDER ID>?”
        
        “Please cancel my order with ID <ORDER ID>.”
        
        “I want to order 2 units of the iPhone 15.”
        
    🛒 Cart Management
    
        “What items are currently in my cart?”
        
        “Add/remove <PRODUCT NAME> to/from my cart.”
    
    🔍 Product Discovery
    
            
        “Show me products related to the Electronics category.”
        
        “Recommend products based on this image.” (Upload picture)
        
    Supported Product Categories:
        
        Electronics, Audio, Computers, Footwear, Apparel, Printers, Wearables, Accessories, Home Appliances, Kitchen.
    
    
    """)

with st.expander("How do image-based recommendations work?"):
    st.markdown("Upload any product image, and ShopWise will analyze it using vision-based models to recommend similar or related items based on category, features, and appearance.")

with st.expander("💸 Is ShopWise free to use?"):
    st.markdown("""Yes! **ShopWise is 100% free to use**.
Just log in as a guest and start exploring all features instantly.""")

with st.expander("Which language model does ShopWise use?"):
    st.markdown("""ShopWise currently uses Gemini-2.5-Flash as its primary Large Language Model to understand queries, reason about tasks, and coordinate agent behavior.""")

with st.expander("🧠 How is ShopWise built?"):
    st.markdown("""

ShopWise is powered by a multi-agent architecture using LangGraph and LangChain.
A Supervisor Agent understands your query and routes it to the right specialist—Products, Orders, or Cart.

It is built using:

    ⚙️ LangGraph (agent orchestration)
    
    🧩 LangChain (tools + reasoning)
    
    🚀 FastAPI (backend services)
    
    💻 Streamlit (interactive UI)
    
    📦 Docker (deployment)
    
    🖼️ Vision Models (image-based product analysis)

This modular design ensures speed, reliability, and seamless end-to-end interactions.
    
    """)

    