import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from settings import *
from bild import create_tables
from bild import Publisher, Book, Shop, Stock, Sale



def find_publisher_name(Session, name=None):
    with Session() as session:
        query = session.query(Sale).join(Stock).join(Shop).join(Book).join(Publisher)\
            .filter(Publisher.name.ilike(f'%{name}%'))
        return query

def insert_data_from_json(Session):
    with Session() as session:
        with open("data.json", "r", encoding="utf-8") as data:
            data = json.load(data)

        tables = {'publisher': Publisher, 'book': Book, 'shop': Shop, 'stock': Stock, 'sale': Sale}

        for kwargs in data:
            query = tables[kwargs['model']](id=kwargs['pk'], **kwargs['fields'])
            session.add(query)
        session.commit()

def main():
    insert_data_from_json(Session)
    while True:
        name = input('Select a publisher: ')
        if name == 'exit':
            print('Script off')
            break

        for sale in find_publisher_name(Session, name):
            print(f'{sale.stock.book.title}| {sale.stock.shop.name} | {sale.price} | {sale.date_sale}')

        print('Turn off script - "exit"')
if __name__ == '__main__':
    # login = input('login - ')
    # password = input('password - ')
    # connection_name = input('connection_name - ')
    # port = input('port - ')
    # db_name = input('db_name - ')

    DSN = f"postgresql://{login}:{password}@{connection_name}:{port}/{db_name}"
    engine = sqlalchemy.create_engine(DSN)
    Session = sessionmaker(bind=engine)

    try:
        create_tables(engine)
    except:
        print('Failed to connect, invalid logins or something...')

    main()



