from PIL import Image

def sobel_filter(image, width, height):
    kernel_x = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    kernel_y = [-1, -2, -1, 0, 0, 0, 1, 2, 1]

    sobel_x = [0] * len(image)
    sobel_y = [0] * len(image)
    for i in range(1, width - 1):
        for j in range(1, height - 1):
            for k in range(-4, 5):
                sobel_x[j * width + i]  += image[j * width + i + k] * kernel_x[k + 4]
                sobel_y[j * width + i]  += image[j * width + i + k] * kernel_y[k + 4] 
    gradient_magnitude = list(map(lambda a, b: int((a**2 + b**2)**0.5), sobel_x, sobel_y))
    
    return gradient_magnitude

if __name__ == '__main__':
    with Image.open('example.png') as im:
        im_arr = im.convert('L').getdata()
        result = sobel_filter(im_arr, im.size[0], im.size[1])

        new_im = Image.new(mode="RGB", size=(im.size[0], im.size[1]))
        new_im.putdata(result)
        new_im = new_im.convert('L')
        new_im.save('sobel_example.png')
        new_im.close()
