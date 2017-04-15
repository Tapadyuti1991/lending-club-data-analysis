
# coding: utf-8

# In[1]:

from io import StringIO
import requests
import json
import pandas as pd

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

grade_df_1 = pd.read_csv(get_object_storage_file_with_credentials_b6d2dc4304df42d5bf425b6ca8af67ff('LendingClub', 'Manual_Grade_Cluster_0.csv'))
# print(len(grade_df_1))

grade_df_2 = pd.read_csv(get_object_storage_file_with_credentials_b6d2dc4304df42d5bf425b6ca8af67ff('LendingClub', 'Manual_Grade_Cluster_1.csv'))
# print(len(grade_df_2))

grade_df_3 = pd.read_csv(get_object_storage_file_with_credentials_b6d2dc4304df42d5bf425b6ca8af67ff('LendingClub', 'Manual_Grade_Cluster_2.csv'))
# print(len(grade_df_3))

grade_df_4 = pd.read_csv(get_object_storage_file_with_credentials_b6d2dc4304df42d5bf425b6ca8af67ff('LendingClub', 'Manual_Grade_Cluster_3.csv'))
# print(len(grade_df_4))

grade_df_5 = pd.read_csv(get_object_storage_file_with_credentials_b6d2dc4304df42d5bf425b6ca8af67ff('LendingClub', 'Manual_Grade_Cluster_4.csv'))
# print(len(grade_df_5))

grade_df_6 = pd.read_csv(get_object_storage_file_with_credentials_b6d2dc4304df42d5bf425b6ca8af67ff('LendingClub', 'Manual_Grade_Cluster_5.csv'))
# print(len(grade_df_6))

grade_df_7 = pd.read_csv(get_object_storage_file_with_credentials_b6d2dc4304df42d5bf425b6ca8af67ff('LendingClub', 'Manual_Grade_Cluster_6.csv'))
# print(len(grade_df_7))


# In[2]:

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


# In[3]:

grade_df_list=[grade_df_1,grade_df_2,grade_df_3,grade_df_4,grade_df_5,grade_df_6,grade_df_7]


# In[4]:

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

for i in grade_df_list:
    
#     df_lr=i[['total_pymnt_inv', 'revol_util', 'loan_status', 'fico_range_grade', 'total_rec_prncp', 'revol_bal', 'grade_based_on_inq_last_6mths', 'acc_open_past_24mths', 'installment', 'last_pymnt_amnt', 'funded_amnt_inv', 'total_acc', 'credit_age', 'issue_d', 'annual_inc', 'meanfico','int_rate']]
    df_lr=i
    df_lr.ix[:, df_lr.columns != 'int_rate']=dummyEncode(df_lr.ix[:, df_lr.columns != 'int_rate'])
    X_train_lr_df, X_test_lr_df, Y_train_lr_df, Y_test_lr_df = train_test_split(df_lr.ix[:, df_lr.columns != 'int_rate'], df_lr.int_rate, test_size=0.2, random_state=0)
    print("Starting Linear Regression algorithm")
    linear_reg = LinearRegression()
    fit=linear_reg.fit(X_train_lr_df, Y_train_lr_df)

    print ("Intercept is ",linear_reg.intercept_)
    print("Coefficient is ",linear_reg.coef_)
    
    print("Training score is ",linear_reg.score(X_train_lr_df, Y_train_lr_df))

    print("Testing score is ",linear_reg.score(X_test_lr_df, Y_test_lr_df))


# In[5]:

from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor

for i in grade_df_list:
    
#     ran_for_df=i[['total_pymnt_inv', 'revol_util', 'loan_status', 'fico_range_grade', 'total_rec_prncp', 'revol_bal', 'grade_based_on_inq_last_6mths', 'acc_open_past_24mths', 'installment', 'last_pymnt_amnt', 'funded_amnt_inv', 'total_acc', 'credit_age', 'issue_d', 'annual_inc', 'meanfico','int_rate']]
    ran_for_df=i
    ran_for_df.ix[:, ran_for_df.columns != 'int_rate']=dummyEncode(ran_for_df.ix[:, ran_for_df.columns != 'int_rate'])

    X_train_ran_for, X_test_ran_for, Y_train_ran_for, Y_test_ran_for = train_test_split(ran_for_df.ix[:, ran_for_df.columns != 'int_rate'], ran_for_df.int_rate, test_size=0.2, random_state=0)

    print("Staring Random forest algorithm")
    random_forest = RandomForestRegressor(n_jobs=2)
    random_forest.fit(X_train_ran_for, Y_train_ran_for)
    y_pred=random_forest.predict(X_test_ran_for)
    print("Accuracy of the model is ",r2_score(Y_test_ran_for,y_pred))


# In[6]:

from sklearn.neighbors import KNeighborsRegressor

for i in grade_df_list:

#     knn_df=i[['total_pymnt_inv', 'revol_util', 'loan_status', 'fico_range_grade', 'total_rec_prncp', 'revol_bal', 'grade_based_on_inq_last_6mths', 'acc_open_past_24mths', 'installment', 'last_pymnt_amnt', 'funded_amnt_inv', 'total_acc', 'credit_age', 'issue_d', 'annual_inc', 'meanfico','int_rate']]
    knn_df=i
    knn_df.ix[:, knn_df.columns != 'int_rate']=dummyEncode(knn_df.ix[:, knn_df.columns != 'int_rate'])

    X_train_knn, X_test_knn, Y_train_knn, Y_test_knn = train_test_split(knn_df.ix[:, knn_df.columns != 'int_rate'], knn_df.int_rate, test_size=0.2, random_state=0)

    print("Starting KNN algorithm")
    for K in range(12):
         K_value = K+1
         knn_reg = KNeighborsRegressor(n_neighbors = K_value, weights='uniform', algorithm='auto')
         knn_reg.fit(X_train_knn, Y_train_knn)
         y_pred = knn_reg.predict(X_test_knn)
         print("Accuracy of the model is ",r2_score(Y_test_knn,y_pred))


# In[7]:

from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

for i in grade_df_list:
#     neural_network_df=i[['total_pymnt_inv', 'revol_util', 'loan_status', 'fico_range_grade', 'total_rec_prncp', 'revol_bal', 'grade_based_on_inq_last_6mths', 'acc_open_past_24mths', 'installment', 'last_pymnt_amnt', 'funded_amnt_inv', 'total_acc', 'credit_age', 'issue_d', 'annual_inc', 'meanfico','int_rate']]
    neural_network_df=i
    neural_network_df.ix[:, neural_network_df.columns != 'int_rate']=dummyEncode(neural_network_df.ix[:, neural_network_df.columns != 'int_rate'])

    #neural network
    print("Staring Neural Network")

    X_train_nn, X_test_nn, Y_train_nn, Y_test_nn = train_test_split(neural_network_df.ix[:, neural_network_df.columns != 'int_rate'], neural_network_df.int_rate, test_size=0.2, random_state=0)


    X_train_nn = StandardScaler().fit_transform(X_train_nn)
    X_test_nn = StandardScaler().fit_transform(X_test_nn)

    mlp = MLPRegressor(solver='lbfgs', hidden_layer_sizes=50,
                               max_iter=150, shuffle=True, random_state=1)
    mlp.fit(X_train_nn, Y_train_nn)

    print("Training score is ",mlp.score(X_train_nn, Y_train_nn))
    print("Testing score is ",mlp.score(X_test_nn, Y_test_nn))

