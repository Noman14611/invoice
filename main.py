import streamlit as st
from invoice_logic import create_invoice, load_invoices, save_invoice
from datetime import date

st.set_page_config(page_title="Invoice Maker", layout="wide")
st.title("📄 Invoice Maker Software")

st.sidebar.header("Customer Info")
customer_name = st.sidebar.text_input("Customer Name")
customer_address = st.sidebar.text_area("Customer Address")
customer_phone = st.sidebar.text_input("Phone Number")

st.subheader("🛒 Items")
items = []
num_items = st.number_input("How many items?", 1, 50, 1)

for i in range(num_items):
    with st.expander(f"Item {i+1}"):
        name = st.text_input(f"Item Name {i+1}", key=f"name_{i}")
        qty = st.number_input(f"Quantity {i+1}", 1.0, 10000.0, key=f"qty_{i}")
        price = st.number_input(f"Price per unit {i+1}", 0.0, 100000.0, key=f"price_{i}")
        items.append({"name": name, "quantity": qty, "price": price})

discount = st.number_input("Discount (%)", 0.0, 100.0, 0.0)
tax = st.number_input("Tax (%)", 0.0, 100.0, 0.0)
invoice_date = st.date_input("Invoice Date", date.today())

if st.button("📥 Generate Invoice"):
    invoice = create_invoice(customer_name, customer_address, customer_phone, items, discount, tax, invoice_date)
    save_invoice(invoice)
    st.success(f"Invoice #{invoice['invoice_no']} created successfully!")
    st.download_button("Download Invoice PDF", invoice["pdf_bytes"], file_name=f"Invoice_{invoice['invoice_no']}.pdf")
