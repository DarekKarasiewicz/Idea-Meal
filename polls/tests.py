from django.test import TestCase
from django.contrib.auth.models import User

# MODELS IMPORTS
from .models import (
    Product,
    Comment,
    Recipe,
    Fridge,
    Fridge_products_counts,
    Comments_to_Recipe,
    Recipe_products_counts,
)

class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="Forbiden_name",
                            email="notyourbuisnes@oo.com",
                            password = "Fantasy123!")
        user_fridge = Fridge(user = user.id)
        product = Product(user=user.id, name =
                                         "test_product")


    def test_user_fridge_test(self):
        self.assertIsNotNone(user_fridge.objects.filter(user = user.id))

    def test_user_can_add_product(self):
        test_product_in_fridge = Fridge_products_counts(product= product, ammount=1, fridge=
                               user_fridge.id)
        self.assertEqual(Fridge_products_counts.objects.filter(fridge.user_fridge.id).id,test_product_in_fridge.id)
