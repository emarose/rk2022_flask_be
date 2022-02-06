from base64 import decode
from flask import Flask, redirect, Response, json, url_for, render_template, request, session, flash, make_response, jsonify
from datetime import timedelta, datetime, date
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
import jsonpickle
from flask_cors import CORS, cross_origin
from flask_mongoalchemy import MongoAlchemy
import time


app = Flask(__name__)

CORS(app)
app.config['MONGOALCHEMY_DATABASE'] = 'RK2022DB'
db = MongoAlchemy(app)
app.secret_key = "SecretKey"


class Products(db.Document):
    code = db.StringField()  # Input / automatico
    product_name = db.StringField()  # Input
    description = db.StringField()  # Input
    cost = db.StringField()  # Input
    price = db.StringField()  # Input
    notes = db.StringField()  # Input
    #image = db.Column(db.String) #
    def __repr__(self):
        return '<__main__.Products: '+self.code +' '+ self.product_name+' ' + self.description+' '+self.cost +' '+ self.price+' ' + self.notes


""" app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///RK2022database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
helper_table = db.Table('helper_table',
                        db.Column("id", db.Integer, primary_key=True),
                        db.Column('order_id', db.Integer,
                                  db.ForeignKey('Orders.id')),
                        db.Column('customer_id', db.Integer,
                                  db.ForeignKey('Customers.id')),
                        db.Column('product_id', db.Integer, db.ForeignKey('Products.id')))
# Tabla Ventas
class Orders(db.Model):
    __tablename__ = 'Orders'

    id = db.Column("id", db.Integer, primary_key=True)
    order_date = db.Column(db.Date)  # DatePicker
    # Enviado / Pago Pendiente / Pagada / Recibido
    order_state = db.Column(db.String(30))
    # Personal / Instagram / Tienda Virtual / Facebook / Otro (Input)
    sale_mode = db.Column(db.String(30))
    # Efectivo / Transferencia / MercadoPago / Otro (Input)
    pay_method = db.Column(db.String(30))
    discount = db.Column(db.Integer)  # [0] Input
    # Retiro / Envio local / Envio por correo
    shipping_method = db.Column(db.String(30))
    shipping_destination = db.Column(db.String(30))  # Input
    shipping_tracking = db.Column(db.String(30))  # [Pendiente] / Input
    shipping_cost = db.Column(db.Float)  # Input
    shipping_date = db.Column(db.Date)  # DatePicker

    customer = db.relationship("Customers",
                               secondary=helper_table,
                               backref="Orders",
                               lazy='joined',
                               uselist=False)
    product = db.relationship("Products",
                              secondary=helper_table,
                              lazy='joined',
                              uselist=False,
                              backref="Orders")

    def __init__(self,
                 order_date,
                 order_state,
                 sale_mode,
                 pay_method,
                 discount,
                 shipping_method,
                 shipping_destination,
                 shipping_tracking):
        self.order_date = order_date
        self.order_state = order_state
        self.sale_mode = sale_mode
        self.pay_method = pay_method
        self.discount = discount
        self.shipping_method = shipping_method
        self.shipping_destination = shipping_destination
        self.shipping_tracking = shipping_tracking
# Tabla Clientes
class Customers(db.Model):
    __tablename__ = 'Customers'

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(30))  # Input
    address = db.Column(db.String(30))  # Input
    email = db.Column(db.String(30))  # Input
    phone = db.Column(db.Integer)  # Input
    notes = db.Column(db.String)  # Input

    def __init__(self, name, address, email, phone, notes):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.notes = notes

    def dump(self):
            return {"Customers":
                        {
                            'name': self.name,
                            'address': self.address,
                            'email': self.email,
                            'phone': self.phone,
                            'notes': self.notes,
                        }}
# Tabla Productos
class Products(db.Model):
    __tablename__ = 'Products'

    id = db.Column("id", db.Integer, primary_key=True)
    code = db.Column(db.Integer)  # Input / automatico
    product_name = db.Column(db.String(30))  # Input
    description = db.Column(db.String)  # Input
    cost = db.Column(db.Float)  # Input
    price = db.Column(db.Float)  # Input
    notes = db.Column(db.String)  # Input
    #image = db.Column(db.String) #

    def __init__(self, code, product_name, description, cost, price, notes):
        self.code = code
        self.product_name = product_name
        self.description = description
        self.cost = cost
        self.price = price
        self.notes = notes

    def dump(self):
            return {"Products":
                        {
                            'code': self.code,
                            'product_name': self.product_name,
                            'description': self.description,
                            'cost': self.cost,
                            'price': self.price,
                            'notes': self.notes,
                        }}
 """


@app.route("/", methods=['POST'])
def Home():
    return "Hello World!"


@app.route('/products', methods=['POST', 'GET'])
def products():
    documents = Products.query.all()
    list = []
    for x in documents:
        list.append({"code": x.code,"product_name": x.product_name, "description": x.description,"cost": x.cost,"price": x.price, "notes": x.notes})
        
    return jsonify(list)


@app.route('/products/add', methods=['POST', 'GET'])
def add():
    code = None
    product_name = None
    description = None
    cost = None
    price = None
    notes = None

    if request.method == 'POST':
        req = request.get_json()

        code = (req['data']['code'])
        product_name = (req['data']['product_name'])
        description = (req['data']['description'])
        cost = (req['data']['cost'])
        price = (req['data']['price'])
        notes = (req['data']['notes'])

        data = Products(code=code, product_name=product_name, description=description,
                 cost=cost, price=price,notes=notes)

        data.save()

        return jsonify({
            'status': 'OK',
                'message': 'Successfully Added'
            })


@app.route("/deleteproduct/<string:code>", methods=["DELETE","POST"])
def deleteproduct(code):
    query = Products.query.filter(Products.code == code).first()
    query.remove()

    return jsonify({
        'status': 'OK',
            'message': 'Successfully Deleted'
        })


@app.route("/editproduct/<int:code>", methods=["POST"])
def editproduct(code):
    product = Products.query.filter(Products.code == code).first()

    print(product)
    if request.method == 'POST':

        # product_to_edit = Products.query.filter(Products.code == code).first()
        # print(product_to_edit)

        # db.session.commit()

        return jsonify(message="POST request returned")


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)
