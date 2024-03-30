from flask import url_for
from app.models import Product


# def test_create_product_success(client, db):
#     product_data = {
#         'name': 'Test Product',
#         'price': 10.99,
#         'description': 'Test description',
#         'quantity': 5
#     }

#     response = client.post('/api/create_product', data=product_data, follow_redirects=True)
#     assert response.status_code == 404
#     product = Product.query.filter_by(name='Test Product').first()
#     assert product.name == 'Test Product'
#     assert product.price == 10.99
#     assert product.description == 'Test description'
#     assert product.quantity == 5


def test_create_product_invalid_form(client, db):
    response = client.post('/api/create_product', data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Product added successfully!' not in response.data
    assert b'Invalid form data' in response.data










    # # Ensure that the product is added to the database
    # with client.application.app_context():
    #     # Retrieve the product from the database
    #     product = Product.query.filter_by(name='Test Product').first()

    #     # # Check if the product is not None
    #     # assert product is not None, "Product not found in the database"

    #     # Check specific attributes of the product
    #     assert product.name == 'Test Product', "Incorrect product name"
    #     assert product.price == 10.99, "Incorrect product price"
    #     assert product.description == 'Test description', "Incorrect product description"
    #     assert product.quantity == 5, "Incorrect product quantity"


# def test_products_list(client, db):
#     with client.application.test_request_context():
#         product1 = Product(name='Product 1', price=10.99, description='Description 1', quantity=5)
#         product2 = Product(name='Product 2', price=20.99, description='Description 2', quantity=10)
#         db.session.add(product1)
#         db.session.add(product2)
#         db.session.commit()

#     # Retrieve the products from the database and check their presence in the response
#     response = client.get('/products')
#     assert response.status_code == 200
#     assert b'Product 1' in response.data
#     assert b'Product 2' in response.data


# def test_update_product(client, db):
#     with client.application.test_request_context():
#         product = Product(name='Test Product', price=10.99, description='Test description', quantity=5)
#         db.session.add(product)
#         db.session.commit()

#     # Send a POST request to update the product
#     response = client.post(f'/update_product/{product.id}', data={
#         'name': 'Updated Product',
#         'price': 20.99,
#         'description': 'Updated description',
#         'quantity': 10
#     }, follow_redirects=True)

#     # Check if the product is updated successfully
#     assert response.status_code == 200
#     assert b'Updated Product' in response.data
#     assert b'Updated description' in response.data
#     assert b'20.99' in response.data
#     assert b'10' in response.data
