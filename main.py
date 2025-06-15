import streamlit as st
from invoice_logic import create_invoice
from datetime import date

# Initialize session state
if "items" not in st.session_state:
    st.session_state["items"] = []

# Sidebar
st.sidebar.title("🧾 Invoice Generator")
st.sidebar.markdown("Fill the form to create invoice")

# Title
st.title("Customer & Product Details")

# Customer Info
name = st.text_input("Customer Name")
address = st.text_input("Customer Address")
phone = st.text_input("Customer Phone")
invoice_date = st.date_input("Invoice Date", value=date.today())

# Add Item Form
st.subheader("Add Item")
with st.form("item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    add_btn = st.form_submit_button("➕ Add Item")
    if add_btn:
        st.session_state["items"].append({
            "name": item_name,
            "quantity": quantity,
            "price": price
        })

# Show items
if st.session_state["items"]:
    st.subheader("🧺 Item List")
    for i,
