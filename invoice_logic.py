import os
from jinja2 import Environment, FileSystemLoader
import base64

invoice_counter = 1

def create_invoice(name, address, phone, items, discount, tax, invoice_date):
    global invoice_counter
    subtotal = sum(item["quantity"] * item["price"] for item in items)
    total = subtotal - discount + tax
    invoice_data = {
        "invoice_no": invoice_counter,
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

    # Load template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("invoice_template.html")
    html_out = template.render(invoice=invoice_data)

    file_name = f"invoice_{invoice_counter}.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_out)

    # Encode HTML for download
    b64 = base64.b64
