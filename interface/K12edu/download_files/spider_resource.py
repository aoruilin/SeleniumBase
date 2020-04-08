import requests
import os
import time


class SpiderResource:
    def __init__(self, series_id):
        self.series_id = series_id
        self.ip = 'https://eduapi.dingdangcode.com'
        self.headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36"
        }
        # 登录
        data = {
            'username': '13900000088',
            'password': '123456'
        }
        url = f'{self.ip}/pc/login'
        t = requests.session()
        login_ret = t.post(url=url, headers=self.headers, json=data)
        token = login_ret.json()['data']['token']
        self.headers['token'] = token

    def get_point_id(self) -> list:
        # 获取一个系列所有知识点的pointId
        url = f'{self.ip}/pc/common/getPointList?seriesId={self.series_id}'
        response = requests.get(url=url, params=self.headers)
        point_list_ret = response.json()
        data_list = point_list_ret['data']
        point_id_list = []
        for data in data_list:
            course_list = data['list']
            for id_data in course_list:
                point_id = id_data['id']
                point_id_list.append(point_id)
        return point_id_list  # 返回知识点pointId列表，在之后的获取资源中作为参数

    def resource_plan(self) -> list:
        # 获取一个系列所有知识点的资源链接并下载保存到resource文件夹下
        point_id_list = self.get_point_id()
        course_name_list = []
        course_ware_list = []
        course_video_list = []
        course_materials_list = []
        course_ware_info = {}
        course_video_info = {}
        course_materials_info = {}
        resource_list = []
        for point_id in point_id_list:
            for resource_type in range(2):
                url = f'{self.ip}/pc/course/getResourcePlanList?' \
                    f'resourceType={resource_type}&pointId={point_id}&pageNum=1&pageSize=3'
                response = requests.get(url=url, params=self.headers)
                time.sleep(2)
                data_ret = response.json()
                data_list = data_ret['data']
                course_list = data_list['list']
                for course_info in course_list:
                    course_name = course_info['title']
                    course_ware = course_info['coursewareUrl']
                    course_video = course_info['videoUrl']
                    course_materials = course_info['materialsUrl']
                    course_name_list.append(course_name)
                    course_ware_list.append(course_ware)
                    course_video_list.append(course_video)
                    course_materials_list.append(course_materials)
                    for num in range(len(course_name_list)):
                        course_ware_info[course_name_list[num]] = course_ware_list[num]
                    for num in range(len(course_name_list)):
                        course_video_info[course_name_list[num]] = course_video_list[num]
                    for num in range(len(course_name_list)):
                        course_materials_info[course_name_list[num]] = course_materials_list[num]

        for d in course_name_list:
            os.makedirs(f'resource{self.series_id}/{d}', exist_ok=True)
        resource_list.append(course_ware_info)
        resource_list.append(course_video_info)
        resource_list.append(course_materials_info)
        index = 0
        for i in ['pptx', 'mp4', 'docx']:
            ppt_url = resource_list[index]
            index += 1
            for point_name, link in ppt_url.items():
                try:
                    if link == '':
                        pass
                    elif not link:
                        pass
                    else:
                        res = requests.get(url=link, params=self.headers)
                        time.sleep(2)
                        with open(f'resource{self.series_id}/{point_name}/{point_name}.{i}', 'wb') as ppt_file:
                            ppt_file.write(res.content)
                except BaseException as e:
                    print(f'{point_name, i}资源链接错误：{e}')

        return resource_list  # 返回知识点中PPT，视频，doc文档列表


if __name__ == '__main__':
    resource = SpiderResource(series_id='1')
    print(resource.resource_plan())
