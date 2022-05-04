import pygame as pg


class GFX:
    def __init__(self, disp_size, disp_scale, frame_delay):
        # colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.background = (247, 247, 247)
        self.midground = (218, 218, 218)
        self.foreground = (83, 83, 83)

        # setup
        self.disp_size = disp_size
        self.sf = disp_scale
        self.fd = frame_delay
        self.ground_level = 0
        self.disp = pg.display.set_mode(disp_size)
        self.images, self.image_rects = self.loadImages()
        self.gnd = 0
        self.font = pg.font.SysFont('Comic Sans MS', 30)

        # values
        self.dino_anim_tick = 0
        self.ptero_anim_tick = 0
        self.dino_image = 'dino_still'
        self.ptero_image = 'ptero_up'
        self.anim_tickstep = 1 * (self.fd / 30)

    def loadImages(self):
        """
        Imports all the images into a dictionary
        """
        dino_all = pg.image.load('bin/dino_images.png')
        w = dino_all.get_width()
        h = dino_all.get_height()

        # load in the images and scale them uniformly according to scale factor
        ground = dino_all.subsurface((2, 104, w - 4, h - 104))
        ground = pg.transform.scale(ground, (ground.get_width() * self.sf, ground.get_height() * self.sf))
        game_over = dino_all.subsurface((954, 29, 380, 20))
        game_over = pg.transform.scale(game_over, (game_over.get_width() * self.sf, game_over.get_height() * self.sf))
        cloud = dino_all.subsurface((954, 29, 380, 20))
        cloud = pg.transform.scale(cloud, (cloud.get_width() * self.sf, cloud.get_height() * self.sf))

        dino_still = dino_all.subsurface((1338, 2, 87, 93))
        dino_still = pg.transform.scale(dino_still, (dino_still.get_width() * self.sf, dino_still.get_height() * self.sf))
        dino_step1 = dino_all.subsurface((1514, 2, 87, 93))
        dino_step1 = pg.transform.scale(dino_step1, (dino_step1.get_width() * self.sf, dino_step1.get_height() * self.sf))
        dino_step2 = dino_all.subsurface((1602, 2, 87, 93))
        dino_step2 = pg.transform.scale(dino_step2, (dino_step2.get_width() * self.sf, dino_step2.get_height() * self.sf))

        cactus1 = dino_all.subsurface((652, 2, 49, 99))
        cactus1 = pg.transform.scale(cactus1, (cactus1.get_width() * self.sf, cactus1.get_height() * self.sf))
        cactus2 = dino_all.subsurface((801, 2, 150, 99))
        cactus2 = pg.transform.scale(cactus2, (cactus2.get_width() * self.sf, cactus2.get_height() * self.sf))
        cactus3 = dino_all.subsurface((702, 2, 99, 99))
        cactus3 = pg.transform.scale(cactus3, (cactus3.get_width() * self.sf, cactus3.get_height() * self.sf))
        cactus4 = dino_all.subsurface((446, 2, 33, 71))
        cactus4 = pg.transform.scale(cactus4, (cactus4.get_width() * self.sf, cactus4.get_height() * self.sf))
        cactus5 = dino_all.subsurface((480, 2, 67, 71))
        cactus5 = pg.transform.scale(cactus5, (cactus5.get_width() * self.sf, cactus5.get_height() * self.sf))
        cactus6 = dino_all.subsurface((548, 2, 101, 71))
        cactus6 = pg.transform.scale(cactus6, (cactus6.get_width() * self.sf, cactus6.get_height() * self.sf))

        ptero_up = dino_all.subsurface((260, 2, 91, 79))
        ptero_up = pg.transform.scale(ptero_up, (ptero_up.get_width() * self.sf, ptero_up.get_height() * self.sf))
        ptero_down = dino_all.subsurface((352, 2, 91, 79))
        ptero_down = pg.transform.scale(ptero_down, (ptero_down.get_width() * self.sf, ptero_down.get_height() * self.sf))

        image_map = {
            'ground': ground,
            'game_over': game_over,
            'cloud': cloud,
            'dino_still': dino_still,
            'dino_step1': dino_step1,
            'dino_step2': dino_step2,
            'cactus1': cactus1,
            'cactus2': cactus2,
            'cactus3': cactus3,
            'cactus4': cactus4,
            'cactus5': cactus5,
            'cactus6': cactus6,
            'ptero_up': ptero_up,
            'ptero_down': ptero_down
        }

        ground_1_rect = pg.rect.Rect(0, 0, ground.get_width(), ground.get_height())
        ground_2_rect = pg.rect.Rect(ground_1_rect.right, 0, ground.get_width(), ground.get_height())
        gow, goh = game_over.get_size()
        game_over_rect = pg.rect.Rect((self.disp_size[0] / 2) - (gow / 2), self.disp_size[1] / 3, gow, goh)
        rect_map = {
            'ground_1': ground_1_rect,
            'ground_2': ground_2_rect,
            'game_over': game_over_rect
        }

        return image_map, rect_map

    def setGround(self, ground):
        self.gnd = ground
        self.image_rects['ground_1'].top = ground - self.image_rects['ground_1'].h * 1.1 * self.sf
        self.image_rects['ground_2'].top = ground - self.image_rects['ground_2'].h * 1.1 * self.sf

    def getSizes(self):
        """
        Returns the sizes (shape) of the particular images that need to be exported to the game
        """
        size_map = {
            'dino': self.images['dino_still'].get_size(),
            'cactus1': self.images['cactus1'].get_size(),
            'cactus2': self.images['cactus2'].get_size(),
            'cactus3': self.images['cactus3'].get_size(),
            'cactus4': self.images['cactus4'].get_size(),
            'cactus5': self.images['cactus5'].get_size(),
            'cactus6': self.images['cactus6'].get_size(),
            'ptero': self.images['ptero_up'].get_size()
        }
        return size_map

    def animate(self, game_state):
        # update position for ground
        if self.image_rects['ground_2'].left <= 0:
            self.image_rects['ground_1'].move_ip(self.image_rects['ground_1'].width, 0)
            self.image_rects['ground_2'].move_ip(self.image_rects['ground_2'].width, 0)
        else:
            self.image_rects['ground_1'].move_ip(-1 * game_state['game_speed'], 0)
            self.image_rects['ground_2'].move_ip(-1 * game_state['game_speed'], 0)

        # update dino drawing
        if game_state['on_ground']:
            if self.dino_anim_tick < 4:
                self.dino_image = 'dino_step1'
            else:
                self.dino_image = 'dino_step2'
                if self.dino_anim_tick >= 8:
                    self.dino_anim_tick = 0
        else:
            self.dino_image = 'dino_still'

        # update ptero drawing
        if self.ptero_anim_tick < 10:
            self.ptero_image = 'ptero_up'
        else:
            self.ptero_image = 'ptero_down'
            if self.ptero_anim_tick >= 20:
                self.ptero_anim_tick = 0

        self.dino_anim_tick += self.anim_tickstep
        self.ptero_anim_tick += self.anim_tickstep

    def draw(self, game_state, dino, obstacles):
        """
        Draws the display for the game, given the current game state
        """
        self.disp.fill(self.background)

        # draw scrolling ground
        self.disp.blit(self.images['ground'], self.image_rects['ground_1'])
        self.disp.blit(self.images['ground'], self.image_rects['ground_2'])

        # draw running dino
        self.disp.blit(self.images[self.dino_image], dino.hitbox)

        # draw moving cacti
        for obst in game_state['obstacles']:
            if obst.name == 'ptero':
                self.disp.blit(self.images[self.ptero_image], obst.hitbox)
            else:
                self.disp.blit(self.images[obst.name], obst.hitbox)

        if game_state['showhb']:
            pg.draw.line(self.disp, (255, 0, 0), (0, self.gnd), (self.disp.get_width(), self.gnd))
            pg.draw.rect(self.disp, (255, 0, 0), dino.hitbox, 1)
            for obst in obstacles:
                pg.draw.rect(self.disp, (255, 0, 0), obst.hitbox, 1)

        text = self.font.render(str(game_state['score']), False, self.foreground)
        self.disp.blit(text, (0, 0))

        # update animations or disp game over
        if game_state['playing']:
            self.animate(game_state)
        else:
            self.dino_image = 'dino_still'
            self.disp.blit(self.images['game_over'], self.image_rects['game_over'])

        pg.display.flip()
