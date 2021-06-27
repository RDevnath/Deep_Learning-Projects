from flask import Flask,render_template,session,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,DateTimeField,RadioField,SelectField,TextField,TextAreaField,SubmitField,FloatField,IntegerField
from wtforms.validators import DataRequired
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

model = pickle.load(open('Car_price_prediction_model.pkl', 'rb'))

class predictionForm(FlaskForm):

    Year =  IntegerField('Purchasing year of the car/bike?',validators=[DataRequired()])
    Present_Price = FloatField('Purchasing cost of the car/bike?(In Lakhs)',validators=[DataRequired()])
    Kms_Driven = FloatField('How many KMs has it ran?',validators=[DataRequired()])
    Owner = SelectField(u'How many Owners did the car had?(0 or 1 or 3):',choices=[(0,'Zero'),(1,'One'),(3,'three')])
    Fuel_Type_Diesel = RadioField('Is this vehicle has the fuel type as Diesel?',choices=[(1,'Yes'),(0,'No')])
    Fuel_Type_Petrol = RadioField('Is this vehicle has the fuel type as Petrol?',choices=[(1,'Yes'),(0,'No')])
    Seller_Type_Individual = RadioField('Are you a Seller or Individual?',choices=[(1,'seller'),(0,'individual')])
    Transmission_Manual = SelectField('What is the Transmission type of the vehicle?(Automatic or Manual)',choices=[(1,'Manual'),(0,'Automatic')])
    Car_Name = StringField('What is the Car Name along with model?',validators=[DataRequired()])
    Description = TextAreaField()
    Submit = SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():

    form = predictionForm()
    if form.validate_on_submit():

        session['Year'] = form.Year.data
        session['Present_Price'] = form.Present_Price.data
        session['Kms_Driven'] = form.Kms_Driven.data
        session['Owner'] = form.Owner.data
        session['Fuel_Type_Diesel'] = form.Fuel_Type_Diesel.data
        session['Fuel_Type_Petrol'] = form.Fuel_Type_Petrol.data
        session['Seller_Type_Individual'] = form.Seller_Type_Individual.data
        session['Transmission_Manual'] = form.Transmission_Manual.data
        session['Car_Name'] = form.Car_Name.data
        session['Description'] = form.Description.data
        No_of_Year = 2021 - session['Year']
        prediction = model.predict([[session['Present_Price'], session['Kms_Driven'], session['Owner'], No_of_Year,
        session['Fuel_Type_Diesel'], session['Fuel_Type_Petrol'], session['Seller_Type_Individual'], session['Transmission_Manual']]])
        output = round(prediction[0],2)
        if output < 0:
            return render_template('prediction.html',prediction_text = "Sorry! You can't sell this Car")
        else:
            return render_template('prediction.html',prediction_text = "You Can sell this Car at {} Lakhs".format(output))

    return render_template('index.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
