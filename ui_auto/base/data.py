production = False


class Data:
    """ip信息"""

    homework_name = '作业流程自动测试'
    work_name = '测试作品'
    test_field_file_name = 'hey'
    test_field_output = 'Hello World!'
    material_name = 'test1'
    password_for_edu = '123456'

    password_for_uniTeach = '123456'

    username_for_uniLab = '15208451940'  # 高校实验版
    password_for_uniLab = '123456'

    def __init__(self):
        self.production = production

    def ip_for_edu(self):
        ip_for_edu = 'https://edu.dingdangcode.com' \
            if self.production else 'https://edu.dingdangcode.cn/'

        return ip_for_edu

    def api_ip_for_edu(self):
        ip_for_edu = 'https://api.dingdangcode.com/ddc-edu3' \
            if self.production else 'https://api.dingdangcode.cn/ddc-edu3'

        return ip_for_edu

    def ip_for_uni_teach(self):
        ip_for_uni_teach = 'https://uni-teach.dingdangcode.com' \
            if self.production else 'http://192.168.0.160:8100'

        return ip_for_uni_teach

    def api_ip_for_uni_teach(self):
        ip_for_uni_teach = 'https://uniteachapi.dingdangcode.com' \
            if self.production else 'http://192.168.0.160:8099'

        return ip_for_uni_teach

    def ip_for_uni_lab(self):
        ip_for_uni_lab = 'https://uni-lab.dingdangcode.com' \
            if self.production else 'http://192.168.0.160:8098'

        return ip_for_uni_lab

    def api_ip_for_uni_lab(self):
        ip_for_uni_lab = 'https://uniteachapi.dingdangcode.com' \
            if self.production else 'http://192.168.0.160:8097'

        return ip_for_uni_lab

    '''用户名密码'''

    def manager_username_for_edu(self):
        manager_username_for_edu = '15008447557' if self.production else '15208451947'
        return manager_username_for_edu

    @property
    def global_id(self):
        global_id = '086' if self.production else '160'
        return global_id

    def manager_data(self):
        manager_data = {
            'username': '15008447557',
            'password': '12345600',
            'name': '叮当老师'
        } if self.production else {
            'username': '15208451947',
            'password': '123456',
            'name': '测试管理员new'
        }
        return manager_data

    def teacher_data(self):
        return {
            'username': f'13900000{self.global_id}',
            'password': '123456',
            'name': f'教师{self.global_id}'
        }

    def student_data(self):
        return {
            'username': f'G00{self.global_id}',
            'password': '123456',
            'name': f'学生{self.global_id}'
        }

    def teacher_username_for_edu(self):
        # 教育版教师账号
        return f'13900000{self.global_id}'

    def student_username_for_edu(self):
        # 教育版学生账号
        return f'G00{self.global_id}'

    def teacher_name_for_edu(self):
        return f'教师{self.global_id}'

    def student_name_for_edu(self):
        return f'学生{self.global_id}'

    def admin_class_name_for_edu(self):
        return f'行政班{self.global_id}'

    def pro_class_name_for_edu(self):
        return f'课程班{self.global_id}'

    def manager_username_for_uni_teach(self):
        manager_username_for_uni_teach = '' if self.production else ''

        return manager_username_for_uni_teach

    def teacher_username_for_uni_teach(self):
        teacher_username_for_uni_teach = '15208451946' if self.production else '1234567'

        return teacher_username_for_uni_teach

    def student_username_for_uni_teach(self):
        student_username_for_uni_teach = 'GXQZHZX20160101' if self.production else 'KDA0.1'

        return student_username_for_uni_teach

    def edu_manager_name(self):
        edu_manager_name = '叮当老师' if self.production else '测试管理员new'

        return edu_manager_name

    def uni_teach_teacher_name(self):
        uni_teach_teacher_name = '敖瑞麟' if self.production else '测试教师5'

        return uni_teach_teacher_name

    def uni_teach_student_name(self):
        uni_teach_student_name = '中学生' if self.production else '小学生'

        return uni_teach_student_name


class UnPw(Data):
    """用户名密码"""
    # username_for_uniTeach = '15208451946'  # 高校教学版生产环境教师账号
    username_for_uniTeach = '1234567'  # 高校教学版
    password_for_uniTeach = '123456'

    username_for_uniLab = '15208451940'  # 高校实验版
    password_for_uniLab = '123456'


class PointIdIndex:
    # 知识点索引
    level_one_index = 2
    level_two_index = 2
    level_three_index = 0

    checkpoint_level_one_index = 1
    checkpoint_level_two_index = 4
    checkpoint_level_three_index = 0


class EmailData:
    mail_server = 'smtp.126.com'
    port = '25'
    sender_email = 'aoruilin@126.com'
    sender_password = 'ao940208'
    receive_email = '646010544@qq.com'
