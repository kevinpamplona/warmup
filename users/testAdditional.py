import unittest
import os
import testLib

class TestUnit(testLib.RestTestCase):
    """Issue a REST API request to run the unit tests, and analyze the result"""
    def testUnit(self):
    	#print '*************************************\n'
        respData = self.makeRequest("/TESTAPI/unitTests", method="POST")
        self.assertTrue('output' in respData)
        print ("Unit tests output:\n"+
               "\n***** ".join(respData['output'].split("\n")))
        self.assertTrue('totalTests' in respData)
        print "***** Reported "+str(respData['totalTests'])+" unit tests. nrFailed="+str(respData['nrFailed'])
        # When we test the actual project, we require at least 10 unit tests
        minimumTests = 10
        if "SAMPLE_APP" in os.environ:
            minimumTests = 4
        self.assertTrue(respData['totalTests'] >= minimumTests,
                        "at least "+str(minimumTests)+" unit tests. Found only "+str(respData['totalTests'])+". use SAMPLE_APP=1 if this is the sample app")
        self.assertEquals(0, respData['nrFailed'])

class TestAddUser(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testAdd1(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'usdfgher1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)

    # multiple add requests, different users
    def testAdd2(self):
        respData1 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'abc', 'password' : 'password'} )
        self.assertResponse(respData1, count = 1)

        respData2 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'def', 'password' : 'password'} )
        self.assertResponse(respData2, count = 1)

        respData3 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'ghi', 'password' : 'password'} )
        self.assertResponse(respData3, count = 1)

        respData4 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'jkl', 'password' : 'password'} )
        self.assertResponse(respData4, count = 1)

        respData5 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'mno', 'password' : 'password'} )
        self.assertResponse(respData5, count = 1)

    # bad add
    def testAdd4(self):
        respData1 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'abc', 'password' : 'password'} )
        self.assertResponse(respData1, count = 1)
        respData1 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'abc', 'password' : 'password'} )
        self.assertResponse(respData1, count = None, errCode = -2)


class TestLoginUser(testLib.RestTestCase):
    """Test logging in users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testLogin1(self):
        addUser = self.makeRequest("/users/add", method="POST", data = { 'user' : 'functional', 'password' : 'test'})
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'functional', 'password' : 'test'})
        self.assertResponse(respData, count = 2)

    # multiple login requets, one time, different users
    def testLogin2(self):
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'abc', 'password' : 'password'} )
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'def', 'password' : 'password'} )
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'ghi', 'password' : 'password'} )
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'jkl', 'password' : 'password'} )
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'mno', 'password' : 'password'} )

        respData1 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'abc', 'password' : 'password'} )
        respData2 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'def', 'password' : 'password'} )
        respData3 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'ghi', 'password' : 'password'} )
        respData4 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'jkl', 'password' : 'password'} )
        respData5 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'mno', 'password' : 'password'} )

        self.assertResponse(respData1, count = 2)
        self.assertResponse(respData2, count = 2)
        self.assertResponse(respData3, count = 2)
        self.assertResponse(respData4, count = 2)
        self.assertResponse(respData5, count = 2)

    # multiple login requests, multiple times, different users
    def testLogin3(self):
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'abc', 'password' : 'password'} )
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'def', 'password' : 'password'} )
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'ghi', 'password' : 'password'} )

        self.makeRequest("/users/login", method="POST", data = { 'user' : 'abc', 'password' : 'password'} ) # user: abc
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'def', 'password' : 'password'} ) # user: def
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'abc', 'password' : 'password'} ) # user: abc
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'abc', 'password' : 'password'} ) # user: abc
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'abc', 'password' : 'password'} ) # user: abc
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'def', 'password' : 'password'} ) # user: def
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'abc', 'password' : 'password'} ) # user: abc
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'ghi', 'password' : 'password'} ) # user: ghi
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'abc', 'password' : 'password'} ) # user: abc

        user1 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'abc', 'password' : 'password'} ) # user: abc
        user2 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'ghi', 'password' : 'password'} ) # user: ghi
        user3 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'def', 'password' : 'password'} ) # user: def

        self.assertResponse(user1, count = 8)
        self.assertResponse(user2, count = 3)
        self.assertResponse(user3, count = 4)

    # login failure
    def testLogin4(self):
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'not here!#@', 'password' : 'password'} )
        self.assertResponse(respData, count = None, errCode = -1)


