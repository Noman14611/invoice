import streamlit as st
from invoice_logic import create_invoice, save_invoice

st.title("🧾 Invoice Generator")

st.markdown("Enter customer and product details below:")

name = st.text_input("Customer Name")
address = st.text_input("Customer Address")
phone = st.text_input("Customer Phone")
invoice_date = st.date_input("Invoice Date")

items = []
with st.form("item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    submitted = st.form_submit_button("Add Item")
    if submitted:
        items.append({"name": item_name, "quantity": quantity, "price": price})

discount = st.number_input("Discount", min_value=0.0, value=0.0)
tax = st.number_input("Tax", min_value=0.0, value=0.0)

if st.button("Generate Invoice"):
    if name and address and phone and items:
        invoice = create_invoice(name, address, phone, items, discount, tax, str(invoice_date))
        st.success(f"Invoice #{invoice['invoice_no']} generated successfully!")
    else:
        st.error("Please fill all required fields.")
