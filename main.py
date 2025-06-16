import streamlit as st
from invoice_logic import create_invoice_html
from datetime import date
from weasyprint import HTML
import tempfile
import os

# Initialize session state
if "items" not in st.session_state:
    st.session_state["items"] = []

st.set_page_config(page_title="Invoice Generator", layout="centered")
st.sidebar.title("🧾 Invoice Generator")
st.sidebar.markdown("Fill the form to create invoice")

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
    for i, item in enumerate(st.session_state["items"], 1):
        st.write(f"{i}. {item['name']} — Qty: {item['quantity']}, Price: {item['price']}")

# Discount & Tax
discount = st.number_input("Discount", min_value=0.0, value=0.0)
tax = st.number_input("Tax", min_value=0.0, value=0.0)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🧹 Clear All Shopping"):
        st.session_state["items"] = []
        st.experimental_rerun()

with col2:
    if st.button("✅ Generate Invoice"):
        if name and address and phone and st.session_state["items"]:
            html = create_invoice_html(
                name=name,
                address=address,
                phone=phone,
                items=st.session_state["items"],
                discount=discount,
                tax=tax,
                invoice_date=str(invoice_date)
            )

            # Save PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                HTML(string=html).write_pdf(tmp_file.name)
                pdf_path = tmp_file.name

            st.success("✅ Invoice Generated Successfully!")
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Invoice PDF", f, file_name="invoice.pdf", mime="application/pdf")
            
            st.markdown('<br><button onclick="window.print()">🖨️ Print Invoice</button>', unsafe_allow_html=True)
            st.components.v1.html(html, height=1000, scrolling=True)

        else:
            st.error("❌ Please fill all customer fields and add at least one item.")
