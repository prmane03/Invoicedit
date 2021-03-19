from flask import Flask ,render_template,url_for,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('DATABASE_URL')

db=SQLAlchemy(app)

class logintable(db.Model):
	id=db.Column(db.Integer(),primary_key=True,autoincrement=True,nullable=False,unique=True)
	email=db.Column(db.String(25),unique=True)
	username=db.Column(db.String(25),unique=True)
	password=db.Column(db.String(20),nullable=False)

class invoicetable(db.Model):
	id=db.Column(db.Integer(),primary_key=True,autoincrement=True,nullable=False,unique=True)
	username=db.Column(db.String(25))
	invoice_number=db.Column(db.Integer)
	description=db.Column(db.Text)
	quantity=db.Column(db.Integer)
	price=db.Column(db.Integer)
	total=db.Column(db.Integer)
	
class infotable(db.Model):
	id=db.Column(db.Integer(),primary_key=True,autoincrement=True,nullable=False,unique=True)
	username=db.Column(db.String(25))
	invoice_number=db.Column(db.Integer)
	provider_name=db.Column(db.String(25))
	provider_phone=db.Column(db.Integer)
	provider_address=db.Column(db.Text)
	customer_name=db.Column(db.String(25))
	customer_phone=db.Column(db.Integer)
	customer_address=db.Column(db.Text)
	date = db.Column(db.Text)
	
	
#db.create_all()
#db.session.commit()

@app.route("/")
def login():
	return render_template("login.html")
	
		
@app.route("/register")
def register():
		return render_template("register.html")

@app.route("/regval",methods=["POST","GET"])
def regval():
	row=""
	if request.method=="POST":
		email=request.form["email"]
		usrnm=request.form["username"]
		pswd=request.form["password"]
		rpswd=request.form["rpassword"]
		row=logintable.query.filter_by(email=email).first()
		if(row is not None):
			return render_template('register.html',errormsg='Email already registered !!! try forgot password')
		else:
			if (pswd==rpswd):
				   row=logintable(email=email,username=usrnm,password=pswd)
				   try:
				   	db.session.add(row)	
				   	db.session.commit()
				   	return redirect("/")
				   except Exception as e:
				   	return render_template('register.html',errormsg=str(e)+' Maybe Username is taken Try different one... ')
			else:
				   return  render_template('register.html',errormsg='Password Does not match!!!')
	if request.method=="GET":
			   return render_template('register.html')
			   
		   	
@app.route("/logval",methods=["POST","GET"])
def logval():
	   	if request.method=="POST":
	   		usrnm=request.form["username"]
	   		pswd=request.form["password"]
	   		row=logintable.query.filter_by(username=usrnm,password=pswd).first()
	   		if(row is None):
	   			return render_template('login.html',errormsg='Invalid Credentials !!!')
	   		else:
	   			return render_template("invoice.html",usrnm=usrnm)
	   		
	   	return "printed"
	    	    
@app.route("/invoice")
def invoice():
	usrnm=request.args.get('usrnm')
	return render_template("invoice.html",usrnm=usrnm)
	
@app.route("/search")
def search():
	usrnm=request.args.get('usrnm')
	return render_template("search.html",usrnm=usrnm)
	
	
@app.route("/save")
def save():
	data = request.args.get('dict')
	inum= request.args.get('invnum')
	usrnm= request.args.get('usrnm')
	provider_name = request.args.get('provider_name')
	provider_phone =request.args.get('provider_phone')
	provider_address =request.args.get('provider_address')
	customer_name = request.args.get('customer_name')
	customer_phone =request.args.get('customer_phone')
	customer_address =request.args.get('customer_address')
	date = request.args.get('date')
	data=json.loads(data)
	
	db.session.query(invoicetable).filter(invoicetable.username==usrnm).filter(invoicetable.invoice_number==inum).delete()
	db.session.query(infotable).filter(infotable.username==usrnm).filter(infotable.invoice_number==inum).delete()
	
	try:		
		info=infotable(username=usrnm,invoice_number=inum,provider_name=provider_name,provider_phone=provider_phone,provider_address=provider_address,customer_name=customer_name,customer_phone=customer_phone,customer_address=customer_address,date=date)
		db.session.add(info)
	except Exception as e:
			print("Sql Exception infotable : "+str(e))
			return ("Got Exception "+str(e))
		
	for i in range(len(data['description'])):
		description = data['description'][i]
		quantity = data['quantity'][i]
		total = data['total'][i]
		price = data['price'][i]
		try:
			invoice= invoicetable(invoice_number=inum,description=description,quantity=quantity,price=price,total=total,username=usrnm)
			
			db.session.add(invoice)
			db.session.commit()
			print('new data inserted')
		except Exception as e:
			print("Sql Exception invoicetable : "+str(e))
			return ("Got Exception "+str(e))	
	return 'success'

	
@app.route('/getinvoice')
def getinvoice():
	inum= request.args.get('invnum')
	usrnm= request.args.get('usrnm')
	print(inum)
	print(usrnm)
	descriptionlist=[]
	quantitylist =[]
	pricelist=[]
	totallist=[]
	m = db.session.query(invoicetable).filter(invoicetable.username==usrnm).filter(invoicetable.invoice_number==inum)
	n = db.session.query(infotable).filter(infotable.username==usrnm).filter(infotable.invoice_number==inum).first()
	
	provider_name=n.provider_name
	provider_phone=n.provider_phone
	provider_address=n.provider_address
	customer_name=n.customer_name
	customer_phone=n.customer_phone
	customer_address=n.customer_address
	date= str(n.date)
	for i in m:
		descriptionlist.append(i.description)
		quantitylist.append(i.quantity)
		totallist.append(i.total)
		pricelist.append(i.price)
		print(descriptionlist)
		print(quantitylist)
		print(pricelist)
		print(totallist)
		
	dic = {
		'username':usrnm,
		'invoice_number':inum,
		'description':descriptionlist,
		'quantity':quantitylist,
		'total':totallist,
		'price':pricelist,
		'provider_name':provider_name,
		'provider_phone':provider_phone,
		'provider_address':provider_address,
		'customer_name':customer_name,
		'customer_phone':customer_phone,
		'customer_address':customer_address,
		'date':date[:11]
	}
	for i in dic.keys():
		print(dic[i])
	return jsonify(result=dic)
	
if  __name__ == "__main__":
	app.run(debug=True)	


