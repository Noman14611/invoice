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
st.subheader("➕ Add Item")
with st.form("item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    add_btn = st.form_submit_button("Add to List")
    if add_btn:
        if item_name.strip() != "" and price > 0:
            st.session_state["items"].append({
                "name": item_name,
                "quantity": quantity,
                "price": price
            })
        else:
            st.warning("Item name and price are required!")

# Show items
if st.session_state["items"]:
    st.subheader("🧺 Items List")
    for i, item in enumerate(st.session_state["items"], start=1):
        st.write(f"{i}. {item['name']} - Qty: {item['quantity']} - Price: {item['price']}")

# Clear All Button
if st.button("🗑️ Clear All Items"):
    st.session_state["items"] = []
    st.rerun()  # ✅ New version safe

# Discount & Tax
st.subheader("💰 Discount & Tax")
discount = st.number_input("Discount", min_value=0.0, value=0.0)
tax = st.number_input("Tax", min_value=0.0, value=0.0)

# Generate Invoice
if st.button("✅ Generate Invoice"):
    if name and address and phone and st.session_state["items"]:
        invoice = create_invoice(
            name=name,
            address=address,
            phone=phone,
            items=st.session_state["items"],
            discount=discount,
            tax=tax,
            invoice_date=str(invoice_date)
        )
        st.success(f"✅ Invoice #{invoice['invoice_no']} generated successfully!")
        st.download_button("⬇️ Download Invoice", invoice['file'], file_name=invoice['file_name'], mime='application/pdf')
        st.session_state["items"] = []
    else:
        st.error("❌ Please fill all customer fields and add at least one item.")
