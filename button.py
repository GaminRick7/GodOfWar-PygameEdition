"""
ICS3U
Raihaan Sandhu
This file is responsible for creating the button
"""

class imageButton():
	def __init__(self, image, pos):
		'''
		Args: image, pos
		Returns: none
		Creates a button
		'''
		#button image
		self.image = image
		#position of the button on the screen
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		#image rect
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		'''
		Args: none
		Returns: none
		blits button onto screen
		'''
		screen.blit(self.image, self.rect)

	def checkForInput(self, position):
		
		'''
		Args: position
		Returns: True, False
		checks if the x position of the mouse position is within the x coordinates of the button
		checks if the y position of the mouse position is within the y coordinates of the button
		'''
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False