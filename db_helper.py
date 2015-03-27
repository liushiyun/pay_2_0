# -*- coding: utf-8 -*-

import sqlite3

class DbAgent(object):
    '''
    和数据库有关的操作代理给此类
    '''
    def __init__(self):
        self.cx = sqlite3.connect("./test.db")

    def create_purchase_order(self):
        cu = self.cx.cursor()
        cu.execute("create table purchase_order (id integer primary key, purchase_id integer, status integer, lock integer,product_name string, breed_name string)")
        cu.close()

    def create_payment_info(self):
        cu = self.cx.cursor()
        cu.execute("create table payment_info (id integer primary key,payment_id, order_id integer, deal_money integer, unit string)")
        cu.close()

    def insert_into_purchase_order(self):
        cu = self.cx.cursor()
        cu.execute("insert into purchase_order values(1, 627, 400, 0, '土豆','王大妈')")
        self.cx.commit()
        cu.close()

    def insert_into_payment_order(self):
        cu = self.cx.cursor()
        cu.execute("insert into payment_info values(1, 627, 627, 250,'土豆网')")
        self.cx.commit()
        cu.close()

    def get_pay_info_by_id(self, order_id):
        sql = """
        select * from payment_info where order_id = {0};
        """
        cu = self.cx.cursor()
        cu.execute(sql.format(int(order_id)))
        results = cu.fetchall()
        cu.close()
        return results[0]

    def order_lock(self, order_id):
        sql = """
        update purchase_order set lock = 1 where order_id = {0};
        """
        cu = self.cx.cursor()
        result = cu.execute(sql.format(int(order_id)))
        cu.commit()
        cu.close()
        return result

    # FIXME
    # 这个代码提供的接口好么？如何保证一定能够获取到数据呢？
    # 这里的代码是否需要判断是否为零？
    # if results == []: return []
    # else return results[0]
    def get_product_info_by_order_id(self, order_id):
        sql = """
        select product_name ,breed_name from purchase_order where purchase_id= {0} ;
        """
        cu = self.cx.cursor()
        cu.execute(sql.format(int(order_id)))
        results = cu.fetchall()
        cu.close()
        return results[0]

if __name__ == '__main__':
    db = DbAgent()
    
    # db.create_purchase_order()
    # db.create_payment_info()

    # db.insert_into_purchase_order()
    # db.insert_into_payment_order()

    res = db.get_pay_info_by_id(627)
    print res
