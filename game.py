import pygame, sys
from data import *
from pygame.locals import *

import vector

# obj.id() = 오브젝트 인덱스

# Player_Move_left, right, jump
# Event_Area_Enter
# Coll_With_Button / Obstacle/ 


# move_player

test_player = PlayerObject(len(objects), "player", (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2), (40, 40))


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("절대지지않겠다")
        self.clock = pygame.time.Clock()

        self.bg_1 = pygame.image.load(os.path.join(DIR_IMAGE, "back_1.jpg"))
        self.bg_1 = pygame.transform.smoothscale(self.bg_1, WINDOW_SIZE)
        self.bg_2 = pygame.image.load(os.path.join(DIR_IMAGE, "back_2.png"))
        self.bg_2 = pygame.transform.smoothscale(self.bg_2, (self.bg_2.get_size()[0] * 0.9, WINDOW_SIZE[1]))
        self.bg_3 = pygame.image.load(os.path.join(DIR_IMAGE, "back_3.png"))
        self.bg_3 = pygame.transform.smoothscale(self.bg_3, WINDOW_SIZE)
        self.camera_scroll = [1,0]
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.screen_scaled = pygame.Surface(WINDOW_SIZE)

        BACKGROUND.append(self.bg_1)
        BACKGROUND.append(self.bg_2)
        BACKGROUND.append(self.bg_3)
        objects.append(test_player)
        test_wall = WallObject(len(walls), "wall", (-100, 523), (3000, 20))
        walls.append(test_wall)
        test_wall_1 = WallObject(len(walls), "wall", (520, 470), (500, 100))
        walls.append(test_wall_1)

        self.keyLeft = False
        self.keyRight = False
        self.keyJump = False

        self.run()

    def convert_img(self):
        self.bg_1 = self.bg_1.convert()
        self.bg_2 = self.bg_2.convert()
        self.bg_3 = self.bg_3.convert()

    def run(self):
        while True:
            # 배경 그리기
            self.screen_scaled.fill(BACKGROUND_COLOR_2)

            # 이벤트 입력받기
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.convert_img()
                    print(pygame.mouse.get_pos())
                    print(test_player.rect.center)
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.keyLeft = True
                    if event.key == K_RIGHT:
                        self.keyRight = True
                    if event.key == K_SPACE or event.key == K_UP:
                        self.keyJump = True
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.keyLeft = False
                    if event.key == K_RIGHT:
                        self.keyRight = False
                    if event.key == K_SPACE or event.key == K_UP:
                        self.keyJump = False
            # 플레이어 움직임 처리
            delta = [0, 0]
            if self.keyLeft:
                delta[0] += -3
            if self.keyRight:
                delta[0] += 3
            if delta[0] > 0:
                test_player.direction = True
            if delta[0] < 0:
                test_player.direction = False
            if self.keyJump:
                if test_player.collision["bottom"]:
                    delta[1] = -15
            test_player.vector.x += delta[0]
            if abs(test_player.vector.x) >= 5:
                test_player.vector.x = 5 * abs(test_player.vector.x) / test_player.vector.x
            test_player.vector.y += delta[1]
            test_player.physics()

            # 화면 그리기
            draw_screen(self.screen_scaled)
            """
            try:
                serf = self.screen_scaled.subsurface((loc[0] - 300, loc[1] - 400, 600, 300))
                self.screen.blit(serf, (0, 0))
            except:
                pass
            """
            self.screen.blit(self.screen_scaled, (0, 0))
            pygame.display.flip()
            self.clock.tick(120)


if __name__ == "__main__":
    game = Game()
