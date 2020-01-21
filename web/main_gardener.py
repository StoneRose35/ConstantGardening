import controllers
import time
import http.server
import threading
import webRequestHandler


app_is_running = True


def log_humidities():
    dba = controllers.DbAccessor()
    sc = controllers.SensorController()
    while app_is_running is True:
        hum = sc.read_humidity()
        dba.insert_humidity_value(hum)
        for c in range(60*15):
            time.sleep(1)
            if app_is_running is False:
                break


if __name__ == "__main__":
    hum_logger = threading.Thread(target=log_humidities)
    hum_logger.start()
    httpd = http.server.HTTPServer(("", 8080), webRequestHandler.GardeningRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Control-C: Shutting down the Web Server and the logger threads")
        app_is_running = False
        httpd.socket.close()
