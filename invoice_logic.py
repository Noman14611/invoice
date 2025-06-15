import os
import uuid
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import streamlit as st

# Create invoices directory if not exists
if not os.path.exists("invoices"):
    os.makedirs("invoices")

def create_invoice(name, address, phone, items, discount, tax, invoice_date):
    invoice_no = str(uuid.uuid4().hex[:8]).upper()

    # Calculate subtotal
    subtotal = sum(item['quantity'] * item['price'] for item in items)
    total = subtotal - discount + tax

    # Prepare invoice dictionary
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

    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("invoice_template.html")
    html = template.render(invoice=invoice)

    # Save as PDF
    pdf_path = f"invoices/invoice_{invoice_no}.pdf"
    with open(pdf_path, "wb") as f:
        pisa.CreatePDF(html, dest=f)

    # Show download button in Streamlit
    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="📄 Download Invoice PDF",
            data=pdf_file,
            file_name=f"invoice_{invoice_no}.pdf",
            mime="application/pdf"
        )

    return invoice
