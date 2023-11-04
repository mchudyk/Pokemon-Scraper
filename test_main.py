import unittest
from main import remove_duplicates

class RemoveDuplicatesTestCase(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(remove_duplicates([]), [])

    def test_no_duplicates(self):
        sample_data = [{'id': 1, 'name': 'Name1'}, {'id': 2, 'name': 'Name2'}]
        self.assertEqual(remove_duplicates(sample_data), sample_data)

    def test_with_duplicates(self):
        sample_data = [
            {'id': 1, 'name': 'Name1'},
            {'id': 1, 'name': 'Name1'},
            {'id': 2, 'name': 'Name2'}
        ]
        expected_data = [
            {'id': 1, 'name': 'Name1'},
            {'id': 2, 'name': 'Name2'}
        ]
        self.assertEqual(remove_duplicates(sample_data), expected_data)

if __name__ == '__main__':
    unittest.main()