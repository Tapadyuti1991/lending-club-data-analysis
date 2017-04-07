
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
#pip install seaborn 
import seaborn as sns
get_ipython().magic('matplotlib inline')
import math

from datetime import datetime


# In[2]:

print("Start downloading data")
df = pd.read_csv("Data/LoanStats3a_securev1.csv",skiprows=1)
#if more than 50% values in an observation is NAN drop that observation
half_count = len(df.columns) / 2
df=df.dropna(axis='columns', how='all')
df = df.dropna(thresh=half_count)
print(df.shape)


# In[3]:

print("Clean and Analyse the slice of data column 1-7")
df.ix[:5,:7]


# In[4]:

# drop the record if value is NaN and convert them in suitable types
df.id=df.id.dropna()
df.id=df.id.astype(int)
df.member_id=df.member_id.dropna()
df.member_id=df.member_id.astype(int)
df.loan_amnt=df.loan_amnt.dropna()
df.loan_amnt=df.loan_amnt.astype(int)
df.funded_amnt=df.funded_amnt.dropna()
df.funded_amnt=df.funded_amnt.astype(int)
df.funded_amnt_inv=df.funded_amnt_inv.dropna()
df.funded_amnt_inv=df.funded_amnt_inv.astype(int)

#term was loaded as an object data type instead of int due to the ' months' character. Let's strip that out and convert the column type.
df.term=pd.Series(df.term).str.replace(' months', '')

#replace missing values for Term with max value
df.term=df.term.fillna(int(df['term'].value_counts().idxmax()))

#int_rate was loaded as an object data type instead of float due to the '%' character. Let's strip that out and convert the column type.
df.int_rate = pd.Series(df.int_rate).str.replace('%', '').astype(float)

#replace missing values for Interest Rate with mean value
df.int_rate=df.int_rate.fillna(float(df.int_rate.mean()))


# In[5]:

df.ix[:5,:7]


# In[6]:

print("Clean and Analyse the slice of data column 8-15")
df.ix[:5,8:15]


# In[7]:

#replace missing values for grade, sub_grade with max value
df.grade=df.grade.fillna(int(df['term'].value_counts().idxmax()))
df.sub_grade=df.sub_grade.fillna(int(df['term'].value_counts().idxmax()))
#replace missing values for emp_title with Not available
df.emp_title=df.emp_title.fillna("Not available")

#replacing missing values with 0
df.emp_length.replace('n/a', np.nan,inplace=True)
df.emp_length.fillna(value=0,inplace=True)

#convert categorical value into numerical value
df['emp_length'].replace(to_replace='[^0-9]+', value='', inplace=True, regex=True)
df['emp_length'] = df['emp_length'].astype(int)

#replace missing values for home_ownership with max value
df.home_ownership=df.home_ownership.fillna("OTHER")

# drop the record if the annual_inc value is missing 
df.annual_inc=df.annual_inc.dropna()
df.annual_inc=df.annual_inc.astype(int)


# In[8]:

df.ix[:5,8:15]


# In[9]:

print("Clean and Analyse the slice of data column 15-21")
df.ix[:5,15:21]


# In[10]:

#replace missing values for issue_d with Not available
df.issue_d=df.issue_d.fillna(df['issue_d'].value_counts().idxmax())

df.issue_d = pd.to_datetime(df.issue_d)
#@@@ LOOK INTO THIS!!!
# dttoday = datetime.now().strftime('%Y-%m-%d')
# # There is a better way to do this :) 
# df.issue_d = df.issue_d.apply(lambda x: (
#         np.timedelta64((x - pd.Timestamp(dttoday)),'D').astype(int))/-365)

# print(df.issue_d)

#replace missing values for loan_status with Not available
df.loan_status=df.loan_status.fillna("Not available")

#replace missing values for pymnt_plan with max value
df.pymnt_plan=df.pymnt_plan.fillna(df['pymnt_plan'].value_counts().idxmax())

#replace missing values for url, desc with Not available
df.url=df.url.fillna("Not available")
df.desc=df.desc.fillna("Not available")
#replace missing values for loan_status with Not available
df.purpose=df.purpose.fillna("other")


# In[11]:

df.ix[:5,15:21]


# In[12]:

print("Clean and Analyse the slice of data column 21-30")
df.ix[:5,21:30]


# In[13]:

#replace missing values for title with Not available
df.title=df.title.fillna("Not available")
#zipcode 000 is not in use
df.title=df.title.fillna("000")
df.zip_code=df.zip_code.astype(str)

#stripping the last two characters and fetching the first three digits of the zipcode
df.zip_code=df.zip_code.map(lambda x: x[:3]).astype(int)

#replace missing values for addr_state with XX (random characters)
df.addr_state=df.addr_state.fillna("XX")

#drop the record if the value of dti is missing 
df.dti=df.dti.dropna()
df.dti=df.dti.astype(float)

#replace missing values for delinq_2yrs with max value count
df.delinq_2yrs=df.delinq_2yrs.fillna(df['delinq_2yrs'].value_counts().idxmax()).astype(int)

#earliest_cr_line@@@@@ remaining same logic as issue_d

#replace missing values for inq_last_6mths with 0
df.inq_last_6mths=df.inq_last_6mths.fillna(0).astype(int)


# In[14]:

# drop the record if the fico_range_high and fico_range_low value is missing 
df.fico_range_low=df.fico_range_low.dropna()
df.fico_range_high=df.fico_range_high.dropna()
df.fico_range_low=df.fico_range_low.astype(int)
df.fico_range_high=df.fico_range_high.astype(int)

#FICO fico_range_low & fico_range_high scores on their own aren't as useful as a range thus we are considering its average
df['fico_range'] = df.fico_range_low.astype('str') + '-' + df.fico_range_high.astype('str')
print("Craeting the FICO range bucket")
print("Calculating the new feature MeanFICO which is the average of low and high fico score and adding this column to the dataframe")
df['meanfico'] = (df.fico_range_low + df.fico_range_high)/2
df['meanfico'] =df['meanfico'].astype(int)
df[['fico_range_low','fico_range_high','fico_range','meanfico']].head(3)


# In[15]:

df.ix[:5,21:30]


# In[16]:

print("Clean and Analyse the slice of data column 30-39")
df.ix[:5,30:39]


# In[17]:

#replace missing values for mths_since_last_delinq with 0
df.mths_since_last_delinq=df.mths_since_last_delinq.fillna(0).astype(int)

#replace missing values for mths_since_last_record with 0
df.mths_since_last_record=df.mths_since_last_record.fillna(0).astype(int)

#replace missing values for mths_since_last_record with 0
df.open_acc=df.open_acc.fillna(df['open_acc'].mean()).astype(int)

#replace missing values for Term with max value
df.pub_rec=df.pub_rec.fillna(df['pub_rec'].value_counts().idxmax()).astype(int)

#replace missing values for mths_since_last_delinq with 0
df.revol_bal=df.revol_bal.dropna().astype(int)

#replace missing values for revol_util with 0
df.revol_util=df.revol_util.dropna()

#revol_util was loaded as an object data type instead of float due to the '%' character. Let's strip that out and convert the column type.
df.revol_util = pd.Series(df.revol_util).str.replace('%', '').astype(float)

#replace missing values for total_acc with 0
df.total_acc=df.total_acc.fillna(df['total_acc'].mean()).astype(int)

#replace missing values for initial_list_status with max value
df.initial_list_status=df.initial_list_status.fillna(df['initial_list_status'].value_counts().idxmax())

#replace missing values for out_prncp with max value
df.out_prncp=df.out_prncp.fillna(df['out_prncp'].value_counts().idxmax()).astype(int)

df.ix[:5,30:39]


# In[19]:

print("Clean and Analyse the slice of data column 39-47")
df.ix[:5,39:47]


# In[31]:

#replace missing values for out_prncp_inv with max value
df.out_prncp_inv=df.out_prncp_inv.fillna(df['out_prncp_inv'].value_counts().idxmax()).astype(int)

#replace missing values for out_prncp_inv with max value
df.total_pymnt=df.total_pymnt.fillna(0).astype(float)
df.total_rec_prncp=df.total_rec_prncp.fillna(0).astype(float)
df.total_rec_late_fee=df.total_rec_late_fee.fillna(0).astype(float)
df.recoveries=df.recoveries.fillna(0).astype(float)
df.collection_recovery_fee=df.collection_recovery_fee.fillna(0).astype(float)

df['total_pymnt']=df['total_pymnt'].apply(ceil_function)
df['total_rec_prncp']=df['total_rec_prncp'].apply(ceil_function)
df['total_rec_late_fee']=df['total_rec_late_fee'].apply(ceil_function)
df['recoveries']=df['recoveries'].apply(ceil_function)
df['collection_recovery_fee']=df['collection_recovery_fee'].apply(ceil_function)


df.ix[:5,39:47]


# In[35]:

print("Clean and Analyse the slice of data column 47-54")
df.ix[:5,47:54]


# In[45]:

#last_pymnt_d/next_pymnt_d/last_credit_pull_d @@@@@@@ same as issue_d

df.last_pymnt_amnt=df.last_pymnt_amnt.fillna(0).astype(float)
df['last_pymnt_amnt']=df['last_pymnt_amnt'].apply(ceil_function)

#dropping the records where the last_fico_range_high or last_fico_range_low are NaN
df.last_fico_range_high=df.last_fico_range_high.dropna(0)
df.last_fico_range_high=df.last_fico_range_high.dropna(0)
df['last_fico_range_high']=df['last_fico_range_high'].astype(int)
df['last_fico_range_low']=df['last_fico_range_low'].astype(int)

#calculating the last mean fico score and adding the new column last_meanfico and also computed the last_fico_range
df['last_fico_range'] = df.last_fico_range_low.astype('str') + '-' + df.last_fico_range_high.astype('str')
df['last_meanfico'] = ((df.last_fico_range_low + df.last_fico_range_high)/2).astype(int)

df.collections_12_mths_ex_med=df.collections_12_mths_ex_med.fillna((df['collections_12_mths_ex_med'].value_counts().idxmax())).astype(int)

df[['last_fico_range_high','last_fico_range_low','last_fico_range','last_meanfico']].head(3)


# In[46]:

df.ix[:5,47:54]


# In[57]:

print("Clean and Analyse the slice of data column 54-62")
df.ix[:5,54:61]


# In[58]:

df.policy_code=df.policy_code.fillna((df['policy_code'].value_counts().idxmax())).astype(int)
df.application_type=df.application_type.fillna((df['application_type'].value_counts().idxmax()))
df.acc_now_delinq=df.acc_now_delinq.fillna((df['acc_now_delinq'].value_counts().idxmax())).astype(int)
df.chargeoff_within_12_mths=df.chargeoff_within_12_mths.fillna((df['chargeoff_within_12_mths'].value_counts().idxmax())).astype(int)
df.delinq_amnt=df.delinq_amnt.fillna((df['delinq_amnt'].value_counts().idxmax())).astype(int)
df.pub_rec_bankruptcies=df.pub_rec_bankruptcies.fillna((df['pub_rec_bankruptcies'].value_counts().idxmax())).astype(int)
df.tax_liens=df.tax_liens.fillna((df['tax_liens'].value_counts().idxmax())).astype(int)

df.ix[:5,54:61]

