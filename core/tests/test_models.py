from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='jahid@gmail.com', password="testpass"):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Every Method name should start with test_"""

    def test_create_user_with_email_successful(self):
        """Test createing user with an email is successful"""
        email = "jahid@gmail.com"
        password = "Test1234"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalize(self):
        email = "jahid@GMAIL.COM"
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'jahid@gmail.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Jahid"
        )
        self.assertEqual(str(tag), tag.name)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

