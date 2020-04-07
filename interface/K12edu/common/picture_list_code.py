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
    code = """import pygame

from pygame.locals import *
background_image = 'userupload/sucai/3702/20200118/bgimg.jpg'
mouse_image = 'userupload/sucai/3702/20200224/Snipaste_2019-07-23_17-44-01.png'
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('hello world')
background = pygame.image.load(background_image)
mouse_cursor = pygame.image.load(mouse_image)
while True:
    screen.blit(background, (0, 0))
    x, y = pygame.mouse.get_pos()
    x -= mouse_cursor.get_width()/2
    y -= mouse_cursor.get_height()/2
    screen.blit(mouse_cursor, (x, y))
    pygame.display.update()
"""

    return code


def multiple_files_code(file_name, content):
    main_code = f"from {file_name} import hello\n\na = hello()\nprint(a)\n\n"
    file_code = f"def hello():\n    s = '{content}'\n\n    return s"

    return main_code, file_code


def three_dimensional_code():
    code = """import cadquery as cq
model = cq.Workplane("XY")
model = model.box(10, 20, 30)
show_model(model, cq)
"""

    return code


def robot_code():
    code = 'import robot\n\n' \
           'r=robot.robot()\n' \
           'r.up(1)\n' \
           'r.nod(1)\n'

    return code
