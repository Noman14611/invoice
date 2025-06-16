import streamlit as st
from datetime import date
from invoice_logic import create_invoice_html

# --- Initialize Session State ---
for key in ["name", "address", "phone", "items", "discount", "tax"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "items" else 0.0 if key in ["discount", "tax"] else ""

# --- Reset Functions ---
def reset_items():
    st.session_state["items"] = []
    st.rerun()

def reset_all():
    for key in ["name", "address", "phone", "items", "discount", "tax"]:
        st.session_state[key] = [] if key == "items" else 0.0 if key in ["discount", "tax"] else ""
    st.rerun()

# --- UI Start ---
st.set_page_config(page_title="Invoice Generator", layout="centered")
st.title("🧾 Invoice Generator")

# --- Customer Info ---
st.session_state["name"] = st.text_input("Customer Name", value=st.session_state["name"])
st.session_state["address"] = st.text_input("Customer Address", value=st.session_state["address"])
st.session_state["phone"] = st.text_input("Customer Phone", value=st.session_state["phone"])
invoice_date = st.date_input("Invoice Date", value=date.today())

# --- Item Form ---
st.subheader("Add Item")
with st.form("item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price = st.number_input("Price", min_value=0.0, value=0.0)
    add_btn = st.form_submit_button("Add Item")
    if add_btn:
        if item_name.strip():
            st.session_state["items"].append({
                "name": item_name,
                "quantity": quantity,
                "price": price
            })
        else:
            st.warning("⚠️ Please enter a valid item name.")

# --- Item List ---
if st.session_state["items"]:
    st.subheader("Items List")
    for i, item in enumerate(st.session_state["items"], 1):
        st.write(f"{i}. {item['name']} — Qty: {item['quantity']}, Price: {item['price']}")

# --- Discount & Tax ---
st.session_state["discount"] = st.number_input("Discount", min_value=0.0, value=st.session_state["discount"])
st.session_state["tax"] = st.number_input("Tax", min_value=0.0, value=st.session_state["tax"])

# --- Buttons ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🧹 Clear Items"):
        reset_items()

with col2:
    if st.button("♻️ Clear All Info"):
        reset_all()

with col3:
    generate_btn = st.button("✅ Generate Invoice")

# --- Generate Invoice Logic ---
if generate_btn:
    if all([
        st.session_state["name"].strip(),
        st.session_state["address"].strip(),
        st.session_state["phone"].strip(),
        len(st.session_state["items"]) > 0
    ]):
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
