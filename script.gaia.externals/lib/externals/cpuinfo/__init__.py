
import sys

if sys.version_info[0] == 2:
	from externals.cpuinfo import *
else:
	from externals.cpuinfo.cpuinfo import *


