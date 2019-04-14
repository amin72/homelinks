import sys, os

cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/homelinks')

INTERP = os.path.expanduser("~/virtualenv/homelinks/3.6/bin/python3")

if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0,'$HOME/virtualenv/homelinks/3.6/bin')
sys.path.insert(0,'$HOME/virtualenv/homelinks/3.6/lib/python3.6/site-packages/django')
sys.path.insert(0,'$HOME/virtualenv/homelinks/3.6/lib/python3.6/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'homelinks.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
