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
           "s = turtle.Screen()\n" \
           "s.bgpic('userupload/sucai/3702/20200118/bgimg.jpg')\n" \
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
           "background_image = 'userupload/sucai/3702/20200114/pygamebg.jpg'\n" \
           "mouse_image = 'userupload/sucai/3702/20200224/Snipaste_2019-07-23_17-44-01.png'\n" \
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


def jieba_files_code(file_name):
    main_code = 'import jieba\n' \
                'import jieba.posseg as pseg\n\n' \
                f'jieba.load_userdict("{file_name}.txt")\n' \
                'jieba.add_word("石墨烯")\n' \
                'jieba.add_word("凱特琳")\n' \
                'jieba.del_word("自定义词")\n' \
                'test_sent = (\n' \
                '    "李小福是创新办主任也是云计算方面的专家; 什么是八一双鹿\n"\n' \
                '    "例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类\n"\n' \
                '    "「台中」正確應該不會被切開。mac上可分出「石墨烯」；此時又可以分出來凱特琳了。"\n' \
                ')\n' \
                'words = jieba.cut(test_sent)\n' \
                'print("/".join(words))\n' \
                'print("=" * 40)\n' \
                'result = pseg.cut(test_sent)\n' \
                'for w in result:\n' \
                '    print(w.word, "/", w.flag, ", ", end=" ")\n' \
                'print("\n" + "=" * 40)\n' \
                'terms = jieba.cut("easy_install is great")\n' \
                'print("/".join(terms))\n' \
                'terms = jieba.cut("python 的正则表达式是好用的")\n' \
                'print("/".join(terms))\n' \
                'print("=" * 40)\n' \
                'testlist = [\n' \
                '    ("今天天气不错", ("今天", "天气")),\n' \
                '    ("如果放到post中将出错。", ("中", "将")),\n' \
                '    ("我们中出了一个叛徒", ("中", "出")),\n' \
                ']\n' \
                'for sent, seg in testlist:\n' \
                '    print("/".join(jieba.cut(sent, HMM=False)))\n' \
                '    word = "".join(seg)\n' \
                '    print(f"{word} Before: {jieba.get_FREQ(word)}, After: {jieba.suggest_freq(seg, True)}")\n' \
                '    print("/".join(jieba.cut(sent, HMM=False)))\n' \
                '    print("-" * 40)\n'

    file_code = '创新办 3 i\n' \
                '云计算 5\n' \
                '凱特琳 nz\n' \
                '台中'

    return main_code, file_code


def matplotlib_code():
    code = 'import matplotlib.pyplot as plt\n' \
           'import numpy\n\n' \
           't = numpy.arange(0., 5., 0.2)\n' \
           'plt.plot(t, t, "r--", t, t ** 2, "bs", t, t ** 3, "g^")\n' \
           'plt.show()\n' \
           'plt.ylabel("no data")\n' \
           'plt.show()\n'

    return code


def three_dimensional_code():
    code = 'import cadquery as cq\n\n' \
           'model = cq.Workplane("XY")\n' \
           'model = model.sphere(20)\n' \
           'show_model(model, cq)\n' \

    return code


"""
import io
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCone
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Ax1, gp_Dir
from OCC.Display.OCCViewer import rgb_color
import cadquery as cq
length = 80.0
width = 60.0
height = 100.0
thickness = 10.0
center_hole_dia = 22.0
cbore_hole_diameter = 2.4
cbore_inset = 12.0
cbore_diameter = 4.4
cbore_depth = 2.1
result = cq.Workplane("XY").box(length, height, thickness).faces(">Z").workplane().hole(center_hole_dia).faces(">Z").workplane().rect(length - cbore_inset, height - cbore_inset, forConstruction=True).vertices().cboreHole(cbore_hole_diameter, cbore_diameter, cbore_depth).edges("|Z").fillet(2.0)
if __name__ == "__main__":
    s = io.StringIO()
    cq.exporters.exportShape(result, cq.exporters.ExportTypes.STL, s, 0.1)
    print(s.getvalue())
"""


def robot_code():
    code = 'import robot\n\n' \
           'r=robot.robot()\n' \
           'r.up(1)\n' \
           'r.nod(1)\n'

    return code
