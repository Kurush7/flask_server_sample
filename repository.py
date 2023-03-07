from typing import Dict

import qrookDB.DB as db

DB = db.DB('postgres', 'amazon', 'user', 'password', format_type='dict')
DB.create_logger()

class Repository:
    def __init__(self):
        DB.create_data(__name__, in_module=True)

    def get_products(self):
        if DB.meta['tables'].get('products') is None:
            return None

        data = DB.products.select().all()
        return data

    def get_product(self, uuid):
        if DB.meta['tables'].get('products') is None:
            return None

        data = DB.products.select().where(uuid=uuid).one()
        self._extend_with_manufacturer(data)
        return data


    def create_product(self, data: Dict):
        if DB.meta['tables'].get('products') is None:
            return None

        columns = [DB.products.__dict__[k] for k in data.keys()]
        ok = DB.products.insert(*columns, auto_commit=True).values(data.values()).exec()
        return ok

    def create_manufacturer(self, data: Dict):
        if DB.meta['tables'].get('manufacturers') is None:
            return None

        columns = [DB.manufacturers.__dict__[k] for k in data.keys()]
        ok = DB.manufacturers.insert(*columns, auto_commit=True).values(data.values()).exec()
        return ok


    def _extend_with_manufacturer(self, product):
        m = DB.manufacturers
        man = m.select(m.name).where(id=product['manufacturer_id']).one()
        product['manufacturer'] = man
        product.pop('manufacturer_id')
