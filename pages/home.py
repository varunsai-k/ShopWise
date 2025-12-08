import streamlit as st
import time
from PIL import Image
#from streamlit.components.v1 import st_page_link, st_navigation
import os


img=Image.open(f"{os.getcwd()}/assets/chaticon3.png")
agent=Image.open(f"{os.getcwd()}/assets/MultiAgentIcon.png").resize((600,400))

# if "user_credentials" not in st.session_state:
#     st.session_state.user_credentials = None
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #277DF5 !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        margin-top: 0px;
        text-align: center;
    }
    .stButton>button:hover {
        background-color: #277DF5!important;
        color: white !important;
    }
    section[data-testid="stSidebarNav"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)
def main():
    APP_TITLE="ShopWise"
    APP_ICON=img
    title="E-Commerce Multi-Agent System"
    
    st.set_page_config(page_title=APP_TITLE,page_icon=APP_ICON)

    with st.sidebar:
        
        st.caption("Made with :material/favorite: by [Varun](https://www.linkedin.com/in/varun-sai-kanuri-089b34226/)")
    

    # with st.sidebar:
    #     st.markdown("### 📂 Navigation")
    #     st.page_link("app.py", label="🏠 Home")
    #     st.page_link("pages/guest.py", label="👤 Guest Login")
    #     st.page_link("pages/chat.py", label="💬 ShopWise")
    #     st.page_link("pages/faqs.py", label="❓ FAQs")
        
    home_title=f"💬{APP_TITLE}"
    #home_title=f"{title}"
    st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=2>Beta</font></span>""",unsafe_allow_html=True)
    st.caption("🚀 ShopWise - Your Smart AI Shopping Assistant powered by LangGraph")
    st.write(

        """

    Welcome to ****:violet[ShopWise]****, your intelligent AI shopping assistant powered by a multi-agent architecture.
    This system uses a Supervisor Agent to intelligently route user queries to specialized agents—Orders Agent, Products Agent, and Cart Agent—ensuring accurate and efficient task execution.

        """
    )

    st.image(agent)

    st.write(
        """
        It supports:
    
    - 🔍 Product Search by text, category, or uploaded image (vision-based recommendations).
    
    - 🛒 Cart Management including adding, removing, and viewing items.
    
    - 📦 Order Operations such as placing orders, cancelling, viewing all orders, and checking specific order details.
    
    The system combines tool-driven workflows, image classification, and category-matching algorithms to deliver seamless e-commerce interactions.
    
    Navigate to the ****:blue[Guest Login]**** page using the button below, choose any guest account, and start interacting with the AI-powered shopping assistant instantly.

        """)

    if st.button("Enter Guest Mode"):
        st.switch_page("pages/guest.py")

#     if "onboarding_complete" not in st.session_state:
#         st.session_state.onboarding_complete=False
#         st.session_state.user_credentials=[]

    


#     if not st.session_state.onboarding_complete:
#         col1, col2, col3 = st.columns([1,1,1], gap="large")
#         with col1:
#             st.markdown('<div class="image-container-1">', unsafe_allow_html=True)
#             st.markdown('<div class="circular-image-container">', unsafe_allow_html=True)
#             st.image(img1, use_container_width=False)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#             if st.button("Login as Tanya"):
#                 st.session_state.user_credentials = ["Tanya", 1003]
#                 st.session_state.onboarding_complete = True
#                 st.switch_page("pages/chat.py")

        
#             st.markdown('</div>', unsafe_allow_html=True)
            
            
        
#         with col2:
#             st.markdown('<div class="image-container-2">', unsafe_allow_html=True)
#             st.markdown('<div class="circular-image-container">', unsafe_allow_html=True)
#             st.image(img2, use_container_width=False)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#             if st.button("Login as Arjun"):
#                 st.session_state.user_credentials = ["Arjun", 1009]
#                 st.session_state.onboarding_complete = True

#             st.markdown('</div>', unsafe_allow_html=True)
             
        

#         with col3:
#             st.markdown('<div class="image-container-3">', unsafe_allow_html=True)
#             st.markdown('<div class="circular-image-container">', unsafe_allow_html=True)
#             st.image(img3, use_container_width=False)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#             if st.button("Login as Rahul"):
#                 st.session_state.user_credentials = ["Rahul", 1011]
#                 st.session_state.onboarding_complete = True

#             st.markdown('</div>', unsafe_allow_html=True)
#         return
                

#     # st.markdown(f"### 👋 Hello, **{"Varun"}**")
#     # st.caption("Ask anything or upload a file.")
#     # st.markdown(f"### 👋 Welcome, **{st.session_state.user_credentials}**!")
#     # #show_home_page()   # ← your home page function

# # Run app
if __name__ == "__main__":
    main()