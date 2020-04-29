#!c:\users\hbrit\desktop\kcm\kcmvenv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'PyDictionary==1.5.2','console_scripts','pydictionary'
__requires__ = 'PyDictionary==1.5.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('PyDictionary==1.5.2', 'console_scripts', 'pydictionary')()
    )
