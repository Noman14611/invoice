import streamlit as st
from datetime import date
from invoice_logic import create_invoice_html

# --- Initialize Session State ---
if "name" not in st.session_state:
    st.session_state["name"] = ""
if "address" not in st.session_state:
    st.session_state["address"] = ""
if "phone" not in st.session_state:
    st.session_state["phone"] = ""
if "items" not in st.session_state:
    st.session_state["items"] = []
if "discount" not in st.session_state:
    st.session_state["discount"] = 0.0
if "tax" not in st.session_state:
    st.session_state["tax"] = 0.0

# --- Reset Functions ---
def reset_items():
    st.session_state["items"] = []
    st.rerun()

def reset_all():
    st.session_state["name"] = ""
    st.session_state["address"] = ""
    st.session_state["phone"] = ""
    st.session_state["items"] = []
    st.session_state["discount"] = 0.0
    st.session_state["tax"] = 0.0
    st.rerun()

# --- UI ---
st.set_page_config(page_title="Invoice Generator", layout="centered")
st.title("🧾 Invoice Generator")

# Customer Inputs
st.session_state["name"] = st.text_input("Customer Name", value=st.session_state["name"])
st.session_state["address"] = st.text_input("Customer Address", value=st.session_state["address"])
st.session_state["phone"] = st.text_input("Customer Phone", value=st.session_state["phone"])
invoice_date = st.date_input("Invoice Date", value=date.today())

# Add Item Form
st.subheader("Add Item")
with st.form("item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    add_btn = st.form_submit_button("Add Item")
    if add_btn:
        if item_name.strip():
            st.session_state["items"].append({
                "name": item_name,
                "quantity": quantity,
                "price": price
            })
        else:
            st.warning("⚠️ Item Name cannot be empty.")

# Show Items List
if st.session_state["items"]:
    st.subheader("Items List")
    for i, item in enumerate(st.session_state["items"], 1):
        st.write(f"{i}. {item['name']} — Qty: {item['quantity']}, Price: {item['price']}")

# Discount & Tax
st.session_state["discount"] = st.number_input("Discount", min_value=0.0, value=st.session_state["discount"])
st.session_state["tax"] = st.number_input("Tax", min_value=0.0, value=st.session_state["tax"])

# Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🧹 Clear Items"):
        reset_items()

with col2:
    if st.button("♻️ Clear All Info"):
        reset_all()

with col3:
    if st.button("✅ Generate Invoice"):
        name = st.session_state["name"].strip()
        address = st.session_state["address"].strip()
        phone = st.session_state["phone"].strip()
        items = st.session_state["items"]

        if name and address and phone and items:
            html = create_invoice_html(
                name=name,
                address=address,
                phone=phone,
                items=items,
                discount=st.session_state["discount"],
                tax=st.session_state["tax"],
                invoice_date=str(invoice_date)
            )
            st.success("✅ Invoice Ready. You can print or save it.")
            st.markdown('<button onclick="window.print()">🖨️ Print / Save Invoice</button><br><br>', unsafe_allow_html=True)
            st.components.v1.html(html, height=1000, scrolling=True)
        else:
            st.error("❌ Please fill all customer fields and add at least one item.")
