import streamlit as st
from datetime import date
from invoice_logic import create_invoice_html, save_invoice_pdf

# Session state initialize
for key in ["name", "address", "phone", "items"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "items" else []

st.set_page_config(page_title="Invoice Generator", layout="centered")
st.title("🧾 Invoice Generator")

# Customer info
st.session_state["name"] = st.text_input("Customer Name", st.session_state["name"])
st.session_state["address"] = st.text_input("Customer Address", st.session_state["address"])
st.session_state["phone"] = st.text_input("Customer Phone", st.session_state["phone"])
invoice_date = st.date_input("Invoice Date", value=date.today())

# Add item form
st.subheader("Add Item")
with st.form("item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    add_btn = st.form_submit_button("Add")
    if add_btn and item_name:
        st.session_state["items"].append({
            "name": item_name,
            "quantity": quantity,
            "price": price
        })

# Display items
if st.session_state["items"]:
    st.subheader("Items")
    for i, item in enumerate(st.session_state["items"], 1):
        st.write(f"{i}. {item['name']} — Qty: {item['quantity']}, Price: {item['price']}")

# Discount and Tax
discount = st.number_input("Discount", min_value=0.0, value=0.0)
tax = st.number_input("Tax", min_value=0.0, value=0.0)

# Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🧹 Clear All"):
        for k in ["name", "address", "phone", "items"]:
            st.session_state[k] = "" if k != "items" else []

with col2:
    if st.button("✅ Generate Invoice"):
        if all([st.session_state["name"], st.session_state["address"], st.session_state["phone"], st.session_state["items"]]):
            html = create_invoice_html(
                name=st.session_state["name"],
                address=st.session_state["address"],
                phone=st.session_state["phone"],
                items=st.session_state["items"],
                discount=discount,
                tax=tax,
                invoice_date=str(invoice_date)
            )
            pdf_file = save_invoice_pdf(html)
            st.success("✅ Invoice Generated")
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download Invoice", data=f, file_name="invoice.pdf", mime="application/pdf")
        else:
            st.error("❌ Please fill all customer fields and add at least one item.")
