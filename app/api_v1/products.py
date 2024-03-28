# from flask import render_template
# from . import api
# from ..auth import login_required
# from app.forms.products import ProductForm


# @api.route("/products", methods=["GET"])
# @login_required
# def get_products():
#     return render_template("products.html")



# @api.route('/products', methods=['GET', 'POST'])
# def create_product():
#     form = ProductForm()
#     if form.validate_on_submit():
#         product = Product(name=form.name.data, price=form.price.data)
#         db.session.add(product)
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template('create_product.html', title='Create Product', form=form)





# @api.route("/")
# def get_user():
#     return "Hello World!"


# @api.route('/product/<int:product_id>', methods=['GET'])
# def get_product(product_id):
#     product = Product.query.get_or_404(product_id)
#     return render_template('product.html', product=product)



# @api.route('/product/<int:product_id>', methods=['PUT'])
# def update_product(product_id):
#     product = Product.query.get_or_404(product_id)
#     form = ProductForm()
#     if form.validate_on_submit():
#         product.name = form.name.data
#         product.price = form.price.data
#         db.session.commit()
#         return render_template('update_product.html', form=form)
#     return jsonify({'error': 'Invalid form data'})


# @api.route('/product/<int:product_id>', methods=['DELETE'])
# def delete_product(product_id):
#     product = Product.query.get_or_404(product_id)
#     db.session.delete(product)
#     db.session.commit()
#     return render_template('delete_product.html', product=product)