import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

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

    # Generate PDF using WeasyPrint
    output_file = f"invoice_{invoice_counter}.pdf"
    HTML(string=html_out).write_pdf(output_file)

    invoice_counter += 1

    # Return PDF content for download
    with open(output_file, "rb") as f:
        pdf_bytes = f.read()

    return {
        "invoice_no": invoice_data["invoice_no"],
        "file": pdf_bytes,
        "file_name": output_file
    }
