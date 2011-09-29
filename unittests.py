import unittest
import playvid
#import random

class testCVRect(unittest.TestCase):
    randomRects = 10
    def setUp(self):
        self.rectangle_list = []
        self.solution_list = []
    def test_known_rectangles(self):
        self.rectangle_list.append(((1,1),(3,3)))
        self.solution_list.append((1,1,2,2))
        for number, element in enumerate(self.rectangle_list):
            self.assertEqual(playvid.convert_to_cvrect(element),self.solution_list[number], "Failed to calculate cvRect properly from input data")
                            
if __name__=="__main__":
    unittest.main()
