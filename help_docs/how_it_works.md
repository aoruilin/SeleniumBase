[<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_sb4.png" title="SeleniumBase" height="48">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

<a id="how_seleniumbase_works"></a>
## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> **How it works:**

At the core, SeleniumBase works by extending [pytest](https://docs.pytest.org/en/latest/) and [nosetests](http://nose.readthedocs.io/en/latest/) as a direct plugin to each one. SeleniumBase automatically spins up web browsers for tests, and then gives those tests access to the SeleniumBase libraries through the [BaseCase class](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/fixtures/base_case.py). Tests are also given access to SeleniumBase [command-line arguments](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/pytest_plugin.py), which provide additional functionality.
在核心，SeleniumBase的工作方式是作为每个插件的直接扩展。SeleniumBase自动为测试启动web浏览器，然后让那些测试通过[BaseCase类]访问SeleniumBase库。

(NOTE: pytest and nosetests use a feature called test discovery to automatically find and run Python methods that start with "``test_``" from the file that you specified on the command line.)
(注意:pytest和nosetests使用一个名为test discovery的特性，从命令行中指定的文件中自动查找并运行以 "``test_``" 开头的Python方法。)

To use SeleniumBase calls you need the following:
要使用SeleniumBase调用你需要以下:
```python
from seleniumbase import BaseCase
```
And then have your test classes inherit BaseCase:
然后让你的测试类继承BaseCase:
```python
class MyTestClass(BaseCase):
```
(*See the example test, [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py), for reference.*)
