import os
import uuid
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import streamlit as st

# 📁 Create invoices folder if it doesn't exist
if not os.path.exists("invoices"):
    os.makedirs("invoices")

def create_invoice(name, address, phone, items, discount, tax, invoice_date):
    # 🔢 Unique invoice number
    invoice_no = str(uuid.uuid4().hex[:8]).upper()

    # 💰 Calculate totals
    subtotal = sum(item['quantity'] * item['price'] for item in items)
    total = subtotal - discount + tax

    # 📦 Invoice data structure
    invoice = {
        "invoice_no": invoice_no,
        "date": invoice_date,
        "customer": {
            "name": name,
            "address": address,
            "phone": phone
        },
        "items": items,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total
    }

    # 📄 Load and render HTML template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("invoice_
