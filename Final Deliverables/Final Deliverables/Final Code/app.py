import flask
import ibm_db
import joblib
import numpy as np
from flask import Flask, redirect, render_template, request, session, url_for
from flask_cors import CORS

app = flask.Flask(__name__, static_url_path='')
CORS(app)
import pickle
model=pickle.load(open('prediction.sav','rb'))
conn = None

##connecting database db2
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=znz39692;PWD=UtiaNHvnO4brxedz;PROTOCOL=TCPIP",'','')
    print("Successfully connected with db2")
except:
    print("Unable to connect: ", ibm_db.conn_errormsg())

@app.route('/')
@app.route('/home')
@app.route('/entry')
def entry():
    return render_template('index.html')

@app.route('/signuppage')
def signuppage():
    return render_template('registration.html')

@app.route('/loginpage')
def loginpage():
    return render_template('Login.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route("/adduser", methods=["POST"])
def adduser():
    username = request.form.get("username")
    lastname = request.form.get("lastname")
    emailid = request.form.get("emailid")
    password = request.form.get("password")
    tel = request.form.get("tel")
    gender = request.form.get("gender")
    dob = request.form.get("dob")
    address = request.form.get("address")
    

    sql = "SELECT * FROM user WHERE emailid = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, emailid)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
        return render_template('login.html', ibm1="You are already a member, please login using your details")
    else:
        insert_sql = "INSERT INTO user VALUES (?,?,?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, username)
        ibm_db.bind_param(prep_stmt, 2, lastname)
        ibm_db.bind_param(prep_stmt, 3, emailid)
        ibm_db.bind_param(prep_stmt, 4, password)
        ibm_db.bind_param(prep_stmt, 5, tel)
        ibm_db.bind_param(prep_stmt, 6, gender)
        ibm_db.bind_param(prep_stmt, 7, dob)
        ibm_db.bind_param(prep_stmt, 8, address)
        ibm_db.execute(prep_stmt)
        return render_template('login.html', ibm="You are Successfully Registered, please login using your crendentials")


@app.route("/checkuser", methods=["POST"])
def checkuser():
    emailid = request.form.get("emailid")
    password = request.form.get("password")
    
    sql = "SELECT * FROM user WHERE emailid = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, emailid)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if not account:
        return render_template('login.html', msg="No Account found! \n Please Signup")
        
    else:
        if(password == str(account['PASSWORD']).strip()):
            return render_template('prediction.html',msg = "successfully logged in")
        else:
            return render_template('login.html', msg="Please enter the correct password")
        
        
@app.route('/details', methods = ['GET','POST'])
def details():
	if request.method == "POST":
		gender=request.form['gender']
		married=request.form['married']
		dependents=request.form['Dependents']
		education=request.form['education']
		self_employment=request.form['employment']
		applicant_income=request.form['income']
		co_applicant=request.form['coincome']
		Loan_Amount=request.form['loan']
		credit_history=request.form['history']
		if(gender=="Male"):
			gender=1
		else:
			gender=0
		if(married=="Yes"):
			married=1
		else:
			married=0
		if(education=="Graduate"):
			education=0
		else:
			education=1
		if(self_employment=="Yes"):
			self_employment=1
		else:
			self_employment=0
		S=[[gender,married,dependents,education,self_employment,applicant_income,co_applicant,Loan_Amount,credit_history]]	
		ans=model.predict(S)
		print(ans)
		if (ans==1):
			ans="yes"
			print("Congratulations your eligble for this Loan")
			return render_template('result.html', result="Congratulations!", result1="you are eligble for this Loan")
		else:
			ans="No"
			print("We are sad to inform that your request has not been accepted")
	return render_template('result.html', result=ans)
	
if __name__ =='__main__':
	app.run()			






	
    
    


   
	
