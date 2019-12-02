from selenium.webdriver.common.keys import Keys


def input_code(code, code_input):
    code_input.send_keys(Keys.CONTROL, 'a')
    code_input.send_keys(Keys.BACKSPACE)
    for c in code.split("\n"):
        code_input.send_keys(c)
        if c != "":
            code_input.send_keys(Keys.ESCAPE)
            code_input.send_keys(Keys.ENTER)
            code_input.send_keys(Keys.HOME)
            code_input.send_keys(Keys.SHIFT, Keys.TAB)
        else:
            code_input.send_keys(Keys.ENTER)
