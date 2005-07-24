import unittest
import ufsi.NativePath
import test.ufsi.TestNativeWindowsPathData


class TestNativeWindowsPath(unittest.TestCase):
	def setUp(self):
		# get a list of all of the sets of test data
		self.testData=map(
				lambda a:getattr(test.ufsi.TestNativeWindowsPathData,a),
				filter(
						lambda s:not s.startswith('__'),
						dir(test.ufsi.TestNativeWindowsPathData)
						)
				)

		# create a path object for each set of test data
		for d in self.testData:
			d['pathObject']=ufsi.NativePath.NativeWindowsPath(d['path'])
		
		# initialise a counter of the total number of tests being executed
		self.executedTests=0

		# TODO: test isDir, isFile, isSymlink methods. test getDir, getFile methods

	#def tearDown(self):
		#print "%i tests executed"%(self.executedTests)

	# ===========================================
	# ===========================================
	# Test methods that DONT access the file system
	# ===========================================
	# ===========================================
	def testStrMethod(self):
		for d in self.testData:
			self.__assertEqual(str(d['pathObject']),d['str'],'str',d['path'])
			self.executedTests+=1
	
	# =========================
	# Test split method
	# =========================
	def testSplitMethod(self):
		self.runMethodTest('split')
	
	# =========================
	# Test getDriveLetter method (windows specific))
	# =========================
	def testGetDriveLetterMethod(self):
		self.runMethodTest('getDriveLetter')

	# =========================
	# Test dir splitting methods
	# =========================
	def testGetDirsListMethod(self):
		self.runMethodTest('getDirsList')
	def testGetDirsStringMethod(self):
		self.runMethodTest('getDirsString')
	def testGetParentDirPathMethod(self):
		for d in self.testData:
			result=d['pathObject'].getParentDirPath()
			if result: result=str(result)
			self.__assertEqual(result,d['getParentDir'],'getParentDirPath',d['path'])
			self.executedTests+=1

	# =========================
	# Test filename splitting methods
	# =========================
	def testGetFileNameMethod(self):
		self.runMethodTest('getFileName')
	def testGetFileBaseMethod(self):
		self.runMethodTest('getFileBase')
	def testGetFileExtMethod(self):
		self.runMethodTest('getFileExt')


	# =========================
	# Test isAbsolute related methods
	# =========================
	def testIsAbsoluteMethod(self):
		self.runMethodTest('isAbsolute')
	def testIsRelativeMethod(self):
		for d in self.testData:
			self.__assertEqual(d['pathObject'].isRelative(),not d['isAbsolute'],'isRelative',d['path'])
			self.executedTests+=1
		




	# =========================
	# Helper functions
	# =========================
	def runMethodTest(self,method):
		for d in self.testData:
			result=getattr(d['pathObject'],method)()
			expected=d[method]
			#self.assertEqual(result,expected,"%r != %r for method %s on path %s"%(result,expected,method,d['path']))
			self.__assertEqual(result,expected,method,d['path'])
			self.executedTests+=1

	def __assertEqual(self,result,expected,method,path):
		self.assertEqual(result,expected,"%r != %r for method %s on path %s"%(result,expected,method,path))
		

# TestNativeWindowsDriveBasedPath
# TestNativeWindowsUNCBasedPath
