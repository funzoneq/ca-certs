import re
import textwrap
import base64
import M2Crypto
from pprint import pprint

with open('certdata.txt') as f:
	data = f.readlines()
	data = "".join(data)

	pat = re.compile(r"^CKA_VALUE MULTILINE_OCTAL\n(.*?)END\n\n", re.S|re.M)
	result = pat.findall(data)
	for i in result:
		value = ""
		line = "".join(i.split("\n"))
		for a in re.finditer(r'\\([0-3][0-7][0-7])', line):
			value += chr(int(a.group(1), 8))
		pem = "-----BEGIN CERTIFICATE-----\n%s\n-----END CERTIFICATE-----" % "\n".join(textwrap.wrap(base64.b64encode(value), 64))
		cert = M2Crypto.X509.load_cert_string(str(pem))
		try:
			subject = cert.get_subject().as_text()
			print subject
		except:
			print "issue/subject: Unexpected error:", sys.exc_info()[0]
			pass
