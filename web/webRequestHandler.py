import http.server
import controllers
import json


class GardeningRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if hasattr(self, "db_accessor") is False:
            self.db_accessor = controllers.DbAccessor()

        # Send the html message
        if self.path == "/":
            self.path = "/index.html"

        if self.path.endswith(".html"):
            try:
                with open("." + self.path, "rt") as f:
                    lines = f.readlines()
                    total_resp = ""
                    for li in lines:
                        total_resp += li
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(total_resp.encode("utf-8"))
            except FileNotFoundError:
                self.send_404()

        elif self.path.endswith(".js"):
            try:
                with open("." + self.path, "rt") as f:
                    lines = f.readlines()
                    total_resp = ""
                    for li in lines:
                        total_resp += li
                    self.send_response(200)
                    self.send_header('Content-type', 'text/javascript')
                    self.end_headers()
                    self.wfile.write(total_resp.encode("utf-8"))
            except FileNotFoundError:
                self.send_404()

        elif self.path.endswith(".css"):
            try:
                with open("." + self.path, "rt") as f:
                    lines = f.readlines()
                    total_resp = ""
                    for li in lines:
                        total_resp += li
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    self.wfile.write(total_resp.encode("utf-8"))
            except FileNotFoundError:
                self.send_404()

        elif self.path.startswith("/humidities"):
            p_args = self.path.split("/")
            if len(p_args) > 2:
                max_elements = int(p_args[2])
            else:
                max_elements = None
            try:
                hum_vals = self.db_accessor.get_humidity_values(max_elements)
                vals_array = []
                for hv in hum_vals:
                    vals_array.append({'data': hv[0], 'timestamp': hv[1].__str__()})
                json_vals = {'values': vals_array}
                msg = json.dumps(json_vals)
                code = 200
            except:
                code = 500
                msg = "{'error': 'database access error occurred during reading the humidity table'}"
            self.send_response(code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(msg.encode("utf-8"))

        elif self.path.startswith("/brightnesses"):
            p_args = self.path.split("/")
            if len(p_args) > 2:
                max_elements = int(p_args[2])
            else:
                max_elements = None
            try:
                hum_vals = self.db_accessor.get_brightness_values(max_elements)
                vals_array = []
                for hv in hum_vals:
                    vals_array.append({'data': hv[0], 'timestamp': hv[1].__str__()})
                json_vals = {'values': vals_array}
                msg = json.dumps(json_vals)
                code = 200
            except:
                code = 500
                msg = "{'error': 'database access error occurred during reading the brightness table'}"
            self.send_response(code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(msg.encode("utf-8"))

        else:
            self.send_404()



    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.wfile.write("""
        <html>
        <head>
        <title>
        Oh no, a 404 error :-(
        </title>
        </head>
        <body>
        <h2>Something bad happened</h2>
        <h3>The path {} could not be found</h3>
        </body>
        </html>
        """.format(self.path).encode("utf-8"))
