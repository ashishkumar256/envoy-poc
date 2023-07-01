import http.server
from prometheus_client import start_http_server
from prometheus_client import Counter

import requests

REQUESTS = Counter('server_requests_total', 'Total number of requests to this webserver')

class ServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        REQUESTS.inc()
        hostname = 'localhost:5000'
        url = 'http://{}{}'.format(hostname, self.path)

        # Call the target service
        resp = requests.get(url, verify=False)

        # Respond with the requested data
        self.wfile.write(resp.content)

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('', 8001), ServerHandler)
    print("Prometheus metrics available on port 8000 /metrics")
    print("HTTP server available on port 8001")
    server.serve_forever()
