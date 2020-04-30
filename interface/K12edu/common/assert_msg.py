import json


def assert_res(res_text, except_tip=''):
    """
    断言服务器返回是否操作成功
    :param res_text: 服务器返回值
    :param except_tip: 错误操作的提示
    :return: None
    """
    try:
        res_dic = json.loads(res_text)
        actual_tip = res_dic['msg']
        try:
            assert '操作成功' == actual_tip
            print(actual_tip)
        except AssertionError as a:
            print(f'{a} 尝试断言错误操作的提示')
            try:
                assert actual_tip == except_tip
                print('错误提示断言成功')
            except AssertionError as s:
                print(f'{s} 接口出现异常"{actual_tip}"，'
                      f'不再尝试断言，请查看传参是否错误')
        except BaseException as e:
            print(f'出现未知异常：{e}')
    except json.JSONDecodeError:
        print(f'没有返回字典格式，服务器返回为"{res_text}"')
    except KeyError as k:
        print(f'{k}没有找到msg')
    except BaseException as x:
        print(f'出现未知异常：{x}')
