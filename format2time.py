import time
import re
import sys
import getopt
import os

class log:
    def __init__(self, current_zone=+0, export_zone=+8, timeformat=None, time_regx=None):
        self.current_zone = current_zone
        self.export_zone = export_zone
        self.timeformat = timeformat
        self.file = None
        self.max_time = None
        self.min_time = None
        self.time_regx = time_regx

    @staticmethod
    def time2stamp(current_time, current_zone=+0, export_zone=+8, timeformat=None):
        sum_zone = (current_zone - export_zone)*60*60
        current_time = time.strptime(current_time, timeformat)
        current_timestamp= time.mktime(current_time)
        return current_timestamp - sum_zone

    def timerange(self, max_time=None, min_time=None, timeformat="%Y-%m-%d %H:%M:%S"):
        if max_time and min_time:
            self.max_time = time.mktime(time.strptime(max_time, timeformat))
            self.min_time = time.mktime(time.strptime(min_time, timeformat))

    def __greptime(self, tim, time_regx):
        s = re.search(time_regx, tim)
        return s.group() if s else False

    def __greptext(self, text, text_regx):
        if not text_regx:
            return True

        if isinstance(text_regx, list):
            all_condition = True
            for condition in all_condition:
                if not re.search(text_regx, condition):
                    all_condition = False
                    return all_condition
            return all_condition
        else:
            return True if re.search(text_regx, text) else False
                    
    def getlog(self, file_name, text_regx=None):
        with open(file_name, 'r') as f:
            while True:
                line = f.readline()
                if line:
                    log_time = self.__greptime(line, self.time_regx)
                    if log_time:
                        log_timestamp = self.time2stamp(log_time, current_zone=self.current_zone, export_zone=self.export_zone, timeformat=self.timeformat)
                        exist_str = self.__greptext(line, text_regx)
                        if log_timestamp >= self.min_time and log_timestamp <= self.max_time and exist_str:
                            #print "log_timestamp: %s, min_time: %s, max_time: %s" % (log_timestamp,self.min_time, self.max_time)
                            print line,
			    pass
                    else:
                        pass
                else:
                    break

def help():
    print "syntax: python format2time.py option -"
    print "usage: python fromat2time.py \n" \
            "\t-i time range, min time\n" \
            "\t-a time range, max time\n" \
            "\t-d log directory\n" \
            "\t-e time expression, regular expression\n" \
            "\t-f file name, regular expression\n" \
            "\t--szone current time zone\n" \
            "\t--dzone converted time zone\n" \
            "\t--string text filtering conditions"

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "ha:i:d:e:f:", ["szone=", "dzone=", "string="])

    s_zone = +0
    d_zone = +8
    time_format = "%d/%b/%Y:%H:%M:%S"
    time_regx = '[0-9]{1,2}\/[A-z]{3}\/[0-9]{2,4}:[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}'
    re_string = None
    for opt, value in opts:
        if opt == "-h":
            help()
            sys.exit(0)

        if opt == "-a":
            max_time = value
        if opt == "-i":
            min_time = value
        if opt == "--szone":
            s_zone = value
        if opt == "--dzone":
            d_zone = value
        if opt == "-d":
            log_dir = value
        if opt == "-f":
            log_file_name = value
        if opt == "-t":
            time_format = value
        if opt == "-e":
            time_regx = value
	if opt == "--string":
	    re_string = value

    log_obj = log(current_zone=s_zone, export_zone=d_zone, timeformat=time_format, time_regx=time_regx)
    log_obj.timerange(max_time=max_time, min_time=min_time)
    for file_name in os.listdir(log_dir):
        if re.search(log_file_name, file_name):
            log_obj.getlog(os.path.join(log_dir, file_name), text_regx=re_string)

#python format2time.py -i "2019-02-27 00:00:03" -a "2019-02-27 00:00:05" -d /var/log/nginx/ -f  ^gadmobe-com-access.log$ --string favicon\.ico
