# -*- coding: utf-8 -*-
"""
	Default Mortgage Predictions
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	An example web application for making predicions using a saved WLM model
	using Flask and the IBM WLM APIs.

	Created by Rich Tarro
	May 2017
"""

import os, urllib3, requests, json
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development key',
))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://admin:xxxx@bluemix-sandbox-dal-9-portal.8.dblayer.com:26360/MortgageDefault'
#postgres://admin:XZLNWWMRNZHWXOCK@bluemix-sandbox-dal-9-portal.8.dblayer.com:26360/mydb
db = SQLAlchemy(app)

class mortgagedefault(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	FirstName = db.Column(db.String(20))
	LastName = db.Column(db.String(20))
	Income = db.Column(db.Integer)
	AppliedOnline = db.Column(db.String(3))
	Residence = db.Column(db.String(20))
	YearCurrentAddress = db.Column(db.Integer)
	YearsCurrentEmployer = db.Column(db.Integer)
	NumberOfCards = db.Column(db.Integer)
	CCDebt = db.Column(db.Integer)
	Loans = db.Column(db.Integer)
	LoanAmount = db.Column(db.Integer)
	SalePrice = db.Column(db.Integer)
	Location = db.Column(db.Integer)
	prediction = db.Column(db.Numeric)
	probability = db.Column(db.Numeric)
	
	def __init__(self, FirstName, LastName, Income, AppliedOnline, Residence, YearCurrentAddress,
		YearsCurrentEmployer, NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location,
		prediction, probability):
		self.FirstName = FirstName
		self.LastName = LastName
		self.Income = Income
		self.AppliedOnline = AppliedOnline
		self.Residence = Residence
		self.YearCurrentAddress = YearCurrentAddress
		self.YearsCurrentEmployer = YearsCurrentEmployer
		self.NumberOfCards = NumberOfCards
		self.CCDebt = CCDebt
		self.Loans = Loans
		self.LoanAmount = LoanAmount
		self.SalePrice = SalePrice
		self.Location = Location
		self.prediction = prediction
		self.probability = probability

	def __repr__(self):
		return '<mortgagedefault%r>' % self.Income

def saveDB(FirstName, LastName, Income, AppliedOnline, Residence, YearCurrentAddress,
		YearsCurrentEmployer, NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location,
		prediction, probability):
	record = mortgagedefault(FirstName, LastName, Income, AppliedOnline, Residence, YearCurrentAddress,
		YearsCurrentEmployer, NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location,
		prediction, probability)
	db.session.add(record)
	db.session.commit()


def predictDefault(ID,Gender,Status,Children,EstIncome,CarOwner,Age,LongDistance,International,Local,Dropped,Paymethod,LocalBilltype,LongDistanceBilltype,Usage,RatePlan):
	
	service_path = 'https://ibm-watson-ml.mybluemix.net'
	username = 'xxxx'
	password = '****'

	headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
	url = '{}/v2/identity/token'.format(service_path)
	response = requests.get(url, headers=headers)
	mltoken = json.loads(response.text).get('token')
	header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
	scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/3194"
	payload_scoring = ({"record":[ID,Gender,Status,Children,EstIncome,CarOwner,Age,LongDistance,International,Local,Dropped,Paymethod,LocalBilltype,LongDistanceBilltype,Usage,RatePlan]})
	response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
	
	result = response_scoring.text
	return response_scoring


@app.route('/',  methods=['GET', 'POST'])
def index():

	if request.method == 'POST':
		ID = 999
		#Gender='F'
		#Status='S'
		#Children=0.000000
		#EstIncome=5185.310000
		#CarOwner='N'
		#Age=62.053333
		#LongDistance=16.390000
		#International=5.990000
		#Local=30.510000
		#Dropped=0.000000
		#Paymethod='CC'
		#LocalBilltype='FreeLocal'
		#LongDistanceBilltype='Intnl_discount'
		#Usage=52.900000
		#RatePlan=2.000000

		Gender=request.form['Gender']
		Status='S'
		Children=int(request.form['Children'])
		EstIncome=int(request.form['EstIncome'])
		CarOwner=request.form['CarOwner']
		Age=int(request.form['Age'])
		LongDistance=int(request.form['LongDistance'])
		International=int(request.form['International'])
		Local=int(request.form['Local'])
		Dropped=int(request.form['Dropped'])
		Paymethod=request.form['Paymethod']
		LocalBilltype='FreeLocal'
		LongDistanceBilltype='Intnl_discount'
		Usage=52.900000
		RatePlan=int(request.form['RatePlan'])
		
		#Gender=request.form['Gender']
		#print "Gender=" %Gender
		#Status='S'
		#Children=int(request.form['Children'])
		#EstIncome=int(request.form['EstIncome'])
		#CarOwner='N'
		#Age=int(request.form['Age'])
		#LongDistance=int(request.form['YearsCurrentEmployer'])
		#International=5.990000
		#Local=30.510000
		#Dropped=int(request.form['Dropped'])
		#Paymethod=request.form['Paymethod']
		#LocalBilltype='FreeLocal'
		#LongDistanceBilltype='Intnl_discount'
		#Usage=52.900000
		#RatePlan=int(request.form['RatePlan'])

		#Income = int(request.form['Income'])
		#AppliedOnline = request.form['AppliedOnline']
		#Residence = request.form['Residence']
		#YearCurrentAddress = int(request.form['YearCurrentAddress'])
		#YearsCurrentEmployer = int(request.form['YearsCurrentEmployer'])
		#NumberOfCards = int(request.form['NumberOfCards'])
		#CCDebt = int(request.form['CCDebt'])
		#Loans = int(request.form['Loans'])
		#LoanAmount = int(request.form['LoanAmount'])
		#SalePrice = int(request.form['SalePrice'])
		#Location = int(request.form['Location'])
		
		
		session[Gender]=Gender
		session[Status]=Status
		session[Children]=Children
		session[EstIncome] = EstIncome
		session[CarOwner]=CarOwner
		session[Age]=Age
		session[LongDistance]=LongDistance
		session[International]=International
		session[Local]=Local
		session[Dropped]=Dropped
		session[Paymethod]=Paymethod
		session[LocalBilltype]=LocalBilltype
		session[LongDistanceBilltype]=LongDistanceBilltype
		session[Usage]=Usage
		session[RatePlan]=RatePlan

		#session['Income'] = EstIncome
		#session['AppliedOnline'] = AppliedOnline
		#session['Residence'] = Residence
		#session['YearCurrentAddress'] = YearCurrentAddress
		#session['YearsCurrentEmployer'] = YearsCurrentEmployer
		#session['NumberOfCards'] = NumberOfCards
		#session['CCDebt'] = CCDebt
		#session['Loans'] = Loans
		#session['LoanAmount'] = LoanAmount
		#session['SalePrice'] = SalePrice
		#session['Location'] = Location


		response_scoring = predictDefault(ID,Gender,Status,Children,EstIncome,CarOwner,Age,LongDistance,International,Local,Dropped,Paymethod,LocalBilltype,LongDistanceBilltype,Usage,RatePlan)

		prediction = response_scoring.json()["result"]["prediction"]
		probability = response_scoring.json()["result"]["probability"]["values"][1]

		session['prediction'] = prediction
		session['probability'] = probability

		flash('Successful Prediction')
		return render_template('scoreSQL.html', response_scoring=response_scoring, request=request)


	else:
		return render_template('input.html')

@app.route('/saveData', methods=['POST'])
def saveData():
	FirstName = request.form['FirstName']
	LastName = request.form['LastName']

	Income = session['Income']
	AppliedOnline = session['AppliedOnline']
	Residence = session['Residence']
	YearCurrentAddress = session['YearCurrentAddress']
	YearsCurrentEmployer = session['YearsCurrentEmployer']
	NumberOfCards = session['NumberOfCards']
	CCDebt = session['CCDebt']
	Loans = session['Loans']
	LoanAmount = session['LoanAmount']
	SalePrice = session['SalePrice']
	Location = session['Location']
	prediction = session['prediction']
	probability = session['probability']

	#print(FirstName, LastName, Income, AppliedOnline, Residence, YearCurrentAddress, YearsCurrentEmployer, NumberOfCards,
	#   CCDebt, Loans, LoanAmount, SalePrice, Location)

	saveDB(FirstName, LastName, Income, AppliedOnline, Residence, YearCurrentAddress,YearsCurrentEmployer,
		NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location, prediction, probability)

	flash('Prediction Successfully Stored in Database')

	return render_template('save.html')

@app.route('/scoretest', methods=['GET', 'POST'])
def scoretest():
	
	service_path = 'https://ibm-watson-ml.mybluemix.net'
	username = 'xxxx'
	password = 'xxxx'

	headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
	url = '{}/v2/identity/token'.format(service_path)
	response = requests.get(url, headers=headers)
	mltoken = json.loads(response.text).get('token')
	header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
	scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/2264"
	payload_scoring = {"record":[999,47422.000000,"YES","Owner Occupier",11.000000,12.000000,2.000000,2010.000000,1.000000,12315.000000,330000,100]}
	response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
	
	result = response_scoring.text
	return render_template('scoretest.html', result=result, response_scoring=response_scoring)

#if __name__ == '__main__':
#   app.run()
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
