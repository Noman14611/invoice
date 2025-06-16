import streamlit as st
from invoice_logic import create_invoice_html
from datetime import date

# Initialize session state
if "items" not in st.session_state:
    st.session_state["items"] = []
if "name" not in st.session_state:
    st.session_state["name"] = ""
if "address" not in st.session_state:
    st.session_state["address"] = ""
if "phone" not in st.session_state:
    st.session_state["phone"] = ""
if "discount" not in st.session_state:
    st.session_state["discount"] = 0.0
if "tax" not in st.session_state:
    st.session_state["tax"] = 0.0
if "invoice_date" not in st.session_state:
    st.session_state["invoice_date"] = date.today()

st.set_page_config(page_title="Invoice Generator", layout="centered")
st.title("🧾 Invoice Generator")

# Input fields (linked to session state)
st.session_state["name"] = st.text_input("Customer Name", st.session_state["name"])
st.session_state["address"] = st.text_input("Customer Address", st.session_state["address"])
st.session_state["phone"] = st.text_input("Customer Phone", st.session_state["phone"])
st.session_state["invoice_date"] = st.date_input("Invoice Date", value=st.session_state["invoice_date"])

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
    st.subheader("Items List")
    for i, item in enumerate(st.session_state["items"], 1):
        st.write(f"{i}. {item['name']} — Qty: {item['quantity']}, Price: {item['price']}")

st.session_state["discount"] = st.number_input("Discount", min_value=0.0, value=st.session_state["discount"])
st.session_state["tax"] = st.number_input("Tax", min_value=0.0, value=st.session_state["tax"])

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🧹 Clear All Shopping"):
        st.session_state["items"] = []
        st.experimental_rerun()

with col2:
    if st.button("🧼 Clear All Info"):
        st.session_state["items"] = []
        st.session_state["name"] = ""
        st.session_state["address"] = ""
        st.session_state["phone"] = ""
        st.session_state["invoice_date"] = date.today()
        st.session_state["discount"] = 0.0
        st.session_state["tax"] = 0.0
        st.experimental_rerun()

with col3:
    if st.button("✅ Generate Invoice"):
        missing = []
        if not st.session_state["name"]: missing.append("Name")
        if not st.session_state["address"]: missing.append("Address")
        if not st.session_state["phone"]: missing.append("Phone")
        if not st.session_state["items"]: missing.append("at least one Item")

        if missing:
            st.error(f"❌ Please fill the following fields: {', '.join(missing)}")
        else:
            html = create_invoice_html(
                name=st.session_state["name"],
                address=st.session_state["address"],
                phone=st.session_state["phone"],
                items=st.session_state["items"],
                discount=st.session_state["discount"],
                tax=st.session_state["tax"],
                invoice_date=str(st.session_state["invoice_date"])
            )
            st.success("✅ Invoice Ready. You can print or save it.")
            st.markdown('<button onclick="window.print()">🖨️ Print / Save Invoice</button><br><br>', unsafe_allow_html=True)
            st.components.v1.html(html, height=1000, scrolling=True)
