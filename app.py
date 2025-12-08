import streamlit as st
from PIL import Image
import os
# st.write(os.listdir())
# st.write(os.getcwd())

img=Image.open(rf"{os.getcwd()}/assets/chaticon3.png")
st.set_page_config(page_title="ShopWise", page_icon=img)

page1 = st.Page("pages/home.py",title="🏠 Home")
page2 = st.Page("pages/guest.py", title="👤 Guest Login")
page3 = st.Page("pages/chat.py", title="💬 ShopWise")
page4 = st.Page("pages/faqs.py", title="❓ FAQs")


# Create the navigation structure (this replaces the default)
# To hide it completely, just don't put it in a sidebar or build the menu
my_nav = st.navigation([page1, page2, page3,page4])

# Run the navigation - this hides the default menu if not placed in a sidebar
     # Or run_with_sidebar() if you want the menu in the sidebar

my_nav.run()