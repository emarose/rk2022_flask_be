from flask import Flask, redirect, url_for, render_template, request, session, flash, make_response, jsonify
from datetime import timedelta, datetime, date
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

import time

app = Flask(__name__)
CORS(app)

app.secret_key = "SecretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///RK2022database.sqlite3'
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


@app.route("/", methods=['POST'])
def Home():
    return "Hello World!"

@app.route('/products', methods=['POST', 'GET'])

def products():
    code = None
    product_name = None
    description = None
    cost = None
    price = None
    notes = None
    
    query_all_products = Products.query.all()

    if request.method == 'POST':
        code = request.json["code"]
        product_name = request.json["productName"]
        description = request.json["description"]
        cost = request.json["cost"]
        price = request.json["price"]  
        notes = request.json["notes"]

        data = [{"code": code, "product_name": product_name, "description": description,
                 "cost": cost, "price": price, "notes": notes}]
        
        db.session.bulk_insert_mappings(Products, data)
        db.session.commit()
        
        return jsonify({
                'status': 'OK',
                'message': 'Successfully Added'
                })
    else:
        return redirect(url_for('products'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
