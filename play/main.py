import pygame
import random

BLACK = (0,0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

r = random.randint(0, 255)
g = random.randint(10, 255)
b = random.randint(22, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Block(pygame.sprite.Sprite):
	""" Simple block player """

	def __init__(self):
		super().__init__()
		# background
		self.image = pygame.Surface([10, 20]) # ukuran kotak
		for i in range(100):
			self.image.fill((i,g,b))
		self.rect = self.image.get_rect()

	def reset_pos(self):
		self.rect.y = random.randrange(-300, -20) # reset posisi
		self.rect.x = random.randrange(SCREEN_WIDTH)

	def update(self):
		self.rect.y += 2

		if self.rect.y > SCREEN_HEIGHT + self.rect.height:
			self.reset_pos()

class Player(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([20, 20]) # ukuran kotak
		self.image.fill(RED)
		self.rect = self.image.get_rect()

	def update(self):
		""" update the player location """
		pos = pygame.mouse.get_pos()
		self.rect.x = pos[0]
		self.rect.y = pos[1]


class Game(object):

	def __init__(self):
		self.score = 0
		self.game_over = False

		self.block_list = pygame.sprite.Group()
		self.all_sprites_list = pygame.sprite.Group()

		for i in range(100):
			block = Block()

			block.rect.x = random.randrange(SCREEN_WIDTH)
			block.rect.y = random.randrange(-300, SCREEN_HEIGHT)

			self.block_list.add(block)
			self.all_sprites_list.add(block)

		self.player = Player()
		self.all_sprites_list.add(self.player)

	def process_events(self):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
			#print(event)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.game_over:
					self.__init__()
		return False

	def run_logic(self):
		if not self.game_over:
			# move all the sprites
			self.all_sprites_list.update()

			# see
			block_hit_list = pygame.sprite.spritecollide(self.player, self.block_list, True)

			for block in block_hit_list:
				self.score += 1
				print(self.score)

			if len(self.block_list) == 0:
				self.game_over = True

	def display_frame(self, screen):
		screen.fill(WHITE)

		if self.game_over:
			font = pygame.font.SysFont("serif", 25)
			text = font.render("Game Over, Click to restart", True, BLACK)
			center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
			center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
			screen.blit(text, [center_x, center_y])

		if not self.game_over:
			self.all_sprites_list.draw(screen)
		pygame.display.flip()


def main():
	pygame.init()
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)

	pygame.display.set_caption('Makan makan')
	pygame.mouse.set_visible(False)

	done = False
	clock = pygame.time.Clock()

	game = Game()

	while not done:
		done = game.process_events()

		# Update object position, check for collisions
		game.run_logic()

		game.display_frame(screen)

		clock.tick(60)

	pygame.quit()

if __name__ == '__main__':
	main()
