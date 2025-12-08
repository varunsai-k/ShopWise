## ORDERS AGENT TOOLS
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, ToolRuntime
from typing import Optional, Annotated, Union
import sqlite3
from datetime import datetime, timedelta
from random import randint
from langchain.messages import HumanMessage
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import io
load_dotenv()
from pydantic import BaseModel
from typing import Literal

class Product(BaseModel):
    category: Literal["Electronics","Audio","Computers","Footwear","Apparel","Printers","Wearables","Accessories","Home Appliances","Kitchen", "None"]


llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
ProductsLLM=llm.with_structured_output(Product)

DB_PATH=os.getenv("DB_PATH","ecommerce.db")
DB_PATH=f"{os.getcwd()}/{DB_PATH}"


def pil_to_bytes(pil_img, format="PNG"):
    
    buf = io.BytesIO()
    pil_img.save(buf, format=format)
    return buf.getvalue()

def handle_tool_error(e: ValueError) -> str:
    return f"Invalid input provided, {e}"

@tool
def get_order_info(orderid: str, runtime: ToolRuntime) -> dict:
    """ 

    Fetches the complete order information for a given Order ID.
    This includes the user's order details, current order status, shipping timelines, pricing information, ordered product information and the estimated number of days remaining for delivery.
    
    Returns:
    A dictionary containing:
    
    Order details (items, item details, quantity, order date, etc.)
    
    Order status (placed, packed, shipped, out for delivery, delivered, cancelled, etc.)
    
    Shipping information (shipping date, expected delivery date, transit updates)
    
    Price details (item price, taxes, discounts, total amount)

    
    Delivery estimate (remaining days to deliver the order)


    """

    
    userid = runtime.context.userid
    usernmae = runtime.context.username
    
    if not userid:
        raise ValueError("No User ID Configured.")
    if not orderid:
        raise ValueError("Order ID is not Informed.")

    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    query="""

        SELECT o.order_id, o.order_date, o.total_amount, o.status, oi.item_id, oi.quantity, oi.price, pd.brand, pd.model, pd.specifications, s.shipped_date, s.delivery_date
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN product_details pd ON pd.product_id = oi.product_id
        JOIN shipping s ON s.order_id = oi.order_id
        WHERE o.order_id = ? AND o.user_id = ?

        """
    cur.execute(query,(orderid,userid))
    rows=cur.fetchall()
    column_names = [column[0] for column in cur.description]
    results = [dict(zip(column_names, row)) for row in rows]
    cur.close()
    conn.close()
    return results

    
    
@tool
def show_all_orders(runtime: ToolRuntime) -> dict:
    """

        Retrieves a complete list of all orders associated with the user.
        
        This includes each order’s basic details, current status, shipping information, and pricing summary.
        
        Returns:
        A dictionary containing a list of all user orders, where each entry includes:
        
        Order ID
        
        Order status
        
        Order date
        
        Items and quantities
        
        Shipping details (shipping date, expected delivery date)
        
        Price summary (item total, taxes, discounts, final amount)

    """

    userid = runtime.context.userid
    usernmae = runtime.context.username
    
    if not userid:
        raise ValueError("No User ID Configured.")

    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    query="""

        SELECT o.order_id, o.order_date, o.total_amount, o.status, oi.item_id, oi.quantity, oi.price, pd.brand, pd.model, pd.specifications, s.shipped_date, s.delivery_date
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN product_details pd ON pd.product_id = oi.product_id
        JOIN shipping s ON s.order_id = oi.order_id
        WHERE o.user_id = ?

        """
    cur.execute(query,(userid,))
    rows=cur.fetchall()
    column_names = [column[0] for column in cur.description]
    results = [dict(zip(column_names, row)) for row in rows]
    cur.close()
    conn.close()
    return results

@tool
def place_order(productname: str, quantity: Optional[int]=1, *, runtime: ToolRuntime) -> str:
    """
        Creates a new order for the specified product with the given quantity. Quantity is optional by default it is one. It will updated once the 
        user sepcified quantity.
        This tool processes the order request and initiates the order placement workflow.
        
        Returns:
        A confirmation message indicating that the order has been successfully placed.
    
    """
    userid = runtime.context.userid
    usernmae = runtime.context.username
    
    if not userid:
        raise ValueError("No User ID Configured.")
    if not productname:
        return ValueError("Product Name is NOT Informed")

    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()

    orr=cur.execute("SELECT COUNT(*) FROM orders;")
    order_rows=orr.fetchone()
    oit=cur.execute("SELECT COUNT(*) FROM cart_items;")
    order_items_total=oit.fetchone()

    cur.execute("SELECT product_id, price FROM products WHERE name = ? ", (productname,))
    pid=cur.fetchone()
    product_id=pid
    if not product_id:
        
        cur.close()
        conn.close()
        
        return "No such Product to Order. Check Out some other Products"
    
    order_id=f"ORD-{str(datetime.now().year)}-0{order_rows[0]+5}"
    order_items_id=f"OIT-{str(datetime.now().year)}-0{order_items_total[0]+5}"
    shipping_id=f"SHP-{datetime.year}-0{order_items_total[0]+5}"
    order_date=str(datetime.now())
    shipped_date=str(datetime.now().date()+timedelta(randint(1,4)))
    delivery_date=str(datetime.now().date()+timedelta(randint(5,20)))
    shipping_satus="Processing"
    item_price=product_id[1]
    order_status="Processing"
    productID=product_id[0]
    total_order_price=quantity*item_price
    query1="INSERT INTO orders VALUES(?, ?, ?, ?, ?)"
    query2="INSERT INTO order_items VALUES (?, ?, ?, ?, ?)"
    query3="INSERT INTO shipping VALUES (?,?,?,?,?)"
    
    cur.execute(query1,(order_id,userid,order_date,total_order_price,order_status))
    cur.execute(query2,(order_items_id,order_id,productID, quantity, item_price))
    cur.execute(query3,(shipping_id,order_id,shipped_date,delivery_date,shipping_satus))
    conn.commit()
    cur.close()
    conn.close()
    return f"Your Order Product {productname} is Placed Successfully. Order Successfully Placed and check your order history about your product"

@tool
def cancel_order(order_id: str, runtime: ToolRuntime) -> str:
    """
        Cancels the user’s order associated with the provided Order ID.
        This tool verifies the order and processes the cancellation request.
        
        Returns:
        A confirmation message indicating whether the order was successfully canceled.
    """

    userid = runtime.context.userid
    usernmae = runtime.context.username
    
    if not userid:
        raise ValueError("No User ID Configured.")
    if not order_id:
        return ValueError("Order ID is NOT Informed")
    
    
    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    query="""

        SELECT *
        FROM orders
        WHERE order_id = ? AND user_id = ?

        """
    orr=cur.execute(query,(order_id,userid))
    order_rows=orr.fetchone()
    if not order_rows:
        cur.close()
        conn.close()
        return f"No Existing Order found for the given order id: {order_id}."
    cur.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    cur.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
    cur.execute("DELETE FROM shipping WHERE order_id = ?", (order_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return f"Order {order_id} cancelled successfully."
    
    
    

## Products Agent Tools

@tool
def get_products_based_on_category(category: str, runtime: ToolRuntime) -> dict:
    """
        Fetches all available products belonging to the specified category.
        Provides detailed product information to help the user explore items within that category.
        
        Returns:
        A dictionary containing a list of products, where each product includes:
        
        Product name
        
        Product ID
        
        Description
        
        Category
        
        Price details
        
        Availability/stock status
        
        

    """

    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    query="""

        SELECT p.name, p.category, pd.brand, pd.model, p.price,  pd.specifications, p.stock, p.description
        FROM products p
        JOIN product_details pd ON p.product_id = pd.product_id
        WHERE p.category = ?

        """
    cur.execute(query,(category,))
    rows=cur.fetchall()
    column_names = [column[0] for column in cur.description]
    results = [dict(zip(column_names, row)) for row in rows]
    cur.close()
    conn.close()
    return results

@tool
def get_product_recommendation_through_image(runtime: ToolRuntime) -> dict:

    """

        Analyzes the provided product image and identifies the most relevant product category.
        Based on the detected category, the tool returns a list of recommended products that closely match or relate to the item in the image.
        Tool automatically calls when it is related to the products recommendation related to images
        
        Returns:
        A dictionary containing:
        
        Detected product category
        
        List of recommended products, each with:
        
        Product name
        
        Product ID
        
        Description
        
        Price details
        
        Availability/stock status

    """
    state=runtime.state
    #print(state)
    image_bytes=state.image_data
    if image_bytes is None:
        return "Image not found"
    
    mime_type = "image/jpeg"
    
    product_image=ProductsLLM.invoke([HumanMessage(
        content=[{"type": "text", "text": "Describe the local image."},
        {
            "type": "image",
            "base64": image_bytes,
            "mime_type": mime_type,
        },]
    )])
    category=product_image.category

    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    query="""

        SELECT p.name, p.category, pd.brand, pd.model, p.price,  pd.specifications, p.stock, p.description
        FROM products p
        JOIN product_details pd ON p.product_id = pd.product_id
        WHERE p.category = ?

        """
    cur.execute(query,(category,))
    rows=cur.fetchall()
    column_names = [column[0] for column in cur.description]
    results = [dict(zip(column_names, row)) for row in rows]
    cur.close()
    conn.close()
    return results


# Cart Management Agent Tools

@tool
def view_cart_items(runtime: ToolRuntime) -> dict:
    """
        Fetches all items currently present in the user’s cart.
        Provides detailed information for each item along with a complete cart summary.
        
        Returns:
        A dictionary containing:
        
        List of cart items, each with:
        
        Product name
        
        Product ID
        
        Quantity
        
        Price details
        
        Subtotal
        
        Overall cart summary, including total items and total cost.
    """
    
    userid = runtime.context.userid
    usernmae = runtime.context.username
    
    if not userid:
        raise ValueError("No User ID Configured.")
        
    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    query="""

        SELECT p.name, p.category, pd.brand, pd.model, p.price,  ci.quantity, pd.specifications, p.description
        FROM cart c
        JOIN cart_items ci ON ci.cart_id = c.cart_id
        JOIN products p ON p.product_id = ci.product_id
        JOIN product_details pd ON pd.product_id = p.product_id
        WHERE c.user_id = ?

        """
    cur.execute(query,(userid,))
    rows=cur.fetchall()
    column_names = [column[0] for column in cur.description]
    results = [dict(zip(column_names, row)) for row in rows]
    cur.close()
    conn.close()
    return results

@tool
def add_product_to_cart(productname: str, quantity: Optional[int]=1,*, runtime: ToolRuntime) -> str:
    """
        Adds the specified product to the user’s cart with the given quantity. quantity is optional by default it is one if user provided then it will be updated.
        Returns:
            A confirmation message indicating that the product has been successfully added to the cart.

    """

    userid = runtime.context.userid
    username = runtime.context.username

    if not userid:
        raise ValueError("No User ID Configured.")

    if not productname:
        raise ValueError("Product Name not provided")
    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()

    cr=cur.execute("SELECT COUNT(*) FROM cart;")
    cart_rows=cr.fetchone()
    
    print(cart_rows)
    cit=cur.execute("SELECT COUNT(*) FROM cart_items;")
    cart_items_total=cit.fetchone()
    print(cart_items_total)

    cur.execute("SELECT product_id FROM products WHERE name = ? ", (productname,))
    pid=cur.fetchone()
    product_id=pid
    if not product_id:
        
        cur.close()
        conn.close()
        
        return "No such Product to Order. Check Out some other Products"

    check_product_already_exists_in_cart_query="""

    SELECT * 
    FROM cart c
    JOIN cart_items ci ON c.cart_id = ci.cart_id
    WHERE c.user_id = ? and ci.product_id = ?

    """
    cur.execute(check_product_already_exists_in_cart_query,(userid,product_id[0]))
    existing_=cur.fetchall()
    if existing_:
        cur.close()
        conn.close()
        return f"Product {productname} already in your cart"
        
    print(product_id)
    # cid=cur.execute("SELECT cart_id FROM cart WHERE user_id = ? ", (userid,))
    # cID=cid.fetchone()
    # cart_id=cID[0]
    cart_id=f"CRT-{str(datetime.now().year)}-{cart_rows[0]+5}"
    cart_user_id=userid
    cart_time_stamp=str(datetime.now())

    cart_items_id=f"CIT-{str(datetime.now().year)}-{cart_items_total[0]+5}"

    query1="INSERT INTO cart VALUES(?, ?, ?)"
    query2="INSERT INTO cart_items VALUES (?, ?, ?, ?)"

    cur.execute(query1,(cart_id,userid,cart_time_stamp))
    cur.execute(query2,(cart_items_id, cart_id, product_id[0], quantity))
    conn.commit()

    cur.close()
    conn.close()
    return f"Product {productname} added to {username}'s cart successfully."
    
@tool
def remove_product_from_cart(productname: str, runtime: ToolRuntime) -> str:
    """
        Removes the specified product from the user’s cart.
        This tool searches the cart for the given product name and deletes it if found.
        
        Returns:
        A confirmation message indicating whether the product was successfully removed from the cart

    """

    userid = runtime.context.userid
    username = runtime.context.username

    if not userid:
        raise ValueError("No User ID Configured.")

    if not productname:
        raise ValueError("Product Name not provided")
        
    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    cur.execute("SELECT product_id FROM products WHERE name = ? ", (productname,))
    pid=cur.fetchone()
    product_id=pid
    if not product_id:
        
        cur.close()
        conn.close()
        
        return "No such Product to Order. Check Out some other Products"
    query="""

        SELECT ci.item_id
        FROM cart c
        JOIN cart_items ci ON ci.cart_id = c.cart_id
        WHERE c.user_id = ? AND ci.product_id = ?

    """
    cart_item=cur.execute(query,(userid,product_id[0]))
    CartItem=cart_item.fetchone()
    if not CartItem:
        cur.close()
        conn.close()
        return f"{productname} is not available in your cart"
    cur.execute("DELETE FROM cart_items WHERE item_id = ?",(CartItem[0],))
    conn.commit()
    cur.close()
    conn.close()

    return f"Product {productname} is removed from cart successfully."
    