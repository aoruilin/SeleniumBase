"""
This module contains a set of methods that can be used for page loads and
for waiting for elements to appear on a page.

These methods improve on and expand existing WebDriver commands.
Improvements include making WebDriver commands more robust and more reliable
by giving page elements enough time to load before taking action on them.

The default option for searching for elements is by CSS Selector.
This can be changed by overriding the "By" parameter.
此模块包含一组可用于页面加载和
用于等待元素出现在页面上。

这些方法改进并扩展了现有的WebDriver命令。
改进包括使WebDriver命令更健壮、更可靠
在对页面元素采取操作之前，给它们足够的加载时间。

搜索元素的默认选项是通过CSS选择器。
这可以通过覆盖“by”参数来更改
Options are:
By.CSS_SELECTOR
By.CLASS_NAME
By.ID
By.NAME
By.LINK_TEXT
By.XPATH
By.TAG_NAME
By.PARTIAL_LINK_TEXT
"""

import codecs
import os
import sys
import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.errorhandler import ElementNotVisibleException
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from selenium.webdriver.remote.errorhandler import NoAlertPresentException
from selenium.webdriver.remote.errorhandler import NoSuchFrameException
from selenium.webdriver.remote.errorhandler import NoSuchWindowException
from seleniumbase.config import settings
from seleniumbase.core import log_helper


def is_element_present(driver, selector, by=By.CSS_SELECTOR):
    """
    Returns whether the specified element selector is present on the page.
    返回指定的元素是否出现在页面上。
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    @Returns
    Boolean (is element present)
    """
    try:
        driver.find_element(by=by, value=selector)
        return True
    except Exception:
        return False


def is_element_visible(driver, selector, by=By.CSS_SELECTOR):
    """
    Returns whether the specified element selector is visible on the page.
    返回指定的元素选择器在页上是否可见。
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    @Returns
    Boolean (is element visible)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_displayed()
    except Exception:
        return False


def is_text_visible(driver, text, selector, by=By.CSS_SELECTOR):
    """
    Returns whether the specified text is visible in the specified selector.
    返回指定的文本在指定的定位器中是否可见。
    @Params
    driver - the webdriver object (required)
    text - the text string to search for
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    @Returns
    Boolean (is text visible)
    """
    try:
        element = driver.find_element(by=by, value=selector)
        return element.is_displayed() and text in element.text
    except Exception:
        return False


def hover_on_element(driver, selector, by=By.CSS_SELECTOR):
    """
    Fires the hover event for the specified element by the given selector.
    通过给定的选择器触发指定元素的悬停事件。
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    """
    element = driver.find_element(by=by, value=selector)
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()


def hover_element(driver, element):
    """
    Similar to hover_on_element(), but uses found element, not a selector.
    类似于hover_on_element()，但是使用的是found元素，而不是选择器。
    """
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()


def hover_and_click(driver, hover_selector, click_selector,
                    hover_by=By.CSS_SELECTOR, click_by=By.CSS_SELECTOR,
                    timeout=settings.SMALL_TIMEOUT):
    """
    Fires the hover event for a specified element by a given selector, then
    clicks on another element specified. Useful for dropdown hover based menus.
    通过给定的选择器触发指定元素的悬停事件
    单击指定的另一个元素。比如鼠标悬停出现的菜单。
    @Params
    driver - the webdriver object (required)
    hover_selector - the css selector to hover over (required)
    click_selector - the css selector to click on (required)
    hover_by - the hover selector type to search by (Default: By.CSS_SELECTOR)
    click_by - the click selector type to search by (Default: By.CSS_SELECTOR)
    timeout - number of seconds to wait for click element to appear after hover
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    element = driver.find_element(by=hover_by, value=hover_selector)
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=click_by, value=click_selector)
            element.click()
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise NoSuchElementException(
        "%s秒后{%s}元素仍不存在！" %
        (timeout, click_selector))


def hover_element_and_click(driver, element, click_selector,
                            click_by=By.CSS_SELECTOR,
                            timeout=settings.SMALL_TIMEOUT):
    """
    Similar to hover_and_click(), but assumes top element is already found.
    与hover_and_click()类似，但假设已经找到top元素。
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=click_by, value=click_selector)
            element.click()
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise NoSuchElementException(
        "%s秒后{%s}元素仍不存在！" %
        (timeout, click_selector))


def hover_element_and_double_click(driver, element, click_selector,
                                   click_by=By.CSS_SELECTOR,
                                   timeout=settings.SMALL_TIMEOUT):
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()
    for x in range(int(timeout * 10)):
        try:
            element_2 = driver.find_element(by=click_by, value=click_selector)
            actions = ActionChains(driver)
            actions.move_to_element(element_2)
            actions.double_click(element_2)
            actions.perform()
            return element_2
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise NoSuchElementException(
        "%s秒后{%s}元素仍不存在！" %
        (timeout, click_selector))


def wait_for_element_present(driver, selector, by=By.CSS_SELECTOR,
                             timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the element is present on the page. The element can be
    invisible. Raises an exception if the element does not appear in the
    specified timeout.
    通过给定的选择器搜索指定的元素。返回
    元素对象(如果该元素出现在页面上)。元素可以是
    看不见的。方法中不出现元素时引发异常
    指定的超时。
    @Params
    driver - the webdriver object
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object
    """
    element = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            return element
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    if not element:
        raise NoSuchElementException(
            "%s秒后{%s}元素仍不存在！" % (
                timeout, selector))


def wait_for_element_visible(driver, selector, by=By.CSS_SELECTOR,
                             timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the element is present and visible on the page.
    Raises an exception if the element does not appear in the
    specified timeout.
    通过给定的选择器搜索指定的元素。
    如果该元素在页面上存在且可见则返回元素对象，。
    方法中不出现元素时引发异常
    指定的超时。
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds

    @Returns
    A web element object
    """
    element = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            if element.is_displayed():
                return element
            else:
                element = None
                raise Exception()
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element and by != By.LINK_TEXT:
        raise ElementNotVisibleException(
            "%s秒后{%s}元素仍不存在！%s" % (
                timeout, selector, plural))
    if not element and by == By.LINK_TEXT:
        raise ElementNotVisibleException(
            "%s秒后{%s}链接文本仍不存在！%s" % (
                selector, timeout, plural))


def wait_for_text_visible(driver, text, selector, by=By.CSS_SELECTOR,
                          timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the text is present in the element and visible
    on the page. Raises an exception if the text or element do not appear
    in the specified timeout.
    通过给定的选择器搜索指定的元素。
    如果文本出现在元素文本中并且是可见的则返回元素对象，
    如果文本或元素在指定的超时内未出现，则引发异常。
    @Params
    driver - the webdriver object (required)
    text - the text that is being searched for in the element (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """
    element = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            if element.is_displayed() and text in element.text:
                return element
            else:
                element = None
                raise Exception()
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element:
        raise ElementNotVisibleException(
            "%s秒后期望的元素{%s}中的文本{%s}仍未出现！%s" %
            (timeout, selector, text, plural))


def wait_for_exact_text_visible(driver, text, selector, by=By.CSS_SELECTOR,
                                timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector. Returns the
    element object if the text matches exactly with the text in the element,
    and the text is visible.
    Raises an exception if the text or element do not appear
    in the specified timeout.
    通过给定的选择器搜索指定的元素。
    如果文本与元素中的文本完全匹配且是可见的，返回元素对象，
    如果文本或元素在指定的超时内未出现，则引发异常。
    @Params
    driver - the webdriver object (required)
    text - the exact text that is expected for the element (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """
    element = None
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            if element.is_displayed() and text.strip() == element.text.strip():
                return element
            else:
                element = None
                raise Exception()
        except Exception:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    if not element:
        raise ElementNotVisibleException(
            "%s秒后期望的元素{%s}中的指定文本{%s}仍未出现！%s" %
            (timeout, selector, text, plural))


def wait_for_element_absent(driver, selector, by=By.CSS_SELECTOR,
                            timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector.
    Raises an exception if the element is still present after the
    specified timeout.
    通过给定的选择器搜索指定的元素。
    指定的超时后如果元素仍然存在，则引发异常。
    @Params
    driver - the webdriver object
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            driver.find_element(by=by, value=selector)
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
        except Exception:
            return True
    plural = "s"
    if timeout == 1:
        plural = ""
    raise Exception("%s秒后元素{%s}仍存在%s！" %
                    (timeout, selector, plural))


def wait_for_element_not_visible(driver, selector, by=By.CSS_SELECTOR,
                                 timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the specified element by the given selector.
    Raises an exception if the element is still visible after the
    specified timeout.
    通过给定的选择器搜索指定的元素。
    指定的超时后如果元素仍然可见，则引发异常。
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for the element in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            element = driver.find_element(by=by, value=selector)
            if element.is_displayed():
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
            else:
                return True
        except Exception:
            return True
    plural = "s"
    if timeout == 1:
        plural = ""
    raise Exception(
        "%s秒后元素{%s}仍可见%s！" % (
            timeout, selector, plural))


def wait_for_text_not_visible(driver, text, selector, by=By.CSS_SELECTOR,
                              timeout=settings.LARGE_TIMEOUT):
    """
    Searches for the text in the element of the given selector on the page.
    Returns True if the text is not visible on the page within the timeout.
    Raises an exception if the text is still present after the timeout.
    在页面上给定选择器的元素中搜索文本。
    如果文本在超时期间在页面上不可见，则返回True。
    如果超时后文本仍然存在，则引发异常。
    @Params
    driver - the webdriver object (required)
    text - the text that is being searched for in the element (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    timeout - the time to wait for elements in seconds
    @Returns
    A web element object that contains the text searched for
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        if not is_text_visible(driver, text, selector, by=by):
            return True
        now_ms = time.time() * 1000.0
        if now_ms >= stop_ms:
            break
        time.sleep(0.1)
    plural = "s"
    if timeout == 1:
        plural = ""
    raise Exception("%s秒后元素{%s}的文本{%s}仍可见%s！" % (timeout, selector, text, plural))


def find_visible_elements(driver, selector, by=By.CSS_SELECTOR):
    """
    Finds all WebElements that match a selector and are visible.
    Similar to webdriver.find_elements.
    查找与定位器匹配且可见的所有WebElements。
    类似于webdriver.find_elements。
    @Params
    driver - the webdriver object (required)
    selector - the locator for identifying the page element (required)
    by - the type of selector being used (Default: By.CSS_SELECTOR)
    """
    elements = driver.find_elements(by=by, value=selector)
    return [element for element in elements if element.is_displayed()]


def save_screenshot(driver, name, folder=None):
    """
    Saves a screenshot to the current directory (or to a subfolder if provided)
    If the folder provided doesn't exist, it will get created.
    The screenshot will be in PNG format.
    将屏幕截图保存到当前目录(或提供的子文件夹)
    如果提供的文件夹不存在，将创建它。
    截图将是PNG格式。
    """
    if "." not in name:
        name = name + ".png"
    if folder:
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % folder
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        screenshot_path = "%s/%s" % (file_path, name)
    else:
        screenshot_path = name
    try:
        element = driver.find_element_by_tag_name('body')
        element_png = element.screenshot_as_png
        with open(screenshot_path, "wb") as file:
            file.write(element_png)
    except Exception:
        if driver:
            driver.get_screenshot_as_file(screenshot_path)
        else:
            pass


def save_page_source(driver, name, folder=None):
    """
    Saves the page HTML to the current directory (or given subfolder).
    If the folder specified doesn't exist, it will get created.
    将页面HTML保存到当前目录(或给定的子文件夹)。
    如果指定的文件夹不存在，将创建它。
    @Params
    name - The file name to save the current page's HTML to.文件名
    folder - The folder to save the file to. (Default = current folder)文件夹
    """
    if "." not in name:
        name = name + ".html"
    if folder:
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % folder
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        html_file_path = "%s/%s" % (file_path, name)
    else:
        html_file_path = name
    page_source = driver.page_source
    html_file = codecs.open(html_file_path, "w+", "utf-8")
    rendered_source = log_helper.get_html_source_with_base_href(
        driver, page_source)
    html_file.write(rendered_source)
    html_file.close()


def _get_last_page(driver):
    try:
        last_page = driver.current_url
    except Exception:
        last_page = '[警告! Browser Not Open!]'
    if len(last_page) < 5:
        last_page = '[警告! Browser Not Open!]'
    return last_page


def save_test_failure_data(driver, name, browser_type, folder=None):
    """
    Saves failure data to the current directory (or to a subfolder if provided)
    If the folder provided doesn't exist, it will get created.
    将报错数据保存到当前目录(或提供的子文件夹中)
    如果提供的文件夹不存在，将创建它。
    :param driver: driver对象
    :param name: 文件名
    :param browser_type: 浏览器
    :param folder: 文件夹
    :return:
    """
    if folder:
        abs_path = os.path.abspath('.')
        file_path = abs_path + "/%s" % folder
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        failure_data_file_path = "%s/%s" % (file_path, name)
    else:
        failure_data_file_path = name
    failure_data_file = codecs.open(failure_data_file_path, "w+", "utf-8")
    last_page = _get_last_page(driver)
    data_to_save = []
    data_to_save.append("Last_Page: %s" % last_page)
    data_to_save.append("Browser: %s " % browser_type)
    data_to_save.append("Traceback: " + ''.join(
        traceback.format_exception(sys.exc_info()[0],
                                   sys.exc_info()[1],
                                   sys.exc_info()[2])))
    failure_data_file.writelines("\r\n".join(data_to_save))
    failure_data_file.close()


def wait_for_and_accept_alert(driver, timeout=settings.LARGE_TIMEOUT):
    """
    Wait for and accept an alert. Returns the text from the alert.
    等待并接受弹框。从弹框返回文本。
    @Params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """
    alert = wait_for_and_switch_to_alert(driver, timeout)
    alert_text = alert.text
    alert.accept()
    return alert_text


def wait_for_and_dismiss_alert(driver, timeout=settings.LARGE_TIMEOUT):
    """
    Wait for and dismiss an alert. Returns the text from the alert.
    等待并解除弹框。从弹框返回文本。
    @Params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """
    alert = wait_for_and_switch_to_alert(driver, timeout)
    alert_text = alert.text
    alert.dismiss()
    return alert_text


def wait_for_and_switch_to_alert(driver, timeout=settings.LARGE_TIMEOUT):
    """
    Wait for a browser alert to appear, and switch to it. This should be usable
    as a drop-in replacement for driver.switch_to.alert when the alert box
    may not exist yet.
    等待浏览器弹窗出现，然后切换到它。
    @Params
    driver - the webdriver object (required)
    timeout - the time to wait for the alert in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            alert = driver.switch_to.alert
            # Raises exception if no alert present
            dummy_variable = alert.text  # noqa
            return alert
        except NoAlertPresentException:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise Exception("%s秒后弹框仍未出现！" % timeout)


def switch_to_frame(driver, frame, timeout=settings.SMALL_TIMEOUT):
    """
    Wait for an iframe to appear, and switch to it. This should be usable
    as a drop-in replacement for driver.switch_to.frame().
    等待iframe出现，然后切换到它。
    可以作为driver.switch_to.frame()的替代。
    @Params
    driver - the webdriver object (required)
    frame - the frame element, name, or index
    timeout - the time to wait for the alert in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    for x in range(int(timeout * 10)):
        try:
            driver.switch_to.frame(frame)
            return True
        except NoSuchFrameException:
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            time.sleep(0.1)
    raise Exception("子页面在%s秒后仍未出现！" % timeout)


def switch_to_window(driver, window, timeout=settings.SMALL_TIMEOUT):
    """
    Wait for a window to appear, and switch to it. This should be usable
    as a drop-in replacement for driver.switch_to.window().
    等待一个窗口出现，然后切换到它。作为driver.switch_to.window()的替代。
    @Params
    driver - the webdriver object (required)
    window - the window index or window handle/窗口索引
    timeout - the time to wait for the window in seconds
    """
    start_ms = time.time() * 1000.0
    stop_ms = start_ms + (timeout * 1000.0)
    if isinstance(window, int):
        for x in range(int(timeout * 10)):
            try:
                window_handle = driver.window_handles[window]
                driver.switch_to.window(window_handle)
                return True
            except IndexError:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
        raise Exception("窗口标签在%s秒后仍未出现！" % timeout)
    else:
        window_handle = window
        for x in range(int(timeout * 10)):
            try:
                driver.switch_to.window(window_handle)
                return True
            except NoSuchWindowException:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
        raise Exception("窗口标签在%s秒后仍未出现！" % timeout)
