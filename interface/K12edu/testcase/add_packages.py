import unittest
import requests

from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.cover_url import get_cover_url


class AddPackages(unittest.TestCase):

    def setUp(self):
        self.parameter = ParameterForOthers(identity='teacher')
        self.url = f'{self.parameter.ip}/pc/resource/addResource'
        self.headers = self.parameter.headers

    def test_01(self):
        public_list = [1, 3]
        for p in public_list:
            data = {
                "coursewareUrl": "https://edu-release-1255999742.file.myqcloud.com/userupload/teach/"
                                 "courseware/9815/ppt1.pptx,"
                                 "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/courseware/"
                                 "20190612094509/ppt2.pptx,"
                                 "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/courseware/"
                                 "20190612094522/ppt3.pptx,"
                                 "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/courseware/"
                                 "20190612094529/ppt4.pptx,"
                                 "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/courseware/"
                                 "20190612094532/ppt5.pptx",
                "desc": "",
                "langType": 2,
                "lessonPlanUrl": "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/materials/"
                                 "20190612094559/word6.doc,"
                                 "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/materials/"
                                 "20190612094612/word7.doc,"
                                 "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/materials/"
                                 "20190612094615/word8.docx,"
                                 "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/courseware/"
                                 "20190612094620/ppt6.ppt,"
                                 "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/courseware/"
                                 "20190612094625/ppt7.ppt",
                "materialsUrl": "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/materials/"
                                "20190612094552/word1.docx,"
                                "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/materials/"
                                "20190612094601/word2.docx,"
                                "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/materials/"
                                "20190612094604/word3.docx,"
                                "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/materials/"
                                "20190612094606/word4.doc,"
                                "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/materials/"
                                "20190612094608/word5.docx",
                "title": "自动上传课件",
                "videoUrl": "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/video/20190612094517/"
                            "fdb8dd021739db290da1d5d30d270054.mp4,"
                            "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/video/20190612094540/"
                            "test视频.mp4,"
                            "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/video/20190612094543/"
                            "测试视频.mp4,"
                            "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/video/20190612094546/"
                            "音乐.mp4"
            }
            cover_url = get_cover_url()
            data['coverUrl'] = cover_url
            data['publicStatus'] = p
            response = requests.post(url=self.url, headers=self.headers, json=data)
            self.assertIn('操作成功', response.text, '上传失败')
