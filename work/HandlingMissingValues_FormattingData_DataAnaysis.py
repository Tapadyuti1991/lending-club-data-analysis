
# coding: utf-8

# In[114]:

import numpy as np
import pandas as pd
#pip install seaborn 
import seaborn as sns
get_ipython().magic('matplotlib inline')
import math


# In[115]:

df = pd.read_csv("Data/LoanStats3a_securev1.csv",skiprows=1)
#if more than 50% values in an observation is NAN drop that observation
half_count = len(df.columns) / 2
df=df.dropna(axis='columns', how='all')

df = df.dropna(thresh=half_count)


# In[116]:

df.ix[:5,:7]


# In[117]:

#work on every feature slice-by-slice which one's are informative. We would drop some useless attributes and clean-up/modify others.
# .ix[row slice, column slice]
#df.ix[:4,:7]

# We won't need id or member_id as it has no real predictive power so we can drop them from this table
df=df.drop(['id','member_id'],1)

# drop the record if loan_amnt, funded_amnt is missing
df.loan_amnt=df.loan_amnt.dropna()
df.funded_amnt=df.funded_amnt.dropna()

# if the funded_amnt_inv is missing replace it with 
df.funded_amnt_inv=df.funded_amnt_inv.fillna(0)


# In[118]:


#int_rate was loaded as an object data type instead of float due to the '%' character. Let's strip that out and convert the column type.
df.int_rate = pd.Series(df.int_rate).str.replace('%', '').astype(float)

#replace missing values for Interest Rate with mean value
df.int_rate=df.int_rate.fillna(float(df.int_rate.mean()))


# In[119]:


#term was loaded as an object data type instead of int due to the ' months' character. Let's strip that out and convert the column type.
df.term=pd.Series(df.term).str.replace(' months', '')

#replace missing values for Term with max value
df.term=df.term.fillna(int(df['term'].value_counts().idxmax()))


# In[120]:

df.ix[:5,8:15]


# In[121]:

#get the total number of value and unique values, total values are 42538 and unique values are 30660
df.emp_title.shape
df.emp_title.unique().shape

#replace missing values for emp_title with Not available
df.emp_title=df.emp_title.fillna("Not available")


# In[122]:


#replacing missing values with 0
df.emp_length.replace('n/a', np.nan,inplace=True)
df.emp_length.fillna(value=0,inplace=True)

#convert categorical value into numerical value
df['emp_length'].replace(to_replace='[^0-9]+', value='', inplace=True, regex=True)
df['emp_length'] = df['emp_length'].astype(int)


# In[123]:

#replace missing values for verification_status with Not verified
df.verification_status=df.verification_status.fillna("Not verified")


# In[124]:

#replace missing values for home_ownership with max value
df.home_ownership=df.home_ownership.fillna("OTHER")

# drop the record if the annual_inc value is missing 
df.annual_inc=df.annual_inc.dropna()

#replace missing values for issue_d with Not available
df.issue_d=df.issue_d.fillna("Not available")

#replace missing values for loan_status with Not available
df.loan_status=df.loan_status.fillna("Not available")


# In[125]:

df.ix[:5,15:21]


# In[126]:

#these four fields would not provide any important informaation thus we are dropping them
df.drop(['pymnt_plan','url','desc','title','zip_code' ],1, inplace=True)


# In[127]:


print(df.purpose.value_counts())

#replace missing values for loan_status with Not available
df.purpose=df.purpose.fillna("Not available")


# In[128]:

df.ix[:5,17:25]


# In[129]:

#replace missing values for loan_status with Not available
df.addr_state=df.addr_state.fillna("Not available")


# In[130]:

#replace missing values for loan_status with Not available
df.delinq_2yrs=df.delinq_2yrs.fillna(0)


# In[18]:



#from datetime import datetime

#df.earliest_cr_line = pd.to_datetime(df.earliest_cr_line)

#dttoday = datetime.now().strftime('%Y-%m-%d')
# There is a better way to do this :) 
#df.earliest_cr_line = df.earliest_cr_line.apply(lambda x: (
 #       np.timedelta64((x - pd.Timestamp(dttoday)),'D').astype(int))/-365)

#df.earliest_cr_line"""



# In[131]:

# drop the record if the fico_range_high and fico_range_low value is missing 
df.fico_range_low=df.fico_range_low.dropna()
df.fico_range_high=df.fico_range_high.dropna()


#FICO fico_range_low & fico_range_high scores on their own aren't as useful as a range thus we are considering its average
df['fico_range'] = df.fico_range_low.astype('str') + '-' + df.fico_range_high.astype('str')
df['meanfico'] = (df.fico_range_low + df.fico_range_high)/2
# drop the features that are not relevant
df.drop(['fico_range_low','fico_range_high','initial_list_status', 'mths_since_last_delinq','mths_since_last_record','pub_rec','open_acc'],1, inplace=True)


# In[132]:

#replace missing values for inq_last_6mths with 0
df.inq_last_6mths=df.inq_last_6mths.fillna(0)

df.ix[:10,17:25]


# In[21]:

#dti and open_acc is yet to be taken care @@@@


# In[133]:

df.ix[:10,25:35]


# In[134]:

#replace missing values for revol_bal with 0
df.revol_bal=df.revol_bal.fillna(0)

#replace missing values for revol_util with 0
df.revol_util=df.revol_util.fillna(0)

#replace missing values for total_acc with 0
df.total_acc=df.total_acc.fillna(0)


#revol_util was loaded as an object data type instead of float due to the '%' character. Let's strip that out and convert the column type.
df.revol_util = pd.Series(df.revol_util).str.replace('%', '').astype(float)



# In[135]:

#on checking the value count we see that majority portion of data is inclined towards one value thus these columns do not provide any relevant information, thus we are dropping the columns

print(df.out_prncp_inv.value_counts())
print(df.out_prncp.value_counts())

df.drop(['out_prncp_inv','out_prncp'],1, inplace=True)


# In[136]:

#total_pymnt, total_pymnt_inv, total_rec_prncp, total_rec_int, total_rec_late_fee are not relevant in calculating the interest rate of the user, thus dropping them

df.drop(['total_pymnt','total_pymnt_inv', 'total_rec_prncp', 'total_rec_int', 'total_rec_late_fee','recoveries','collection_recovery_fee','next_pymnt_d','last_credit_pull_d'],1, inplace=True)


# In[137]:

df.ix[:5,25:45]


# In[138]:

#calculating the last mean fico score
df['last_fico_range'] = df.last_fico_range_low.astype('str') + '-' + df.last_fico_range_high.astype('str')
df['last_meanfico'] = (df.last_fico_range_low + df.last_fico_range_high)/2
df.drop(['last_fico_range_high','last_fico_range_low','policy_code'],1, inplace=True)


# In[139]:

#since the value count indicate majority of the data has just one value, we are dropping the column
print(df.collections_12_mths_ex_med.value_counts())
print(df.application_type.value_counts())
print(df.acc_now_delinq.value_counts())
print(df.chargeoff_within_12_mths.value_counts())
print(df.delinq_amnt.value_counts())
print(df.pub_rec_bankruptcies.value_counts())
print(df.tax_liens.value_counts())

df.drop(['acc_now_delinq','chargeoff_within_12_mths','delinq_amnt','pub_rec_bankruptcies','tax_liens','application_type','collections_12_mths_ex_med'],1, inplace=True)
#since the highest and lowest fico score is already considered, we can drop this field
df.drop(['fico_range', 'last_fico_range'],1, inplace=True)


# In[141]:

#after carefully examining each field we have shortlisted 38 features listed below

print(df.columns)
df.head(5)


# In[142]:

#alter the dtypes of the column
df.loan_amnt  =df.loan_amnt.astype(int)
df.funded_amnt  =df.funded_amnt.astype(int)
df.annual_inc  =df.annual_inc.astype(int)
df.delinq_2yrs  =df.delinq_2yrs.astype(int)
df.inq_last_6mths  =df.inq_last_6mths.astype(int)
df.revol_bal  =df.revol_bal.astype(int)
df.total_acc  =df.total_acc.astype(int)
df.meanfico  =df.meanfico.astype(int)
df.last_meanfico  =df.last_meanfico.astype(int)
  
#math.ceil(i*100)/100
ceil_function= lambda x: math.ceil(x*100)/100
df['funded_amnt_inv']=df['funded_amnt_inv'].apply(ceil_function)


# In[143]:


from sklearn.preprocessing import LabelEncoder
#using label encoder to convert categorical columns into numeric values
def dummyEncode(df):
        columnsToEncode = list(df.select_dtypes(include=['category','object']))
        le = LabelEncoder()
        for feature in columnsToEncode:
            #try:
                df[feature] = le.fit_transform(df[feature])
            #except:
             #   print('Error encoding '+feature)
        return df


# In[146]:


cols = df.columns
#getting the list of features that are numeric
num_cols_list = df._get_numeric_data().columns

#getting the list of features that are categorical
cat_cols_list=list(set(cols) - set(num_cols_list))
#print(df[cat_cols_list])

#print("Next one")
#print(df[num_cols_list])
#X=df[num_cols_list].ix[:, df[num_cols_list].columns != 'int_rate']


df[cat_cols_list]=dummyEncode(df[cat_cols_list])



X=df.ix[:, df.columns != 'int_rate']
Y=df.int_rate

X=X.as_matrix()
Y=Y.as_matrix()

#Describe each features distribution  @@@ uncomment this later
#print(df.describe())

#Compute the corelation between the features to determine the relationship between all the features
correlations = df.corr(method='pearson')
#print(correlations.ix[4:5,25:35])

new_df= pd.read_csv("Data/LoanStats3a_securev1.csv",skiprows=1)
new_df=new_df.dropna(axis='columns', how='all')
new_df = new_df.dropna()
new_df=dummyEncode(new_df)

correlations2 = new_df.corr(method='pearson')
correlations2.ix[6:7,59:65]



# In[33]:

print(df.loan_status    .dtypes)
print(new_df.loan_status    .dtypes)

print(df.loan_status    .head(5))
print(new_df.loan_status    .head(5))


# In[34]:

# #@@@not working

# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2
# feature_test = SelectKBest(score_func=chi2, k=4)

# fit = feature_test.fit(X, Y)

# print("Selected Features: %s") % fit.support_


# In[147]:

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
knn = KNeighborsClassifier(n_neighbors=4)
lr = LinearRegression()
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs

lr = LinearRegression()

sfs = SFS(lr, 
          k_features=13, 
          forward=True, 
          floating=False, 
          scoring='neg_mean_squared_error',
          cv=10)

sfs = sfs.fit(X, Y)
fig = plot_sfs(sfs.get_metric_dict(), kind='std_err')

plt.title('Sequential Forward Selection (w. StdErr)')
plt.grid()
plt.show()



# In[148]:

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
#Funded_amt_inv
#Term
#Grade
#Subgrade
#Dti
#Delinq_2_yrs
#Total_payment_inv
#Total_rec_int


# new_df= pd.read_csv("Data/LoanStats3a_securev1.csv",skiprows=1)
# new_df=new_df.dropna(axis='columns', how='all')
# new_df = new_df.dropna()
# new_df=dummyEncode(new_df)

#Y_train=df.int_rate
my_list=['loan_amnt','funded_amnt_inv','term','grade','sub_grade','verification_status','revol_util']

#X_train=df
#random split method for creating the training and test splits
X_train, X_test, Y_train, Y_test = train_test_split(df.ix[:, df.columns != 'int_rate'], df.int_rate, test_size=0.2, random_state=0)

print(len(df))
print(len(Y_train))

print(len(X_test))
print(len(Y_test))


# In[149]:

from sklearn.model_selection import cross_val_score
from sklearn import cross_validation

print("Starting Linear Regression algorithm")
linear_reg = LinearRegression()
fit=linear_reg.fit(X_train, Y_train)

print ("Intercept is ",linear_reg.intercept_)
print("Coefficient is ",linear_reg.coef_)
#print(lm.predict([18,3,0,4]))
print("Training score is ",linear_reg.score(X_train, Y_train))

#np.mean((linear_reg.predict(X_test)-Y_test)**2)
print("Testing score is ",linear_reg.score(X_test, Y_test))

train_scores = cross_val_score(fit, df.ix[:, df.columns != 'int_rate'], df.int_rate, cv=10)
print(train_scores)

#Simple K-Fold cross validation. 10 folds.
print(X_train.shape)
cv = cross_validation.KFold(len(X_train), n_folds=10)

results = []


# X_train=X_train.as_matrix()
# Y_train=Y_train.as_matrix()

# "Error_function" can be replaced by the error function of your analysis
for traincv, testcv in cv:
        print(X_train[800])
        probas = linear_reg.fit(X_train[traincv], Y_train[traincv])
        #results.append( Error_function )
        
print ("Results: " + str( np.array(probas).mean() ))


