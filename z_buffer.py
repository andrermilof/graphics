from PIL import Image
from Bresenham import draw_line, draw
from CyrusBeck import point2
from fill import fill2D

class point3:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

def get_plane(point1, point2, point3):
    x1, y1, z1 = point1.x, point1.y, point1.z
    x2, y2, z2 = point2.x, point2.y, point2.z
    x3, y3, z3 = point3.x, point3.y, point3.z

    vector1 = [x2 - x1, y2 - y1, z2 - z1]
    vector2 = [x3 - x1, y3 - y1, z3 - z1]

    normal_vector = [
        vector1[1] * vector2[2] - vector1[2] * vector2[1],
        vector1[2] * vector2[0] - vector1[0] * vector2[2],
        vector1[0] * vector2[1] - vector1[1] * vector2[0]
    ]

    A, B, C = normal_vector
    D = -(A * x1 + B * y1 + C * z1)

    return A, B, C, D

def fill3D(vertexes):
	points = fill2D(vertexes)
	A, B, C, D = get_plane(vertexes[0], vertexes[1], vertexes[2])
	find_z = lambda x, y: int((-D - A*x - B*y) / C)

	new_points = []
	for point in points:
		z = find_z(point[0], point[1])
		new_points.append(point3(point[0], point[1], z))
	return new_points	

def update_buffer(points, z_buffer):
	for point in points:
		if point.z < z_buffer[800 * point.y + point.x]:
			z_buffer[800 * point.y + point.x] = point.z

def draw_buffer(image, points, z_buffer, color):
	for point in points:
		if point.z <= z_buffer[800 * point.y + point.x]:
			image.putpixel((int(point.x), int(point.y)), color)

if __name__ == '__main__':
	vertexes1 = [
		point3(300, 300, 100),
		point3(350, 400, 100),
	 	point3(500, 150, 300)
	]

	vertexes2 = [
		point3(200, 100, 0),
		point3(400, 400, 200),
		point3(500, 200, 200)
	]

	with Image.open('z-buffer.png') as im:
		im.paste((0, 0, 0), (0, 0, im.size[0], im.size[1]))

		z_buffer = [1000] * 800 * 600

		points1 = fill3D(vertexes1)
		points2 = fill3D(vertexes2)

		update_buffer(points1, z_buffer)
		update_buffer(points2, z_buffer)

		draw_buffer(im, points2, z_buffer, (0, 0, 255))
		draw_buffer(im, points1, z_buffer, (255, 0, 0))
		
 
		im.save('z-buffer.png')