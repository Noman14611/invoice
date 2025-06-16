import streamlit as st
from datetime import date
from invoice_logic import create_invoice_html

st.set_page_config(page_title="Invoice Generator", layout="centered")

if "items" not in st.session_state:
    st.session_state["items"] = []

st.title("🧾 Invoice Generator")

name = st.text_input("Customer Name")
address = st.text_input("Customer Address")
phone = st.text_input("Customer Phone")
invoice_date = st.date_input("Invoice Date", value=date.today())

st.subheader("Add Item")
with st.form("item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    add_btn = st.form_submit_button("Add Item")
    if add_btn:
        st.session_state["items"].append({
            "name": item_name,
            "quantity": quantity,
            "price": price
        })

if st.session_state["items"]:
    st.subheader("Items")
    for i, item in enumerate(st.session_state["items"], 1):
        st.write(f"{i}. {item['name']} — Qty: {item['quantity']}, Price: {item['price']}")

discount = st.number_input("Discount", min_value=0.0, value=0.0)
tax = st.number_input("Tax", min_value=0.0, value=0.0)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🧹 Clear All"):
        st.session_state["items"] = []

with col2:
    if st.button("✅ Generate Invoice"):
        if name and address and phone and st.session_state["items"]:
            html = create_invoice_html(
                name, address, phone, st.session_state["items"],
                discount, tax, str(invoice_date)
            )
            st.success("✅ Invoice Ready")
            st.components.v1.html(html, height=1000, scrolling=True)

            # Create download link
            st.download_button("📥 Download Invoice as HTML", html, file_name="invoice.html")
        else:
            st.error("❌ Please fill all customer fields and add at least one item.")
