import pygame




class Utils:

    def re_size(size, relative_percent):
        return (int(size[0] * relative_percent),
                int(size[1] * relative_percent))

    def load_and_convert(path):
        return pygame.image.load(path).convert_alpha()

    def transform_scale(img, size):
        return pygame.transform.scale(img,size)
