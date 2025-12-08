import streamlit as st
from PIL import Image
import os

API_BASE = os.getenv("API_URL", "http://127.0.0.1:8000")
img=Image.open(f"{os.getcwd()}/assets/chaticon3.png")
img1 = f"{os.getcwd()}/assets/women__1.jpg"
img2 = f"{os.getcwd()}/assets/men__5.jpg"
img3 = f"{os.getcwd()}/assets/men__6.jpg"
agent=Image.open(f"{os.getcwd()}/assets/boticon.png")
userimg=img1
APP_TITLE="ShopWise"
APP_ICON=img
import uuid
import base64
import io
import requests

st.set_page_config(page_title=APP_TITLE,page_icon=APP_ICON)
title="E-Commerce Multi-Agent System"

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
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    # st.markdown("### 📂 Navigation")
    # st.page_link("app.py", label="🏠 Home")
    # st.page_link("pages/guest.py", label="👤 Guest Login")
    # st.page_link("pages/chat.py", label="💬 ShopWise")
    # st.page_link("pages/faqs.py", label="❓ FAQs")
        
    
    
    #     st.header(f"{APP_ICON} {APP_TITLE}")
    #     "Assists users with product inquiries, order tracking, and support on e-commerce platforms. Built with Langgraph and Streamlit." 
    with st.popover(":material/settings: Settings", use_container_width=True):
            st.markdown("Settings")
            option = st.selectbox("Select Model",("gemini-2.5-flash","gemini-1.5-flash"),)
            temp = st.slider("Temparature", 0.0, 1.0,0.1)
            # api_key=st.text_input("Your Google API Key",type="password")
            # "Don't have an API key? No worries! Create one [here](https://makersuite.google.com/app/apikey)."
        
    uploaded_file = st.file_uploader("Upload image for product recommendations", accept_multiple_files=False,type=["jpg", "jpeg", "png"])
    if uploaded_file:
        uploadedimg = Image.open(uploaded_file)

        # Resize image (keep aspect ratio)
        max_width = 200  # Sidebar width is small, this is perfect
        uploadedimg = uploadedimg.resize((max_width, 200))
        st.sidebar.image(uploadedimg, caption="Uploaded Image 📷", use_container_width=False)
    if st.button("Clear Chat History"):
        st.session_state.messages.clear()     
    st.caption("Made with :material/favorite: by [Varun](https://www.linkedin.com/in/varun-sai-kanuri-089b34226/)")


home_title=f"💬{APP_TITLE}"
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=2>Beta</font></span>""",unsafe_allow_html=True)
st.caption("🚀 Your Smart AI Shopping Assistant powered by LangGraph")

if "messages" not in st.session_state or st.session_state.messages==[]:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
try:
    user_data=st.session_state.user_credentials
    print(f"User Data: {user_data}")
    print(f"Length: {len(user_data)}")

    if user_data is not None:
        if user_data[0]=="Sanya Mehta":
            userimg=Image.open(img1)
        elif user_data[0]=="Aakash Sharma":
            userimg=Image.open(img2)
        else:
            userimg=Image.open(img3)
            
except:
    st.info("Please log in as a guest to start chatting with ShopWise and explore all its features! 😊")
    st.stop()
    
for msg in st.session_state.messages:
    #st.chat_message(msg["role"]).write(msg["content"])
    if msg["role"]=="assistant":
        
        st.chat_message(msg["role"],avatar=agent).write(msg['content'])
                    
    else:
        
        st.chat_message(msg["role"],avatar=userimg).write(msg['content']) 

if prompt := st.chat_input():
    
    if user_data:
        thread_id = str(uuid.uuid4())
        username=user_data[0]
        userid=user_data[1]
        # config = {
        #     "configurable": {
        #         "CustomerName":username,
        #         "CustomerID": userid,
        #         "thread_id": thread_id,
        #     }
        # }   
        data = {
            "messages":prompt,
            "username":username,
            "userid":userid
        }
        if uploaded_file:
            bytes_data = uploaded_file.getvalue()
          
            img_b64 = base64.b64encode(bytes_data).decode()
            data={**data,"file":img_b64}
            
        # Sending the POST request
        response = requests.post(f"{API_BASE}/workflows/Agent/run", json=data)
        # st.write(os.getcwd())
        # st.write("STATUS:", response.status_code)
        # st.write("RAW RESPONSE:", response.text)
        output = response.json()
        msg=output["Agent"]
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user",avatar=userimg).write(prompt)

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant",avatar=agent).write(msg)
    else:
        st.info("To start using Shoppy, please provide your Google API key in the Settings section. 😊")
        st.stop()
