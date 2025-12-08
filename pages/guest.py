import streamlit as st
from PIL import Image
import os
img=Image.open(f"{os.getcwd()}/assets/chaticon3.png")
img1 = f"{os.getcwd()}/assets/women__1.jpg"

img2 = f"{os.getcwd()}/assets/men__5.jpg"
img3 = f"{os.getcwd()}/assets/men__6.jpg"
st.markdown(
    """
    <style>
    .container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .image-container-1, .image-container-2, .image-container-3 {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .circular-image-container {
        width: 10px; 
        height: 10px;
        overflow: hidden;
        border-radius: 10%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .circular-image {
        border-radius: 10%;
        width: 60px;
        height: 60px;
        object-fit: cover;
    }
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
        

    home_title=f"{title}"
    home_title=f"💬{APP_TITLE}"
    st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=2>Beta</font></span>""",unsafe_allow_html=True)
    st.caption("🚀 Your Smart AI Shopping Assistant powered by LangGraph")
    st.write("""
    Explore the E-Commerce Multi-Agent System instantly using our pre-configured guest accounts.
    No signup or authentication required—simply choose a guest profile and start interacting with the AI-powered shopping assistant.
    
    Each guest account comes with its own sample products, cart items, and order history, allowing you to experience the full workflow, including:
    
    - 🔍 Product search & recommendations
    
    - 🛒 Cart management
    
    - 📦 Placing and cancelling orders
    
    - 📄 Viewing all orders or specific order details
    
    Select any guest user below and begin using the system within seconds.
    
    This mode is ideal for demo, testing, and quick exploration of all multi-agent capabilities.
    
    """)
    
    if "onboarding_complete" not in st.session_state:
        st.session_state.onboarding_complete=False
        st.session_state.user_credentials=[]

    


    if not st.session_state.onboarding_complete:
        col1, col2, col3 = st.columns([1,1,1], gap="large")
        with col1:
            st.markdown('<div class="image-container-1">', unsafe_allow_html=True)
            st.markdown('<div class="circular-image-container">', unsafe_allow_html=True)
            st.image(img1, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
        
            if st.button("Login as Sanya"):
                st.session_state.user_credentials = ["Sanya Mehta", "USR-2025-009"]
                st.session_state.onboarding_complete = True
                st.switch_page("pages/chat.py")

        
            st.markdown('</div>', unsafe_allow_html=True)
            
            
        
        with col2:
            st.markdown('<div class="image-container-2">', unsafe_allow_html=True)
            st.markdown('<div class="circular-image-container">', unsafe_allow_html=True)
            st.image(img2, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
        
            if st.button("Login as Aakash"):
                st.session_state.user_credentials = ["Aakash Sharma", "USR-2025-001"]
                st.session_state.onboarding_complete = True
                st.switch_page("pages/chat.py")

            st.markdown('</div>', unsafe_allow_html=True)
             
        

        with col3:
            st.markdown('<div class="image-container-3">', unsafe_allow_html=True)
            st.markdown('<div class="circular-image-container">', unsafe_allow_html=True)
            st.image(img3, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
        
            if st.button("Login as Rahul"):
                st.session_state.user_credentials = ["Rahul Verma", "USR-2025-003"]
                st.session_state.onboarding_complete = True
                st.switch_page("pages/chat.py")

            st.markdown('</div>', unsafe_allow_html=True)
        return
                

    st.stop()
# Run app
if __name__ == "__main__":
    main()