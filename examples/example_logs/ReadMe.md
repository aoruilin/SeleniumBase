#### Logging, Screenshots, and Reports examples

Log files in [example_logs/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples/example_logs) were generated when [test_fail.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/test_fail.py) ran and failed. By default, logs are saved to ``latest_logs/``. If ARCHIVE_EXISTING_LOGS is set to True in [settings.py](https://github.com/seleniumbase/SeleniumBase/blob/master/seleniumbase/config/settings.py), past logs get saved to ``archived_logs/``.

```bash
pytest test_fail.py --browser=chrome

nosetests test_fail.py --browser=firefox
```

**Expected log files generated during failures:**
**故障期间生成的预期日志文件:**
* [basic_test_info.txt](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/basic_test_info.txt)
* [page_source.html](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/page_source.html)
* [screenshot.png](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/example_logs/screenshot.png)

---
**In addition to logging, you can also generate test reports:**
**除了日志记录，您还可以生成测试报告:**

Reports are most useful when running large test suites. Pytest and Nosetest reports are handled differently.
报告在运行大型测试套件时最有用。Pytest和Nosetest报告的处理方式不同。

#### **Pytest Reports:**

Using ``--html=report.html`` gives you a fancy report of the name specified after your test suite completes.
使用 ``--html=report.html`` 在您的测试套件完成后，为您提供报告。

```bash
pytest test_suite.py --html=report.html
```
![](https://cdn2.hubspot.net/hubfs/100006/images/PytestReport.png "Example Pytest Report")

#### **Nosetest Reports:**

The ``--report`` option gives you a fancy report after your test suite completes. (Requires ``--with-testing_base`` to also be set when ``--report`` is used because it's part of that plugin.)
``--report``选项将在测试套件完成后为您提供一个漂亮的报告。（需要 ``--with-testing_base`` 在使用 ``--report`` 时也被设置，因为它是插件的一部分。）

```bash
nosetests test_suite.py --report --browser=chrome
```
<img src="https://cdn2.hubspot.net/hubfs/100006/images/Test_Report_2.png" title="Example Nosetest Report" height="420">

(NOTE: You can add ``--show_report`` to immediately display Nosetest reports after the test suite completes. Only use ``--show_report`` when running tests locally because it pauses the test run.)
（注意：注意:您可以添加 ``--show_report`` 来在测试套件完成后立即显示Nosetest报告。仅在本地运行测试时使用 ``--show_report`` 因为它会暂停测试运行。）