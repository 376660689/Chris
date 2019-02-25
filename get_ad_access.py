#!/usr/bin/python
import getopt
import sys
import re
import os
import gzip

F = None
sep = "|"

opts, args = getopt.getopt(sys.argv[1:], "d:f:e:s:k:h")
if not opts:
	print "#############################################################################################"
	print "###Usage: python get_access.py -d log_dir -f file_name -e text_rule -F | [-s /tmp/logfile]"
	print "### -d log dir			"
	print "### -f file name			"
	print "### -e text filtering rules	"
	print "### -F text segmenter		"
	print "### -s output log file		"
	print "############################################################################################"
	sys.exit(0)

for opt, value in opts:
	if opt == "-d":
		log_dir = value
	if opt == "-f":
		file_law =  value
	if opt == "-e":
		text_law = value
	if opt == "-s":
		sep = value
	if opt == "-k":
		log_file = value
	if opt == "-h":
		print "#############################################################################################"
		print "Usage: python get_access.py -d log_dir -f file_name -e text_rule -F | [-s /tmp/logfile]"
		print "### -d log dir			"
		print "### -f file name			"
		print "### -e text filtering rules	"
		print "### -F text segmenter		"
		print "### -s output log file		"
		print "#############################################################################################"
		sys.exit(0)

def read_gzip_file(name, regx, sep, log):
	reg = re.compile(regx)
	gzip_file = gzip.open(name, "r")
	while True:
		line = gzip_file.readline()
		if line:
			if re.search(reg, line):
				log.write(line)
			else:
				pass
		else:
			break

F = open(log_file, "a")
file_regx = re.compile(file_law)
for file_name in os.listdir(log_dir):
	if re.findall(file_regx, file_name):
		name = os.path.join(log_dir, file_name)
		if re.search("\.gz$", file_name) :
			read_gzip_file(name, text_law, sep, log=F)
		else:
			pass

#python get_ad_access.py -d /var/log/nginx/ -f gadmobe-com-access.log_2019022[2-5] -e 'campaign=12413&creative=14413&partner=1395' -s '|' -k '/tmp/test.log'
