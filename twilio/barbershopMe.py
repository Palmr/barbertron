#!/usr/bin/env python
from datetime import datetime 
print(str(datetime.now()) + "\n")

import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()

for k in form.keys():
  print( "k: " + str(k) + "v: " + str(form[k]))
