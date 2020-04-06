def author_picture():
    author_picture_list = [
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190524/"
        "2ca50ff2ca024a75a893b80257458104.jpg",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190524/"
        "f3b24a5e1d534ba49b36f4ac36ce4f09.jpg",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190524/"
        "e7c07866de6f4cb0bccac1baad568d93.jpg",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190524/"
        "9c405d8ba8824dcab891b483afbea2bb.png",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190524/"
        "8800fb7a237740779f17b8ac57defa57.png"
    ]

    return author_picture_list


def work_picture():
    work_picture_list = [
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190527/"
        "4a60ada1fc0f478ca109f9fe49419328.jpg",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190527/"
        "20595550fe6e4830bcc8a03f2f7d4b9c.jpg",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190527/"
        "83c57efc02d74c7687bcbe62b06b5245.jpg",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190527/"
        "330d96fde0644196bc9a87276782b1f0.jpg",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190527/"
        "19e2e5ad971a4bf4af25d2b62b428854.jpg",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190527/"
        "26b333ce54724623aeb1d83f68b4b512.png",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190527/"
        "3734093298344d09834fd4897100530f.png",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190527/"
        "8005c7f2b69a4111ad5351c5dec8f022.png",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190524/"
        "8800fb7a237740779f17b8ac57defa57.png",
        "https://edu-test-1255999742.file.myqcloud.com/portrait/20190524/"
        "4b3f7fdef342445fb2941dbb15a7eed0.jpg"
    ]
    return work_picture_list


def turtle_code():
    code = """import turtle

t = turtle.Turtle()
screen = turtle.Screen()
screen.bgpic('userupload/sucai/3702/20200218/58eb54f9753d1.jpg')
t.begin_fill()
turtle.colormode(255)
t.forward(150)
t.right(90)
t.forward(170)
t.right(90)
t.forward(150)
t.right(90)
t.forward(170)
t.fillcolor(250, 255, 230)
t.end_fill()
t.right(30)
t.begin_fill()
t.fillcolor(255, 120, 60)
t.forward(150)
t.right(120)
t.forward(150)
t.end_fill()

print('abc')"""

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
