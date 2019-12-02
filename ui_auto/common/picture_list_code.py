def author_picture():
    author_picture_list = [
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "dd4f56aba5524d28beac93dbb2770783.jpg",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "3a09d554769e45fe9c1f68e58d44350a.jpg",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "7f13e9f1d0114525b7f9223ca8a81555.jpg",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "ab6dc8ddca3d44d8804c6350fec60e4d.jpg",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "861ba67ea8114864b336825b58a1801e.jpg"
    ]

    return author_picture_list


def work_picture():
    work_picture_list = [
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "ff2caee02c5347e58e4b649cd799fbe6.png",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "dc6459892d7b4c8a8640bc87ad44ddc9.png",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "0d29185e565048618efc5ac3eea9c818.png",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "fcab5c67cd7643748ca1196fad9fa405.jpg",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "0567a1d739da4352bb25389dee4588da.png",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "b667c94d61054affa71d8a6c19f28db7.jpg",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "593c6672eb564b6fbb54e6960d98ce2d.jpg",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "57fe966743674ea3883f179fb303ae4b.png",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "b60268cf66794fc08f6d1376ec3bcfbb.jpg",
        "https://edu-test-1255999742.cos.ap-chengdu.myqcloud.com/portrait/20190612/"
        "4d3850efa5d6443ea65d296520af25d7.jpg"
    ]
    return work_picture_list


def turtle_code():
    code = "import turtle\n\n" \
           "t = turtle.Turtle()\n" \
           "t.begin_fill()\n" \
           "turtle.colormode(255)\n" \
           "t.forward(150)\n" \
           "t.right(90)\n" \
           "t.forward(170)\n" \
           "t.right(90)\n" \
           "t.forward(150)\n" \
           "t.right(90)\n" \
           "t.forward(170)\n" \
           "t.fillcolor(250, 255, 230)\n" \
           "t.end_fill()\n" \
           "t.right(30)\n" \
           "t.begin_fill()\n" \
           "t.fillcolor(255, 120, 60)\n" \
           "t.forward(150)\n" \
           "t.right(120)\n" \
           "t.forward(150)\n" \
           "t.end_fill()\n\n" \
           "print('abc')\n"

    return code


def wrong_code():
    code = "import turtle\n\n" \
           "t = turtle.Turtle()\n" \
           "t.forward(150)\n" \
           "print(abc)\n"

    return code


def pygame_code():
    code = "import pygame\n\n" \
           "from pygame.locals import *\n" \
           "background_image = 'https://edu-release-1255999742.file.myqcloud.com/static/sucai/%E8%83%8C%E6%99%AF.png'\n" \
           "mouse_image = 'https://edu-release-1255999742.file.myqcloud.com/userupload/sucai/9816/2019-11-2/1572669762412Snipaste_2019-07-23_17-44-01.png'\n" \
           "pygame.init()\n" \
           "screen = pygame.display.set_mode((640, 480), 0, 32)\n" \
           "pygame.display.set_caption('hello world')\n" \
           "background = pygame.image.load(background_image)\n" \
           "mouse_cursor = pygame.image.load(mouse_image)\n" \
           "while True:\n" \
           "    screen.blit(background, (0, 0))\n" \
           "    x, y = pygame.mouse.get_pos()\n" \
           "    x -= mouse_cursor.get_width()/2\n" \
           "    y -= mouse_cursor.get_height()/2\n" \
           "    screen.blit(mouse_cursor, (x, y))\n" \
           "    pygame.display.update()"

    return code


def multiple_files_code(file_name, content):
    main_code = f"from {file_name} import hello\n\na = hello()\nprint(a)\n\n"
    file_code = f"def hello():\n    s = '{content}'\n\n    return s"

    return main_code, file_code


def three_dimensional_code():
    code = 'import io\n\n' \
           'from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCone\n' \
           'from OCC.Core.TopLoc import TopLoc_Location\n' \
           'from OCC.Core.TopoDS import TopoDS_Shape\n' \
           'from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Ax1, gp_Dir\n' \
           'from OCC.Display.OCCViewer import rgb_color\n\n' \
           'import cadquery as cq\n\n' \
           'length = 80.0\n' \
           'width = 60.0\n' \
           'height = 100.0\n' \
           'thickness = 10.0\n' \
           'center_hole_dia = 22.0\n' \
           'cbore_hole_diameter = 2.4\n' \
           'cbore_inset = 12.0\n' \
           'cbore_diameter = 4.4\n' \
           'cbore_depth = 2.1\n\n' \
           'result = cq.Workplane("XY").box(length, height, thickness).faces(">Z").workplane().hole(center_hole_dia).faces(">Z").workplane().rect(length - cbore_inset, height - cbore_inset, forConstruction=True).vertices().cboreHole(cbore_hole_diameter, cbore_diameter, cbore_depth).edges("|Z").fillet(2.0)\n\n' \
           'if __name__ == "__main__":\n' \
           '    s = io.StringIO()\n' \
           '    cq.exporters.exportShape(result, cq.exporters.ExportTypes.STL, s, 0.1)\n' \
           '    print(s.getvalue())\n'

    return code


def robot_code():
    code = 'import robot\n\n' \
           'r=robot.robot()\n' \
           'r.up(1)\n' \
           'r.nod(1)\n'

    return code
