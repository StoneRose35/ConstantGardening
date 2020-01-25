import controllers
import time
import http.server
import threading
import webRequestHandler


app_is_running = True
DELTA_T = 60*5
PORT = 8080


def log_data_values():
    dba = controllers.DbAccessor()
    sc = controllers.SensorController()
    while app_is_running is True:
        hum = sc.read_humidity()
        #print("Humidity Value read is: {}".format(hum))
        dba.insert_value(hum, controllers.TYPE_HUMIDITY)
        br = sc.read_brightness()
        #print("brightness Value read is: {}".format(br))
        dba.insert_value(br, controllers.TYPE_BRIGHTNESS)
        for c in range(DELTA_T):
            time.sleep(1)
            if app_is_running is False:
                break


if __name__ == "__main__":
    data_logger = threading.Thread(target=log_data_values)
    data_logger.start()
    print("start data logger")
    httpd = http.server.HTTPServer(("", PORT), webRequestHandler.GardeningRequestHandler)
    try:
        print("happily serving gardening monitor data")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Control-C: Shutting down the Web Server and the logger threads")
        app_is_running = False
        httpd.socket.close()
