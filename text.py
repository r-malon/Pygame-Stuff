from pygame import sprite, font

class Text(sprite.Sprite):
	def __init__(self, msg, font_name, size, color, topleft):
		sprite.Sprite.__init__(self)
		self.msg = msg
		self.size = size
		self.font_name = font_name
		self.color = color
		self.image = self.write()
		self.rect = self.image.get_rect()
		self.rect.topleft = topleft

	def write(self):
		return font.Font(self.font_name, self.size).render(self.msg, True, self.color).convert_alpha()
