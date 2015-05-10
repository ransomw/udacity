import turtle

window = turtle.Screen()
window.bgcolor('red')


def draw_square(tobj):
    for _ in range(4):
        tobj.forward(100)
        tobj.right(90)

def draw_circle():
    tobj = turtle.Turtle()
    tobj.color('yellow')
    tobj.circle(100)

def draw_triangle():
    tobj = turtle.Turtle()
    tobj.color('green')
    tobj.shape('classic')
    tobj.right(105)
    for _ in range(3):
        tobj.forward(110)
        tobj.right(120)

def draw_shapes():
    tobj = turtle.Turtle()
    # tobj.speed(2)
    tobj.color('blue')
    tobj.shape('turtle')
    draw_square(tobj)
    draw_circle()
    draw_triangle()

def draw_circle_of_squares(num_squares):
    tobj = turtle.Turtle()
    tobj.color('green')
    for _ in range(num_squares):
        draw_square(tobj)
        tobj.right(360./float(num_squares))

def draw_frac(tobj, flen, depth):
    if depth == 0:
        tobj.begin_fill()
        for _ in range(3):
            tobj.forward(flen)
            tobj.left(120)
        tobj.end_fill()
    else:
        hlen = float(flen)/2.
        tobj.forward(hlen)
        draw_frac(tobj, hlen, depth - 1)
        tobj.left(120)
        tobj.forward(hlen)
        tobj.right(120)
        draw_frac(tobj, hlen, depth - 1)
        tobj.right(120)
        tobj.forward(hlen)
        tobj.left(120)
        draw_frac(tobj, hlen, depth - 1)


tobj = turtle.Turtle()
tobj.color('blue', 'green')
draw_frac(tobj, 360, 4)
window.exitonclick()
