from django.test import TestCase
from restaurant.models import MenuItem

class MenuItemtest(TestCase):
    def test_get_item(self):
        item = MenuItem.objects.create(title="IceCream", price='80', inventory=100)
        itemstr = item.get_item()
        print(itemstr)
        self.assertEqual(itemstr, "IceCream : 80")