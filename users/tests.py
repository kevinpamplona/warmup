from django.test import TestCase
import models

class TestUsersModel_ADD(TestCase):
	# simeple case - common un/pw
	def testSimple1(self):
		self.assertEqual(models.g_users.add("kpam", "123"), models.g_users.SUCCESS)

	# simple case - numerical un
	def testSimple2(self):
		self.assertEqual(models.g_users.add("7128", "lava!"), models.g_users.SUCCESS)

	# simple case - random signs, less common characters
	def testSimple3(self):
		self.assertEqual(models.g_users.add("?", "-021../"), models.g_users.SUCCESS)

	# username length exactly at limit
	def testBadUsername1(self):
		username = 'x'
		while(len(username) < models.g_users.MAX_USERNAME_LENGTH):
			username = username + 'x'
		self.assertEqual(models.g_users.add(username, "pwpwpw"), models.g_users.SUCCESS)

	# username length 1 character too long
	def testBadUsername2(self):
		username = 'x'
		while(len(username) <= models.g_users.MAX_USERNAME_LENGTH):
			username = username + 'x'
		self.assertEqual(models.g_users.add(username, "?>?<"), models.g_users.ERR_BAD_USERNAME)

	# username length many characters too long
	def testBadUsername3(self):
		username = 'x'
		while(len(username) <= models.g_users.MAX_USERNAME_LENGTH + 10):
			username = username + 'x'
		self.assertEqual(models.g_users.add(username, "?>?<"), models.g_users.ERR_BAD_USERNAME)

	# username length of 0
	def testBadUsername4(self):
		username = ''
		self.assertTrue(len(username) == 0)
		self.assertEqual(models.g_users.add(username, "hHh h h h[]["), models.g_users.ERR_BAD_USERNAME)

	# both of length 0
	def testBadUsername5(self):
		username = ''
		self.assertTrue(len(username) == 0)
		password = ''
		self.assertTrue(len(password) == 0)
		self.assertEqual(models.g_users.add(username, password), models.g_users.ERR_BAD_USERNAME)

	# password length exactly at limit
	def testBadPassword1(self):
		password = 'x'
		while(len(password) < models.g_users.MAX_PASSWORD_LENGTH):
			password = password + 'x'
		self.assertEqual(models.g_users.add("? is ??", password), models.g_users.SUCCESS)

	# password length 1 character too long
	def testBadPassword2(self):
		password = 'x'
		while(len(password) <= models.g_users.MAX_PASSWORD_LENGTH):
			password = password + 'x'
		self.assertEqual(models.g_users.add("hello, world!", password), models.g_users.ERR_BAD_PASSWORD)

	# password length many characters too long
	def testBadPassword3(self):
		password = 'x'
		while(len(password) <= models.g_users.MAX_PASSWORD_LENGTH + 10):
			password = password + 'x'
		self.assertEqual(models.g_users.add("hello, world!", password), models.g_users.ERR_BAD_PASSWORD)

	# password length of 0
	def testBadPassword4(self):
		password = ''
		self.assertTrue(len(password) == 0)
		self.assertEqual(models.g_users.add("banana bluth 1!", password), models.g_users.ERR_BAD_PASSWORD)

	# trying to add same user w/ same pw
	def testUserExists1(self):
		self.assertEqual(models.g_users.add("i am here", "pass123"), models.g_users.SUCCESS)
		self.assertEqual(models.g_users.add("i am here", "pass123"), models.g_users.ERR_USER_EXISTS)

	# trying to add same user w/ different pw
	def testUserExists2(self):
		self.assertEqual(models.g_users.add("here again!", "pass123"), models.g_users.SUCCESS)
		self.assertEqual(models.g_users.add("here again!", "but different PW, yo!"), models.g_users.ERR_USER_EXISTS)

class TestUsersModel_LOGIN(TestCase):
		# simeple case - common un/pw
	def testSimple1(self):
		self.assertEqual(models.g_users.add("easy", "peasy1"), models.g_users.SUCCESS)
		self.assertEqual(models.g_users.login("easy", "peasy1"), 2)

	# simple case - numerical un
	def testSimple2(self):
		self.assertEqual(models.g_users.add("31495687", "mmmm pie"), models.g_users.SUCCESS)
		self.assertEqual(models.g_users.login("31495687", "mmmm pie"), 2)

	# simple case - random signs, less common characters
	def testSimple3(self):
		self.assertEqual(models.g_users.add("#$#$#$#$", "()()()()()"), models.g_users.SUCCESS)
		self.assertEqual(models.g_users.login("#$#$#$#$", "()()()()()"), 2)

	# bad credentials - normal case
	def testBadCredentials1(self):
		self.assertEqual(models.g_users.login("never ever been added!", "python > javascript"), models.g_users.ERR_BAD_CREDENTIALS)

	# bad credentials - empty username
	def testBadCredentials2(self):
		self.assertEqual(models.g_users.login("", "no name?!!?!"), models.g_users.ERR_BAD_CREDENTIALS)

	# bad credentials - empty password
	def testBadCredentials3(self):
		self.assertEqual(models.g_users.login("h0l up, n0 pw??!?! :(", ""), models.g_users.ERR_BAD_CREDENTIALS)

	# bad credentials - both empty
	def testBadCredentials4(self):
		self.assertEqual(models.g_users.login("", ""), models.g_users.ERR_BAD_CREDENTIALS)

	# bad credentials - same name, different password
	def testBadCredentials5(self):
		self.assertEqual(models.g_users.add("same name", "password diff!"), models.g_users.SUCCESS)
		self.assertEqual(models.g_users.login("same name", "diff password!"), models.g_users.ERR_BAD_CREDENTIALS)

	# bad credentials - different name, same password
	def testBadCredentials6(self):
		self.assertEqual(models.g_users.add("foo bar", "717"), models.g_users.SUCCESS)
		self.assertEqual(models.g_users.login("baz qux", "717"), models.g_users.ERR_BAD_CREDENTIALS)

class TestUsersModel_RESET(TestCase):
	# add user, reset tables, no users left
	def testReset1(self):
		self.assertEqual(models.g_users.add("to be deleted", "bye bye"), models.g_users.SUCCESS)
		self.assertEqual(models.g_users.TESTAPI_resetFixture(), models.g_users.SUCCESS)
		from users.models import User
		self.assertFalse(User.objects.all())

	# still returns success even though theres no users
	def testReset2(self):
		from users.models import User
		self.assertFalse(User.objects.all())
		self.assertEqual(models.g_users.TESTAPI_resetFixture(), models.g_users.SUCCESS)



