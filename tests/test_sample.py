import unittest
import sys
# append the parent folder
sys.path.append('../') 
# import out class located in "battleship" and then in 
from battleship.api import create_board, check_ship_range, check_ship_overlap, game_board, ships

import numpy as np

class TestSampleClass(unittest.TestCase):

    def test_create_board(self):
        # loop on each row of the board to make sure it`s full of zeros 
        for index in range(len(create_board(10,10))):
           self.assertCountEqual(create_board(10,10)[index], np.zeros((10, 10))[index])         

    def test_check_ship_range_H(self):
        shipTest =  {
            "x": 5,
            "y": 5,
            "size": 6,
            "direction": "H"
        }
        self.assertEqual(check_ship_range(shipTest), False)

    def test_check_ship_range_V(self):
        shipTest =  {
            "x": 2,
            "y": 7,
            "size": 7,
            "direction": "V"
        }
        self.assertEqual(check_ship_range(shipTest), False)

if __name__=="__main__":
    unittest.main()
