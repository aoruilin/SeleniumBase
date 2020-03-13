import time
import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.picture_list_code import turtle_code
from interface.K12edu.common.parameter_for_others import ParameterForOthers


def save_draft_for_works(parameter):
    """
    保存草稿后发布作品
    :return:
    """
    code = turtle_code()
    url = f'{parameter.ip[:-8]}/ddc-port/play/saveDraft'
    data = {
        "codeList": [
            {
                "fileContent": code,
                "fileName": "main.py",
                "fileType": 1,
                "rwType": 1
            }
        ],
        "id": "0",
        "title": "接口保存草稿",
        "type": 0
    }
    response = requests.post(url=url, headers=parameter.headers, json=data)
    assert_res(response.text)


# save_draft_for_works(ParameterForOthers(identity='student'))
