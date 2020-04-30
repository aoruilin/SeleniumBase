import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class TestCategorySucai(unittest.TestCase):
    """试炼场素材分类和素材添加修改删除"""

    def setUp(self) -> None:
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

        self.category_id_list = self.student_parm.get_category_list()

    def test_01_add_category(self):
        url = f'{self.ip[:-8]}/ddc-port/play/addSucaiCategory'
        data = {
            'categoryName': '接口添加分类待删'
        }
        response = requests.post(url=url, headers=self.student_headers, json=data)
        assert_res(response.text, '操作成功')

    def test_02_add_image(self):
        image_name = '1-43.jpg'
        url = f'{self.ip[:-8]}/ddc-port/play/userSaveImageFile'
        data = {
            'categoryId': self.category_id_list[0],
            'fileName': image_name,
            'url': f'{self.student_parm.get_sucai_url()}{image_name}'
        }
        response = requests.post(url=url, headers=self.student_headers, json=data)
        assert_res(response.text, '操作成功')

    def test_03_change_category(self):
        url = f'{self.ip[:-8]}/ddc-port/play/changeSucaiCategory/{self.category_id_list[0]}?categoryName=接口修改分类待删'
        response = requests.put(url=url, headers=self.student_headers)
        assert_res(response.text, '操作成功')

    def test_04_change_image_name(self):
        image_id = self.student_parm.get_image_id_list(self.category_id_list[1])[0]
        url = f'{self.ip[:-8]}/ddc-port/play/changeImageFileName/{image_id}?imageTitle=接口修改素材名称待删.jpg'
        response = requests.put(url=url, headers=self.student_headers)
        assert_res(response.text, '操作成功')

    def test_05_del_image(self):
        image_id = self.student_parm.get_image_id_list(self.category_id_list[0])[0]
        url = f'{self.ip[:-8]}/ddc-port/play/deleteImageFile?imageId={image_id}'
        response = requests.delete(url=url, headers=self.student_headers)
        assert_res(response.text, '操作成功')

    def test_06_del_category(self):
        url = f'{self.ip[:-8]}/ddc-port/play/deleteSucaiCategory?categoryId={self.category_id_list[0]}'
        response = requests.delete(url=url, headers=self.student_headers)
        assert_res(response.text, '操作成功')


if __name__ == '__main__':
    unittest.main()
