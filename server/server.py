import http.server
import ssl
import os

PORT = int(os.environ.get('PORT', 8000))
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
    httpd = server_class(("", PORT), handler_class)

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERTIFICATE)

    # Wrap the server's socket with the SSL context
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Serving HTTPS on port {PORT} (https://localhost:{PORT})")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
