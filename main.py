# main.py
import streamlit as st
from invoice_logic import create_invoice_html
from datetime import date

# Initialize session state
def reset_all():
    st.session_state["name"] = ""
    st.session_state["address"] = ""
    st.session_state["phone"] = ""
    st.session_state["items"] = []
    st.session_state["discount"] = 0.0
    st.session_state["tax"] = 0.0

if "items" not in st.session_state:
    reset_all()

st.set_page_config(page_title="Invoice Generator", layout="centered")
st.title("🧾 Invoice Generator")

st.text_input("Customer Name", key="name")
st.text_input("Customer Address", key="address")
st.text_input("Customer Phone", key="phone")
invoice_date = st.date_input("Invoice Date", value=date.today())

st.subheader("Add Item")
with st.form("item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    add_btn = st.form_submit_button("Add Item")
    if add_btn:
        if item_name.strip() != "":
            st.session_state["items"].append({
                "name": item_name,
                "quantity": quantity,
                "price": price
            })
        else:
            st.warning("⚠️ Item name is required.")

if st.session_state["items"]:
    st.subheader("Items List")
    for i, item in enumerate(st.session_state["items"], 1):
        st.write(f"{i}. {item['name']} — Qty: {item['quantity']}, Price: {item['price']}")

discount = st.number_input("Discount", min_value=0.0, value=st.session_state.get("discount", 0.0), key="discount")
tax = st.number_input("Tax", min_value=0.0, value=st.session_state.get("tax", 0.0), key="tax")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧹 Clear All Shopping"):
        st.session_state["items"] = []
        st.rerun()

with col2:
    if st.button("🧹 Clear All Info"):
        reset_all()
        st.rerun()

with col3:
    if st.button("✅ Generate Invoice"):
        if st.session_state["name"] and st.session_state["address"] and st.session_state["phone"] and st.session_state["items"]:
            html = create_invoice_html(
                name=st.session_state["name"],
                address=st.session_state["address"],
                phone=st.session_state["phone"],
                items=st.session_state["items"],
                discount=st.session_state["discount"],
                tax=st.session_state["tax"],
                invoice_date=str(invoice_date)
            )
            st.success("✅ Invoice Ready. You can print or save it.")
            st.markdown('<button onclick="window.print()">🖨️ Print / Save Invoice</button><br><br>', unsafe_allow_html=True)
            st.components.v1.html(html, height=1000, scrolling=True)
        else:
            st.error("❌ Please fill all customer fields and add at least one item.")
