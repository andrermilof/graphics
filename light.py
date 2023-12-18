from PIL import Image
from z_buffer import point3, fill3D, update_buffer, draw_buffer, get_plane

class point3:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

def diffuse_light(light_point, point, color, A, B, C):
	light_direction = point3(light_point.x - point.x, light_point.y - point.y, light_point.z - point.z) 
	light = (light_direction.x * A + light_direction.y * B + light_direction.z * C) / ((light_direction.x**2 + light_direction.y**2 + light_direction.z**2)**0.5) / ((A**2 + B**2 + C**2)**0.5)
	if light < 0:
		light = 0

	diffuse_light = point3(light * color[0] * 1, light * color[1] * 1, light * color[2] * 1) 
	return diffuse_light

def specular_light(view_point, normal, light_point, point, color):
	norm = point3(normal[0] / (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5, 
				  normal[1] / (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5,
				  normal[2] / (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5)
	light_direction = point3(light_point.x - point.x, light_point.y - point.y, light_point.z - point.z)
	scalar = norm.x * light_direction.x + norm.y * light_direction.y + norm.z * light_direction.z

	reflection_point = point3(2 * norm.x * scalar - light_direction.x,
							  2 * norm.y * scalar - light_direction.y,
							  2 * norm.z * scalar - light_direction.z)

	light = (reflection_point.x * view_point.x + reflection_point.y * view_point.y + reflection_point.z * view_point.z) / ((reflection_point.x**2 + reflection_point.y**2 + reflection_point.z**2)**0.5) / ((view_point.x**2 + view_point.y**2 + view_point.z**2)**0.5)
	light *= (light_direction.x * norm.x + light_direction.y * norm.y + light_direction.z * norm.z) / ((light_direction.x**2 + light_direction.y**2 + light_direction.z**2)**0.5) / ((norm.x**2 + norm.y**2 + norm.z**2)**0.5)
    
	specular_light = point3(light * color[0] * 1, light * color[1] * 1, light * color[2] * 1)
	return specular_light


def draw_light(image, points, color, z_buffer, light_point, norm):
	
	for point in points:
		if point.z <= z_buffer[800 * point.y + point.x]:
			lightd = diffuse_light(light_point, point, color, norm[0], norm[1], norm[2])
			lights = specular_light(point3(400, 300, 0), norm, light_point, point, color)
			image.putpixel((int(point.x), int(point.y)), (int(lightd.x + lights.x), int(lightd.y + lights.y), int(lightd.z + lights.z)))
			# image.putpixel((int(point.x), int(point.y)), (int(lightd.x), int(lightd.y), int(lightd.z)))

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

	with Image.open('light.png') as im:
		im.paste((0, 0, 0), (0, 0, im.size[0], im.size[1]))

		z_buffer = [1000] * 800 * 600

		points1 = fill3D(vertexes1)
		points2 = fill3D(vertexes2)

		update_buffer(points1, z_buffer)
		update_buffer(points2, z_buffer)

		draw_light(im, points2, (0, 0, 255), z_buffer, point3(400, 300, 50), get_plane(vertexes2[0], vertexes2[1], vertexes2[2]))
		draw_light(im, points1, (255, 0, 0), z_buffer, point3(400, 300, 50), get_plane(vertexes1[0], vertexes1[1], vertexes1[2]))
		
		im.save('light_with_spec.png')