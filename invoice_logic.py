import json, uuid
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa
from jinja2 import Template

def create_invoice(name, address, phone, items, discount, tax, date):
    subtotal = sum(i["quantity"] * i["price"] for i in items)
    discount_amt = subtotal * discount / 100
    tax_amt = (subtotal - discount_amt) * tax / 100
    total = subtotal - discount_amt + tax_amt
    invoice_no = str(uuid.uuid4())[:8]

    invoice = {
        "invoice_no": invoice_no,
        "date": str(date),
        "customer": {"name": name, "address": address, "phone": phone},
        "items": items,
        "subtotal": round(subtotal, 2),
        "discount": round(discount_amt, 2),
        "tax": round(tax_amt, 2),
        "total": round(total, 2),
    }

    # Load HTML Template
    with open("templates/invoice_template.html") as f:
        template = Template(f.read())
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
