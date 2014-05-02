import sys

activate_this = '/var/www/dev/projectdb/venv/projectdb-v1/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, '/var/www/dev/projectdb/projectdb')

from projectdb import app as application
