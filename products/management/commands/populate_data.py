from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product
from django.core.files.base import ContentFile
import os

class Command(BaseCommand):
    help = 'Populate the database with sample data for Side Wind'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create categories
        categories_data = [
            {
                'name': 'Clothing',
                'slug': 'clothing',
                'description': 'Premium men\'s clothing including shirts, pants, jackets, and more.'
            },
            {
                'name': 'Accessories',
                'slug': 'accessories',
                'description': 'Stylish accessories including watches, belts, wallets, and jewelry.'
            },
            {
                'name': 'Footwear',
                'slug': 'footwear',
                'description': 'High-quality footwear including shoes, boots, and sneakers.'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample products
        products_data = [
            {
                'name': 'Classic White Oxford Shirt',
                'slug': 'classic-white-oxford-shirt',
                'category': categories['clothing'],
                'description': 'A timeless white Oxford shirt made from premium cotton. Perfect for any occasion.',
                'price': 89.99,
                'stock': 50,
                'featured': True
            },
            {
                'name': 'Slim Fit Dark Jeans',
                'slug': 'slim-fit-dark-jeans',
                'category': categories['clothing'],
                'description': 'Modern slim fit jeans in dark wash. Comfortable and stylish.',
                'price': 129.99,
                'sale_price': 99.99,
                'stock': 30,
                'featured': True
            },
            {
                'name': 'Leather Bomber Jacket',
                'slug': 'leather-bomber-jacket',
                'category': categories['clothing'],
                'description': 'Classic leather bomber jacket with a modern twist. Durable and stylish.',
                'price': 299.99,
                'stock': 20,
                'featured': True
            },
            {
                'name': 'Premium Leather Watch',
                'slug': 'premium-leather-watch',
                'category': categories['accessories'],
                'description': 'Elegant leather watch with a minimalist design. Perfect for everyday wear.',
                'price': 199.99,
                'stock': 25,
                'featured': True
            },
            {
                'name': 'Classic Leather Belt',
                'slug': 'classic-leather-belt',
                'category': categories['accessories'],
                'description': 'Handcrafted leather belt with a classic buckle design.',
                'price': 59.99,
                'stock': 40,
                'featured': False
            },
            {
                'name': 'Leather Wallet',
                'slug': 'leather-wallet',
                'category': categories['accessories'],
                'description': 'Premium leather wallet with multiple card slots and coin pocket.',
                'price': 79.99,
                'stock': 35,
                'featured': False
            },
            {
                'name': 'Classic Oxford Shoes',
                'slug': 'classic-oxford-shoes',
                'category': categories['footwear'],
                'description': 'Timeless Oxford shoes perfect for formal occasions.',
                'price': 249.99,
                'stock': 15,
                'featured': True
            },
            {
                'name': 'Casual Sneakers',
                'slug': 'casual-sneakers',
                'category': categories['footwear'],
                'description': 'Comfortable casual sneakers for everyday wear.',
                'price': 119.99,
                'sale_price': 89.99,
                'stock': 45,
                'featured': False
            },
            {
                'name': 'Leather Boots',
                'slug': 'leather-boots',
                'category': categories['footwear'],
                'description': 'Durable leather boots perfect for outdoor activities.',
                'price': 189.99,
                'stock': 20,
                'featured': False
            },
            {
                'name': 'Polo Shirt',
                'slug': 'polo-shirt',
                'category': categories['clothing'],
                'description': 'Classic polo shirt made from breathable cotton.',
                'price': 69.99,
                'stock': 60,
                'featured': False
            },
            {
                'name': 'Dress Pants',
                'slug': 'dress-pants',
                'category': categories['clothing'],
                'description': 'Professional dress pants suitable for office wear.',
                'price': 149.99,
                'stock': 25,
                'featured': False
            },
            {
                'name': 'Sunglasses',
                'slug': 'sunglasses',
                'category': categories['accessories'],
                'description': 'Stylish sunglasses with UV protection.',
                'price': 159.99,
                'stock': 30,
                'featured': False
            }
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        # Create a superuser if none exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@sidewind.com',
                password='admin123'
            )
            self.stdout.write('Created superuser: admin (password: admin123)')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write('You can now log in to the admin panel with:')
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
