This program requires lxml, which can be installed at: http://lxml.de/installation.html

It also requires your computer username.  This can be added to the actual code by commenting out line 7 "import environment" and changing the variable "username" in line 10 to reflect your username.  Alternatively, you may also create a document called "environment.py" and write "username = <your username>" inside it.

A further note -- I had difficulty installing lxml for Python 2.7, so if this is the case you may find it easier to create a virtual environment with Python 2.6 installed, and then install lxml from there.