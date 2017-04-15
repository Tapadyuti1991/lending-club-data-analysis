
# coding: utf-8

# In[222]:

from io import StringIO
import requests
import json
import pandas as pd
import numpy as np
# @hidden_cell
# This function accesses a file in your Object Storage. The definition contains your credentials.
# You might want to remove those credentials before you share your notebook.
def get_object_storage_file_with_credentials_b6d2dc4304df42d5bf425b6ca8af67ff(container, filename):
    """This functions returns a StringIO object containing
    the file content from Bluemix Object Storage."""

    url1 = ''.join(['https://identity.open.softlayer.com', '/v3/auth/tokens'])
    data = {'auth': {'identity': {'methods': ['password'],
            'password': {'user': {'name': 'member_cd9be0e4ff1994ebede81451af2f9ee17e1d0d66','domain': {'id': '9d54dfb7f46d48d8930e2e61e1e7ddab'},
            'password': 'IbA26vS(8zQl.2_P'}}}}}
    headers1 = {'Content-Type': 'application/json'}
    resp1 = requests.post(url=url1, data=json.dumps(data), headers=headers1)
    resp1_body = resp1.json()
    for e1 in resp1_body['token']['catalog']:
        if(e1['type']=='object-store'):
            for e2 in e1['endpoints']:
                        if(e2['interface']=='public'and e2['region']=='dallas'):
                            url2 = ''.join([e2['url'],'/', container, '/', filename])
    s_subject_token = resp1.headers['x-subject-token']
    headers2 = {'X-Auth-Token': s_subject_token, 'accept': 'application/json'}
    resp2 = requests.get(url=url2, headers=headers2)
    return StringIO(resp2.text)

df = pd.read_csv(get_object_storage_file_with_credentials_b6d2dc4304df42d5bf425b6ca8af67ff('LendingClub', 'Processed_Acc_Dim_Red_hasNANs.csv'))
df.head()


# In[223]:

remove_cols=[]
for cols in list(df):
    diff = len(df[cols]) - df[cols].count()
    if(diff/len(df[cols]) * 100 >50):
#        
        remove_cols.append(cols)
df=df[df.columns.difference(remove_cols)] 


# In[224]:

df.head()


# In[225]:

df["acc_open_past_24mths"]=df["acc_open_past_24mths"].fillna(0)
df["acc_open_past_24mths"]=df["acc_open_past_24mths"].astype(int)

#print(df.annual_inc.isnull().values.any())



# del df["annual_inc_joint"]
del df["avg_cur_bal"]
del df["bc_open_to_buy"]
del df["bc_util"]
del df["desc"]
del df["earliest_cr_line"]
#print(df.annual_inc_joint.value_counts())


# In[226]:


df.ix[:3,10:20]


# In[227]:

df.insert(14, "fico_range_grade", "A")


# In[228]:


df.fico_range_grade=np.where(df['fico_range_high'] > 800,'Excellent', 
           np.where(df['fico_range_high'].between(750,799), 'Very Good',
           np.where(df['fico_range_high'].between(700,749), 'Good',
           np.where(df['fico_range_high'].between(650,699), 'Fair',
           np.where(df['fico_range_high'].between(600,649), 'Poor',
           'Very bad'
         )))))
del df["fico_range_high"]
del df["fico_range_low"]
del df["inq_last_6mths"]
del df["last_credit_pull_d"]
del df["last_credit_pull_d_year"]
del df["last_fico_range"]
del df["last_fico_range_high"]
del df["last_fico_range_low"]
del df["last_meanfico"]
del df["mo_sin_old_rev_tl_op"]
del df["mo_sin_rcnt_rev_tl_op"]


# In[229]:

df['issue_d']=pd.Series(df['issue_d'].str[4:])


# In[230]:

df["mo_sin_old_il_acct"]=df["mo_sin_old_il_acct"].fillna(int(df["mo_sin_old_il_acct"].mean()))

df['mo_sin_old_il_acct']=df['mo_sin_old_il_acct'].astype(int)

df["mo_sin_rcnt_tl"]=df["mo_sin_rcnt_tl"].fillna(int(df["mo_sin_rcnt_tl"].mean()))

df['mo_sin_rcnt_tl']=df['mo_sin_rcnt_tl'].astype(int)

df["mort_acc"]=df["mort_acc"].fillna(int(df["mort_acc"].mean()))

df['mort_acc']=df['mort_acc'].astype(int)

df.ix[:3,19:30]



# In[231]:


del df["mths_since_recent_bc"]
del df["mths_since_recent_inq"]
del df["num_actv_bc_tl"]
del df["num_bc_sats"]
del df["num_bc_tl"]
del df["num_il_tl"]
del df["num_op_rev_tl"]
del df["num_rev_accts"]
del df["num_rev_tl_bal_gt_0"]
del df["num_sats"]
del df["num_tl_120dpd_2m"]
del df["num_tl_30dpd"]
del df["num_tl_90g_dpd_24m"]
del df["out_prncp"]
del df["policy_code"]
del df["earliest_cr_line_year"]


# In[193]:

import math
ceil_function= lambda x: math.ceil(x*100)/100

df["num_accts_ever_120_pd"]=df["num_accts_ever_120_pd"].fillna(int(df["num_accts_ever_120_pd"].mean()))

df['num_accts_ever_120_pd']=df['num_accts_ever_120_pd'].astype(int)


df["num_actv_rev_tl"]=df["num_actv_rev_tl"].fillna(int(df["num_actv_rev_tl"].mean()))

df['num_actv_rev_tl']=df['num_actv_rev_tl'].astype(int)


df["num_tl_op_past_12m"]=df["num_tl_op_past_12m"].fillna(int(df["num_tl_op_past_12m"].mean()))

df['num_tl_op_past_12m']=df['num_tl_op_past_12m'].astype(int)

df["pct_tl_nvr_dlq"]=df["pct_tl_nvr_dlq"].fillna(float(df["pct_tl_nvr_dlq"].mean()))

df['pct_tl_nvr_dlq']=df['pct_tl_nvr_dlq'].apply(ceil_function)

df["percent_bc_gt_75"]=df["percent_bc_gt_75"].fillna(float(df["percent_bc_gt_75"].mean()))

df['percent_bc_gt_75']=df['percent_bc_gt_75'].apply(ceil_function)

df.ix[:3,30:40]


# In[232]:

del df["tax_liens"]
del df["title"]
del df["tot_coll_amt"]
del df["tot_cur_bal"]
del df["tot_hi_cred_lim"]
del df["total_bal_ex_mort"]
del df["total_bc_limit"]
del df["total_il_high_credit_limit"]
del df["total_pymnt"]
del df["total_rec_late_fee"]
del df["total_rev_hi_lim"]
del df["zip_code"]
del df["recoveries"]


# In[233]:

# print(len(df))
# print(df.verification_status.isnull().sum())
# del df["zip_code"]
# print(df.recoveries.value_counts())
df = df[pd.notnull(df['revol_util'])]

df["total_rec_prncp"]=df["total_rec_prncp"].astype(int)


# In[234]:

df.int_rate.head(3)


# In[50]:

from io import BytesIO  
import requests  
import json  
import pandas as pd

def put_file(credentials, local_file_name):  
    """This functions returns a StringIO object containing
    the file content from Bluemix Object Storage V3."""
    f = open(local_file_name,'r')
    my_data = f.read()
    url1 = ''.join(['https://identity.open.softlayer.com', '/v3/auth/tokens'])
    data = {'auth': {'identity': {'methods': ['password'],
            'password': {'user': {'name': credentials['username'],'domain': {'id': credentials['domain_id']},
            'password': credentials['password']}}}}}
    headers1 = {'Content-Type': 'application/json'}
    resp1 = requests.post(url=url1, data=json.dumps(data), headers=headers1)
    resp1_body = resp1.json()
    for e1 in resp1_body['token']['catalog']:
        if(e1['type']=='object-store'):
            for e2 in e1['endpoints']:
                        if(e2['interface']=='public'and e2['region']=='dallas'):
                            url2 = ''.join([e2['url'],'/', credentials['container'], '/', local_file_name])
    s_subject_token = resp1.headers['x-subject-token']
    headers2 = {'X-Auth-Token': s_subject_token, 'accept': 'application/json'}
    resp2 = requests.put(url=url2, headers=headers2, data = my_data )
    print (resp2)


# In[ ]:


# @hidden_cell
credentials_4 = {
  'auth_url':'https://identity.open.softlayer.com',
  'project':'object_storage_b6d2dc43_04df_42d5_bf42_5b6ca8af67ff',
  'project_id':'b27f8cf040e5488eb7ceb30211ba0896',
  'region':'dallas',
  'user_id':'bd256d68aea5489f8b140af608a2dbe9',
  'domain_id':'9d54dfb7f46d48d8930e2e61e1e7ddab',
  'domain_name':'1257643',
  'username':'member_cd9be0e4ff1994ebede81451af2f9ee17e1d0d66',
  'password':"""IbA26vS(8zQl.2_P""",
  'container':'LendingClub',
  'tenantId':'undefined',
  'filename':'azure_classfication.csv'
}


# In[ ]:

df.to_csv("accepted_merged_final.csv",index=False)


# In[ ]:

put_file(credentials_4,'accepted_merged_final.csv')


# In[198]:

#Compute the corelation between the features to determine the relationship between all the features
correlations_technique1 = df.corr(method='pearson')
correlations_technique1.ix[12:13,0:9]


# In[142]:

#Compute the corelation between the features to determine the relationship between all the features
correlations_technique1 = df.corr(method='pearson')
correlations_technique1.ix[12:13,9:14]


# In[143]:

#Compute the corelation between the features to determine the relationship between all the features
correlations_technique1.ix[12:13,14:24]


# In[144]:

#Compute the corelation between the features to determine the relationship between all the features
correlations_technique1.ix[12:13,24:37]


# In[235]:

from sklearn.preprocessing import LabelEncoder

#using label encoder to convert categorical columns into numeric values
def dummyEncode(df):
        columnsToEncode = list(df)
        le = LabelEncoder()
        for feature in columnsToEncode:
            try:
                df[feature] = le.fit_transform(df[feature])
            except:
                print('Error encoding '+feature)
        return df


# In[201]:

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression



#my_list=['term','revol_util','total_rec_int','meanfico','int_rate']
pearson_df=df.copy()
pearson_df=pearson_df[['acc_open_past_24mths','num_tl_op_past_12m','percent_bc_gt_75','term','revol_util','total_rec_int','meanfico','int_rate']]

#random split method for creating the training and test splits
X_train_pearson, X_test_pearson, Y_train_pearson, Y_test_pearson = train_test_split(pearson_df.ix[:, pearson_df.columns != 'int_rate'], pearson_df.int_rate, test_size=0.2, random_state=0)


print("Starting Linear Regression algorithm")
linear_reg = LinearRegression()
fit=linear_reg.fit(X_train_pearson, Y_train_pearson)

print ("Intercept is ",linear_reg.intercept_)
print("Coefficient is ",linear_reg.coef_)

print("Training score is ",linear_reg.score(X_train_pearson, Y_train_pearson))

print("Testing score is ",linear_reg.score(X_test_pearson, Y_test_pearson))


# In[202]:

pearson_df.int_rate.head()


# In[148]:

# percentile_df=df.copy()

# cols = percentile_df.columns
# num_cols = percentile_df._get_numeric_data().columns

# list_of_categorical_data=list(set(cols) - set(num_cols))

# print(list_of_categorical_data)
# percentile_df[list_of_categorical_data]=dummyEncode(percentile_df[list_of_categorical_data])


# cols1 = percentile_df.columns
# num_cols1 = percentile_df._get_numeric_data().columns

# list_of_categorical_data1=list(set(cols1) - set(num_cols1))
# print(list_of_categorical_data1)


# In[203]:


percentile_df=df.copy()
percentile_df.ix[:, percentile_df.columns != 'int_rate']=dummyEncode(percentile_df.ix[:, percentile_df.columns != 'int_rate'])

from sklearn import feature_selection

#percentile_df=df
#percentile_df=percentile_df.dropna(how='any') 
#percentile_df[list_of_categorical_data]=dummyEncode(percentile_df[list_of_categorical_data])

X_train_percentile, X_test_percentile, Y_train_percentile, Y_test_percentile = train_test_split(percentile_df.ix[:, percentile_df.columns != 'int_rate'], percentile_df.int_rate, test_size=0.2, random_state=0)
feature_names = percentile_df.columns

fs = feature_selection.SelectPercentile(feature_selection.f_regression, percentile=20)
X_train_fs = fs.fit_transform(X_train_percentile, Y_train_percentile)

# print ('All features:', feature_names)
# print ('Scores of these features:', fs.scores_)
print ('***Features sorted by score:', [feature_names[i] for i in np.argsort(fs.scores_)[::-1]])
# print ('Peeking into first few samples (before and after):')
# print (X_train_percentile[:10])
# print (X_train_fs[:10])


# In[205]:


percentile_df=percentile_df[['grade', 'total_pymnt_inv', 'revol_util', 'loan_status', 'fico_range_grade', 'total_rec_prncp', 'revol_bal', 'grade_based_on_inq_last_6mths', 'acc_open_past_24mths', 'installment', 'last_pymnt_amnt', 'funded_amnt_inv', 'total_acc', 'credit_age', 'issue_d', 'annual_inc', 'meanfico','int_rate']]
#pearson_df=pearson_df.dropna(how='any') 
#percentile_df=dummyEncode(percentile_df)

#X_train=df
#random split method for creating the training and test splits
X_train_percentile, X_test_percentile, Y_train_percentile, Y_test_percentile = train_test_split(percentile_df.ix[:, percentile_df.columns != 'int_rate'], percentile_df.int_rate, test_size=0.2, random_state=0)

print(X_train_percentile.columns)
print(X_test_percentile.columns)
print(Y_train_percentile.head(2))
print(Y_test_percentile.head(2))

print("Starting Linear Regression algorithm")
linear_reg = LinearRegression()
fit=linear_reg.fit(X_train_percentile, Y_train_percentile)

print ("Intercept is ",linear_reg.intercept_)
print("Coefficient is ",linear_reg.coef_)
#print(lm.predict([18,3,0,4]))
print("Training score is ",linear_reg.score(X_train_percentile, Y_train_percentile))

#np.mean((linear_reg.predict(X_test)-Y_test)**2)
print("Testing score is ",linear_reg.score(X_test_percentile, Y_test_percentile))


# In[207]:

from sklearn.linear_model import RandomizedLasso
lasso_df=df.copy()

#lasso_df=dummyEncode(lasso_df)
X=lasso_df.ix[:, lasso_df.columns != 'int_rate']
X=dummyEncode(X)
Y=lasso_df.int_rate

rlasso = RandomizedLasso(alpha='bic', verbose=False, n_resampling=50, random_state=1001, n_jobs=1)
rlasso.fit(X, Y)
 
print( "Features sorted by their score:")
coef = pd.DataFrame(rlasso.scores_, columns = ['RandomizedLasso_score'])

print (sorted(zip(map(lambda x: round(x, 4), rlasso.scores_), X), reverse=True))


# In[208]:

lasso_df.int_rate.head(3)


# In[210]:

from sklearn.feature_selection import RFE

rfe_df=df.copy()
rfe_df.ix[:, rfe_df.columns != 'int_rate']=dummyEncode(rfe_df.ix[:, rfe_df.columns != 'int_rate'])

X_train_rfe, X_test_rfe, Y_train_rfe, Y_test_rfe = train_test_split(rfe_df.ix[:, rfe_df.columns != 'int_rate'], rfe_df.int_rate, test_size=0.2, random_state=0)

lr = LinearRegression()
#rank all features, i.e continue the elimination until the last one
rfe = RFE(lr, n_features_to_select=1)
rfe.fit(X_train_rfe,Y_train_rfe)
 
print ("Features sorted by their rank:")
print (sorted(zip(map(lambda x: round(x, 4), rfe.ranking_), X_train_rfe)))




# In[211]:

rfe_df.int_rate.head(5)


# In[212]:

# rfe_df=df.copy()


rfe_df=rfe_df[['grade','verification_status','issue_d','term','initial_list_status','grade_based_on_inq_last_6mths','collections_12_mths_ex_med','fico_range_grade','chargeoff_within_12_mths',
               'loan_status','num_tl_op_past_12m','acc_open_past_24mths','pub_rec','pub_rec_bankruptcies','purpose','meanfico','total_acc','int_rate']]
#pearson_df=pearson_df.dropna(how='any') 
#rfe_df=dummyEncode(rfe_df)

rfe_df.ix[:, rfe_df.columns != 'int_rate']=dummyEncode(rfe_df.ix[:, rfe_df.columns != 'int_rate'])

#X_train=df
#random split method for creating the training and test splits
X_train_rfe, X_test_rfe, Y_train_rfe, Y_test_rfe = train_test_split(rfe_df.ix[:, rfe_df.columns != 'int_rate'], rfe_df.int_rate, test_size=0.2, random_state=0)

# print(X_train_rfe.columns)
# print(X_test_rfe.columns)
# print(Y_train_rfe.head(10))
# print(Y_test_rfe.head(2))

print("Starting Linear Regression algorithm")
linear_reg = LinearRegression()
fit=linear_reg.fit(X_train_rfe, Y_train_rfe)

print ("Intercept is ",linear_reg.intercept_)
print("Coefficient is ",linear_reg.coef_)
#print(lm.predict([18,3,0,4]))
print("Training score is ",linear_reg.score(X_train_rfe, Y_train_rfe))

#np.mean((linear_reg.predict(X_test)-Y_test)**2)
print("Testing score is ",linear_reg.score(X_test_rfe, Y_test_rfe))


# In[240]:

# common features from RFE and Select Percentile are
# grade, loan_status, fico_range_grade, grade_based_on_inq_last_6mths, acc_open_past_24mths, total_acc, issue_d, meanfico
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

neural_network_df=df.copy()
neural_network_df=neural_network_df[['grade', 'total_pymnt_inv', 'revol_util', 'loan_status', 'fico_range_grade', 'total_rec_prncp', 'revol_bal', 'grade_based_on_inq_last_6mths', 'acc_open_past_24mths', 'installment', 'last_pymnt_amnt', 'funded_amnt_inv', 'total_acc', 'credit_age', 'issue_d', 'annual_inc', 'meanfico','int_rate']]

neural_network_df.ix[:, neural_network_df.columns != 'int_rate']=dummyEncode(neural_network_df.ix[:, neural_network_df.columns != 'int_rate'])

#neural network
print("Staring Neural Network")

X_train_nn, X_test_nn, Y_train_nn, Y_test_nn = train_test_split(neural_network_df.ix[:, neural_network_df.columns != 'int_rate'], neural_network_df.int_rate, test_size=0.2, random_state=0)


X_train_nn = StandardScaler().fit_transform(X_train_nn)
X_test_nn = StandardScaler().fit_transform(X_test_nn)

mlp = MLPRegressor(solver='lbfgs', hidden_layer_sizes=50,
                           max_iter=150, shuffle=True, random_state=1)
mlp.fit(X_train_nn, Y_train_nn)

# print(X_train_nn.columns)
# print(X_test_nn.columns)
# print(Y_train_nn.head(2))
# print(Y_test_nn.head(2))

# neural_network_reg=MLPClassifier(hidden_layer_sizes=(20,10,20))
# neural_network_reg.fit(X_train_nn,Y_train_nn)
#predictions = neural_network_reg.predict(X_test_nn)
# print("Intercept is ",mlp.intercept_)
# print("Coefficient is ",mlp.coef_)
print("Training score is ",mlp.score(X_train_nn, Y_train_nn))
print("Testing score is ",mlp.score(X_test_nn, Y_test_nn))


# In[245]:

from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score

knn_df=df.copy()
knn_df=knn_df[['grade', 'total_pymnt_inv', 'revol_util', 'loan_status', 'fico_range_grade', 'total_rec_prncp', 'revol_bal', 'grade_based_on_inq_last_6mths', 'acc_open_past_24mths', 'installment', 'last_pymnt_amnt', 'funded_amnt_inv', 'total_acc', 'credit_age', 'issue_d', 'annual_inc', 'meanfico','int_rate']]

knn_df.ix[:, knn_df.columns != 'int_rate']=dummyEncode(knn_df.ix[:, knn_df.columns != 'int_rate'])

X_train_knn, X_test_knn, Y_train_knn, Y_test_knn = train_test_split(knn_df.ix[:, knn_df.columns != 'int_rate'], knn_df.int_rate, test_size=0.2, random_state=0)


print("Starting KNN algorithm")
for K in range(12):
         K_value = K+1
         knn_reg = KNeighborsRegressor(n_neighbors = K_value, weights='uniform', algorithm='auto')
         knn_reg.fit(X_train_knn, Y_train_knn)
         y_pred = knn_reg.predict(X_test_knn)
#          print("Mean Absolute Error is ",mean_absolute_error(Y_train,y_pred),"% for K-Value:",K_value)
#          #print("Mean Absolute Percentage Error is ",mean_absolute_percentage_error(Y_train,y_pred))
#          print("Root Mean Squared Error ",np.sqrt(mean_squared_error(Y_train,y_pred)))
         print("Accuracy of the model is ",r2_score(Y_test_knn,y_pred))


# In[244]:

from sklearn.ensemble import RandomForestRegressor

random_df=df.copy()
random_df=random_df[['grade', 'total_pymnt_inv', 'revol_util', 'loan_status', 'fico_range_grade', 'total_rec_prncp', 'revol_bal', 'grade_based_on_inq_last_6mths', 'acc_open_past_24mths', 'installment', 'last_pymnt_amnt', 'funded_amnt_inv', 'total_acc', 'credit_age', 'issue_d', 'annual_inc', 'meanfico','int_rate']]

random_df.ix[:, random_df.columns != 'int_rate']=dummyEncode(knn_df.ix[:, random_df.columns != 'int_rate'])

X_train_random, X_test_random, Y_train_random, Y_test_random = train_test_split(random_df.ix[:, random_df.columns != 'int_rate'], random_df.int_rate, test_size=0.2, random_state=0)


print("Staring Random forest algorithm")
random_forest = RandomForestRegressor(n_jobs=2)
random_forest.fit(X_train_random, Y_train_random)
y_pred=random_forest.predict(X_test_random)
#predict probability of first 10 records
#print(random_forest.predict_proba(X_test)[0:10])
# print("Mean Absolute Error is ",mean_absolute_error(Y_train,y_pred))
# #print("Mean Absolute Percentage Error is ",mean_absolute_percentage_error(Y_train,y_pred))
# print("Root Mean Squared Error ",np.sqrt(mean_squared_error(Y_train,y_pred)))
print("Accuracy of the model is ",r2_score(Y_test_random,y_pred)) 

