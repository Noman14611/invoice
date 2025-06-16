import os
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

def create_invoice(name, address, phone, items, discount, tax, invoice_date):
    invoice_no = len(os.listdir("invoices")) + 1 if os.path.exists("invoices") else 1
    subtotal = sum(item["quantity"] * item["price"] for item in items)
    total = subtotal - discount + tax

    invoice = {
        "invoice_no": invoice_no,
        "date": invoice_date,
        "customer": {
            "name": name,
            "address": address,
            "phone": phone
        },
        "items": items,
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "tax": round(tax, 2),
        "total": round(total, 2)
    }
    return invoice

def generate_pdf(invoice):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("invoice_template.html")
    html = template.render(invoice=invoice)

    if not os.path.exists("invoices"):
        os.makedirs("invoices")

    output_path = f"invoices/invoice_{invoice['invoice_no']}.pdf"
    with open(output_path, "w+b") as f:
        pisa.CreatePDF(html, dest=f)
    return output_path
