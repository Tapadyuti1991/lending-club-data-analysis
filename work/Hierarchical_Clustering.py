
# coding: utf-8

# In[2]:

import pandas as pd


# In[3]:

df = pd.read_csv('accepted_merged_final.csv',low_memory=False, encoding='cp1252')
#df with all na's replaced with max and most unwanted columns removed
print("CSV loaded..")
print(df.ix[:5,:10])


# In[116]:

#Hierarchical clustering
from sklearn.cluster import AgglomerativeClustering

import datetime

from sklearn.utils import shuffle
shuffled_df = shuffle(df) #df_normalized
print("CSV shuffled..")
print(shuffled_df.head())


# In[ ]:

# Slice of data for now
# shuffled_df = shuffled_df.head(1000)
# shuffled_df


# In[118]:

#using label encoder to convert categorical columns into numeric values
def dummyEncode(df):
        columnsToEncode = list(df.select_dtypes(include=['category','object']))
        le = LabelEncoder()
        for feature in columnsToEncode:
            try:
                if feature!='Deliquency':
                    df[feature] = le.fit_transform(df[feature])
                else:
                    print('Hello')
                    df[feature] = df[feature]
            except:
                print('Error encoding '+feature)
        return df


# In[ ]:

from sklearn.preprocessing import LabelEncoder
# columns = ['Amount_Requested','Loan_Title','Risk_Score','Debt-To-Income_Ratio','Zip_Code','Employment_Length','Policy_Code','accept_reject_loan','State']


# X = pd.DataFrame(shuffled_df) 
df_new = shuffled_df.copy()# makes a separate copy of the dataframe, not a shared instance
# df_new = shuffled_df
X_enc=dummyEncode(df_new)
print("CSV encoded..")
print(X_enc.head())


# In[ ]:

# ## NORMALIZE
# from sklearn import preprocessing

# min_max_scaler = preprocessing.MinMaxScaler()
# np_scaled = min_max_scaler.fit_transform(X_enc)
# df_normalized = pd.DataFrame(np_scaled)
# df_normalized.head()


# In[120]:

print(datetime.datetime.now()," Clustering begins... ")


# In[121]:


complete = AgglomerativeClustering(n_clusters=3, linkage='complete').fit(X_enc)
average = AgglomerativeClustering(n_clusters=3, linkage='average').fit(X_enc)
#memory error for full data
#worked on 1000 immediately
#took 7 mins for 10000 :( 2017-04-13 00:50:08.586042  Clustering begins.. 017-04-13 00:57:48.821571  Done!!... 

print(datetime.datetime.now()," Clustering Done!!... ")


# In[ ]:

# label1=complete.labels_
# label1


# In[ ]:

# label2=average.labels_
# label2


# In[122]:

# to-do
X_enc['complete.label'] = pd.Series(complete.labels_, index=X_enc.index)
print("Encoded clusters..")
print(X_enc.head())


# In[123]:

shuffled_df['complete.label'] = pd.Series(complete.labels_, index=shuffled_df.index)
print("Original clusters...")
print(shuffled_df.head())


# In[ ]:

grouped = shuffled_df.groupby(['complete.label'])

l_grouped = list(grouped)

# print("First cluster..")   
# print(l_grouped[0][1])


# In[35]:

count = 0
h_cluster =[]
for hierarchy_group in l_grouped:
    df_clustered = l_grouped[count][1]
    h_cluster.append(df_clustered)
    print("Cluster ",count," of " ,len(df_clustered), " rows!")
    pd.to_csv("Cluster_"+str(count)+".csv", index= False)
    count+=1

