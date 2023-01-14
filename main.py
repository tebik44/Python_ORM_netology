import sqlalchemy
import psycopg2
from sqlalchemy.orm import sessionmaker
from pprint import pprint
import json

from bild import create_tables
from bild import Publisher, Book, Shop, Stock, Sale

login = 'postgres'
password = 'Wew019283746556'
connection_name = 'localhost'
port = '5432'
db_name = 'python_ORM'
DSN = f'postgresql://{login}:{password}@{connection_name}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open("data.json", "r", encoding="utf-8") as data:
    data = json.load(data)
    for item in data:
        if "publisher" in item.values():
            print(item['fields']['name'])
            pub = Publisher(name=item['fields']['name'])
            session.add(pub)
        elif "book" in item.values():
            print(item['fields']['title'])
            book = Book(title=item['fields']['title'],\
                        id_publisher=item['fields']['id_publisher'])
            session.add(book)
        elif "shop" in item.values():
            print(item['fields']['name'])
            shop = Shop(name=item['fields']['name'])
            session.add(shop)
        elif "stock" in item.values():
            print(item['fields']['count'])
            stock = Stock(id_book=item['fields']['id_book'],\
                          id_shop=item['fields']['id_shop'],\
                          count=item['fields']['count'])
            session.add(stock)
        elif "sale" in item.values():
            print(item['fields']['price'])
            sale = Sale(price=item['fields']['price'], \
                        data_sale=item['fields']['date_sale'], \
                        id_stock=item['fields']['id_stock'],\
                        count=item['fields']['count'])
            session.add(sale)

    session.commit()



session.close()