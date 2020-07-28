from pygame import *
from pygame import event as events
from random import randrange
from text import Text
import os

move_translate = {
	K_LEFT: (-1, 0),
	K_RIGHT: (1, 0),
	K_UP: (0, -1),
	K_DOWN: (0, 1),
	K_a: (-1, 0),
	K_d: (1, 0),
	K_w: (0, -1),
	K_s: (0, 1)
}


class Player(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image = Surface((32, 32))
		self.image.fill((0, 200, 0))
		self.rect = self.image.get_rect()

	def update(self, keys, delta):
		move_x, move_y = 0, 0
		self.speed = 200 * delta

		for key in move_translate:
			if keys[key]:
				if not move_x:
					move_x = move_translate[key][0] * self.speed
				if not move_y:
					move_y = move_translate[key][1] * self.speed

		if move_x and move_y:
			move_x *= 0.7071
			move_y *= 0.7071

		self.rect.x += move_x
		self.rect.y += move_y


class Bullet(sprite.Sprite):
	def __init__(self, x, y, size):
		sprite.Sprite.__init__(self)
		self.image = Surface(size)
		self.image.fill((255, 255, 0))
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speed = -10

	def update(self):
		self.rect.y += self.speed
		if self.rect.bottom < 0:
			self.kill()


class Enemy(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image = Surface((16, 16))
		self.image.fill((255, 0, 0))
		self.rect = self.image.get_rect()
		self.spawn()

	def spawn(self):
		self.rect.x = randrange(624)
		self.rect.y = randrange(-100, -20)

	def update(self, keys, delta):
		self.rect.y += delta // randrange(1, 6)

		if self.rect.top > 640:
			self.spawn()


class Game:
	#Game.all_sprites = sprite.Group()
	def __init__(self, size, fps):
		self.clock = time.Clock()
		self.screen = display.set_mode(size)
		self.running = True
		self.fps = fps
		self.player = Player()
		self.all_sprites = sprite.Group()
		self.enemies = sprite.Group()
		self.bullets = sprite.Group()
		self.all_sprites.add(self.player)
		#Game.all_sprites.add(Text('Hello!', "fonts/Shoguns Clan.ttf", 32, (0, 255, 0), (50, 50)))
		self.keys = key.get_pressed()
		self.spawn_enemies(10)

	def spawn_enemies(self, number):
		for i in range(number):
			enemy = Enemy()
			self.all_sprites.add(enemy)
			self.enemies.add(enemy)

	def render(self):
		self.screen.fill((0, 0, 0))
		self.all_sprites.update(self.keys, self.delta)
		#display.update()
		self.all_sprites.draw(self.screen)
		display.flip()

	def loop(self):
		while self.running:
			self.delta = self.clock.tick(self.fps) / 1000
			for event in events.get():
				if event.type == QUIT:
					self.running = False
				elif event.type in [KEYUP, KEYDOWN]:
					if event.key == K_ESCAPE:
						self.running = False
					self.keys = key.get_pressed()
			self.render()


if __name__ == '__main__':
	init()
	mixer.init()
	os.environ['SDL_VIDEO_CENTERED'] = "1"
	display.set_caption("2Doom")
	Game((640, 480), 60).loop()
	quit()