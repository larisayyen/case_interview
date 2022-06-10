
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

df = pd.read_csv('raw_data/ML_Cars.csv')
df.drop_duplicates(inplace=True)

# data preprocessing

# null values
df['carwidth'] = df['carwidth'].apply(lambda x: 'nan' if x=='*'else x)

imputer = SimpleImputer(strategy='median')
imputer.fit(df[['carwidth']])
df['carwidth'] = imputer.transform(df[['carwidth']])

imputer = SimpleImputer(strategy='most_frequent')
imputer.fit(df[['enginelocation']])
df['enginelocation'] = imputer.transform(df[['enginelocation']])
#print(df.enginelocation.unique())

# feature scaling

r_scaler = RobustScaler()
r_scaler.fit(df[['peakrpm' , 'carwidth' , 'stroke']])
df[['peakrpm' , 'carwidth' , 'stroke']] = r_scaler.transform(df[['peakrpm' , 'carwidth' , 'stroke']])

scaler = StandardScaler()
scaler.fit(df[['curbweight']])
df['curbweight'] = scaler.transform(df[['curbweight']])

# feature encoding

ohe = OneHotEncoder(sparse = False)
ohe.fit(df[['aspiration']])
df['std'],df['turbo'] = ohe.transform(df[['aspiration']]).T
df.drop(columns = 'aspiration',inplace=True)

ohe = OneHotEncoder(sparse = False)
ohe.fit(df[['enginelocation']])
df['front'],df['rear'] = ohe.transform(df[['enginelocation']]).T
df.drop(columns = 'enginelocation',inplace=True)

ohe = OneHotEncoder(sparse = False,handle_unknown='ignore')
ohe.fit(df[['enginetype']])
enginetype_encoded = ohe.transform(df[['enginetype']])
df['dohc'],df['dohcv'],df['l'],df['ohc'],df['ohcf'],df['ohcv'],df['rotor'] = enginetype_encoded.T
df.drop(columns='enginetype',inplace=True)

# manual ordinal encoding
dict = {'four':4,'six':6,'five':5,'three':3,'twelve':12,'two':2,'eight':8}
df['cylindernumber'] = df['cylindernumber'].replace(dict)

le = LabelEncoder()
le.fit(df[['price']])
df['price'] = le.transform(df[['price']])

# drop correlated and unimportant features
df.drop(columns = ['ohcv','dohc','dohcv','l','ohcf','rotor'],inplace=True)

# baseline model

X = df[['carwidth','curbweight','cylindernumber','stroke','peakrpm','ohc']]
y = df['price']

base_model = LogisticRegression()
base_model.fit(X,y)

cv_results = cross_validate(base_model,X,y,cv=3)
base_model_score=round(cv_results['test_score'].mean(),2)
print(base_model_score)
