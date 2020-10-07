from structs import test_structs
import unittest


class TestCase1(test_structs.Test_UserStats):
    emp: int = 0


print("Unit tests started")
if __name__ == '__main__':
    unittest.main()
