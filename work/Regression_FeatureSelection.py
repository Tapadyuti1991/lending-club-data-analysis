
# coding: utf-8

# In[1]:


from io import StringIO
import requests
import json
import pandas as pd
import numpy as np

# @hidden_cell
# This function accesses a file in your Object Storage. The definition contains your credentials.
# You might want to remove those credentials before you share your notebook.
def get_object_storage_file_with_credentials_63f2dc1df232458db8431e5111d801de(container, filename):
    """This functions returns a StringIO object containing
    the file content from Bluemix Object Storage."""

    url1 = ''.join(['https://identity.open.softlayer.com', '/v3/auth/tokens'])
    data = {'auth': {'identity': {'methods': ['password'],
            'password': {'user': {'name': 'member_daf273ebef271a59dacfbbd2c8c1d6ce70c9b215','domain': {'id': 'bff414f8f6fe40c7a77ed050397d07db'},
            'password': 'c7,~7.bf/~HXUoRL'}}}}}
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

df= pd.read_csv(get_object_storage_file_with_credentials_63f2dc1df232458db8431e5111d801de('LendingClubcasestudy', 'Cleaned_and_featured_engineered_accepted_data.csv'))
df.head()



# In[2]:

df=df.drop(df.columns[0], axis=1)
df.head(3)


# In[3]:

#Compute the corelation between the features to determine the relationship between all the features
correlations_technique1 = df.corr(method='pearson')
correlations_technique1.ix[6:7,0:14]


# In[4]:

#Compute the corelation between the features to determine the relationship between all the features
correlations_technique1.ix[6:7,14:26]


# In[5]:

#Compute the corelation between the features to determine the relationship between all the features
correlations_technique1.ix[6:7,26:36]


# In[6]:

#Compute the corelation between the features to determine the relationship between all the features
correlations_technique1.ix[6:7,36:47]


# In[7]:

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


# In[8]:

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression



#my_list=['term','revol_util','total_rec_int','meanfico','int_rate']
pearson_df=df[['term','revol_util','total_rec_int','meanfico','int_rate']]

pearson_df=pearson_df.dropna(how='any') 
pearson_df=dummyEncode(pearson_df)

#X_train=df
#random split method for creating the training and test splits
X_train_pearson, X_test_pearson, Y_train_pearson, Y_test_pearson = train_test_split(pearson_df.ix[:, pearson_df.columns != 'int_rate'], pearson_df.int_rate, test_size=0.2, random_state=0)

print("Starting Linear Regression algorithm")
linear_reg = LinearRegression()
fit=linear_reg.fit(X_train_pearson, Y_train_pearson)

print ("Intercept is ",linear_reg.intercept_)
print("Coefficient is ",linear_reg.coef_)
#print(lm.predict([18,3,0,4]))
print("Training score is ",linear_reg.score(X_train_pearson, Y_train_pearson))

#np.mean((linear_reg.predict(X_test)-Y_test)**2)
print("Testing score is ",linear_reg.score(X_test_pearson, Y_test_pearson))


# In[9]:

from sklearn import feature_selection

percentile_df=df
percentile_df=percentile_df.dropna(how='any') 
percentile_df=dummyEncode(percentile_df)

X_train_percentile, X_test_percentile, Y_train_percentile, Y_test_percentile = train_test_split(percentile_df.ix[:, percentile_df.columns != 'int_rate'], percentile_df.int_rate, test_size=0.2, random_state=0)
feature_names = percentile_df.columns

fs = feature_selection.SelectPercentile(feature_selection.chi2, percentile=20)
X_train_fs = fs.fit_transform(X_train_percentile, Y_train_percentile)

print ('All features:', feature_names)
print ('Scores of these features:', fs.scores_)
print ('***Features sorted by score:', [feature_names[i] for i in np.argsort(fs.scores_)[::-1]])
print ('Peeking into first few samples (before and after):')
print (X_train_percentile[:10])
print (X_train_fs[:10])


# In[12]:


lasso_df=df

del lasso_df['last_pymnt_d']

del lasso_df['next_pymnt_d']


# In[13]:

from sklearn.linear_model import RandomizedLasso
lasso_df=df

lasso_df=dummyEncode(lasso_df)
X=lasso_df.ix[:, lasso_df.columns != 'int_rate']
Y=lasso_df.int_rate

rlasso = RandomizedLasso(alpha=0.025)
rlasso.fit(X, Y)
 
print( "Features sorted by their score:")
print (sorted(zip(map(lambda x: round(x, 4), rlasso.scores_), 
                 names), reverse=True))


# In[92]:

df.columns


# In[37]:

from sklearn.decomposition import PCA

pca = PCA(n_components=4)
fit = pca.fit(X_train)
print(fit.components_)

