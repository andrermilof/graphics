from PIL import Image
from random import randint
 
def draw_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    slope = dy > dx

    if slope:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    error = dx // 2
    y = y1
    y_step = 1 if y1 < y2 else -1

    points = []

    for x in range(x1, x2 + 1):
        coord = (y, x) if slope else (x, y)
        points.append(coord)
        error -= dy
        if error < 0:
            y += y_step
            error += dx

    return points

def draw_circle(center_x, center_y, radius):
    x = radius
    y = 0
    decision = 1 - radius
    points = set()

    while x >= y:
        points.add((x + center_x, y + center_y))
        points.add((-x + center_x, y + center_y))
        points.add((x + center_x, -y + center_y))
        points.add((-x + center_x, -y + center_y))
        points.add((y + center_x, x + center_y))
        points.add((-y + center_x, x + center_y))
        points.add((y + center_x, -x + center_y))
        points.add((-y + center_x, -x + center_y))

        y += 1
        if decision <= 0:
            decision += 2 * y + 1
        else:
            x -= 1
            decision += 2 * (y - x) + 1

    return list(points)

def draw(image, points, color):
    for point in points:
        image.putpixel(point, color)

if __name__ == '__main__':
    with Image.open('Bresenham.png') as im:
        im.paste((0, 0, 0), (0, 0, im.size[0], im.size[1]))

        for i in range(100):
            line_points = draw_line(400, 300, randint(0, 799), randint(0, 599))
            draw(im, line_points, (255, 0, 0))

        for i in range(50):
            circle_points = draw_circle(400, 300, randint(0, 299))
            draw(im, circle_points, (255, 0, 0))

        im.save('Bresenham.png')
