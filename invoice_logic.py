<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Invoice</title>
    <style>
        body { font-family: Arial, sans-serif; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #dddddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        h1 { text-align: center; }
    </style>
</head>
<body>
    <h1>Invoice #{{ invoice.invoice_no }}</h1>
    <p><strong>Date:</strong> {{ invoice.date }}</p>

    <h3>Customer Information:</h3>
    <p><strong>Name:</strong> {{ invoice.customer.name }}</p>
    <p><strong>Address:</strong> {{ invoice.customer.address }}</p>
    <p><strong>Phone:</strong> {{ invoice.customer.phone }}</p>

    <h3>Items:</h3>
    <table>
        <tr>
            <th>Item</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Total</th>
        </tr>
        {% for item in invoice.items %}
        <tr>
            <td>{{ item.name }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.price }}</td>
            <td>{{ (item.quantity | float) * (item.price | float) }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>Summary:</h3>
    <p><strong>Subtotal:</strong> {{ invoice.subtotal }}</p>
    <p><strong>Discount:</strong> {{ invoice.discount }}</p>
    <p><strong>Tax:</strong> {{ invoice.tax }}</p>
    <p><strong>Total:</strong> {{ invoice.total }}</p>
</body>
</html>
