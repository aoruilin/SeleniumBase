import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.save_draft import save_draft_for_works
from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.picture_list_code import turtle_code


class WorksController(unittest.TestCase):
    """作品展示学生端接口"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

    def test_01_post_work(self):
        """
        上传作品
        :return:
        """
        save_draft_for_works(self.teacher_parm)
        draft_id_list = self.teacher_parm.get_draft_id_list()
        code = turtle_code()
        url = f'{self.ip[:-8]}/ddc-port/play/postWork'
        for p in range(2):
            data = {
                "codeList": [
                    {
                        "fileContent": code,
                        "fileName": "main.py",
                        "fileType": 1,
                        "rwType": 1
                    }
                ],
                "cover": "https://edu-test-1255999742.file.myqcloud.com/portrait/20190527/"
                         "4a60ada1fc0f478ca109f9fe49419328.jpg",
                "description": "发布接口测试",
                "draftId": draft_id_list[0],
                "publishCode": p,
                "title": f"接口发布作品源代码{p}"
            }
            response = requests.post(url=url, headers=self.teacher_headers, json=data)
            assert_res(response.text)

    def test_02_get_my_work_list(self):
        """
        获取我发布的作品
        :return:
        """
        for s in range(2):
            for k in ['', '测试']:
                url = f'{self.ip}/pc/play/getMyWorksList?pageNum=1&pageSize=12&sort={s}&keyword={k}'
                response = requests.get(url=url, headers=self.teacher_headers)
                assert_res(response.text)
                data_ret = response.json()
                time.sleep(1)
                try:
                    data_list = data_ret['data']['list']
                except TypeError:
                    print(f'接口"/pc/worksDisplay/getMyWorksList"报错，返回{data_ret["msg"]}')
                except KeyError:
                    print(data_ret)
                else:
                    work_list = [{i['id']: i['title']} for i in data_list]
                    print(work_list)

    def test_03_get_student_list_by_class_id(self):
        """
        查询班级所属学生列表
        :return:
        """
        student_id, _ = self.teacher_parm.get_user_school_id()
        url = f'{self.ip}/pc/class/getStudentListByClassId?studentId={student_id}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print([{i['classId']: [{u['id']: u['nickName']} for u in i['userList']]} for i in data_ret['data']])
        except TypeError:
            print(f'接口"/pc/class/getStudentListByClassId"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)

    def test_04_get_teacher_list_by_class_id(self):
        """
        查询班级所属老师列表
        :return:
        """
        url = f'{self.ip}/pc/class/getTeacherListByClassId'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print([{i['classId']: [{u['id']: u['nickName']} for u in i['userList']]} for i in data_ret['data']])
        except TypeError:
            print(f'接口"/pc/class/getTeacherListByClassId"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)

    def test_05_get_work_detail_by_id(self):
        """
        通过作品ID获取作品详情
        :return:
        """
        work_id_list = self.teacher_parm.get_work_id_list()
        url = f'{self.ip[:-8]}/ddc-port/play/getWorkDetailById?worksId={work_id_list[0]}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print({data_ret['data']['id']: data_ret['data']['title']})
        except TypeError:
            print(f'接口"/play/getWorkDetailById"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)

    def test_06_get_works_hall(self):
        """
        获取作品大厅列表
        :return:
        """
        class_id_list = self.teacher_parm.get_class_list(get_all=True)
        class_id_list.append('')
        for class_id in class_id_list:
            for s in range(2):
                for k in ['', '测试']:
                    url = f'{self.ip}/pc/play/getPlayWorksHall'
                    params = f'pageNum=1&pageSize=12&sort={s}&keyword={k}&classId={class_id}'
                    print(params)
                    response = requests.get(url=url, headers=self.teacher_headers,
                                            params=params)
                    assert_res(response.text)
                    data_ret = response.json()
                    time.sleep(1)
                    try:
                        data_list = data_ret['data']['list']
                    except TypeError:
                        print(f'接口"/pc/play/getPlayWorksHall"报错，返回{data_ret["msg"]}')
                        print('##############################################################')
                    except KeyError:
                        print(data_ret)
                        print('##############################################################')
                    else:
                        print(f'班级{class_id}',
                              [{i['id']: {i['title']: f"作者：{i['nickname']}"}} for i in data_list])
                        print('##############################################################')

    def test_07_student_class_list(self):
        """
        获取学生所在的课程班班级列表
        :return:
        """
        url = f'{self.ip}/pc/class/studentClassList'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print([{i['id']: i['name']}for i in data_ret['data']])
        except TypeError:
            print(f'接口"/pc/class/studentClassList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)

    def test_08_user_praise(self):
        """
        通过作品ID对作品进行点赞
        :return:
        """
        works_id_list = self.teacher_parm.get_work_id_list()
        for w in range(2):
            url = f'{self.ip[:-8]}/ddc-port/play/userPraise?worksId={works_id_list[w]}'
            response = requests.get(url=url, headers=self.teacher_headers)
            assert_res(response.text, "今天已经点过赞了")
            time.sleep(1)

    def test_09_work_detail(self):
        """
        游客通过作品ID获取作品详情
        :return:
        """
        works_id_list = self.teacher_parm.get_work_id_list()
        url = f'{self.ip[:-8]}/ddc-port/play/workDetail?worksId={works_id_list[0]}'
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/68.0.3440.84 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_dic = data_ret['data']
            print(f'作品id：{data_dic["id"]}，'
                  f'作品名称：{data_dic["title"]}，'
                  f'作者：{data_dic["nickname"]}')
        except TypeError:
            print(f'接口"/play/workDetail"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)

    def test_10_delete_works_by_id(self):
        """
        删除作品
        :return:
        """
        work_id_list = self.teacher_parm.get_work_id_list()
        for i in range(2):
            url = f'{self.ip[:-8]}/ddc-port/play/deleteWorksById?worksId={work_id_list[i]}'
            response = requests.delete(url=url, headers=self.teacher_headers)
            assert_res(response.text)

    def test_11(self):
        """
        获取草稿列表（暂放此处）
        :return:
        """
        url = 'http://125.69.90.238:8081/ddc-port/play/getDraftList'
        params = 'pageNum=1&pageSize=15&keywords='
        response = requests.get(url=url, headers=self.student_headers, params=params)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/play/getDraftList报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            print([f'id:{i["id"]},title:{i["title"]}' for i in data_list])


if __name__ == '__main__':
    unittest.main()
