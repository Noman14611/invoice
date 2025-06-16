from jinja2 import Template
from weasyprint import HTML
import tempfile
import os

def create_invoice_html(name, address, phone, items, discount, tax, invoice_date):
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    total = subtotal - discount + tax
    invoice_data = {
        "invoice_no": 1,
        "date": invoice_date,
        "customer": {
            "name": name,
            "address": address,
            "phone": phone
        },
        "items": items,
        "subtotal": f"{subtotal:.2f}",
        "discount": f"{discount:.2f}",
        "tax": f"{tax:.2f}",
        "total": f"{total:.2f}"
    }

    with open("templates/invoice_template.html", "r", encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(invoice=invoice_data)

def save_invoice_pdf(html):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    HTML(string=html).write_pdf(tmp_file.name)
    return tmp_file.name
