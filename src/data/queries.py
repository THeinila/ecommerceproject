import psycopg2
from config import config

def connect():
    con = None

    try:
        con = psycopg2.connect(**config())
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if con is not None:
            con.close()
    
    return con

def order_count():
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """SELECT COUNT(id) FROM orders;"""

        try:
            cursor.execute(SQL, )
            con.commit()
            print(cursor.fetchall())

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()

def count_low_stock():
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """SELECT COUNT(id) FROM products WHERE stock_quantity < 10;"""

        try:
            cursor.execute(SQL, )
            con.commit()
            print(cursor.fetchall())

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()

def sales_per_category():
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """SELECT products.category, SUM(order_items.quantity*order_items.price_at_purchase) as total_price FROM products 
INNER JOIN order_items ON products.id = order_items.product_id
GROUP BY products.category;"""

        try:
            cursor.execute(SQL, )
            con.commit()
            print(cursor.fetchall())

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()

def average_order_value():
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """SELECT orders.id, AVG(price_at_purchase*quantity) as average_order FROM orders 
INNER JOIN order_items ON orders.id = order_items.order_id
GROUP BY orders.id
LIMIT 20;"""

        try:
            cursor.execute(SQL, )
            con.commit()
            print(cursor.fetchall())

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()

def top_customers():
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """SELECT customers.id, COUNT(price_at_purchase*quantity) as total_spent FROM customers 
                INNER JOIN orders ON customers.id = orders.customer_id
                    INNER JOIN order_items ON orders.id = order_items.order_id
GROUP BY customers.id
ORDER BY total_spent DESC
LIMIT 5;    """

        try:
            cursor.execute(SQL, )
            con.commit()
            print(cursor.fetchall())

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()

            
def total_sales():
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """SELECT SUM(price_at_purchase * quantity) AS total_price FROM order_items;"""

        try:
            cursor.execute(SQL, )
            con.commit()
            print(cursor.fetchall())

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close()

def monthly_breakdown_orders_total_sales():
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """SELECT DATE_TRUNC('month', orders.order_date) AS order_month, COUNT(orders.order_id) AS total_orders, SUM(order_items.quantity * order_items.price_at_purchase) AS total_sales
        FROM orders
        JOIN order_items ON orders.order_id = order_items.order_id
        GROUP BY order_month
        ORDER BY order_month;"""

        try:
            cursor.execute(SQL, )
            con.commit()
            print(cursor.fetchall())

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close() 


def order_list():
    con = connect()
    if con is not None:
        cursor = con.cursor()
        
        SQL = """SELECT customers.name, SUM(order_items.quantity * order_items.price_at_purchase) AS total_order_value
        FROM customers
        JOIN orders ON customers.customer_id = orders.customer_id
        JOIN order_items ON orders.order_ide = order_items.order_id
        GROUP BY customers.customer_id, customers.name
        ;"""

        try:
            cursor.execute(SQL, )
            con.commit()
            print(cursor.fetchall())

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
            con.close() 

def main():
    #4.1
    #order_count()
    #total_sales()
    #count_low_stock()
    #4.2
    #sales_per_category()
    average_order_value()
    #monthly_breakdown_orders_total_sales()
    #4.3
    #order_list()
    #top_customers()

main()
