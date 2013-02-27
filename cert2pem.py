import re
import textwrap
import base64
from pprint import pprint

with open('certdata.txt') as f:
	data = f.readlines()
	data = "".join(data)

	pat = re.compile(r"^CKA_VALUE MULTILINE_OCTAL\n(.*?)END\n\n", re.S|re.M)
	result = pat.findall(data)
	value = ""
	for i in result:
		line = "".join(i.split("\n"))
		for a in re.finditer(r'\\([0-3][0-7][0-7])', line):
			value += chr(int(a.group(1), 8))
		print "-----BEGIN CERTIFICATE-----"
		print "\n".join(textwrap.wrap(base64.b64encode(value), 64))
		print "-----END CERTIFICATE-----"