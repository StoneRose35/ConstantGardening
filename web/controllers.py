import smbus
import datetime
import pymysql

TYPE_HUMIDITY = {"idx": 0, "tablename": "humidity"}
TYPE_BRIGHTNESS = {"idx": 1, "tablename": "brightness"}

DELTA_T = 60*5

class TimeTaggedValue:
    def __init__(self, val):
        self.timestamp = datetime.datetime.now()
        self.val = val

    def __str__(self):
        return "{} on {}".format(self.val,self.timestamp)

    def __repr__(self):
        return self.__str__()


class DbAccessor:
    def __init__(self):
        self.user = "mira"
        self.passwd = "amelie"
        self.dbname = "gardening"
        self.db = pymysql.connect("localhost", self.user, self.passwd, self.dbname)

    def get_db_version(self):
        cur = self.db.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()
        return version[0]

    def insert_value(self, val: TimeTaggedValue, datatype):
        cur = self.db.cursor()
        stmt = "INSERT INTO {}(value,timestamp) VALUES (%s,%s)".format(datatype["tablename"])
        cur.execute(stmt, (val.val, val.timestamp))
        self.db.commit()

    def get_values(self, datatype, max_values=None, t_start=None, t_end=None):
        stmt = "select value, timestamp from {} {} order by timestamp ASC "
        whereclause = " WHERE "
        cur = self.db.cursor()
        if max_values is not None:
            stmt += "LIMIT {}".format(int(max_values))

        if t_start is not None and isinstance(t_start, datetime.datetime):
            whereclause += "timestamp>=" + "'" + t_start.strftime("%Y-%m-%d %H:%M:%S") + "' "
        if t_end is not None and isinstance(t_end, datetime.datetime):
            if len(whereclause) > 0:
                whereclause += " AND "
            whereclause += "timestamp<=" + "'" + t_end.strftime("%Y-%m-%d %H:%M:%S") + "' "
        if whereclause == " WHERE ":
            whereclause = ""
        cur.execute(stmt.format(datatype["tablename"], whereclause))
        return cur.fetchall()


class SensorController:

    def __init__(self):
        self.bus = smbus.SMBus(1)

    def read_humidity(self):
        address = 4
        self.bus.write_byte(address, 0)
        msb = self.bus.read_byte(address)  # mbs first
        lsb = self.bus.read_byte(address)  # lsb second
        data_val = int(msb * 256 + lsb)
        return TimeTaggedValue(data_val)

    def read_brightness(self):
        address = 4
        self.bus.write_byte(address, 1)
        msb = self.bus.read_byte(address)  # mbs first
        lsb = self.bus.read_byte(address)  # lsb second
        data_val = int(msb * 256 + lsb)
        return TimeTaggedValue(data_val)