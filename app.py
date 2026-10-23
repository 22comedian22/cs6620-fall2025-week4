import os
import sys
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

APP_VERSION = os.environ.get("APP_VERSION", "1.0-manual")
DEPLOY_METHOD = os.environ.get("DEPLOY_METHOD", "Manual (SSH)")
DEPLOY_TIME = os.environ.get("DEPLOY_TIME", "unknown")


def add(a, b):
    """Add two numbers"""
    return a + b


def subtract(a, b):
    """Subtract two numbers"""
    return a - b


def multiply(a, b):
    """Multiply two numbers"""
    return a * b


def divide(a, b):
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate(operation, num1, num2):
    """Perform calculation based on operation"""
    if operation == 'add':
        result = add(num1, num2)
    elif operation == 'subtract':
        result = subtract(num1, num2)
    elif operation == 'multiply':
        result = multiply(num1, num2)
    elif operation == 'divide':
        result = divide(num1, num2)
    else:
        raise ValueError(f"Unknown operation: {operation}")

    return result


class Handler(BaseHTTPRequestHandler):
    def _send(self, content_type, body):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            data = {
                "status": "healthy",
                "version": APP_VERSION,
                "deployment_method": DEPLOY_METHOD,
                "deployed_at": DEPLOY_TIME,
                "timestamp": datetime.now().isoformat(),
            }
            self._send("application/json", json.dumps(data).encode())
            return

        html = f"""
        <html>
        <body>
            <h1>Hello from Automated CI/CD Pipeline!</h1>
            <p><strong>Version:</strong> {APP_VERSION}</p>
            <p><strong>Deployed via:</strong> {DEPLOY_METHOD}</p>
            <p><strong>Deployed at:</strong> {DEPLOY_TIME}</p>
            <p><strong>Assignment:</strong> Automated EC2 Deployment</p>
            <hr>
            <p>10 + 5 = {calculate('add', 10, 5)}</p>
            <p>7 * 3 = {calculate('multiply', 7, 3)}</p>
        </body>
        </html>
        """.encode()
        self._send("text/html; charset=utf-8", html)


if __name__ == "__main__":
    print("Simple Calculator")
    print("-" * 20)

    result1 = calculate('add', 10, 5)
    print(f"10 + 5 = {result1}")

    result2 = calculate('multiply', 7, 3)
    print(f"7 * 3 = {result2}")

    print(f"Version: {APP_VERSION}")
    print(f"Deployment method: {DEPLOY_METHOD}")
    print(f"Deployed at: {DEPLOY_TIME}")
    print("Calculator completed successfully!")
    sys.stdout.flush()

    # Keep the container alive by serving HTTP on port 5000
    HTTPServer(("0.0.0.0", 5000), Handler).serve_forever()

