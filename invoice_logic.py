import os
import json
from datetime import datetime
from jinja2 import Template
from xhtml2pdf import pisa

# ✅ Load HTML Template
def load_template():
    with open("templates/invoice_template.html", "r", encoding="utf-8") as f:
        return Template(f.read())

# ✅ Save Invoice Data to JSON
def save_invoice(invoice, filename="invoices.json"):
    data = load_invoices()
    data.append(invoice)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# ✅ Load All Invoices from JSON
def load_invoices(filename="invoices.json"):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

# ✅ Create Invoice & Generate PDF
def create_invoice(name, address, phone, items, discount, tax, invoice_date):
    # Safely convert items
    processed_items = []
    for item in items:
        processed_items.append({
            "name": item["name"],
            "quantity": int(item["quantity"]),
            "price": float(item["price"]),
        })

    # Subtotal calculation
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

    # Render Template
    template = load_template()
    html = template.render(invoice=invoice)

    # Save as PDF
    filename = f"invoices/invoice_{invoice['invoice_no']}.pdf"
    os.makedirs("invoices", exist_ok=True)
    with open(filename, "wb") as f:
        pisa.CreatePDF(html, dest=f)

    # Save data
    save_invoice(invoice)

    return invoice
