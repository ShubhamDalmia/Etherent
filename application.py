from curses import flash
from email.mime import application
from email.mime.multipart import MIMEMultipart
from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
from sqlalchemy.orm import sessionmaker
import deploy

app = Flask(__name__)
password = urllib.parse.quote_plus("")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://mysqlUsername:{password}@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Session = sessionmaker(bind=app.config['SQLALCHEMY_DATABASE_URI'])
session = Session()

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('Login.html')


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        userName = request.form['userName']
        passwordS = request.form['password']
        isOwner = db.session.execute(
            "select isOwner from DemoUser where userName='" + userName + "' and password='" + passwordS + "'").all()
        if not isOwner:
            return ('Wrong Credentials')
        elif isOwner[0][0] == 1:
            return redirect(url_for('Owner'))
        elif isOwner[0][0] == 0:
            return redirect(url_for('Tenant'))


@app.route('/owner', methods=['POST', 'GET'])
def Owner():
    cus = db.session.execute("select * from customers").all()
    properties = db.session.execute('select * from Property').all()
    print('oaky')
    return render_template('owner.html', properties=properties)


@app.route('/tenant', methods=['POST', 'GET'])
def Tenant():
    return render_template('tenant.html')


@app.route('/addTenant', methods=['POST'])
def AddTenant():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    userName = request.form['userName']
    password = request.form['password']
    phoneNo = request.form['phoneNo']
    linkedWallet = request.form['linkedWallet']
    query = f'''INSERT INTO demouser(Name, userName, password, phoneNo, linkedWallet, isOwner) VALUES('{0}', '{1}', '{2}', '{3}','{4}', 0);commit;'''
    query = query.format(firstName+lastName,userName,password,phoneNo,linkedWallet)
    test = db.session.execute(query)
    return render_template('tenant.html')
    #deploy.addTenant(linkedWallet, firstName, lastName, phoneNo, rating=0, rentalPoints=0, canRent=True, lastRentPaid=0,dueAmount=0)


    # query.format(name,userName,password,phoneNo,linkedWallet)


@app.route('/addOwner', methods=['POST'])
def AddOwner():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    userName = request.form['userName']
    password = request.form['password']
    phoneNo = request.form['phoneNo']
    linkedWallet = request.form['linkedWallet']
    balance = 0

    deploy.addOwner(linkedWallet, firstName, lastName, phoneNo, balance)
    query = "INSERT INTO DemoUser(Name,userName,password,PhoneNo,linkedWallet,isOwner) values('{0}','{1}','{2}','{3}','{4}',1);commit;"
    query = query.format(firstName + ' ' + lastName, userName, password, phoneNo, linkedWallet, balance)
    test = db.session.execute(query)
    # uid = db.session.execute("select max(Uid) from DemoUser where userName='"+userName+"'").all()
    # propInsertQuery = "Insert into Property(Uid,Address,ApplicationNo) values('{0}','-','{1}');commit;"
    # propInsertQuery = propInsertQuery.format(uid[0][0],applicationNo)
    # test = db.session.execute(propInsertQuery)
    # test = db.session.execute
    return redirect(url_for('Owner'))


@app.route('/addProperty', methods=['POST'])
def AddProperty():
    propertyId = request.form['propertyId']
    linkedWallet = request.form['linkedWallet']
    isCurrentlyRented = request.form['isCurrentlyRented']
    if isCurrentlyRented == 'on':
        isCurrentlyRented = True
    else:
        isCurrentlyRented = False
    rent = request.form['rent']

    deploy.addProperty(linkedWallet,int(propertyId),bool(isCurrentlyRented),int(rent))
    propInsertQuery = "Insert into Property(propertyId,linkedWallet,isCurrentlyRented,rent) values('{0}','{1}','{2}','{3}');commit;"
    propInsertQuery = propInsertQuery.format(propertyId, str(linkedWallet),int(isCurrentlyRented),str(rent))
    test = db.session.execute(propInsertQuery)
    return redirect(url_for('Owner'))

@app.route('/rentOut',methods = ['POST'])
def RentOut():
    propertyId =request.form['propertyId']
    ownerLinkedWallet = request.form['ownerLinkedWallet']
    tenantLinkedWallet = request.form['tenantLinkedWallet']
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    # deploy.signAgreement(ownerLinkedWallet,tenantLinkedWallet,int(propertyId),1661599508,1661599508)
    return redirect(url_for('Owner'))


@app.route('/rentClose',methods = ['POST'])
def RentClose():
    propertyId =request.form['propertyId']
    cleanlinessRating = request.form['cleanlinessRating']
    tenantLinkedWallet = request.form['tenantLinkedWallet']
    neighbourRating = request.form['neighbourRating']
    return redirect(url_for('Owner'))


@app.route('/logout')
def Logout():
    return render_template('Login.html')


if __name__ == "__main__":
    app.run(debug=False)