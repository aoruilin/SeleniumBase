[<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_m.png" title="SeleniumBase" height="48">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Customizing test runs

In addition to [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) (which lets you customize SeleniumBase global properties) you can customize test runs from the command line with pytest (or nosetests):

* Choose the browser for tests to use (Default: Chrome)选择要使用的测试浏览器(默认:Chrome)
* Choose betweeen pytest & nose unittest runners选择pytest或nose单元测试运行程序
* Choose whether to enter Debug Mode on failures选择失败时是否进入调试模式
* Choose additional variables to pass into tests选择要传递到测试中的其他变量
* Choose the User-Agent for the browser to use为浏览器选择要使用的用户代理
* Choose the automation speed (with Demo Mode)选择自动化速度(带演示模式)
* Choose whether to run tests multi-threaded选择是否运行多线程测试
* Choose whether to retry failing tests选择是否重试失败的测试
* Choose a Chrome User Data Directory to use选择要使用的Chrome用户数据目录
* Choose a Chrome Extension to load选择一个Chrome扩展加载
* Choose a BrowserStack server to run on选择要在其上运行的BrowserStack服务器
* Choose a Sauce Labs server to run on选择一个酱汁实验室服务器运行
* Choose a TestingBot server to run on选择要在其上运行的TestingBot服务器
* Choose a CrossBrowserTesting server选择一个CrossBrowserTesting服务器
* Choose a Selenium Grid to connect to选择要连接的Selenium网格
* Choose a database to save results to选择要将结果保存到的数据库
* Choose a proxy server to connect to选择要连接的代理服务器

...and more!

#### **Examples:**

(These are run from the **[examples](https://github.com/seleniumbase/SeleniumBase/tree/master/examples)** folder.)

```bash
pytest my_first_test.py

pytest my_first_test.py --demo_mode --browser=chrome

pytest my_first_test.py --browser=firefox

pytest test_suite.py --html=report.html

nosetests test_suite.py --report --show_report

pytest test_suite.py --headless -n 4

pytest test_suite.py --reruns 1 --reruns-delay 2

pytest test_suite.py --server=IP_ADDRESS --port=4444

pytest test_fail.py --pdb -s

pytest proxy_test.py --proxy=IP_ADDRESS:PORT

pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT

pytest user_agent_test.py --agent="USER-AGENT STRING"

pytest my_first_test.py --settings_file=custom_settings.py
```

You can interchange **pytest** with **nosetests**, but using pytest is strongly recommended because developers stopped supporting nosetests. Chrome is the default browser if not specified.
您可以将**pytest**与**nosetests**交换，但是强烈建议使用pytest，因为开发人员已经不再支持nosetest了。如果没有指定，Chrome是默认浏览器。

(NOTE: If you're using **pytest** for running tests outside of the SeleniumBase repo, **you'll want a copy of [pytest.ini](https://github.com/seleniumbase/SeleniumBase/blob/master/pytest.ini) at the base of the new folder structure**. If using **nosetests**, the same applies for [setup.cfg](https://github.com/seleniumbase/SeleniumBase/blob/master/setup.cfg).)
(注意:如果您使用**pytest**在SeleniumBase repo之外运行测试，**您需要在新文件夹结构**的底部得到一个副本。如果使用**nosetests**，同样适用

An easy way to override seleniumbase/config/settings.py is by using a custom settings file.
Here's the command-line option to add to tests: 
覆盖seleniumbase/config/settings.py的一个简单方法是使用自定义设置文件。下面是添加到测试中的命令行选项:(See [examples/custom_settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/custom_settings.py))
``--settings_file=custom_settings.py``
(Settings include default timeout values, a two-factor auth key, DB credentials, S3 credentials, and other important settings used by tests.)
(设置包括默认超时值、双因素验证键、DB凭据、S3凭据和测试使用的其他重要设置。)

#### **Running tests on [BrowserStack](https://www.browserstack.com/automate#)'s Selenium Grid, the [Sauce Labs](https://saucelabs.com/products/open-source-frameworks/selenium) Selenium Grid, the [TestingBot](https://testingbot.com/features) Selenium Grid, (or your own):**

Here's how to connect to a BrowserStack Selenium Grid server for running tests:
这里是如何连接到一个浏览器堆栈Selenium网络服务器运行测试:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.browserstack.com --port=80
```

Here's how to connect to a Sauce Labs Selenium Grid server for running tests:
```bash
pytest my_first_test.py --server=USERNAME:KEY@ondemand.saucelabs.com --port=80
```

Here's how to connect to a TestingBot Selenium Grid server for running tests:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.testingbot.com --port=80
```

Here's how to connect to a CrossBrowserTesting Selenium Grid server for running tests:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.crossbrowsertesting.com --port=80
```

Here's how to connect to a LambdaTest Selenium Grid server for running tests:
```bash
pytest my_first_test.py --server=USERNAME:KEY@hub.lambdatest.com --port=80
```

Or you can create your own Selenium Grid for test distribution. ([See this ReadMe for details](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/utilities/selenium_grid/ReadMe.md))
或者您可以为测试分布创建自己的Selenium网络。

#### **Example tests using Logging:**

```bash
pytest test_suite.py --browser=chrome
```
(During test failures, logs and screenshots from the most recent test run will get saved to the ``latest_logs/`` folder. Those logs will get moved to ``archived_logs/`` if you have ARCHIVE_EXISTING_LOGS set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), otherwise log files with be cleaned up at the start of the next test run.)
(在测试失败期间，最近一次测试运行的日志和屏幕截图将保存到' ' latest_logs/ ' '文件夹中。如果您将ARCHIVE_EXISTING_LOGS设置为True，那么这些日志将被移动到' ' archived_logs/ ' '中，否则日志文件将在下一次测试运行开始时被清除。

#### **Demo Mode:**

If any test is moving too fast for your eyes to see what's going on, you can run it in **Demo Mode** by adding ``--demo_mode`` on the command line, which pauses the browser briefly between actions, highlights page elements being acted on, and lets you know what test assertions are happening in real time:
如果任何测试移动太快对你的眼睛看到发生了什么,您可以运行它通过添加" **演示模式**——demo_mode”“在命令行上,暂停浏览器之间的短暂行为,强调页面元素被付诸行动,并让你知道测试断言是什么发生在真正的时间:

```bash
pytest my_first_test.py --browser=chrome --demo_mode
```

You can override the default wait time by either updating [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py) or by using ``--demo_sleep={NUM}`` when using Demo Mode. (NOTE: If you use ``--demo_sleep={NUM}`` without using ``--demo_mode``, nothing will happen.)
您可以通过更新或在使用演示模式时使用 ``--demo_sleep={NUM}`` 来覆盖默认的等待时间。(注意:如果你使用 ``--demo_sleep={NUM}`` 而不使用 ``--demo_mode``，什么都不会发生。)

```bash
pytest my_first_test.py --browser=chrome --demo_mode --demo_sleep=1.2
```

#### **Passing additional data to tests:**

If you want to pass additional data from the command line to your tests, you can use ``--data=STRING``. Now inside your tests, you can use ``self.data`` to access that.
如果希望从命令行向测试传递额外的数据，可以使用 ``--data=STRING``。现在在你的测试中，你可以使用 ``self.data`` 访问。

#### **Running tests multithreaded:**
#### **多线程运行测试:**

To run Pytest multithreaded on multiple CPUs at the same time, add ``-n=NUM`` or ``-n NUM`` on the command line, where NUM is the number of CPUs you want to use.
要在多个cpu上同时运行Pytest多线程，请在命令行中添加 ``-n=NUM`` 或 ``-n NUM`` ，其中NUM是您希望使用的cpu数量。

#### **Retrying failing tests automatically:**
#### **自动重试失败的测试:**

You can use ``--reruns NUM`` to retry failing tests that many times. Use ``--reruns-delay SECONDS`` to wait that many seconds between retries. Example:
您可以使用 ``--reruns NUM`` 多次重试失败的测试。使用 ``--reruns-delay SECONDS`` 在重试之间等待那么多秒。例子:
```
pytest --reruns 5 --reruns-delay 1
```

#### **Debugging tests:**
#### **调试测试:**

**You can use the following code snippets in your scripts to help you debug issues:**
**您可以在您的脚本中使用以下代码片段来帮助您调试问题:**
```python
import time; time.sleep(5)  # sleep for 5 seconds (add this after the line you want to pause on)
import ipdb; ipdb.set_trace()  # waits for your command. n = next line of current method, c = continue, s = step / next executed line (will jump)
import pytest; pytest.set_trace()  # similar to ipdb, but specific to pytest
```

**To pause an active test that throws an exception or error, add ``--pdb -s``:**
**若要暂停引发异常或错误的活动测试，请添加 ``--pdb -s``:**

```bash
pytest my_first_test.py --browser=chrome --pdb -s
```

The code above will leave your browser window open in case there's a failure. (ipdb commands: 'c', 's', 'n' => continue, step, next).
上面的代码将在出现故障时打开浏览器窗口。(ipdb命令:'c'， 's'， 'n' =>继续，步骤，下一步)。

#### **Pytest Reports:**
#### **Pytest报告:**

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.
使用 ``--html=report.html`` 在您的测试套件完成后，html ' '为您提供了一个奇特的名称报告。

```bash
pytest test_suite.py --html=report.html
```
![](https://cdn2.hubspot.net/hubfs/100006/images/PytestReport.png "Example Pytest Report")

#### **Nosetest Reports:**
#### **Nosetest报告:**

The ``--report`` option gives you a fancy report after your test suite completes.
 ``--report`` 选项将在测试套件完成后为您提供一个漂亮的报告。

```bash
nosetests test_suite.py --report
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png" title="Example Nosetest Report" height="420">

(NOTE: You can add ``--show_report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show_report`` when running tests locally because it pauses the test run.)
(注意:您可以添加 ``--show_report`` 来在测试套件完成后立即显示Nosetest报告。仅在本地运行测试时使用 ``--show_report`` ，因为它会暂停测试运行。)

Here are some other useful command-line options that come with Pytest:
下面是Pytest附带的一些其他有用的命令行选项:
```bash
-v  # 打印每个测试的完整测试名。
-q  # 在运行测试时，在控制台输出中打印更少的细节。
-x  # 到达第一个故障后，停止运行测试。
--html=report.html  # 在测试完成后创建详细的测试报告。(使用pytest-html插件)
--collect-only  # Show what tests would get run without actually running them.显示在不实际运行测试的情况下会运行哪些测试。
-s  # 查看打印语句。(在默认情况下应该是打开的，并且有pytest.ini。)
-n=NUM  # 使用多个线程进行测试。(加速测试运行!)
```

SeleniumBase provides additional Pytest command-line options for tests:
SeleniumBase为测试提供了额外的Pytest命令行选项:
```bash
--browser=BROWSER  # (The web browser to use.)
--cap_file=FILE  # (The web browser's desired capabilities to use.)(web浏览器需要使用的功能。)
--settings_file=FILE  # (Overrides SeleniumBase settings.py values.)(覆盖settings.py的值。)
--env=ENV  # (Set a test environment. Use "self.env" to use this in tests.)设置一个测试环境
--data=DATA  # (Extra data to pass to tests. Use "self.data" in tests.)需要通过测试的额外数据。
--user_data_dir=DIR  # (Set the Chrome user data directory to use.)设置Chrome用户数据目录使用。
--server=SERVER  # (The server / IP address used by the tests.)测试使用的服务器/ IP地址。
--port=PORT  # (The port that's used by the test server.)测试服务器使用的端口。
--proxy=SERVER:PORT  # (This is the proxy server:port combo used by tests.)这是测试使用的 server:port 代理组合。
--agent=STRING  # (This designates the web browser's User Agent to use.)这指定了web浏览器的用户代理。
--extension_zip=ZIP  # (Load a Chrome Extension .zip file, comma-separated.)加载一个Chrome扩展名。zip文件，逗号分隔。
--extension_dir=DIR  # (Load a Chrome Extension directory, comma-separated.)加载一个Chrome扩展目录，逗号分隔。
--headless  # (The option to run tests headlessly. The default on Linux OS.)不加思索地运行测试的选项。Linux操作系统上的默认设置
--headed  # (The option to run tests with a GUI on Linux OS.)在Linux操作系统上使用GUI运行测试的选项。
--start_page=URL  # (The starting URL for the web browser when tests begin.)测试开始时web浏览器的起始URL。
--log_path=LOG_PATH  # (The directory where log files get saved to.)保存日志文件的目录。
--archive_logs  # (Archive old log files instead of deleting them.)归档旧的日志文件，而不是删除它们。
--slow  # (The option to slow down the automation.)降低自动化速度的选项。
--demo  # (The option to visually see test actions as they occur.)当测试动作发生时，可视地查看它们的选项。
--demo_sleep=SECONDS  # (The option to wait longer after Demo Mode actions.)选择等待更长的演示模式动作后。
--highlights=NUM  # (Number of highlight animations for Demo Mode actions.)演示模式动作的高亮动画数量。
--message_duration=SECONDS  # (The time length for Messenger alerts.)Messenger警报的时间长度。
--check_js  # (The option to check for JavaScript errors after page loads.)页面加载后检查JavaScript错误的选项。
--ad_block  # (The option to block some display ads after page loads.)在页面加载后阻止一些显示广告的选项。
--verify_delay=SECONDS  # (The delay before MasterQA verification checks.)延迟之前的MasterQA验证检查。
--disable_csp  # (This disables the Content Security Policy of websites.)这将禁用网站的内容安全策略
--enable_sync  # (The option to enable "Chrome Sync".)启用“Chrome同步”选项
--maximize_window  # (The option to start with the web browser maximized.)选择从web浏览器开始最大化。
--save_screenshot  # (The option to save a screenshot after each test.)在每次测试后保存截图的选项。
--visual_baseline  # (Set the visual baseline for Visual/Layout tests.)设置视觉/布局测试的视觉基线。
--timeout_multiplier=MULTIPLIER  # (Multiplies the default timeout values.)将缺省超时值相乘。
```
(有关详细信息，请参阅命令行选项的完整列表 **[here](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/plugins/pytest_plugin.py)**.)

#### **Using a Proxy Server:**
#### **使用代理服务器:**

If you wish to use a proxy server for your browser tests (Chrome and Firefox only), you can add ``--proxy=IP_ADDRESS:PORT`` as an argument on the command line.
如果希望为浏览器测试使用代理服务器，可以在命令行中添加参数。 ``--proxy=IP_ADDRESS:PORT`` 

```bash
pytest proxy_test.py --proxy=IP_ADDRESS:PORT
```

If the proxy server that you wish to use requires authentication, you can do the following (Chrome only):
如果你想使用的代理服务器需要认证，你可以做以下事情(仅限Chrome):

```bash
pytest proxy_test.py --proxy=USERNAME:PASSWORD@IP_ADDRESS:PORT
```

To make things easier, you can add your frequently-used proxies to PROXY_LIST in [proxy_list.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/proxy_list.py), and then use ``--proxy=KEY_FROM_PROXY_LIST`` to use the IP_ADDRESS:PORT of that key.
为了使事情变得更简单，您可以将您经常使用的代理添加到PROXY_LIST中，然后使用 ``--proxy=KEY_FROM_PROXY_LIST`` 来使用该键。
```bash
pytest proxy_test.py --proxy=proxy1
```

#### **Changing the User-Agent:**
#### **改变用户代理:**

If you wish to change the User-Agent for your browser tests (Chrome and Firefox only), you can add ``--agent="USER-AGENT STRING"`` as an argument on the command line.
如果您希望为您的浏览器测试(仅限Chrome和Firefox)更改用户代理，您可以在命令行中添加 ``--agent="USER-AGENT STRING"`` 作为参数。

```bash
pytest user_agent_test.py --agent="Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU"
```
