"""
"""

import unittest
import os

from TestNativeFile import TestNativeFile
from TestNativeDir import TestNativeDir
from TestNativeWindowsPath import TestNativeWindowsPath
from TestNativeUnixPath import TestNativeUnixPath


suites=[]
suites.append(unittest.makeSuite(TestNativeFile))
suites.append(unittest.makeSuite(TestNativeDir))
if os.name=='nt':
    suites.append(unittest.makeSuite(TestNativeWindowsPath))
else:
    suites.append(unittest.makeSuite(TestNativeUnixPath))
unittest.TextTestRunner(verbosity=10).run(unittest.TestSuite(suites))

