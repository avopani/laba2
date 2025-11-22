import unittest
from app import app
import os

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # Устанавливаем переменную окружения STUDENT_NAME для теста
        os.environ['STUDENT_NAME'] = 'TestStudent'

    def tearDown(self):
        # Очищаем переменную окружения после теста
        os.environ.pop('STUDENT_NAME', None)

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
