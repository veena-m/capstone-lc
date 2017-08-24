import pandas as pd
import numpy as np
import pickle

#---Machine learning------------------
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split 
from sklearn.pipeline import Pipeline

class MultiColumnLabelEncoder:
    def __init__(self,col_names = None):
        self.col_names = col_names # array of column names to encode

    def fit(self,X,y=None):
        return self # not relevant here

    def transform(self,X):
        '''
        Transforms columns of X specified in self.col_names using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        if self.col_names is not None:
            for col in self.col_names:
                output[col] = LabelEncoder().fit_transform(output[col])
        return output

    def fit_transform(self,X,y=None):
        return self.fit(X,y).transform(X)
#----------------------------------------------


def get_lcdata():
    
    df = pd.read_excel('./data/LoanStats3a.xlsx',skiprows=[0],parse_cols = "A:BA,BE,CA,CB,DB,DC")
    #df = df[['member_id','loan_amnt','int_rate','term','grade','home_ownership','annual_inc','purpose','addr_state','loan_status']]
    print len(df)
    with open('./data/df_data.pkl', 'wb') as fp:
        pickle.dump(df,fp) 

    return df
       
def build_model():
    
    df = get_lcdata()
        
    #To build and train model consider only those loans that are Fully Paid or Charged off
    df_filtered = df[(df['loan_status'] == 'Fully Paid') | (df['loan_status'] == 'Charged Off')]
    print len(df_filtered)
    
    #Supervised learning - Classification problem
    #Create label y  - an array that denotes 1 if Loan is 'Fully Paid' or 0 'Charged Off' 
    #set y to the Loan Status column of df as that is what model will be checked against 
    y = np.where(df_filtered['loan_status'] == 'Fully Paid', 1,0)
    
    #Create pipeline 
    rfpipe = Pipeline([
              ('encode',MultiColumnLabelEncoder(['grade','term','home_ownership'])),  # 'addr_state' 
              # ('std_scaler',StandardScaler()),
              ('rf_classifier', RandomForestClassifier(n_estimators=10)) #, max_depth = 5 
              # add more pipeline steps as needed
     ])

    #data = df_filtered[['loan_amnt','term','home_ownership','int_rate','grade', 'annual_inc','addr_state']]
    data = df_filtered[['grade','annual_inc','loan_amnt','term','home_ownership']]  #'int_rate','addr_state'
    
    # Split training and test set using 7:3 ratio
    #trainX, testX, ytrain, ytest = train_test_split(data,y,test_size=0.3,random_state=1)

    trainX = data   
    ytrain = y      
    
    rfpipe.fit_transform(trainX,ytrain)
    
    with open('./data/rfclf_model.pkl', 'wb') as f:
        pickle.dump(rfpipe,f) 
    
    return rfpipe

