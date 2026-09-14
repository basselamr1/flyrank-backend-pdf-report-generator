from datetime import date


def build_report_html(report):
    today = date.today().strftime("%Y-%m-%d")

    top_products_rows = ""

    for product in report["top_products"]:
        top_products_rows += f"""
        <tr>
            <td>{product["product"]}</td>
            <td>{product["order_count"]}</td>
            <td>${product["revenue"]:.2f}</td>
        </tr>
        """

    order_rows = ""

    for order in report["all_orders"]:
        order_rows += f"""
        <tr>
            <td>{order["id"]}</td>
            <td>{order["customer"]}</td>
            <td>{order["product"]}</td>
            <td>${order["amount"]:.2f}</td>
            <td>{order["created_at"]}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">

        <title>Orders Report</title>

        <style>
            @page {{
                size: A4;
                margin: 20mm;
            }}

            body {{
                font-family: Arial, sans-serif;
                color: #222;
                font-size: 12px;
            }}

            h1 {{
                margin-bottom: 5px;
            }}

            .date {{
                color: #666;
                margin-bottom: 25px;
            }}

            .summary {{
                display: flex;
                gap: 20px;
                margin-bottom: 30px;
            }}

            .summary-card {{
                border: 1px solid #ddd;
                padding: 15px;
                width: 200px;
            }}

            .summary-label {{
                font-size: 11px;
                color: #666;
            }}

            .summary-value {{
                font-size: 20px;
                font-weight: bold;
                margin-top: 5px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }}

            th,
            td {{
                border: 1px solid #ddd;
                padding: 7px;
                text-align: left;
            }}

            th {{
                background: #f2f2f2;
                font-weight: bold;
            }}

            /*
             * Prevent individual rows from being split
             * across two pages.
             */
            tr {{
                break-inside: avoid;
                page-break-inside: avoid;
            }}

            /*
             * The browser can repeat this header when
             * the table continues onto another page.
             */
            thead {{
                display: table-header-group;
            }}

            .section-title {{
                margin-top: 25px;
                margin-bottom: 10px;
            }}
        </style>
    </head>

    <body>

        <h1>Orders Report</h1>

        <div class="date">
            Generated on {today}
        </div>

        <div class="summary">

            <div class="summary-card">
                <div class="summary-label">
                    Total Orders
                </div>

                <div class="summary-value">
                    {report["total_orders"]}
                </div>
            </div>

            <div class="summary-card">
                <div class="summary-label">
                    Total Revenue
                </div>

                <div class="summary-value">
                    ${report["total_revenue"]:.2f}
                </div>
            </div>

        </div>

        <h2 class="section-title">
            Top 5 Products by Revenue
        </h2>

        <table>

            <thead>
                <tr>
                    <th>Product</th>
                    <th>Orders</th>
                    <th>Revenue</th>
                </tr>
            </thead>

            <tbody>
                {top_products_rows}
            </tbody>

        </table>


        <h2 class="section-title">
            All Orders
        </h2>

        <table>

            <thead>
                <tr>
                    <th>ID</th>
                    <th>Customer</th>
                    <th>Product</th>
                    <th>Amount</th>
                    <th>Created At</th>
                </tr>
            </thead>

            <tbody>
                {order_rows}
            </tbody>

        </table>

    </body>
    </html>
    """