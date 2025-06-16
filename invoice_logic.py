from jinja2 import Environment, FileSystemLoader

def create_invoice_html(name, address, phone, items, discount, tax, invoice_date):
    subtotal = sum(item["quantity"] * item["price"] for item in items)
    total = subtotal - discount + tax

    invoice = {
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

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("invoice_template.html")
    html = template.render(invoice=invoice)
    return html
