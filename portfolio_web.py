from flask import Flask, render_template_string, send_file
import os
import time
from datetime import datetime

app = Flask(__name__)

# HTML template for displaying the portfolio data
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .controls {
            text-align: center;
            margin: 20px 0;
        }
        .controls button {
            padding: 10px 20px;
            margin: 0 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .controls button:hover {
            background-color: #45a049;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .positive {
            color: green;
        }
        .negative {
            color: red;
        }
        .last-updated {
            text-align: right;
            margin-top: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Portfolio Tracker</h1>
        <div class="controls">
            <button onclick="window.location.reload()">Refresh Data</button>
            <button onclick="window.location.href='/download'">Download CSV</button>
        </div>
        {{ table|safe }}
        <div class="last-updated">
            Last Updated: {{ last_updated }}
        </div>
    </div>
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(function() {
            window.location.reload();
        }, 30000);
    </script>
</body>
</html>
"""

def read_csv_to_html():
    try:
        with open('portfolio_data.csv', 'r') as f:
            lines = f.readlines()
        
        # Convert CSV to HTML table
        html = '<table>\n'
        for i, line in enumerate(lines):
            if i == 0:  # Header row
                html += '<tr><th>' + '</th><th>'.join(line.strip().split(',')) + '</th></tr>\n'
            else:
                cells = line.strip().split(',')
                if len(cells) > 1:  # Skip empty lines
                    html += '<tr>'
                    for cell in cells:
                        # Add color classes for numeric values
                        if cell.startswith('+'):
                            html += f'<td class="positive">{cell}</td>'
                        elif cell.startswith('-'):
                            html += f'<td class="negative">{cell}</td>'
                        else:
                            html += f'<td>{cell}</td>'
                    html += '</tr>\n'
        html += '</table>'
        return html
    except Exception as e:
        return f'<p>Error reading portfolio data: {str(e)}</p>'

@app.route('/')
def index():
    table = read_csv_to_html()
    last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template_string(HTML_TEMPLATE, table=table, last_updated=last_updated)

@app.route('/download')
def download():
    return send_file('portfolio_data.csv',
                    mimetype='text/csv',
                    attachment_filename='portfolio_data.csv',
                    as_attachment=True)

if __name__ == '__main__':
    # Get the IP address of the remote host
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"Starting web server at http://{local_ip}:5000")
    print("You can access the portfolio data from your Windows computer by opening this URL in your web browser")
    app.run(host='0.0.0.0', port=5000) 