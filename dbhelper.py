import mysql.connector as connector
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

class DBHelper:
    def __init__(self):
        self.con = connector.connect(host=os.getenv('HOST'),      
                                     port=os.getenv('PORT'),           
                                     user=os.getenv('USER'),          
                                     password=os.getenv('PASSWORD'),       
                                     database=os.getenv('DB'))
        print("Connected to database")

    def runPostSQL(self, sql):
        try:
            self.con.cursor(buffered=True).execute(sql)

            self.con.commit()
        except Exception as e:
            print(e)
            print("Post query failed")
        # Rollback in case there is any error
            self.con.rollback()

    def runFetchSQL(self, sql):
        try:
            cur = self.con.cursor(buffered=True)
            cur.execute(sql)
            return cur
        except Exception as e:
            print(e)
            print("Fetch query failed")

    def generatePostQuery(self, table, data):
        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in data.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in data.values())
        sql_insert = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table, columns, values)
        return sql_insert

    def addCustomer(self, customer):
        sql = self.generatePostQuery('customers',customer)
        self.runPostSQL(sql)
        print(" -------------------------------------------------------- ")
        print("                Customer added successfully               ")
        print(" -------------------------------------------------------- ")

    def validateCustomer(self, cid):
        query = "select ID from customers"
        cur = self.con.cursor(buffered=True)
        cur.execute(query)
        self.con.commit()
        for row in cur:
            if cid in row: 
                return True
        return False
    
    def fetchProducts(self):
        query = "SELECT * FROM products"
        res = self.runFetchSQL(query)
        products = []
        for row in res:
            products.append(self.setProducts(row))
        return products
    
    def setProducts(self, product_row):
        keys = ['SupplierIDs', 
                'ID',
                'ProductCode',
                'ProductName',
                'Description',
                'StandardCost',
                'ListPrice',
                'ReorderLevel',
                'TargetLevel',
                'QuantityPerUnit',
                'Discontinued',
                'MinimumReorderQuantity',
                'Category',
                'Attachments']
        product = {}
        for i in range(len(keys)):
            product[keys[i]] = product_row[i]
        return product

    def setCustomer(self, customer_row):
        keys = [    'ID',
                    'Company',
                    'LastName',
                    'FirstName',
                    'Email',
                    'JobTitle',
                    'BusinessPhone',
                    'HomePhone',
                    'MobilePhone',
                    'Fax',
                    'Address',
                    'City',
                    'State',
                    'ZIP',
                    'Country',
                    'Web',
                    'Notes',
                    'Attachments']
        customer = {}
        for i in range(len(keys)):
            customer[keys[i]] = customer_row[i]
        return customer

    def setOrder(self, order_row):
        keys = [    'OrderID',
                    'EmployeeID',
                    'CustomerID',
                    'OrderDate',
                    'ShippedDate',
                    'ShipperID',
                    'ShipName',
                    'ShipAddress',
                    'ShipCity',
                    'ShipState',
                    'ShipZIP',
                    'ShipCountry',
                    'ShippingFee',
                    'Taxes',
                    'PaymentType',
                    'PaidDate',
                    'Notes',
                    'TaxRate',
                    'TaxStatus',
                    'StatusID']
        order = {}
        for i in range(len(keys)):
            order[keys[i]] = order_row[i]
        return order

    def addOrder(self):
        while True:
            cid = int(input("Enter CustomerID: "))
            if self.validateCustomer(cid):
                print('Choose product from the list:')
                products = self.fetchProducts()
                if self.renderProducts(products, cid):
                    print(" -------------------------------------------------------- ")
                    print("                Order added successfully               ")
                    print(" -------------------------------------------------------- ")
                break

    def renderProducts(self, products, cid):
        for product in products:
            print("ID: {}, Product Name: {}, Product Code: {}, Price: {}.".format(product['ID'],product['ProductName'],product['ProductCode'],product['ListPrice']))

        orders = []
        while True:
            order  = int(input('Enter product ID to purchase (0 to confirm/exit): '))
            if order == 0:
                break
            found = False
            for product in products:
                if product['ID'] == order:
                    product['Quantity'] = float(input('Enter the quantity for this product: '))
                    orders.append(product)
                    found = True
            if found is False:
                print('No such product found')
            else: 
                print('Your cart: ')
                for o in orders:
                    print("ID: {}, Product Name: {}, Product Code: {}, Price: {}, Quantity: {}.".format(o['ID'],o['ProductName'],o['ProductCode'],o['ListPrice'],o['Quantity']))
        
        if len(orders) != 0:
            
            order_payload = {
                'CustomerID' : str(cid),
            }
            orders_sql = self.generatePostQuery('orders',order_payload)
            self.runPostSQL(orders_sql)
            res = self.runFetchSQL('SELECT LAST_INSERT_ID()')
            for row in res: id = row[0]

            for order in orders:
                order_details_payload = {
                    'OrderID' : id,
                    'ProductID' : order['ID'],
                    'Quantity' : order['Quantity'],
                }
                order_details_sql = self.generatePostQuery('order_details',order_details_payload)
                self.runPostSQL(order_details_sql)
            return True    
        else:
            return False

    def fetchOrders(self):
        query = "SELECT * FROM orders"
        res = self.runFetchSQL(query)
        orders = []
        for row in res:
            orders.append(self.setOrder(row))
        return orders

    def fetchCustomer(self, cid):
        query = "SELECT * FROM customers WHERE ID = {}".format(cid)
        res = self.runFetchSQL(query)
        customers = []
        for row in res:
            customers.append(self.setCustomer(row))
        return customers

    def fetchPendingOrder(self):
        sql = 'SELECT * FROM orders  WHERE ShippedDate is NULL ORDER BY OrderDate'
        res = self.runFetchSQL(sql)
        orders = []
        for row in res:
            orders.append(self.setOrder(row))
        return orders

    def deleteOrder(self):
            orders = self.fetchOrders()
            order_ids = [] 
            if len(orders) != 0 :
                print('Available Orders: ')  
                for i in range(len(orders)):
                    print('Order {}'.format(i+1))
                    order_ids.append(orders[i]['OrderID'])
                    for keys in orders[i]:
                        print('{} - {}'.format(keys,orders[i][keys]))
                    print()
                    print('---------------------------------------------------------------------------')
                    print()
                print('Order Id Summary :',order_ids)
                orderId = int(input('Please select the order to be deleted (0 to confirm/exit0): '))
                if orderId not in order_ids:
                    print('No such order exist') 
                else: 
                    query1 = "DELETE FROM order_details WHERE OrderID= {}".format(orderId)
                    query2 = "DELETE FROM orders WHERE OrderID= {}".format(orderId)
                    self.runPostSQL(query1)
                    self.runPostSQL(query2)
                    print(" -------------------------------------------------------- ")
                    print("                Order : {} has been deleted               ".format(orderId))
                    print(" -------------------------------------------------------- ")
    
    def printPendingOrder(self):
        orders = self.fetchPendingOrder()
        for order in orders:
            cid = order['CustomerID']
            customers = self.fetchCustomer(cid)
            print('Order Details : ')
            for keys in order:
                print('{} - {}'.format(keys,order[keys]))
            print('Customer Details : ')
            for info in customers[0]:
                print('{} - {}'.format(info,customers[0][info]))
            print()
            print('---------------------------------------------------------------------------')
            print()

    def shipOrder(self):
        orderId = int(input('Enter the order the number: '))
        sql_order = 'SELECT Quantity,ProductID from order_details WHERE OrderID={}'.format(orderId)
        ord_res = self.runFetchSQL(sql_order)
        sql_inv = 'SELECT Quantity,ProductID from inventory_transactions WHERE CustomerOrderID={}'.format(orderId)
        inv_res = self.runFetchSQL(sql_inv)
        for order in ord_res:
            for inv in inv_res:
                if order[1] == inv[1]:
                    if order[0] > inv[0]:
                        print('Stocks not available. Order cannot be shipped')
        shippedDate = datetime.datetime.now()
        shipper_id = int(input('Enter shipper ID: '))
        shipping_fee = float(input('Enter shipping Fee: '))
        sql_update_order = "UPDATE orders SET ShippedDate = '{}', ShipperID = {}, ShippingFee = {} WHERE OrderId={}".format(shippedDate,shipper_id,shipping_fee,orderId)
        self.runPostSQL(sql_update_order)
        print(" -------------------------------------------------------- ")
        print("                Order : {} has been updated               ".format(orderId))
        print(" -------------------------------------------------------- ")