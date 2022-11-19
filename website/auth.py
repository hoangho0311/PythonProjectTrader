from flask import Blueprint, render_template, request, flash, redirect, url_for
from .database import mydb
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pass1 = request.form.get('pass')

        mycursor = mydb.cursor()
        query =("SELECT name,pass FROM user WHERE name = %s AND pass = %s")
        mycursor.execute(query, (email, pass1))

        myresult = mycursor.fetchall()
        if(len(myresult)>0):
            flash('login success', category="success")
            return redirect(url_for('views.home'))
        else:
            flash('login fail', category="error")

    return render_template("login.html")

@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        pass1 = request.form.get('pass1')
        pass2 = request.form.get('pass2')

        if len(email)<4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstname)<2:
            flash('firstName must be greater than 4 characters.', category='error')
        elif pass1!=pass2:
            flash('passwords dont match.', category='error')
        elif len(pass1) < 8:
            flash('pass1 must be at least 8 characters.', category='error')
        else:
            mycursor = mydb.cursor()
            sql = "INSERT INTO user (name, pass) VALUES (%s, %s)"
            val = (email, pass1)
            mycursor.execute(sql, val)

            mydb.commit()
            flash('accout create', category="success")

    return render_template("signup.html")


# Customer Manager Page
@auth.route('/customermanager')
def customermanager():
    mycursor = mydb.cursor()
    mycursor.execute("select * from customers")
    data=mycursor.fetchall()
    return render_template("manager/customer.html", data=data)

@auth.route('/customermanager/addCustomer')
def addCustomerOpen():
    return render_template("manager/addCustomer.html")

@auth.route('/customermanager/addCustomer', methods=['GET','POST'])
def addCustomer():
    if request.method == 'POST':
        Customerid = request.form.get('customerid')
        CompanyName = request.form.get('CompanyName')
        ContactName = request.form.get('ContactName')
        Address = request.form.get('Address')
        City = request.form.get('City')
        Country = request.form.get('Country')
        Phone = request.form.get('Phone')

        
        mycursor = mydb.cursor()
        sql = "INSERT INTO customers (Customerid, CompanyName, ContactName, Address, City, Country, Phone) VALUES (%s, %s,%s, %s,%s, %s,%s)"
        val = (Customerid,  CompanyName, ContactName, Address, City, Country, Phone)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Insert success', category="success")

    return redirect(url_for('auth.customermanager'))


@auth.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        ContactName = request.form['ContactName']
        Address = request.form['Address']
        phone = request.form['phone']
        mycursor = mydb.cursor()
        sql = " UPDATE customers SET ContactName=%s, Address=%s, Phone=%s WHERE CustomerID=%s"
        val = (ContactName, Address, phone, id_data)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Update success', category="success")

    return redirect(url_for('auth.customermanager'))


@auth.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM customers WHERE CustomerID=%s", (id_data,))

    mydb.commit()
    flash("Deleted Success", category="success")

    return redirect(url_for('auth.customermanager'))


# Shipper Manager Page
@auth.route('/shippermanager')
def shippermanager():
    mycursor = mydb.cursor()
    mycursor.execute("select * from shippers")
    data=mycursor.fetchall()
    return render_template("manager/shipper.html", data=data)

@auth.route('/shippermanager/addShipper')
def addshipperOpen():
    return render_template("manager/addShipper.html")

@auth.route('/shippermanager/addShipper', methods=['GET','POST'])
def addshipper():   
    if request.method == 'POST':
        ShipperID = request.form.get('ShipperID')
        CompanyName = request.form.get('CompanyName')
        Phone = request.form.get('Phone')
        
        mycursor = mydb.cursor()
        sql = "INSERT INTO shippers (ShipperID, CompanyName, Phone) VALUES (%s, %s,%s)"
        val = (ShipperID,  CompanyName, Phone)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Insert success', category="success")

        return redirect(url_for('auth.shippermanager'))


@auth.route('/updateshipper',methods=['POST','GET'])
def updateshipper():
    if request.method == 'POST':
        id_data = request.form['id']
        CompanyName = request.form['CompanyName']
        Phone = request.form['Phone']
        mycursor = mydb.cursor()
        sql = " UPDATE shippers SET CompanyName=%s, Phone=%s WHERE ShipperID=%s"
        val = (CompanyName, Phone, id_data)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Update success', category="success")

    return redirect(url_for('auth.shippermanager'))


@auth.route('/deleteshipper/<string:id_data>', methods = ['GET'])
def deleteshipper(id_data):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM shippers WHERE ShipperID=%s", (id_data,))

    mydb.commit()
    flash("Deleted Success", category="success")

    return redirect(url_for('auth.shippermanager'))


# Employees Manager Page
@auth.route('/employeemanager')
def employeemanager():
    mycursor = mydb.cursor()
    mycursor.execute("select * from employees")
    data=mycursor.fetchall()
    return render_template("manager/employee.html", data=data)

@auth.route('/employeemanager/addEmployee')
def addEmployeeOpen():
    return render_template("manager/addEmployee.html")

@auth.route('/employeemanager/addEmployee', methods=['GET','POST'])
def addEmployee():   
    if request.method == 'POST':
        LastName = request.form.get('LastName')
        FirstName = request.form.get('FirstName')
        BirthDate = request.form.get('BirthDate')
        HireDate = request.form.get('HireDate')
        Address = request.form.get('Address')
        City = request.form.get('City')
        Region = request.form.get('Region')
        PostalCode = request.form.get('PostalCode')
        Country = request.form.get('Country')
        HomePhone = request.form.get('HomePhone')
        Notes = request.form.get('Notes')
        
        mycursor = mydb.cursor()
        sql = "INSERT INTO employees (LastName, FirstName, BirthDate, HireDate, Address, City, Region, PostalCode, Country, HomePhone, Notes) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s)"
        val = (LastName, FirstName, BirthDate, HireDate, Address, City, Region, PostalCode, Country, HomePhone, Notes)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Insert success', category="success")

        return redirect(url_for('auth.employeemanager'))


@auth.route('/updateEmployee',methods=['POST','GET'])
def updateEmployee():
    if request.method == 'POST':
        id_data = request.form['id']
        LastName = request.form['LastName']
        FirstName = request.form['FirstName']
        BirthDate = request.form['BirthDate']
        HireDate = request.form['HireDate']
        Address = request.form['Address']
        City = request.form['City']
        Region = request.form['Region']
        PostalCode = request.form['PostalCode']
        Country = request.form['Country']
        HomePhone = request.form['HomePhone']
        Notes = request.form['Notes']

        mycursor = mydb.cursor()
        sql = " UPDATE employees SET LastName=%s,FirstName=%s, BirthDate=%s, HireDate=%s, Address=%s, City=%s, Region=%s, PostalCode=%s, Country=%s, HomePhone=%s, Notes=%s WHERE EmployeeID=%s"
        val = (LastName, FirstName, BirthDate, HireDate, Address, City, Region, PostalCode, Country, HomePhone, Notes, id_data)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Update success', category="success")

    return redirect(url_for('auth.employeemanager'))


@auth.route('/deleteEmployee/<string:id_data>', methods = ['GET'])
def deleteEmployee(id_data):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM employees WHERE EmployeeID=%s", (id_data,))

    mydb.commit()
    flash("Deleted Success", category="success")

    return redirect(url_for('auth.employeemanager'))


# Categories Manager Page
@auth.route('/categoriesmanager')
def categoriesmanager():
    mycursor = mydb.cursor()
    mycursor.execute("select * from categories")
    data=mycursor.fetchall()
    return render_template("manager/categories/categories.html", data=data)

@auth.route('/categoriesmanager/addCategories')
def addCategoriesOpen():
    return render_template("manager/categories/addCategories.html")

@auth.route('/categoriesmanager/addCategories', methods=['GET','POST'])
def addCategories():   
    if request.method == 'POST':
        CategoryName = request.form.get('CategoryName')
        Description = request.form.get('Description')
        
        
        mycursor = mydb.cursor()
        sql = "INSERT INTO categories (CategoryName, Description) VALUES (%s, %s)"
        val = (CategoryName, Description)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Insert success', category="success")

        return redirect(url_for('auth.categoriesmanager'))


@auth.route('/updatecategories',methods=['POST','GET'])
def updatecategories():
    if request.method == 'POST':
        id_data = request.form['id']
        CategoryName = request.form['CategoryName']
        Description = request.form['Description']
        

        mycursor = mydb.cursor()
        sql = " UPDATE categories SET Description=%s, Description=%s WHERE categoryID=%s"
        val = (CategoryName, Description, id_data)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Update success', category="success")

    return redirect(url_for('auth.categoriesmanager'))


@auth.route('/deletecategories/<string:id_data>', methods = ['GET'])
def deletecategories(id_data):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM categories WHERE categoryID=%s", (id_data,))

    mydb.commit()
    flash("Deleted Success", category="success")

    return redirect(url_for('auth.categoriesmanager'))



# Supplier Manager Page
@auth.route('/suppliermanager')
def suppliermanager():
    mycursor = mydb.cursor()
    mycursor.execute("select * from suppliers")
    data=mycursor.fetchall()
    return render_template("manager/supplier/supplier.html", data=data)

@auth.route('/suppliermanager/addSupplier')
def addSupplierOpen():
    return render_template("manager/supplier/addSupplier.html")

@auth.route('/suppliermanager/addSupplier', methods=['GET','POST'])
def addSupplier():   
    if request.method == 'POST':
        CompanyName = request.form.get('CompanyName')
        ContactName = request.form.get('ContactName')
        ContactTitle = request.form.get('ContactTitle')
        Address = request.form.get('Address')
        City = request.form.get('City')
        Region = request.form.get('Region')
        PostalCode = request.form.get('PostalCode')
        Country = request.form.get('Country')
        Phone = request.form.get('Phone')
        Fax = request.form.get('Fax')       
        
        mycursor = mydb.cursor()
        sql = "INSERT INTO suppliers (CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Insert success', category="success")

        return redirect(url_for('auth.suppliermanager'))


@auth.route('/updateSupplier',methods=['POST','GET'])
def updateSuppliers():
    if request.method == 'POST':
        id_data = request.form['id']
        CompanyName = request.form['CompanyName']
        ContactName = request.form['ContactName']
        ContactTitle = request.form['ContactTitle']
        Address = request.form['Address']
        City = request.form['City']
        Region = request.form['Region']
        PostalCode = request.form['PostalCode']
        Country = request.form['Country']
        Phone = request.form['Phone']
        Fax = request.form['Fax']

        mycursor = mydb.cursor()
        sql = " UPDATE suppliers SET CompanyName=%s, ContactName=%s, ContactTitle=%s, Address=%s, City=%s, Region=%s, PostalCode=%s, Country=%s, Phone=%s, Fax=%s WHERE SupplierID=%s"
        val = (CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax, id_data)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Update success', category="success")

    return redirect(url_for('auth.suppliermanager'))


@auth.route('/deleteSupplier/<string:id_data>', methods = ['GET'])
def deleteSuppliers(id_data):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM Suppliers WHERE SupplierID=%s", (id_data,))

    mydb.commit()
    flash("Deleted Success", category="success")

    return redirect(url_for('auth.suppliermanager'))



# Supplier Manager Page
@auth.route('/productmanager')
def productmanager():
    mycursor = mydb.cursor()
    mycursor.execute("select * from products")
    data=mycursor.fetchall()

    suppliers = mydb.cursor()
    suppliers.execute("select * from suppliers")
    suppliersdata=suppliers.fetchall()

    categories = mydb.cursor()
    categories.execute("select * from categories")
    categoriesdata=categories.fetchall()

    return render_template("manager/product/product.html", data=data, suppliersdata=suppliersdata, categoriesdata= categoriesdata)

@auth.route('/productmanager/addProduct')
def addProductOpen():
    mycursor = mydb.cursor()
    mycursor.execute("select * from suppliers")
    data=mycursor.fetchall()

    mycursor1 = mydb.cursor()
    mycursor1.execute("select * from categories")
    data1=mycursor.fetchall()
    return render_template("manager/product/addProduct.html", data=data, data1 = data1)

@auth.route('/productmanager/addProduct', methods=['GET','POST'])
def addProduct():   
    if request.method == 'POST':
        ProductName = request.form.get('ProductName')
        SupplierID = request.form.get('SupplierID')
        CategoryID = request.form.get('CategoryID')
        QuantityPerUnit = request.form.get('QuantityPerUnit')
        UnitPrice = request.form.get('UnitPrice')
        UnitsInStock = request.form.get('UnitsInStock')
        UnitsOnOrder = request.form.get('UnitsOnOrder')
        ReorderLevel = request.form.get('ReorderLevel')
        Discontinued = request.form.get('Discontinued')   
        
        mycursor = mydb.cursor()
        sql = "INSERT INTO products (ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Insert success', category="success")

        return redirect(url_for('auth.productmanager'))


@auth.route('/updateProduct',methods=['POST','GET'])
def updateProduct():
    if request.method == 'POST':
        id_data = request.form['id']
        ProductName = request.form['ProductName']
        SupplierID = request.form['SupplierID']
        CategoryID = request.form['CategoryID']
        QuantityPerUnit = request.form['QuantityPerUnit']
        UnitPrice = request.form['UnitPrice']
        UnitsInStock = request.form['UnitsInStock']
        UnitsOnOrder = request.form['UnitsOnOrder']
        ReorderLevel = request.form['ReorderLevel']
        Discontinued = request.form['Discontinued']

        mycursor = mydb.cursor()
        sql = " UPDATE products SET ProductName=%s, SupplierID=%s, CategoryID=%s, QuantityPerUnit=%s, UnitPrice=%s, UnitsInStock=%s, UnitsOnOrder=%s, ReorderLevel=%s, Discontinued=%s WHERE ProductID=%s"
        val = (ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued, id_data)

        mycursor.execute(sql, val)

        mydb.commit()
        flash('Update success', category="success")

    return redirect(url_for('auth.productmanager'))


@auth.route('/deleteProduct/<string:id_data>', methods = ['GET'])
def deleteProduct(id_data):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM products WHERE ProductID=%s", (id_data,))

    mydb.commit()
    flash("Deleted Success", category="success")

    return redirect(url_for('auth.productmanager'))

# Buy Product
@auth.route('/buyproduct')
def buyproduct():
    mycursor = mydb.cursor()
    mycursor.execute("select * from products")
    data=mycursor.fetchall()

    return render_template("manager/Market/buyproduct.html", data=data)

# Order Manager Page
@auth.route('/ordermanager', defaults={'page':1})
@auth.route('/ordermanager/page/<int:page>')
def ordermanager(page):
    perpage=40
    startat=page*perpage
    mycursor = mydb.cursor()
    mycursor.execute("select * from orders limit %s, %s", (startat,perpage))
    data=mycursor.fetchall()
    return render_template("manager/order/order.html", data=data)

@auth.route('/ordermanager/addorder')
def addorderOpen():
    customerData = mydb.cursor()
    customerData.execute("select * from customers")
    CTMdata=customerData.fetchall()

    shipperData = mydb.cursor()
    shipperData.execute("select * from shippers")
    SPdata=shipperData.fetchall()

    employeeData = mydb.cursor()
    employeeData.execute("select * from employees")
    EPldata=employeeData.fetchall()
    return render_template("manager/order/addorder.html", customerData = CTMdata, shipperData = SPdata, employeeData=EPldata)

@auth.route('/ordermanager/addorder', methods=['GET','POST'])
def addorder():   
    if request.method == 'POST':
        CustomerID = request.form.get('CustomerID')
        EmployeeID = request.form.get('EmployeeID')
        OrderDate = request.form.get('OrderDate')
        RequiredDate = request.form.get('RequiredDate')
        ShippedDate = request.form.get('ShippedDate')
        ShipVia = request.form.get('ShipVia')
        Freight = request.form.get('Freight')
        ShipName = request.form.get('ShipName')
        ShipAddress = request.form.get('ShipAddress')   
        ShipCity = request.form.get('ShipCity')
        ShipRegion = request.form.get('ShipRegion')
        ShipPostalCode = request.form.get('ShipPostalCode')
        ShipCountry = request.form.get('ShipCountry')   
        
        mycursor = mydb.cursor()
        sql = "INSERT INTO orders (CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)"
        val = (CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry)
        mycursor.execute(sql, val)

        mydb.commit()
        flash('Insert success', category="success")

        return redirect(url_for('auth.ordermanager'))


@auth.route('/updateOrder',methods=['POST','GET'])
def updateOrder():
    if request.method == 'POST':
        id_data = request.form['id']
        ProductName = request.form['ProductName']
        SupplierID = request.form['SupplierID']
        CategoryID = request.form['CategoryID']
        QuantityPerUnit = request.form['QuantityPerUnit']
        UnitPrice = request.form['UnitPrice']
        UnitsInStock = request.form['UnitsInStock']
        UnitsOnOrder = request.form['UnitsOnOrder']
        ReorderLevel = request.form['ReorderLevel']
        Discontinued = request.form['Discontinued']

        mycursor = mydb.cursor()
        sql = " UPDATE products SET ProductName=%s, SupplierID=%s, CategoryID=%s, QuantityPerUnit=%s, UnitPrice=%s, UnitsInStock=%s, UnitsOnOrder=%s, ReorderLevel=%s, Discontinued=%s WHERE ProductID=%s"
        val = (ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued, id_data)

        mycursor.execute(sql, val)

        mydb.commit()
        flash('Update success', category="success")

    return redirect(url_for('auth.ordermanager'))


@auth.route('/deleteOrder/<string:id_data>', methods = ['GET'])
def deleteOrder(id_data):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM orders WHERE orderID=%s", (id_data,))

    mydb.commit()
    flash("Deleted Success", category="success")

    return redirect(url_for('auth.ordermanager'))

# Order Detail
@auth.route('/orderDetail', defaults={'page':1})
@auth.route('/orderDetail/page/<int:page>')
def orderDetail(page):
    perpage=40
    startat=page*perpage
    mycursor = mydb.cursor()
    mycursor.execute("select * from orders limit %s, %s", (startat,perpage))
    data=mycursor.fetchall()
    return render_template("manager/orderDetail.html", data=data)

































