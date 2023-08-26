import pygame
import pygame.gfxdraw as gfxdraw

BASE_IMG_PATH = "images/"


def draw_square(size, color=(255, 255, 255), alpha=255):
    surf = pygame.Surface((size * 2, size * 2))

    pygame.draw.rect(surf, color, (0, 0, size, size))
    surf.set_alpha(alpha)
    surf.set_colorkey((0, 0, 0))
    return surf


def draw_border(size, color=(255, 255, 255), alpha=255):
    surf = pygame.Surface((size * 2, size * 2))
    gfxdraw.aapolygon(surf, ((0, 0), (size, 0), (size, size), (0, size)), color)

    surf.set_alpha(alpha)
    surf.set_colorkey((0, 0, 0))
    return surf


def load_image(rpath, scale=False, alpha=255):
    path = BASE_IMG_PATH + rpath

    img = pygame.image.load(path).convert()  # convert method makes it easier to render

    img.set_colorkey((0, 0, 0))
    img.set_alpha(alpha)
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


def load_images(path):
    images = []
    for img_path in os.listdir(BASE_IMG_PATH + path):
        img = load_img(path + "/" + img_path)

        images.append(img)
    return images


def list_to_location(myList):
    loc = str(myList[0]) + ";" + str(myList[1])
    return loc
