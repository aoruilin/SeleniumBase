import traceback

import wrapt

from ui_auto.base.logs import log


def log_decorator(log_path):
    @wrapt.decorator
    def inner_decorator(wrapped, instance, args, kwargs):
        func_name = wrapped.__name__
        log(log_path, f'{func_name}开始执行')
        try:
            wrapped(*args)
        except AssertionError as e:
            log(log_path, f'{func_name}执行过程中出现异常，具体信息为：{str(e)}')
        # except:
        #     log(log_path, f'{func_name}执行过程中出现异常，具体信息为：{traceback.format_exc()}')
        #     log(log_path, '出现非断言异常，速度放慢并进行一次重试')
        #     args[0].tearDown()
        #     args[0].setUp(except_tag=True)
        #     try:
        #         wrapped(*args)
        #     except:
        #         log(log_path, f'{func_name}执行过程中又出现异常，不再重试，具体异常为：{traceback.format_exc()}')
        log(log_path, f'{func_name}方法执行结束\n')

    return inner_decorator
