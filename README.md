# Side Wind - Men's Fashion Website

A comprehensive Django web application for a men's fashion e-commerce website called "Side Wind".

## Features

- **User Authentication**: Registration, login, and profile management
- **Product Categories**: Browse products by category (Clothing, Accessories, Footwear)
- **Product Listings**: Display products with search functionality
- **Shopping Cart**: Add, remove, and update product quantities
- **Checkout Process**: Secure payment processing with Stripe
- **Order Management**: Track orders and view order history
- **Admin Dashboard**: Manage products, categories, and orders
- **Responsive Design**: Mobile-friendly interface using Bootstrap

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Payment**: Stripe
- **Deployment**: Heroku/AWS ready

## Setup Instructions

### Prerequisites

1. Python 3.8 or higher
2. pip (Python package installer)
3. Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sidewind
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv sidewind_env
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     sidewind_env\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source sidewind_env/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
   STRIPE_SECRET_KEY=your-stripe-secret-key
   DATABASE_URL=your-database-url
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
sidewind/
├── manage.py
├── requirements.txt
├── README.md
├── .env (create this file)
├── sidewind/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── products/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── cart/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── orders/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
    ├── base.html
    ├── accounts/
    ├── products/
    ├── cart/
    └── orders/
```

## Deployment

### Heroku Deployment

1. **Install Heroku CLI**
2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
   heroku config:set STRIPE_SECRET_KEY=your-stripe-secret-key
   heroku config:set DEBUG=False
   ```

4. **Add PostgreSQL addon**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

6. **Run migrations**
   ```bash
   heroku run python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   heroku run python manage.py createsuperuser
   ```

### AWS Deployment

1. **Set up EC2 instance**
2. **Install dependencies**
3. **Configure nginx and gunicorn**
4. **Set up SSL certificate**
5. **Configure environment variables**

## API Documentation

### Authentication Endpoints
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `POST /accounts/logout/` - User logout
- `GET /accounts/profile/` - User profile

### Product Endpoints
- `GET /products/` - List all products
- `GET /products/<id>/` - Product detail
- `GET /products/category/<category>/` - Products by category
- `GET /products/search/` - Search products

### Cart Endpoints
- `GET /cart/` - View cart
- `POST /cart/add/<product_id>/` - Add to cart
- `POST /cart/update/<item_id>/` - Update cart item
- `POST /cart/remove/<item_id>/` - Remove from cart

### Order Endpoints
- `GET /orders/` - Order history
- `POST /orders/create/` - Create order
- `GET /orders/<order_id>/` - Order detail

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, email support@sidewind.com or create an issue in the repository.
