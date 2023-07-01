import http.server
import requests

from prometheus_client import start_http_server
from prometheus_client import Counter

REQUESTS = Counter('server_requests_total', 'Total number of requests to this webserver')

class ServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        REQUESTS.inc()
        if self.path != "/header":
            hostname = 'flask:5000'
        else:
            hostname =  'debug:8080'

        url = 'http://{}{}'.format(hostname, self.path)

        # Call the target service
        resp = requests.get(url, verify=False)

        # Respond with the requested data
        self.wfile.write(resp.content)

if __name__ == "__main__":
    server = http.server.HTTPServer(('0.0.0.0', 8000), ServerHandler)
    server.serve_forever()
    print("HTTP server available on port 8000")

    start_http_server(8001)
    print("Prometheus metrics available on port 8001 /metrics")
