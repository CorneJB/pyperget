# pyperget

A tool for converting pipermail archives into a .mbox format. 

usage: pyperget.py [-h] [-u URL] [-o OUTPUT]

Download a pipermail archive and convert it to mbox

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Pipermail directory location. Example:
                        http://hostname.tld/directory/. Don't forget the
                        trailing /
  -o OUTPUT, --output OUTPUT
                        Output file name (without.mbox)
