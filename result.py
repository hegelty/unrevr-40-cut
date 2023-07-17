from PIL import Image, ImageDraw


'''
2100 2970

사이 간격 5px
8 * 5 -> 35 * 20
사진 4n * 3n
32n + 35 * 15n + 20
340 * 255

n = 86

좌우 간격 91/92

하단 간격 92

시작점 91, 698

전체 * 2
'''
def make_40_cut(file_hash):
    original_image_path = "./images/40.png"
    start_point = [91 * 2, 630 * 2]
    image_size = [86*4 * 2, 86*3 * 2]
    padding = 5 * 2

    original_image = Image.open(original_image_path)
    cnt = 0
    for i in range(5):
        for j in range(8):
            image = Image.open("./images/" + file_hash + "/" + str(cnt) + ".png")
            crop_width = image.height * image_size[0] / image_size[1]
            image = image.crop(((image.width - crop_width)/2, 0, (image.width + crop_width)/2, image.height))
            image = image.resize((image_size[0], image_size[1]))
            original_image.paste(image, (start_point[0] + (image_size[0] + padding) * j,
                                         start_point[1] + (image_size[1] + padding) * i))
            cnt += 1

    original_image.save("./images/" + file_hash + "/output.png")
    return "./images/" + file_hash + "/output.png"


def make_4_cut(file_hash):
    original_image_path = "./images/4.png"
    start_point = [57, 114]
    image_size = [633 - 57, 576 - 114]
    padding = [111, 10]

    frame_image_path = "./images/4.png"
    frame_image = Image.open(frame_image_path)
    original_image = Image.new("RGBA", (frame_image.width, frame_image.height), (255, 255, 255, 0))

    for i in range(4):
        for j in range(2):
            image = Image.open("./images/" + file_hash + "/" + str(i) + ".png")
            crop_width = image.height * image_size[0] / image_size[1]
            image = image.crop(((image.width - crop_width)/2, 0, (image.width + crop_width)/2, image.height))
            image = image.resize((image_size[0], image_size[1]))
            original_image.paste(image, (start_point[0] + (image_size[0] + padding[0]) * j,
                                         start_point[1] + (image_size[1] + padding[1]) * i))

    # mask if frame pixel's alpha is not 0
    for i in range(frame_image.width):
        for j in range(frame_image.height):
            if frame_image.getpixel((i, j))[3] != 0:
                original_image.putpixel((i, j), frame_image.getpixel((i, j)))

    original_image.save("./images/" + file_hash + "/output.png")
    return "./images/" + file_hash + "/output.png"
