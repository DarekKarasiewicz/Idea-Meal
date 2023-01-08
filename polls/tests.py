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
        Fridge.objects.create(user = user)
        Product.objects.create(user=user,
                               name ="test_product",
                               product_category = "Test",
                               unit = "test",)


    def test_user_fridge_test(self):
        user = User.objects.filter(username = "Forbiden_name")[0]
        self.assertIsNotNone(Fridge.objects.filter(user = user.id))

    def test_user_can_add_product(self):
        user = User.objects.filter(username = "Forbiden_name")[0]
        user_fridge = Fridge.objects.filter(user = user.id)[0]
        product = Product.objects.filter(name= "test_product")[0]
        test_product_in_fridge = Fridge_products_counts.objects.create(product= product, ammount=2, fridge=
                               user_fridge)
        tested = Fridge_products_counts.objects.filter(fridge=user_fridge.id)[0]
        self.assertEqual(tested.id,test_product_in_fridge.id)
