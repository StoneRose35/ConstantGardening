import smbus
import datetime
import pymysql


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

    def insert_humidity_value(self, val: TimeTaggedValue):
        cur = self.db.cursor()
        stmt = "INSERT INTO humidity(value,timestamp) VALUES (%s,%s)"
        cur.execute(stmt, (val.val, val.timestamp))
        self.db.commit()

    def insert_brightness_value(self, val: TimeTaggedValue):
        cur = self.db.cursor()
        stmt = "INSERT INTO brightness(value,timestamp) VALUES (%s,%s)"
        cur.execute(stmt, (val.val, val.timestamp))
        self.db.commit()

    def get_humidity_values(self, max_values=None, t_start=None, t_end=None):
        stmt = "select value, timestamp from humidity {} order by timestamp DESC "
        whereclause = ""
        cur = self.db.cursor()
        if max_values is not None:
            stmt += "LIMIT {}".format(int(max_values))

        if t_start is not None and isinstance(t_start, datetime.datetime):
            whereclause += "timestamp>=" + "'" + t_start.strftime("%y-%M-%d %h:%m:%s") + "' "
        if t_end is not None and isinstance(t_end, datetime.datetime):
            if len(whereclause) > 0:
                whereclause += " AND "
            whereclause += "timestamp<=" + "'" + t_end.strftime("%y-%M-%d %h:%m:%s") + "' "
        cur.execute(stmt.format(whereclause))
        return cur.fetchall()

    def get_brightness_values(self, max_values=None, t_start=None, t_end=None):
        stmt = "select value, timestamp from brightness order by timestamp DESC "
        whereclause = ""
        cur = self.db.cursor()
        if max_values is not None:
            stmt += "LIMIT {}".format(int(max_values))

        if t_start is not None and isinstance(t_start, datetime.datetime):
            whereclause += "timestamp>=" + "'" + t_start.strftime("%y-%M-%d %h:%m:%s") + "' "
        if t_end is not None and isinstance(t_end, datetime.datetime):
            if len(whereclause) > 0:
                whereclause += " AND "
            whereclause += "timestamp<=" + "'" + t_end.strftime("%y-%M-%d %h:%m:%s") + "' "
        cur.execute(stmt.format(whereclause))
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