import controllers
import time
import http.server
import threading
import webRequestHandler


app_is_running = True


def log_data_values():
    dba = controllers.DbAccessor()
    sc = controllers.SensorController()
    while app_is_running is True:
        hum = sc.read_humidity()
        dba.insert_humidity_value(hum)
        br = sc.read_brightness()
        dba.insert_brightness_value(br)
        for c in range(60*15):
            time.sleep(1)
            if app_is_running is False:
                break


if __name__ == "__main__":
    data_logger = threading.Thread(target=log_data_values)
    data_logger.start()
    print("start data logger")
    httpd = http.server.HTTPServer(("", 8080), webRequestHandler.GardeningRequestHandler)
    try:
        print("happily serving gardening monitor data")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Control-C: Shutting down the Web Server and the logger threads")
        app_is_running = False
        httpd.socket.close()
