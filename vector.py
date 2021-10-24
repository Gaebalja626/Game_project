from math import *


def point_vector(loc1, loc2):
    loc2 = (loc2[0] - loc1[0], loc2[1] - loc1[1])
    return Vector(loc2[0], loc2[1])


class Vector:
    def __init__(self, x, y, limit=990):
        self.x, self.y = x, y
        self.limit = limit

    def __add__(self, other):
        if type(other) == list or type(other) == tuple:
            return Vector(self.x + other[0], self.y + other[1])
        elif type(other) == Vector:
            if self.force() < self.limit:
                return Vector(self.x + other.x, self.y + other.y)
            else:
                return Vector(0, 0)
        else:
            raise TypeError("use type list or tuple or Vector")

    def __sub__(self, other):
        if type(other) == list or type(other) == tuple:
            return Vector(self.x - other[0], self.y - other[1])
        elif type(other) == Vector:
            return Vector(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("use type list or tuple or Vector")

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return Vector(self.x * other, self.y * other)
        else:
            raise TypeError("use type int or float")

    def __truediv__(self, other):
        if type(other) == int or type(other) == float:
            return Vector(self.x / other, self.y / other)
        else:
            raise TypeError("use type int or float")

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def force(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        if self.force() > 0:
            return self / self.force()
        else:
            return Vector(0, 0)

    def flip_x(self):  # x축에 대해 대칭
        return Vector(self.x * -1, self.y)

    def flip_y(self):  # y축에 대해 대칭
        return Vector(self.x, self.y * -1)


#
#                 ● 1     ● 0
#
#
#                 ● 2     ● 3
#
# obj_type : 0 = "일반 옵젝"
#            1 = "벽"
#            2 = "보여주기"


class SquareObject:
    def __init__(self, obj_type, loc, vector, mass, wide, height, gravity=True, friction=0.8, bounce=0.8):
        self.loc = loc
        self.vector = vector
        self.mass = mass
        self.gravity = gravity
        self.wide, self.height = wide, height
        self.max_point = (self.loc[0] + self.wide / 2, self.loc[1] + self.height / 2)
        self.min_point = (self.loc[0] - self.wide / 2, self.loc[1] - self.height / 2)
        self.obj_type = obj_type
        self.friction, self.bounce = friction, bounce

    def __eq__(self, other):
        return self.vector == other.vector and self.loc == other.loc and self.mass == other.mass

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self):
        return SquareObject(self.obj_type, self.loc, self.vector, self.mass, self.wide, self.height, self.gravity)

    def point_list(self):
        return [(self.loc[0] + self.wide / 2, self.loc[1] + self.height / 2),
                (self.loc[0] - self.wide / 2, self.loc[1] + self.height / 2),
                (self.loc[0] - self.wide / 2, self.loc[1] - self.height / 2),
                (self.loc[0] + self.wide / 2, self.loc[1] - self.height / 2)]

    def is_in(self, loc):
        return self.min_point[0] < loc[0] < self.max_point[0] \
               and self.min_point[1] < loc[1] < self.max_point[1]

    def predict(self):  # 현재 물체의 벡터를 사용해서 벡터만큼 움직였을때 위치를 반환
        return tuple(self.vector + self.loc)

    def move(self, loc=-1):
        if loc == -1:
            self.loc = self.predict()
        else:
            self.loc = loc
        self.max_point = (self.loc[0] + self.wide / 2, self.loc[1] + self.height / 2)
        self.min_point = (self.loc[0] - self.wide / 2, self.loc[1] - self.height / 2)
