import http.server
import controllers
import json
import matplotlib.pyplot as plt
import datetime
from io import BytesIO


class GardeningWebServer(http.server.HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.db_accessor = controllers.DbAccessor()


class GardeningRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

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
            self.handle_data_request(controllers.TYPE_HUMIDITY)

        elif self.path.startswith("/brightnesses"):
            self.handle_data_request(controllers.TYPE_BRIGHTNESS)


        else:
            self.send_404()

    def handle_data_request(self, datatype):
        max_elements = None
        t_start = None
        t_end = None
        plot = 0
        args = self.path_to_arg_dict()
        ctype = ""
        if "max_elements" in args:
            max_elements = int(args["max_elements"])
        if "t_start" in args:
            t_start = datetime.datetime.strptime(args["t_start"], "%Y%m%d%H%M%S")
        if "t_end" in args:
            t_end = datetime.datetime.strptime(args["t_end"], "%Y%m%d%H%M%S")
        if "plot" in args:
            plot = 1
        try:
            if plot == 0:
                hum_vals = self.server.db_accessor.get_values(datatype, max_elements, t_start, t_end)
                vals_array = []
                for hv in hum_vals:
                    vals_array.append({'data': hv[0], 'timestamp': hv[1].__str__()})
                json_vals = {'values': vals_array}
                msg = json.dumps(json_vals).encode("utf-8")
                ctype = "application/json"
            else:
                r_data = self.generate_temporal_plot(t_start, t_end, datatype)
                ctype = "image/png"
                msg = r_data.getvalue()
            code = 200
        except:
            code = 500
            ctype = "application/json"
            msg = "{{'error': 'database access error occurred during reading the {} table'}}".format(datatype["tablename"]).encode("utf-8")
        self.send_response(code)
        self.send_header('Content-type', ctype)
        self.end_headers()
        self.wfile.write(msg)

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
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

    def generate_temporal_plot(self, t_start: datetime.datetime, t_end: datetime.datetime, datatype):
        vals = self.server.db_accessor.get_values(t_start=t_start, t_end=t_end, datatype=datatype)
        x = []
        y = []
        labels = []
        cnt = 0
        minval = 999999
        for v in vals:
            if int(v[0]) < minval:
                minval = int(v[0])
            y.append(int(v[0]))
            x.append(cnt)
            labels.append(str(v[1]))
            cnt += 1
        fig = plt.figure()
        figdata = BytesIO()
        if cnt > 0:
            plt.plot(x, y)
            ax = plt.gca()
            xt = [0, int(cnt/3), int(2*cnt/3), cnt-1]
            lbl = [labels[x] for x in xt]
            ax.set_xticks(xt)
            ax.set_xticklabels([])
            ax.set_ylim([0, 1024])
            for l in zip(xt, lbl):
                plt.text(l[0], 10, l[1], {'ha': 'left', 'va': 'bottom'}, rotation=90)
        else:
            plt.text(0.25, 0.5, "no data points to display", fontsize=24)
        fig.set_size_inches(10.24, 7.68)
        fig.savefig(figdata, format="png", dpi=100)
        return figdata

    def path_to_arg_dict(self):
        args = {}
        p_args = self.path.split("?")
        if len(p_args) > 1:
            p_args = p_args[1]
            arr_args = p_args.split("&")
            for arg in arr_args:
                key_val = arg.split("=")
                if len(key_val) > 1:
                    args[key_val[0]] = key_val[1]
                else:
                    args[key_val[0]] = 1
        return args