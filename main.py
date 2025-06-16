import streamlit as st
from datetime import date
from invoice_logic import create_invoice, generate_pdf
import base64

# Session state init
if "items" not in st.session_state:
    st.session_state["items"] = []

st.sidebar.title("🧾 Invoice Generator")
st.sidebar.markdown("Fill the form to create invoice")

st.title("Customer & Product Details")

# 👉 Customer Info
name = st.text_input("Customer Name")
address = st.text_input("Customer Address")
phone = st.text_input("Customer Phone")
invoice_date = st.date_input("Invoice Date", value=date.today())

# 👉 Add Item
st.subheader("Add Item")
with st.form("item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    add_btn = st.form_submit_button("➕ Add Item")
    if add_btn:
        if item_name and price > 0:
            st.session_state["items"].append({
                "name": item_name,
                "quantity": quantity,
                "price": price
            })
        else:
            st.warning("Item name and valid price required!")

# 👉 Display items
if st.session_state["items"]:
    st.subheader("🧺 Added Items")
    for i, item in enumerate(st.session_state["items"], 1):
        st.markdown(f"**{i}.** {item['name']} | Qty: {item['quantity']} | Price: {item['price']}")

    # 👉 Clear button
    if st.button("🗑️ Clear All Items"):
        st.session_state["items"] = []
        st.experimental_rerun()

# 👉 Discount & Tax
st.subheader("Discount and Tax")
discount = st.number_input("Discount", min_value=0.0, value=0.0)
tax = st.number_input("Tax", min_value=0.0, value=0.0)

# 👉 Generate
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
        pdf_path = generate_pdf(invoice)

        st.success(f"✅ Invoice #{invoice['invoice_no']} generated successfully!")

        with open(pdf_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="invoice_{invoice["invoice_no"]}.pdf">📥 Download Invoice</a>'
            st.markdown(href, unsafe_allow_html=True)

        # ✅ Reset items
        st.session_state["items"] = []

    else:
        st.error("❌ Please fill all customer fields and add at least one item.")
