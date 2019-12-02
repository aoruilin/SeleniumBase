'''
You can use this as a boilerplate for your test framework.
Define your customized library methods in a master class like this.
Then have all your test classes inherit it.
BaseTestCase will inherit SeleniumBase methods from BaseCase.
您可以将其作为测试框架的样板。
像这样在一个主类中定义定制的库方法。
然后让所有测试类继承它。
BaseTestCase将从BaseCase继承SeleniumBase方法。
'''

from seleniumbase import BaseCase


class BaseTestCase(BaseCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.url = 'http://192.168.0.160:8096'
        # Add custom setUp code for your tests AFTER the super().setUp()

    def tearDown(self):
        # Add custom tearDown code for your tests BEFORE the super().tearDown()
        super(BaseTestCase, self).tearDown()

    def login(self):
        # <<< Placeholder. Add your code here. >>>
        # Reduce duplicate code in tests by having reusable methods like this.
        # If the UI changes, the fix can be applied in one place.
        self.open(self.url)

    def example_method(self):
        # <<< Placeholder. Add your code here. >>>
        pass


'''
# Now you can do something like this in your test files:

from base_test_case import BaseTestCase

class MyTests(BaseTestCase):

    def test_example(self):
        self.login()
        self.example_method()
'''

