import streamlit as st
from invoice_logic import create_invoice, save_invoice

# ✅ Session state for item list
if 'items' not in st.session_state:
    st.session_state['items'] = []

st.set_page_config(page_title="Invoice Generator", layout="centered")

# ✅ Sidebar
st.sidebar.title("🧾 Invoice Generator Menu")
st.sidebar.info("Fill the form to create invoice")

# ✅ Main UI
st.title("🧾 Invoice Generator")

st.markdown("### Enter Customer Details")

name = st.text_input("Customer Name")
address = st.text_input("Customer Address")
phone = st.text_input("Customer Phone")
invoice_date = st.date_input("Invoice Date")

st.markdown("### Add Item")

with st.form("item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    add = st.form_submit_button("Add Item")
    if add:
        st.session_state['items'].append({
            "name": item_name,
            "quantity": quantity,
            "price": price
        })
        st.success("Item added successfully!")

# ✅ Show added items
if st.session_state['items']:
    st.markdown("### Added Items:")
    st.table(st.session_state['items'])

# ✅ Discount & Tax
discount = st.number_input("Discount", min_value=0.0, value=0.0)
tax = st.number_input("Tax", min_value=0.0, value=0.0)

# ✅ Generate Invoice
if st.button("Generate Invoice"):
    if name and address and phone and st.session_state['items']:
        invoice = create_invoice(name, address, phone, st.session_state['items'], discount, tax, str(invoice_date))
        st.success(f"✅ Invoice #{invoice['invoice_no']} generated successfully!")
        st.session_state['items'] = []  # Clear after creation
    else:
        st.error("❌ Please fill all required fields and add at least one item.")
