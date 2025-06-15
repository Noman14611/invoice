import os
import json
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

# ✅ Load the HTML Template using FileSystemLoader
def load_template():
    env = Environment(loader=FileSystemLoader("templates"))
    return env.get_template("invoice_template.html")

# ✅ Load Invoices from JSON file
def load_invoices(filename="invoices.json"):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

# ✅ Save Invoice to JSON file
def save_invoice(invoice, filename="invoices.json"):
    data = load_invoices(filename)
    data.append(invoice)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# ✅ Create Invoice and Generate PDF
def create_invoice(name, address, phone, items, discount, tax, invoice_date):
    processed_items = []
    for item in items:
        processed_items.append({
            "name": item["name"],
            "quantity": int(item["quantity"]),
            "price": float(item["price"]),
        })

    subtotal = sum(i["quantity"] * i["price"] for i in processed_items)
    discount_amount = float(discount)
    tax_amount = float(tax)
    total = subtotal - discount_amount + tax_amount

    invoice = {
        "invoice_no": len(load_invoices()) + 1,
        "date": invoice_date,
        "customer": {
            "name": name,
            "address": address,
            "phone": phone,
        },
        "items": processed_items,
        "subtotal": subtotal,
        "discount": discount_amount,
        "tax": tax_amount,
        "total": total
    }

    # ✅ Render the HTML template with invoice data
    template = load_template()
    html = template.render(invoice=invoice)

    # ✅ Ensure invoices folder exists
    os.makedirs("invoices", exist_ok=True)
    filename = f"invoices/invoice_{invoice['invoice_no']}.pdf"

    # ✅ Generate PDF from HTML
    with open(filename, "wb") as f:
        pisa.CreatePDF(html, dest=f)

    # ✅ Save the invoice data to JSON
    save_invoice(invoice)

    return invoice
