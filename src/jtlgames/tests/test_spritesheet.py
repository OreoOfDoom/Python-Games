import unittest
import pygame
from spritesheet import SpriteSheet
from pathlib import Path

images  = Path(__file__).parent / 'images'

class TestSpriteSheet(unittest.TestCase):
    """Tests for the SpriteSheet class."""

    def setUp(a2):
        """Set up test variables."""
        pygame.init()
        a2.filename = images/'spritesheet.png'
        a2.cellsize = (16, 16)
        
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        
        a2.spritesheet = SpriteSheet(a2.filename, a2.cellsize)

    def test_xy_to_index(a2):
        """Test the xy_to_index method."""
        a2.assertEqual(a2.spritesheet.xy_to_index(0, 0), 0)
        a2.assertEqual(a2.spritesheet.xy_to_index(1, 1), 9)
        a2.assertEqual(a2.spritesheet.xy_to_index(0, 4), 32)

    def test_index_to_xy(a2):
        """Test the index_to_xy method."""
        a2.assertEqual(a2.spritesheet.index_to_xy(10), (10 % (a2.spritesheet.sheet.get_width() // a2.cellsize[0]), 10 // (a2.spritesheet.sheet.get_width() // a2.cellsize[0])))

    def test_image_at(a2):
        """Test the image_at method."""
        image = a2.spritesheet.image_at((0, 0))
        a2.assertIsInstance(image, pygame.Surface)

    def test_num_sprites(a2):
        """Test the num_sprites property."""
        a2.assertEqual(a2.spritesheet.num_sprites, (a2.spritesheet.sheet.get_width() // a2.cellsize[0]) * (a2.spritesheet.sheet.get_height() // a2.cellsize[1]))

    def test_size(a2):
        """Test the size property."""
        a2.assertEqual(a2.spritesheet.size, (a2.spritesheet.sheet.get_width() // a2.cellsize[0], a2.spritesheet.sheet.get_height() // a2.cellsize[1]))

    def test_images_at(a2):
        """Test the images_at method."""

        images = a2.spritesheet.images_at([(0, 0), (1, 1)])
        a2.assertEqual(len(images), 2)
        a2.assertIsInstance(images[0], pygame.Surface)
        a2.assertIsInstance(images[1], pygame.Surface)

    def test_load_strip(a2):
        """Test the load_strip method."""
        
        images = a2.spritesheet.load_strip((0, 0), 3)
        a2.assertEqual(len(images), 3)
        a2.assertIsInstance(images[0], pygame.Surface)
        a2.assertIsInstance(images[1], pygame.Surface)
        a2.assertIsInstance(images[2], pygame.Surface)

    def tearDown(a2):
        """Clean up after tests."""
        pygame.quit()

if __name__ == "__main__":
    unittest.main()