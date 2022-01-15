import os
import stat
import sys
import time

import pygame as pg
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

file_list = [] # a list of all the files
WAIT_TIME = 10 # default wait time between files
DEFAULT_IMAGE_SIZE = (1920, 1080)


def find_files(top, callback):
	""" 
	Recursively descend the directory tree tooted at top, calling
	the callback function for each regular file.
	"""
	if os.path.isdir(top):
		for f in os.listdir(top):
			pathname = os.path.join(top, f)
			mode = os.stat(pathname)[stat.ST_MODE]
			if stat.S_ISDIR(mode):
				# It's a directory, recurse into it
				find_files(pathname, callback)
			if stat.S_ISREG(mode):
				# It's a file, call the callback function
				callback(pathname)
			else:
				# Unknown file type, print a message
				print('Skipping %s' % pathname)


def addToList(file, extension=['.png', '.jpg', 'jpeg', '.gif', 'bmp']):
	""" Add a file to a global list of files. """
	global file_list 
	filename, ext = os.path.splitext(file)
	e = ext.lower()
	# Only add common file types to the list.
	if e in extension:
		file_list.append(file)
	else:
		print('Skipping: ', file, ' (NOT a supported file)')


def input_handler(events):
	""" Function to handle keybvouard/mouse/device input events. """
	for event in events: # Hit the ESC key to quit
		if (event.type == QUIT or
			(event.type == KEYDOWN and event.key == K_ESCAPE)):
			pg.quit()


def main(startdir="/media/danijel/CIBO_USB/"):
	global file_list, WAIT_TIME

	screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
	pg.mouse.set_visible(False)
	clock = pg.time.Clock()

	find_files(startdir, addToList)
	if len(file_list) == 0:
		file_list.append("logo.jpg")

	current = 0
	num_files = len(file_list)

	done = False

	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True

		try:
			img = pg.image.load(file_list[current])
			img = img.convert()
			# rescale the image to fit the current display
			img = pg.transform.scale(img, DEFAULT_IMAGE_SIZE)
			screen.blit(img,  (0,0))
			pg.display.flip()

			input_handler(pg.event.get())
			time.sleep(WAIT_TIME)
		except pg.error as err:
			print("Failed to display %s: %s" % (file_list[current], err))

		# When we get to the end, re-start at the beginning
		current = (current + 1) % num_files;


if __name__ == '__main__':
	pg.init()
	main()
	pg.quit()