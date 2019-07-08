import unittest

from app import get_presigned_url


class AppTestCase(unittest.TestCase):
    def test_get_signed_url(self):
        url = 'https://www.example.com/images/image.jpg'
        resource = 'https://www.example.com/images/*'
        presigned_url_parameters = get_presigned_url(url, resource)
        self.assertEqual(presigned_url_parameters, '')


if __name__ == '__main__':
    unittest.main()
