from flask import Flask
from pymongo import MongoClient
from ..bin.storage import storage
from os import environ as env
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

uri = f"mongodb://{env['DB_USERNAME']}:{env['DB_PASSWORD']}@{env['DB_HOST']}/?authSource=admin"
app.db = MongoClient(uri)["turdbot"]


@app.route("/")
def hello():
    db = storage(1004178748205187083,app.db).db
    count = db('counting', 'count')
    return f"Hello World! {count}"