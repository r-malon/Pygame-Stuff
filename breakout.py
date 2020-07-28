from pygame import *
from pygame import event as events
from random import randrange, choice
from json import load
import os
from text import Text

with open('config.json', encoding='utf-8') as f:
	config = load(f)

move_translate = {
	K_LEFT: (-1, 0),
	K_RIGHT: (1, 0),
	K_a: (-1, 0),
	K_d: (1, 0),
}

class Player(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image = Surface((128, 32), SRCALPHA)
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.centerx = 320
		self.rect.centery = 460

	def update(self, keys, delta):
		move_x = 0
		self.speed = delta // 2

		for key in move_translate:
			if keys[key]:
				move_x = move_translate[key][0] * self.speed

		self.rect.x += move_x

		if self.rect.right > config["win_width"]:
			self.rect.right = config["win_width"]

		if self.rect.left < 0:
			self.rect.left = 0


class Ball(sprite.Sprite):
	def __init__(self, radius):
		sprite.Sprite.__init__(self)
		self.image = Surface((radius * 2, radius * 2), SRCALPHA)
		draw.circle(self.image, (255, 0, 255), (radius, radius), radius)
		self.rect = self.image.get_rect()
		self.rect.centerx = 320
		self.rect.centery = 420
		self.speed = [randrange(3, 10), randrange(-10, 10)]
		self.killed = False

	def update(self, keys, delta):
		self.rect.x += self.speed[0]
		self.rect.y += self.speed[1]

		if self.rect.bottom > config["win_height"]:
			self.killed = True
			self.kill()

		if self.rect.right > config["win_width"] or self.rect.left < 0 or self.rect.top < 0:
			self.bounce()

	def bounce(self):
		self.speed[0] = -self.speed[0]
		self.speed[1] = randrange(-10, 10)


class Block(sprite.Sprite):
	colors = [(255, 0, 0) , (0, 255, 0), (0, 0, 255)]
	def __init__(self, size, position):
		sprite.Sprite.__init__(self)
		self.image = Surface(size, SRCALPHA)
		self.image.fill(choice(Block.colors))
		self.rect = self.image.get_rect()
		self.spawn(position)

	def spawn(self, position):
		self.rect.x = position[0]
		self.rect.y = position[1]


class Game:
	def __init__(self):
		self.clock = time.Clock()
		self.screen = display.set_mode((config["win_width"], config["win_height"]))
		self.running = True
		self.fps = config["MAX_FPS"]
		self.player = Player()
		self.ball = Ball(16)
		self.blocks = sprite.Group()
		self.spawn_blocks(8, 8)
		self.all_sprites = sprite.Group()
		self.all_sprites.add(self.player)
		self.all_sprites.add(self.ball)
		self.all_sprites.add(self.blocks)
		self.keys = key.get_pressed()

	def spawn_blocks(self, rows, columns):
		width, height = config["win_width"] // columns, config["win_height"] // rows
		for x in range(columns):
			for y in range(rows):
				self.blocks.add(Block((width - 1, height - 1), (width * x, height * y)))

	def check_collisions(self):
		if sprite.spritecollide(self.ball, self.blocks, True):
			self.ball.bounce()

		if sprite.collide_mask(self.ball, self.player):
			self.ball.rect.x -= self.ball.speed[0]
			self.ball.rect.y -= self.ball.speed[1]
			self.ball.bounce()

	def check_status(self):
		if not len(self.blocks) or self.ball.killed:
			#self.end_game()
			self.running = False

	def end_game(self):
		self.screen.fill((0, 0, 200))
		self.all_sprites.add(Text('GAME OVER', None, 128, (0, 255, 0), (50, 50)))
		display.flip()
		time.wait(5000)
		self.running = False

	def render(self):
		self.screen.fill((0, 0, 0))
		self.all_sprites.update(self.keys, self.delta)
		self.all_sprites.draw(self.screen)
		display.flip()

	def loop(self):
		while self.running:
			self.delta = self.clock.tick(self.fps)
			for event in events.get():
				if event.type == QUIT:
					self.running = False
				elif event.type in [KEYUP, KEYDOWN]:
					if event.key == K_ESCAPE:
						self.running = False
					self.keys = key.get_pressed()
			self.check_collisions()
			self.check_status()
			self.render()


if __name__ == '__main__':
	init()
	mixer.init()
	os.environ['SDL_VIDEO_CENTERED'] = "1"
	display.set_caption(config["title"])
	Game().loop()
	quit()