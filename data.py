import pygame, os
from math import *
from pygame import gfxdraw
from vector import Vector


def draw_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


WINDOW_SIZE = (960, 640)

BACKGROUND_COLOR_1 = (27, 25, 25)
BACKGROUND_COLOR_2 = (100, 100, 100)
PLAYER_COLOR = (150, 100, 150)
PLAYER_EYE_COLOR = (255, 255, 255)
BACK_WHITE_COLOR = (253, 253, 253)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, "image")

BACKGROUND = []
event_list = []
objects = []
walls = []


def col_check(obj):
    col_list = []
    for wall in walls:
        if obj.rect.colliderect(wall.rect):
            col_list.append(wall)
            continue
    return col_list


def move(obj):
    rect = obj.rect

    collision = {'top': False, 'bottom': False, 'right': False, 'left': False}

    rect.x += obj.vector.x
    col_list = col_check(obj)

    for col_obj in col_list:
        col_rect = col_obj.rect
        if obj.vector.x < 0:
            rect.left = col_rect.right
            collision['left'] = True
        if obj.vector.x > 0:
            obj.rect.right = col_rect.left
            collision['right'] = True

    rect.y += obj.vector.y
    col_list = col_check(obj)

    for col_obj in col_list:
        col_rect = col_obj.rect
        if obj.vector.y < 0:
            rect.top = col_rect.bottom
            collision['top'] = True
        if obj.vector.y > 0:
            rect.bottom = col_rect.top
            collision['bottom'] = True

    return rect, collision


class Object:
    def __init__(self, obj_id, kinds, loc, size):  # size[0] = wide, size[1] height
        self.id = obj_id
        self.type = kinds  # kind는 player, wall, area, obstacle
        self.direction = True  # True면 오른쪽
        self.gravity = Vector(0, 1)
        self.vector = Vector(1, -5)
        self.width = size[0]
        self.height = size[1]
        self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect = pygame.rect.Rect(loc, size)


class PlayerObject(Object):
    def draw(self, img):
        pygame.draw.rect(img, PLAYER_COLOR, self.rect)
        if self.direction:
            draw_circle(img, self.rect.centerx + 8, self.rect.centery - 5,
                        5 + round(sqrt(floor(self.vector.force() * 0.1))) * 0, PLAYER_EYE_COLOR)
        else:
            draw_circle(img, self.rect.centerx - 8, self.rect.centery - 5,
                        5 + round(sqrt(floor(self.vector.force() * 0.1))) * 0, PLAYER_EYE_COLOR)

    def physics(self):
        self.rect, self.collision = move(self)
        if self.collision['bottom'] or self.collision['top']:
            self.vector.y = 0
            self.vector.x = round(self.vector.x / 5)
        else:
            self.vector += self.gravity


class WallObject(Object):
    def __init__(self, obj_id, kinds, loc, size):
        super().__init__(obj_id, kinds, loc, size)
        del self.collision, self.vector, self.direction

    def draw(self, img):
        pygame.draw.rect(img, BLACK, self.rect)


def draw_screen(screen):
    screen.fill(BACKGROUND_COLOR_2)
    screen.blit(BACKGROUND[0], (0, 0))
    screen.blit(BACKGROUND[1], (-0.1 * objects[0].rect.topleft[0], 0))
    for obj in objects:
        if obj.type == "player":
            obj.draw(screen)
    for obj in walls:
        obj.draw(screen)

    screen.blit(BACKGROUND[2], (0, 0))
