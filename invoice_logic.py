import os
from jinja2 import Environment, FileSystemLoader
import pdfkit
from datetime import datetime

invoice_counter = 1  # You can later replace this with file-based or DB-based counting

def create_invoice(name, address, phone, items, discount, tax, invoice_date):
    global invoice_counter

    subtotal = sum(item["price"] * item["quantity"] for item in items)
    total = subtotal - discount + tax

    invoice = {
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

    # Load HTML template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("invoice_template.html")
    html = template.render(invoice=invoice)

    # Save as HTML
    html_filename = f"invoice_{invoice_counter}.html"
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html)

    # Convert HTML to PDF (needs wkhtmltopdf installed)
    pdf_filename = f"invoice_{invoice_counter}.pdf"
    try:
        pdfkit.from_file(html_filename, pdf_filename)
    except OSError as e:
        print("PDF generation failed. Please ensure wkhtmltopdf is installed and configured properly.")
        print(e)

    invoice_counter += 1
    return invoice
