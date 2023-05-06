import pygame


def scale_image(img, factor):
    size = round(img.get_width()* factor),round(img.get_height()* factor)
    return pygame.transform.scale(img,size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image,angle)        # This rotates the image from the top left so to rotate it from the center we write the following
    new_rect = rotated_image.get_rect(center= image.get_rect(topleft = top_left).center)  # Makes the center of the rectangle is the center of the image to rotate uponn instead of rotating on its corner point
    win.blit(rotated_image, new_rect.topleft)