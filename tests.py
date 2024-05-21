import unittest
import os

import digital
import temp
#import waterlvl    water level testing possibly infeasible due to the library requiring hardware to load at all

class TestSensors(unittest.TestCase):
    temp_file_1 = None
    temp_file_2 = None

    def setUp(self) -> None:
        os.mkdir("./test_dir")
        os.mkdir("./test_dir/28_temp_test_dir")
        self.temp_file_1 = open("./test_dir/28_temp_test_dir/test1", 'w')
        self.temp_file_1.write("7d 01 4b 46 7f ff 0c 10 3c : crc=3c YES\n7d 01 4b 46 7f ff 0c 10 3c t=23812")
        self.temp_file_1.close()
        self.temp_file_2 = open("./test_dir/28_temp_test_dir/test2", 'w')
        self.temp_file_2.write("7d 01 4b 46 7f YES\ntest failure")
        self.temp_file_2.close()
        return super().setUp()
    
    def test_temp(self):
        # test finding device
        self.assertEqual(temp.find_device("test_dir/"), "test_dir\\28_temp_test_dir")

        # test reading device
        self.assertEqual(temp.read("./test_dir/28_temp_test_dir/test1"), 23.812)

        # test throwing error with malformed file
        self.assertEqual(temp.read("./test_dir/28_temp_test_dir/test2"), -997)

    def test_digital(self):
        # test throwing error without serial device
        self.assertEqual(digital.read_data("./test_dir/None"), "-10")

        # further testing is difficult without a real serial device
    
    def tearDown(self) -> None:
        os.remove("./test_dir/28_temp_test_dir/test2")
        os.remove("./test_dir/28_temp_test_dir/test1")
        os.rmdir("./test_dir/28_temp_test_dir")
        os.rmdir("./test_dir")
        return super().tearDown()

if __name__ == '__main__':
    unittest.main()