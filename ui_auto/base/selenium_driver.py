from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui_auto.base.config import Config
from ui_auto.base.logs import log
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SeleniumDriver:

    def __init__(self, log_path, url=None, browser=None, except_tag=False):
        self.log_path = log_path
        self.url = url
        self.check_browser(browser)
        self.driver = self.get_webdriver()
        self.set_timeout()
        self.speed = Config.except_speed if except_tag else Config.default_speed
        self.loading_mask_loc = By.XPATH, '//div[@class="el-loading-mask is-fullscreen"]'  # 遮罩层

    def set_timeout(self):
        timeout = Config.timeout
        self.driver.implicitly_wait(timeout)
        self.driver.set_page_load_timeout(timeout)
        self.driver.set_script_timeout(timeout)

    def check_browser(self, browser):
        if browser:
            browser = str.capitalize(browser)
            browser_type_list = Config.browser_type
            if browser in browser_type_list:
                self.browser = browser
            else:
                raise TypeError(f'不支持该浏览器，支持的浏览器为{browser_type_list},你指定的浏览器为{browser}')
        else:
            self.browser = Config.default_browser

    def get_webdriver(self):
        lower = self.browser.lower()
        if self.url is None:
            if 'chrome' == lower:
                chrome_options = Options()
                prefs = {
                    'profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player': 1
                }
                chrome_options.add_experimental_option('prefs', prefs)
                driver = webdriver.Chrome(chrome_options=chrome_options)
                driver.maximize_window()
            elif 'firefox' == lower:
                p = r'C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\stzonx7l.default'
                profile = webdriver.FirefoxProfile(p)
                profile.set_preference('plugin.state.flash', 2)
                driver = webdriver.Firefox(profile)
                driver.maximize_window()
            elif 'ie' == lower:
                driver = webdriver.Ie()
            else:
                raise TypeError('获取浏览器驱动时，驱动未定义')
        else:
            if 'chrome' == lower:
                desired_capabilities = DesiredCapabilities.CHROME
            elif 'firefox' == lower:
                desired_capabilities = DesiredCapabilities.FIREFOX
            elif 'ie' == lower:
                desired_capabilities = DesiredCapabilities.INTERNETEXPLORER
            else:
                raise TypeError('获取浏览器驱动时，驱动未定义')
            driver = WebDriver(command_executor=self.url, desired_capabilities=desired_capabilities)
            if 'chrome' == lower:
                driver.maximize_window()

        return driver

    def get(self, url):
        sleep(self.speed)
        log(self.log_path, f'打开被测网站，地址为{url}')
        self.driver.get(url)

    def quit(self):
        self.driver.quit()

    def find_element(self, by, value, msg=None, content=None, send_keys=False, click=False, clear=False, tag=True,
                     loading=False, no_wait=False, text=False):
        if loading:
            log(self.log_path, '检查遮罩层是否隐藏')
            WebDriverWait(self.driver, 7).until(EC.invisibility_of_element(self.loading_mask_loc))
        if no_wait:
            sleep(0.2)
        else:
            if tag:
                sleep(self.speed)
            else:
                sleep(0.8)

        if send_keys:
            log(self.log_path, f'"{msg}" 中输入"{content}"    对象 {value} 操作特征：{by}')
            return self.driver.find_element(by=by, value=value).send_keys(content)
        elif click:
            log(self.log_path, f'点击 "{msg}"   对象 {value} 操作特征：{by}')
            return self.driver.find_element(by=by, value=value).click()
        elif clear:
            log(self.log_path, f'清除 "{msg}" 中的内容    对象 {value} 操作特征：{by}')
            return self.driver.find_element(by=by, value=value).clear()
        elif text:
            log(self.log_path, f'取出 "{msg}" 中的文本内容      对象 {value} 操作特征：{by}')
            return self.driver.find_element(by=by, value=value).text
        else:
            log(self.log_path, f'定位 "{msg}"    操作对象：{value}   操作特征：{by}')
            return self.driver.find_element(by=by, value=value)

    def find_elements(self, by, value, msg=None, tag=True, loading=False, no_wait=False):
        if loading:
            log(self.log_path, '检查遮罩层是否隐藏')
            WebDriverWait(self.driver, 7).until(EC.invisibility_of_element(self.loading_mask_loc))
        if no_wait:
            sleep(0.2)
        else:
            if tag:
                sleep(self.speed)
            else:
                sleep(0.8)
        log(self.log_path, f'定位 "{msg}" 返回元素列表      操作对象：{value}   操作特征：{by}')

        return self.driver.find_elements(by=by, value=value)

    def find_element_by_xpath(self, xpath, msg=None, content=None, send_keys=False, click=False, clear=False, tag=True,
                              loading=False, no_wait=False, text=False):
        if loading:
            log(self.log_path, '检查遮罩层是否隐藏')
            WebDriverWait(self.driver, 7).until(EC.invisibility_of_element(self.loading_mask_loc))
        if no_wait:
            sleep(0.2)
        else:
            if tag:
                sleep(self.speed)
            else:
                sleep(0.8)

        if send_keys:
            log(self.log_path, f'"{msg}" 中输入"{content}"    操作对象{xpath}')
            return self.driver.find_element_by_xpath(xpath).send_keys(content)
        elif click:
            log(self.log_path, f'点击 "{msg}"   操作对象{xpath}')
            return self.driver.find_element_by_xpath(xpath).click()
        elif clear:
            log(self.log_path, f'清除 "{msg}"    操作对象{xpath}')
            return self.driver.find_element_by_xpath(xpath).clear()
        elif text:
            log(self.log_path, f'取出 "{msg}" 中的文本内容    操作对象{xpath}')
            return self.driver.find_element_by_xpath(xpath).text
        else:
            log(self.log_path, f'定位 "{msg}"    操作对象{xpath}')
            return self.driver.find_element_by_xpath(xpath)

    def find_elements_by_xpath(self, xpath, msg=None, tag=True, loading=False, no_wait=False):
        if loading:
            log(self.log_path, '检查遮罩层是否隐藏')
            WebDriverWait(self.driver, 7).until(EC.invisibility_of_element(self.loading_mask_loc))
        if no_wait:
            sleep(0.2)
        else:
            if tag:
                sleep(self.speed)
            else:
                sleep(0.8)
        log(self.log_path, f'定位 "{msg}" 返回元素列表    操作对象{xpath}')

        return self.driver.find_elements_by_xpath(xpath)

    def find_element_by_tag_name(self, tag_name, msg=None, content=None, send_keys=False, click=False, clear=False,
                                 tag=True,loading=False, no_wait=False, text=False):
        if loading:
            log(self.log_path, '检查遮罩层是否隐藏')
            WebDriverWait(self.driver, 7).until(EC.invisibility_of_element(self.loading_mask_loc))
        if no_wait:
            sleep(0.2)
        else:
            if tag:
                sleep(self.speed)
            else:
                sleep(0.8)

        if send_keys:
            log(self.log_path, f'"{msg}" 中输入"{content}"    操作对象{tag_name}')
            return self.driver.find_element_by_tag_name(tag_name).send_keys(content)
        elif click:
            log(self.log_path, f'点击 "{msg}"   操作对象{tag_name}')
            return self.driver.find_element_by_tag_name(tag_name).click()
        elif clear:
            log(self.log_path, f'清除 "{msg}"    操作对象{tag_name}')
            return self.driver.find_element_by_tag_name(tag_name).clear()
        elif text:
            log(self.log_path, f'取出 "{msg}" 中的文本内容    操作对象{tag_name}')
            return self.driver.find_element_by_tag_name(tag_name).text
        else:
            log(self.log_path, f'定位 "{msg}"    操作对象{tag_name}')
            return self.driver.find_element_by_tag_name(tag_name)

    def find_elements_by_tag_name(self, tag_name, msg=None, tag=True, loading=False, no_wait=False):
        if loading:
            log(self.log_path, '检查遮罩层是否隐藏')
            WebDriverWait(self.driver, 7).until(EC.invisibility_of_element(self.loading_mask_loc))
        if no_wait:
            sleep(0.2)
        else:
            if tag:
                sleep(self.speed)
            else:
                sleep(0.8)
        log(self.log_path, f'定位 "{msg}" 返回元素列表    操作对象{tag_name}')

        return self.driver.find_elements_by_tag_name(tag_name)

    def window_handles(self, index_num):
        sleep(self.speed)
        log(self.log_path, f'切换到第{index_num + 1}个窗口的句柄')

        return self.driver.window_handles[index_num]

    def switch_to_window(self, handle):
        log(self.log_path, '切换到该窗口')
        sleep(0.5)

        return self.driver.switch_to.window(handle)

    def switch_to_frame(self, frame):
        log(self.log_path, '切换到子页面')
        sleep(1)

        return self.driver.switch_to.frame(frame)

    def switch_to_default_content(self):
        log(self.log_path, '切换到默认页面')
        sleep(1)

        return self.driver.switch_to.default_content()

    def close(self):
        sleep(self.speed)
        log(self.log_path, '关闭当前窗口')

        return self.driver.close()

    def refresh(self):
        log(self.log_path, '刷新页面')
        sleep(self.speed)

        return self.driver.refresh()

    def back(self):
        log(self.log_path, '后退上一页')
        sleep(2)

        return self.driver.back()

    def action_chains(self, element, msg=None):
        log(self.log_path, f'鼠标移到 {msg} 上')
        ActionChains(self.driver).move_to_element(element).perform()
        sleep(0.5)

    def webdriver_wait(self):

        return WebDriverWait(self.driver, 15)

    def element_presence(self, element):
        *element, msg = element
        log(self.log_path, f'等待 "{msg}" 出现    对象：{element}')

        return EC.presence_of_element_located(element)

    def element_clickable(self, element):
        *element, msg = element
        log(self.log_path, f'检查元素 "{msg}" 是否存在并可以点击  对象：{element}')

        return EC.element_to_be_clickable(element)

    def element_invisibility(self, element):
        *element, msg = element
        log(self.log_path, f'检查元素 "{msg}" 是否不可见  对象：{element}')

        return EC.invisibility_of_element_located(element)

    def execute_script(self, script):
        log(self.log_path, f'执行{script}')

        return self.driver.execute_script(script)
