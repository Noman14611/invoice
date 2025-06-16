def create_invoice_html(name, address, phone, items, discount, tax, invoice_date):
    subtotal = sum(item["quantity"] * item["price"] for item in items)
    total = subtotal - discount + tax

    rows = ""
    for item in items:
        total_price = item["quantity"] * item["price"]
        rows += f"""
        <tr>
            <td>{item['name']}</td>
            <td>{item['quantity']}</td>
            <td>{item['price']}</td>
            <td>{total_price}</td>
        </tr>"""

    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            th {{ background-color: #f2f2f2; }}
            .total {{ font-weight: bold; }}
        </style>
    </head>
    <body>
        <h2 style='text-align:center;'>Nouman Enterprises</h2>
        <p><b>Date:</b> {invoice_date}</p>
        <p><b>Customer:</b> {name}<br><b>Address:</b> {address}<br><b>Phone:</b> {phone}</p>
        <table>
            <tr><th>Item</th><th>Qty</th><th>Price</th><th>Total</th></tr>
            {rows}
        </table>
        <p class='total'>Subtotal: {subtotal}</p>
        <p class='total'>Discount: {discount}</p>
        <p class='total'>Tax: {tax}</p>
        <p class='total'>Grand Total: {total}</p>
    </body>
    </html>
    """
