import http.server
import ssl
import os

HTTPS_PORT = int(os.environ.get('PORT', 443))
HTTP_PORT = int(os.environ.get('PORT', 8000))
DIRECTORY = os.path.join(os.path.dirname(__file__), "../static")

# Read the certificate path from an environment variable
CERTIFICATE = os.environ.get('CERT_PATH', '../../LocalFiles/MyWebPage/server.pem')


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


def run(server_class=http.server.HTTPServer, handler_class=CustomHTTPRequestHandler):
    os.chdir(DIRECTORY)
    httpd = server_class(("", HTTPS_PORT), handler_class)

    port = HTTPS_PORT
    proto = "HTTPS"

    try:
        # Create SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=CERTIFICATE)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    except:
        print(f"Could not Find certificate, running HTTP")
        port = HTTP_PORT
        proto = "HTTP"
        httpd = server_class(("", HTTP_PORT), handler_class)

    # Wrap the server's socket with the SSL context

    print(f"Serving {proto} on port {port} (https://localhost:{port})")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
