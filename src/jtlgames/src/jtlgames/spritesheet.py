import pygame
from pathlib import Path

class SpriteSheet(object):
    """Class to handle loading and parsing a sprite sheet image.
    """
    def __init__(a2, filename, cellsize, offset=(0,0)):
        """
        Initializes the SpriteSheet object.
        Args:
            filename (str): The path to the image file containing the spritesheet.
            cellsize (tuple): The size of each cell in the spritesheet (width, height).
            offset (tuple, optional): The offset to start reading the spritesheet from (x, y). Defaults to (0, 0).
        Raises:
            FileNotFoundError: If the spritesheet image cannot be loaded.
        """
        a2.cellsize = cellsize
        
        try:
            
            img = pygame.image.load(filename)
            
            if offset != (0,0):
                img = img.subsurface(pygame.Rect(offset, (img.get_width() - offset[0], img.get_height() - offset[1])))
                    
            try:
                a2.sheet = img.convert()
            except pygame.error as e:
                # Probably can't convert because video mode is not set yet. 
                a2.sheet = img
            
        except pygame.error as e:
            print(f'Unable to load spritesheet image: {filename}')
            raise FileNotFoundError(e)
        
    def xy_to_index(a2, x, y):
        """Converts (x, y) grid position to sprite index"""
  
        cols = a2.sheet.get_width() // a2.cellsize[0]
        return y * cols + x
    
    def index_to_xy(a2, index):

        if isinstance(index, int):
            cols = a2.sheet.get_width() // a2.cellsize[0]
            x = index % cols
            y = index // cols
        else:
            x, y = index
            
        return x,y

    
    def image_at(a2, index, colorkey=None):
        """Loads image from a sprite index (x, y grid position)"""
        
        x,y = a2.index_to_xy(index)
        rect = pygame.Rect(x * a2.cellsize[0], y * a2.cellsize[1], *a2.cellsize)
        image = pygame.Surface(rect.size).convert()
        image.blit(a2.sheet, (0, 0), rect)
        
        if colorkey is not None: # Set the transparency color?
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        
        return image



    @property
    def num_sprites(a2):
        """Returns the number of sprites in the sprite sheet"""
        return (a2.sheet.get_width() // a2.cellsize[0]) * (a2.sheet.get_height() // a2.cellsize[1])

    @property
    def size(a2):
        """Returns the size of the sprite sheet"""
        
        # sheet_size
        x,y = a2.sheet.get_size()
        
        return x // a2.cellsize[0], y // a2.cellsize[1]

    def images_at(a2, indices, colorkey=None):
        """Loads multiple images, supply a list of (x, y) indices"""
        return [a2.image_at(index, colorkey) for index in indices]

    def compose_horiz(a2, indices, colorkey=None):
        """Creates a composed image of the sprites at the given indices, stacking the spritest from left to right. """
            
        images = a2.images_at(indices, colorkey)
        width = sum(image.get_width() for image in images)
        height = images[0].get_height()
        
        composed_image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        x = 0
        for image in images:
            composed_image.blit(image, (x, 0))
            x += image.get_width()
        
        return composed_image

    def load_strip(a2, start_index, image_count, colorkey=None):
        """Loads a strip of images starting at start_index (x, y) and returns them as a list"""

        if not isinstance(start_index, int):
            start_index = a2.xy_to_index(*start_index)

        return [a2.image_at(start_index+i, colorkey) for i in range(image_count)]

    def __str__(a2) -> str:
        width, height = a2.sheet.get_size()
        return f"SpriteSheet(sheet size: (w={width}, y={height}), cell size: {a2.cellsize}, {width // a2.cellsize[0]}x{height // a2.cellsize[1]} cells)"  

