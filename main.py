import streamlit as st
from invoice_logic import create_invoice, save_invoice
from datetime import date

st.set_page_config(page_title="📄 Invoice Maker", layout="wide")
st.title("📄 Invoice Maker by Nomi")

# Sidebar Customer Info
st.sidebar.header("👤 Customer Info")
name = st.sidebar.text_input("Name")
address = st.sidebar.text_area("Address")
phone = st.sidebar.text_input("Phone")

# Items Table
st.subheader("🛒 Items")
items = []
num = st.number_input("Number of items", 1, 30, 1)

for i in range(num):
    with st.expander(f"Item {i+1}"):
        item = st.text_input(f"Item Name {i+1}", key=f"name{i}")
        qty = st.number_input(f"Quantity", 1.0, 1000.0, 1.0, key=f"qty{i}")
        price = st.number_input(f"Unit Price", 0.0, 100000.0, 0.0, key=f"price{i}")
        items.append({"name": item, "quantity": qty, "price": price})

discount = st.number_input("Discount (%)", 0.0, 100.0, 0.0)
tax = st.number_input("Tax (%)", 0.0, 100.0, 0.0)
invoice_date = st.date_input("Invoice Date", date.today())

# Generate Invoice
if st.button("📥 Generate Invoice"):
    invoice = create_invoice(name, address, phone, items, discount, tax, invoice_date)
    save_invoice(invoice)

    st.success(f"Invoice #{invoice['invoice_no']} created successfully!")

    st.download_button(
        label="📄 Download PDF",
        data=invoice["pdf_bytes"],
        file_name=f"Invoice_{invoice['invoice_no']}.pdf",
        mime="application/pdf"
    )
