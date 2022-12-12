import sys
if sys.platform == 'win32':
    from externals.tzlocal.win32 import get_localzone, reload_localzone
else:
    from externals.tzlocal.unix import get_localzone, reload_localzone
