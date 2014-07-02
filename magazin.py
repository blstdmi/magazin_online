import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'ceva secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/student/osss-web/db.sqlite'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

@app.route('/')
def home():
    return flask.render_template('home.html', product_list=Product.query.all())

@app.route('/save', methods=['POST'])
def save():
    print "saving...", flask.request.form['name']
    product = Product(name=flask.request.form['name'])
    db.session.add(product)
    db.session.commit()
    flask.flash("product saved")
    
    return flask.redirect('/')

@app.route('/edit/<int:product_id>', methods=['POST','GET'])
def edit(product_id):
    product = Product.query.get(product_id)
    if not product:
        flask.abort(404)
    if flask.request.method == 'POST':
        product.name = flask.request.form['name']
        db.session.commit()
        return flask.redirect('/edit/%d' % product.id)

    return flask.render_template('edit.html', product=product)

@app.route('/delete/<int:product_id>', methods=['DELETE'])
def delete(product_id):
    print "deleting...", flask.request.form['name']
    product = Product(name=flask.request.form['name'])
    db.session.delete(product)
    db.session.commit()
    flask.flash("product deleted")
    
    return flask.redirect('/')
    
@app.route('/api/list')
def api_list():
    product_id_list = []
    for product in Product.query.all():
        product_id_list.append(product.id)
    return flask.jsonify({
        'id_list': product_id_list,
    })

@app.route('/api/product/<int:product_id>')
def api_product(product_id):
    product = Product.query.get(product_id)
    name = product.name
    return flask.jsonify({
        'name': name,
        'id': product_id,
    })
@app.route('/api/product/create', methods = ['POST'])
def api_product_create():
    js = flask.request.get_json()
    prod = Product(name=js['name'])
    db.session.add(prod)
    db.session.commit()

    return flask.jsonify({'status' : 'ok', 'id' : prod.id })

@app.route('/api/product/<int:product_id>/update', methods = ['POST'])
def api_product_update(product_id):
    prod = Product.query.get(product_id)
    js = flask.request.get_json()
    prod.name = js['name']
    db.session.commit()
    return flask.jsonify({'status':'ok'})
    
    

db.create_all()
app.run(debug = True)

