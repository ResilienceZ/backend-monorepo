import unittest
from service.geohash import GeoHash

class TestGeohash(unittest.TestCase):
    def test_geohash(self):
        # Test cases with known geohash results
        test_cases = [
            {"latitude": 37.7749, "longitude": -122.4194, "precision": 12, "expected": "9q8yyk8ytpxr"},
            {"latitude": 40.7128, "longitude": -74.0060, "precision": 12, "expected": "dr5regw3ppyz"},
            {"latitude": 51.5074, "longitude": -0.1278, "precision": 12, "expected": "gcpvj0duq533"},
            {"latitude": -33.8688, "longitude": 151.2093, "precision": 12, "expected": "r3gx2f77bn44"},
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                result = GeoHash.encode(case["latitude"], case["longitude"], case["precision"])
                self.assertEqual(result, case["expected"])
    
    def test_default_precision(self):
        # Test the default precision of 12
        result = GeoHash.encode(37.7749, -122.4194)
        self.assertEqual(result, "9q8yyk8ytpxr")
    
    def test_different_precision(self):
        # Test geohash with different precisions
        result = GeoHash.encode(37.7749, -122.4194, precision=8)
        self.assertEqual(result, "9q8yyk8y")
        
        result = GeoHash.encode(37.7749, -122.4194, precision=5)
        self.assertEqual(result, "9q8yy")

    def test_boundary_conditions(self):
        # Test the boundary conditions
        result = GeoHash.encode(90.0, 180.0, precision=12)
        self.assertEqual(result, "zzzzzzzzzzzz")
        
        result = GeoHash.encode(-90.0, -180.0, precision=12)
        self.assertEqual(result, "000000000000")

if __name__ == '__main__':
    unittest.main()