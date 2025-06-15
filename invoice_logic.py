import json, uuid
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa
from jinja2 import Template

def create_invoice(name, address, phone, items, discount, tax, date):
    subtotal = sum(item["quantity"] * item["price"] for item in items)
    discount_amount = subtotal * (discount / 100)
    tax_amount = (subtotal - discount_amount) * (tax / 100)
    total = subtotal - discount_amount + tax_amount
    invoice_no = str(uuid.uuid4())[:8]

    invoice = {
        "invoice_no": invoice_no,
        "date": str(date),
        "customer": {"name": name, "address": address, "phone": phone},
        "items": items,
        "subtotal": subtotal,
        "discount": discount_amount,
        "tax": tax_amount,
        "total": total,
    }

    # Load and render template
    with open("templates/invoice_template.html") as file:
        template = Template(file.read())
        html = template.render(invoice=invoice)

    # Generate PDF
    pdf = BytesIO()
    pisa.CreatePDF(html, dest=pdf)
    invoice["pdf_bytes"] = pdf.getvalue()
    return invoice

def save_invoice(invoice):
    try:
        with open("invoice_data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(invoice)
    with open("invoice_data.json", "w") as f:
        json.dump(data, f, indent=2)

def load_invoices():
    try:
        with open("invoice_data.json", "r") as f:
            return json.load(f)
    except:
        return []
