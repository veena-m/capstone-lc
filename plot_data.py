from bokeh.plotting import figure
from bokeh.charts import Bar, color
from bokeh.embed import components 
import pandas as pd

def plot_credit_grade_data(df):
   
   plot = Bar(df,'grade',xlabel='Credit Grade Category',ylabel='Count of Borrowers',title='Credit Grade of Borrowers',legend='top_right',color=color(columns='grade'))

   script, div = components(plot)
   return script,div 

def plot_loan_status(df):
   
    df_filtered = df[(df['loan_status'] == 'Fully Paid') | (df['loan_status'] == 'Charged Off')]
    plot = Bar(df,'loan_status',legend=False,ylabel='Count of Borrowers',xlabel='Status of loans',title='Loan Status of borrowers',color=color(columns='loan_status'), width=400, height=600)
    
    script, div = components(plot)
    return script,div 

def plot_state_data(df):
    
    
    plot = Bar(df,'addr_state',legend=False,xlabel= 'By State',ylabel='Count of Borrowers',title='Borrowers by State',color=color(columns='addr_state'), width=1200, height=500)
    
    script, div = components(plot)
    return script,div 