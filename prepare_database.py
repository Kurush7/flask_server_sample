import pandas as pd
import numpy as np
import qrookDB.DB as db

tables =\
'''
create table if not exists manufacturers
(
    id   integer generated always as identity
        constraint manufacturers_pkey primary key,
    name varchar(256) not null
);


create table if not exists products
(
    id              integer generated always as identity
        constraint products_pkey primary key,
    uuid            varchar(256) unique,
    manufacturer_id integer
        constraint products_fkey references manufacturers not null,
    name            varchar(256)                          not null,
    price           float,
    rating          float,
    count           integer,
    description     varchar
);
'''

DB = db.DB('postgres', 'amazon', 'user', 'password', format_type='dict')


# датасет: https://www.kaggle.com/datasets/nguyenngocphung/10000-amazon-products-dataset
def load_data(filename='Amazon_Products.csv'):
    df = pd.read_csv(filename)
    df = df.dropna()
    df = df[df['price'].str.startswith('£')]
    df['price'] = df['price'].str.replace('£', '').str.replace(',', '').astype(np.float16)

    df['number_available_in_stock'] = df['number_available_in_stock'].str.replace(u"\xa0", " ")
    df['number_available_in_stock'] = np.array([x[:x.find(' ')] for
                                                x in df['number_available_in_stock']]).astype(np.uint16)

    df['average_review_rating'] = df['average_review_rating'].str.slice(0, 3).astype(np.float16)

    products = df[['uniq_id', 'manufacturer', 'product_name', 'price',
                   'number_available_in_stock', 'average_review_rating', 'description']]
    manufacturers = df['manufacturer'].unique()
    manufacturer_ids = list(range(1, len(manufacturers) + 1))
    mapping = {m: i for m, i in zip(manufacturers, manufacturer_ids)}
    products['manufacturer'] = [mapping[m] for m in products['manufacturer']]

    products = products.rename(columns={'uniq_id': 'uuid', 'product_name': 'name',
                                        'number_available_in_stock': 'count', 'average_review_rating': 'rating',
                                        'manufacturer': 'manufacturer_id'})
    return products.to_dict('records'), [{'name': m} for m in manufacturers]


def insert_data(products, manufacturers):
    DB.create_data(__name__, in_module=True)
    m = DB.manufacturers
    data = [list(d.values()) for d in manufacturers]
    ok = DB.insert(m, m.name,
                   auto_commit=True) \
        .values(data).exec()
    print('manufacturers created:', ok)

    p = DB.products
    data = [list(d.values()) for d in products]
    ok = DB.insert(p, p.uuid, p.manufacturer_id, p.name, p.price, p.rating, p.count, p.description,
                   auto_commit=True) \
        .values(data).exec()
    print('products created:', ok)

def create_tables():
    ok = DB.exec(tables).exec()
    DB.commit()
    print('tables created:', ok)

def main():
    create_tables()
    products, manufacturers = load_data()
    insert_data(products, manufacturers)


if __name__ == '__main__':
    main()