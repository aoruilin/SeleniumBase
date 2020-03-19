import unittest

from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.homework_operation import do_homework_simple


class DoHomework(unittest.TestCase):

    def setUp(self) -> None:
        self.parameter = ParameterForOthers(identity='student')
        self.ip = self.parameter.ip
        self.headers = self.parameter.headers
        point_id_list = self.parameter.get_point_id()
        self.point_id = point_id_list[0]

    def test_do_homework_01(self):
        do_homework_simple(self.parameter, cut_num=None)

    def test_do_homework_02(self):
        do_homework_simple(self.parameter, cut_num=None)

    def test_do_homework_turtle(self):
        do_homework_simple(self.parameter, cut_num=None, homework_num=3)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
