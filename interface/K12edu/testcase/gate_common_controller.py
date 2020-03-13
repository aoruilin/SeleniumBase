import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers
from ui_auto.common.mysql import get_practise_code


class GateCommonController(unittest.TestCase):
    """闯关授课首页/公共控制器"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

        self.class_id_list = self.teacher_parm.get_class_list(1, get_all=True)
        self.gate_id_list = [g['gate_id'] for g in self.student_parm.get_point_id_checkpoint(get_all=True)]

    def test_01_buy_goods(self):
        """
        购买商品
        :return:
        """
        goods_id_list = self.student_parm.get_goods_id_list()
        for goods_id in goods_id_list:
            url = f'{self.ip}/pc/gate/common/bugGoods'
            response = requests.get(url=url, headers=self.student_headers,
                                    params=f'goodId={goods_id}&number=1')
            assert_res(response.text)
            time.sleep(1)

    def test_02_get_gate_description(self):
        """
        获取关卡的描述
        :return:
        """
        for gate_id in self.gate_id_list:
            url = f'{self.ip}/pc/gate/common/getGateDescription'
            response = requests.get(url=url, headers=self.teacher_headers,
                                    params=f'gateId={gate_id}&classId={self.class_id_list[0]}')
            assert_res(response.text, '关卡暂未解锁')
            time.sleep(1)
            data_ret = response.json()
            try:
                data_dic = data_ret['data']
                print({data_dic['id']: data_dic['description']})
            except TypeError:
                print(f'接口"//pc/gate/common/getGateDescription"报错，返回{data_ret["msg"]}')

    def test_03_get_gate_list_by_class_id(self):
        """
        通过classId获取关卡列表
        :return:
        """
        series_id_list = self.teacher_parm.get_series_list()
        for s in series_id_list:
            for class_id in self.class_id_list:
                url = f'{self.ip}/pc/gate/common/getGateListByClassId'
                response = requests.get(url=url, headers=self.teacher_headers,
                                        params=f'classId={class_id}&seriesId={s}')
                assert_res(response.text)
                time.sleep(1)
                data_ret = response.json()
                try:
                    print([{i['id']: i['gateName']} for i in data_ret['data']])
                except TypeError:
                    print(f'接口"//pc/gate/common/getGateDescription"报错，返回{data_ret["msg"]}')

    def test_04_get_gate_list_by_series_id(self):
        """
        通过系列Id获取关卡列表
        :return:
        """
        series_id_list = self.student_parm.get_series_list()
        for s in series_id_list:
            url = f'{self.ip}/pc/gate/common/getGateListBySeriesId'
            response = requests.get(url=url, headers=self.teacher_headers,
                                    params=f'seriesId={s}')
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                print([{i['id']: i['gateName']} for i in data_ret['data']])
            except TypeError:
                print(f'接口"//pc/gate/common/getGateListBySeriesId"报错，返回{data_ret["msg"]}')

    def test_05_get_gate_practise_detail(self):
        """
        获取关卡例题练习的详情
        :return:
        """
        class_id = self.class_id_list[0]
        for gate_id in self.gate_id_list:
            try:
                practise_id_list, _ = self.student_parm.get_gate_practise_id_list(gate_id, class_id)
                for practise_id in practise_id_list:
                    url = f'{self.ip}/pc/gate/common/getGatePractiseDetail'
                    response = requests.get(url=url, headers=self.student_headers,
                                            params=f'practiseId={practise_id}&classId={class_id}')
                    assert_res(response.text)
                    time.sleep(1)
                    data_ret = response.json()
                    try:
                        print(f'关卡id：{data_ret["data"]["gateId"]},'
                              f'practise_id:{data_ret["data"]["practiseId"]}'
                              f'title:{data_ret["data"]["title"]}')
                    except TypeError:
                        print(f'接口"/pc/gate/common/getGatePractiseDetail"报错，返回{data_ret["msg"]}')
            except TypeError as t:
                print(t)

    def test_06_get_gate_practise_list(self):
        """
        获取关卡例题练习的列表
        :return:
        """
        for class_id in self.class_id_list:
            for gate_id in self.gate_id_list:
                url = f'{self.ip}/pc/gate/common/getGatePractiseList'
                response = requests.get(url=url, headers=self.student_headers,
                                        params=f'gateId={gate_id}&classId={class_id}')
                assert_res(response.text)
                time.sleep(1)
                data_ret = response.json()
                try:
                    print([{i['practiseId']: i['title']} for i in data_ret['data']])
                except TypeError:
                    print(f'接口"/pc/gate/common/getGatePractiseList"报错，返回{data_ret["msg"]}')

    def test_07_get_goods_list(self):
        """
        获取商品列表
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getGoodsList'
        response = requests.get(url=url, headers=self.teacher_headers,
                                params='pageNum=1&pageSize=3')
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/gate/common/getGoodsList"报错，返回{data_ret["msg"]}')
        else:
            print([{i['id']: {i['name']: i['price']}} for i in data_list])

    def test_08_get_next_gate(self):
        """
        获取下一个关卡
        :return:
        """
        for t in range(2):
            url = f'{self.ip}/pc/gate/common/getNextGate'
            response = requests.get(url=url, headers=self.teacher_headers,
                                    params=f'type={t}&langType=2')
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                pro_gate_dic = data_ret['data']['proGate']
                next_gate_dic = data_ret['data']['nextGate']
            except TypeError:
                print(f'接口"/pc/gate/common/getNextGate"报错，返回{data_ret["msg"]}')
            else:
                pro_gate = {pro_gate_dic['id']: pro_gate_dic['gateName']}
                next_gate = {next_gate_dic['id']: next_gate_dic['gateName']}
                print(f'当前关卡：{pro_gate}，下一关卡：{next_gate}')

    def test_09_get_package_goods_list(self):
        """
        获取个人背包列表
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getPackageGoodsList'
        response = requests.get(url=url, headers=self.student_headers,
                                params='pageNum=1&pageSize=3')
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/gate/common/getNextGate"报错，返回{data_ret["msg"]}')
        else:
            print([{i['id']: {i['name']: i['ownNumber']}} for i in data_list])

    def test_10_get_series_list_for_map(self):
        """
        获取地图系列列表
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getSeriesListForMap'
        response = requests.get(url=url, headers=self.student_headers,
                                params=f'classId={self.class_id_list[0]}')
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']
            print([{i['id']: i['name']} for i in data_list])
        except TypeError:
            print(f'接口"/pc/gate/common/getSeriesListForMap"报错，返回{data_ret["msg"]}')

    def test_11_get_student_index_gate(self):
        """
        学生获取首页当前关卡以及下一个关卡
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getStudentIndexGate'
        response = requests.get(url=url, headers=self.student_headers,
                                params=f'classId={self.class_id_list[0]}')
        assert_res(response.text)
        data_ret = response.json()
        try:
            pro_gate_dic = data_ret['data']['proGate']
            next_gate_dic = data_ret['data']['nextGate']
        except TypeError:
            print(f'接口"/pc/gate/common/getStudentIndexGate"报错，返回{data_ret["msg"]}')
        else:
            try:
                pro_gate = {pro_gate_dic['id']: pro_gate_dic['gateName']}
            except TypeError:
                print('没有当前关卡')
            else:
                print(f'当前关卡：{pro_gate}', end=',')
            try:
                next_gate = {next_gate_dic['id']: next_gate_dic['gateName']}
            except TypeError:
                print('没有下一关卡')
            else:
                print(f'下一关卡：{next_gate}')

    def test_12_get_student_info(self):
        """
        获取学生个人信息
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getStudentInfo'
        response = requests.get(url=url, headers=self.student_headers,
                                params=f'classId={self.class_id_list[0]}')
        assert_res(response.text)
        data_ret = response.json()
        try:
            print(data_ret['data'])
        except TypeError:
            print(f'接口"/pc/gate/common/getStudentIndexGate"报错，返回{data_ret["msg"]}')

    def test_13_get_student_trail(self):
        """
        获取学生线索
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getStudentTrail'
        response = requests.get(url=url, headers=self.student_headers,
                                params='pageNum=1&pageSize=12')
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/gate/common/getStudentTrail"报错，返回{data_ret["msg"]}')
        else:
            print([i['description'] for i in data_list])

    def test_14_get_teacher_index_gate(self):
        """
        老师获取首页当前关卡以及下一个关卡
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getTeacherIndexGate'
        response = requests.get(url=url, headers=self.teacher_headers,
                                params=f'classId={self.class_id_list[0]}')
        assert_res(response.text)
        data_ret = response.json()
        try:
            pro_gate_dic = data_ret['data']['proGate']
            next_gate_dic = data_ret['data']['nextGate']
        except TypeError:
            print(f'接口"/pc/gate/common/getTeacherIndexGate"报错，返回{data_ret["msg"]}')
        else:
            pro_gate = {pro_gate_dic['id']: pro_gate_dic['gateName']}
            next_gate = {next_gate_dic['id']: next_gate_dic['gateName']}
            print(f'当前关卡：{pro_gate}，下一关卡：{next_gate}')

    def test_15_get_teacher_info(self):
        """
        获取老师个人信息
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getTeacherInfo'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print(data_ret['data'])
        except TypeError:
            print(f'接口"/pc/gate/common/getTeacherInfo"报错，返回{data_ret["msg"]}')

    def test_16_get_teacher_trail(self):
        """
        获取老师线索
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getTeacherTrail'
        response = requests.get(url=url, headers=self.teacher_headers,
                                params='pageNum=1&pageSize=12')
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/gate/common/getTeacherTrail"报错，返回{data_ret["msg"]}')
        else:
            print([i['description'] for i in data_list])

    def test_17_save_gate_practise(self):
        """
        保存关卡题目
        :return:
        """
        practise_id_list, practise_title_list = self.student_parm.get_gate_practise_id_list(
            self.gate_id_list[0], self.class_id_list[0])
        url = f'{self.ip}/pc/gate/common/saveGatePractise'
        n = len(practise_id_list)
        for i in range(n):
            data = {
                "classId": self.class_id_list[0],
                "ojcode": [
                    {
                        "fileContent": get_practise_code(practise_title_list[i]),
                        "fileName": practise_title_list[i],
                        "fileType": 2,
                        "rwType": 0,
                        "sort": 0
                    }
                ],
                "practiseId": practise_id_list[i]
            }
            response = requests.post(url=url, headers=self.student_headers, json=data)
            assert_res(response.text)
            time.sleep(1)

    def test_18_unlock_gate(self):
        """
        解锁关卡
        :return:
        """
        url = f'{self.ip}/pc/gate/common/unlockGate'
        data = {
            "classId": self.class_id_list[0],
            "gateId": self.gate_id_list[6]
        }
        response = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(response.text)


if __name__ == '__main__':
    unittest.main()
