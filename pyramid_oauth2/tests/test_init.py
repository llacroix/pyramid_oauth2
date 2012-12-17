from pyramid import testing
from unittest import TestCase
from pyramid.exceptions import ConfigurationError

class Test_includeme(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_with_config(self):
        self.assertEqual(True, False)

    def test_without_config(self):
        self.assertEqual(True, False)



class Test_load_providers(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_with_config(self):
        self.assertEqual(True, False)

    def test_without_config(self):
        self.assertEqual(True, False)

class Test_add_oauth2_provider(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_with_provider_none(self):
        self.assertEqual(True, False)

    def test_with_provider(self):
        self.assertEqual(True, False)

class Test_get_provider(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_with_valid_request(self):
        self.assertEqual(True, False)

    def test_with_invalid_request(self):
        self.assertEqual(True, False)

class Test_authenticate(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_with_valid_request(self):
        from pyramid_oauth2 import authenticate
        from pyramid.exceptions import NotFound
        try:
            authenticate(None)
            success = True
        except NotFound:
            success = False

        self.assertEqual(True, success)

    def test_with_invalid_request(self):
        from pyramid_oauth2 import authenticate
        from pyramid.exceptions import NotFound
        try:
            authenticate(None)
            success = True
        except NotFound:
            success = False

        self.assertEqual(True, success)
