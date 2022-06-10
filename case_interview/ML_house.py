
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate
from sklearn.inspection import permutation_importance

df = pd.read_csv('raw_data/ML_house_clean.csv')

# correlation

correlation_df = df.corr()
corr_df = correlation_df.unstack().reset_index()
corr_df.rename(columns={'level_0':'feature_1','level_1':'feature_2',0:'correlation'},inplace=True)
corr_df.sort_values(by = 'correlation',ascending=True,inplace=True)
correlated_features = corr_df[corr_df['correlation'] >= 0.9].count()[0]
#print(correlated_features)

X = df[['NoGarage', 'GrLivArea','CentralAir','KitchenAbvGr','OverallCond','BedroomAbvGr','RoofSurface']]
y = df['SalePrice']

# baseline model

base_model = LinearRegression()
base_model.fit(X,y)

cv_results = cross_validate(base_model,X,y,cv=3)
base_model_score=round(cv_results['test_score'].mean(),1)
print(base_model_score)

# feature permutation

permutation_score = permutation_importance(base_model,X,y,n_repeats=10)
importance_df = pd.DataFrame(np.vstack((X.columns,permutation_score.importances_mean)).T)

# best feature
importance_df.columns=['feature','score decrease']
importance_df.sort_values(by="score decrease", ascending = False)
