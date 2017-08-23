import os
from flask import Flask, render_template, request, redirect,json
import pandas as pd
import pickle

import get_lcdata as lcdata
import plot_data as pltdata


app = Flask(__name__)

@app.route('/')
def main():
  return render_template('index.html')

@app.route('/predictor', methods=['GET','POST'])
def predictor():
  if request.method == 'GET':
    return render_template('inputinfo.html')
  else: #method was POST
    return redirect('/results')

@app.route('/results', methods=['GET', 'POST'])
def get_data():
    amount = request.form['amount']
    term = request.form['term']
    grade = request.form['grade']
    income = request.form['income']
    home_ownership = request.form['home_ownership']
    
    if not amount or not term or not grade or not income or not home_ownership:
        return render_template('error.html', message='Please fill in all of the fields.')
    prob=0
    rfmdl = lcdata.build_model()
    
    #print amount, term, grade, income,prob
    #Inputs to model
    X = pd.DataFrame({'loan_amnt':float(amount), 'term':term, 'grade':grade, 'annual_inc':float(income), 'home_ownership': home_ownership}, index = range(1))
    
    #with open('rfclf_model.pkl', 'r') as input:
    #    rfmodel = pickle.load(input)
    
    #prob = rfmodel.predict_proba(X)
    prob = rfmdl.predict_proba(X)
    result = '{:,.2%}'.format(prob[0][0])    
    return render_template('results.html', data = result)
    
@app.route('/credit_grade_viz', methods=['GET', 'POST'])
def get_lcdata_plots():
    if request.method == 'GET':
        data_df = lcdata.get_lcdata()
        if len(data_df):
            script, div = pltdata.plot_credit_grade_data(data_df)
            return render_template('graph_grade.html', script=script, div=div)
    else:
        return redirect('/results')
    
@app.route('/by_state_viz', methods=['GET', 'POST'])
def get_statedata_plots():
    if request.method == 'GET':
        data_df = lcdata.get_lcdata()
        if len(data_df):
            script, div = pltdata.plot_state_data(data_df)
            return render_template('graph_states.html', script=script, div=div)
    else:
        return redirect('/results')

@app.route('/loan_status_viz', methods=['GET', 'POST'])
def get_loanstatus_plots():
    if request.method == 'GET':
        data_df = lcdata.get_lcdata()
        if len(data_df):
            script, div = pltdata.plot_loan_status(data_df)
            return render_template('graph_ls.html', script=script, div=div)
    else:
        return redirect('/results')
    
    
    
@app.route('/index',methods=['GET','POST'])
def index():
  if request.method == 'GET':
     return render_template('index.html')
  else:
    #request was a POST
     return render_template('error.html')
             

        
#if __name__ == '__main__':
#  app.run(port=33507)     #comment if running on DO
# app.run(host='0.0.0.0')    #need this to run on DO local
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)         #for heroku app

    
    
    