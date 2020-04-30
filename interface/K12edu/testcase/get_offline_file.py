import os
import time
import unittest

import requests

from interface.K12edu.common.parameter_for_others import ParameterForOthers


class TestGetOfflineFile(unittest.TestCase):

    def setUp(self):
        self.parameter = ParameterForOthers(identity='teacher')
        self.ip = self.parameter.ip
        self.headers = self.parameter.headers

    def test_01(self):
        series_list = self.parameter.get_series_list()
        for s in series_list:
            os.makedirs(f'E://offline_series{s}', exist_ok=True)
            all_point_resource_id_list = self.parameter.get_all_point_resource_id(s)
            for r in all_point_resource_id_list:
                url = f'{self.ip}/teachcenter/coursemanage/offline/{r["id"]}/{r["resource_id"]}'
                response = requests.get(url=url, headers=self.headers)
                time.sleep(1.5)
                data_ret = response.json()
                msg = data_ret['msg']
                try:
                    self.assertEqual(msg, '操作成功')
                except AssertionError:
                    print(f'{r}资源报错：{msg}')
                else:
                    data_url = data_ret['data']
                    download = requests.get(url=data_url, headers=self.headers)
                    with open(f'E://offline_series{s}/{r["resource_id"]}.zip', 'wb') as zip_file:
                        zip_file.write(download.content)
