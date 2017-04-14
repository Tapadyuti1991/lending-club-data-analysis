
# coding: utf-8

# In[ ]:

import pandas as pd


# In[33]:


df = pd.read_csv(get_object_storage_file_with_credentials_b6d2dc4304df42d5bf425b6ca8af67ff('LendingClub', 'accepted_merged_final.csv'),low_memory=False, encoding='cp1252')
df.head()


# In[34]:


import datetime

from sklearn.utils import shuffle
shuffled_df = shuffle(df) #df_normalized
shuffled_df.head()


# In[35]:

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


# In[9]:

from sklearn.preprocessing import LabelEncoder
# columns = ['Amount_Requested','Loan_Title','Risk_Score','Debt-To-Income_Ratio','Zip_Code','Employment_Length','Policy_Code','accept_reject_loan','State']


# X = pd.DataFrame(shuffled_df) 
df_new = shuffled_df.copy()# makes a separate copy of the dataframe, not a shared instance
# df_new = shuffled_df
X_enc=dummyEncode(df_new)
X_enc.head()


# In[36]:

from sklearn import cluster
# from sklearn.decomposition import PCA


# In[22]:

# print("Dim reduction begins...")
# pca = PCA(n_components=2).fit(X_enc)
# pca_2d = pca.transform(X_enc)
# print("Dim reduction done !!")


# In[38]:

print(datetime.datetime.now()," Clustering begins... ")
k_means=cluster.KMeans(n_clusters=6).fit(X_enc)
print(datetime.datetime.now()," Done!!... ")


# In[ ]:

# print(k_means.labels_)


# In[25]:

import numpy as np
from pandas import *
# from matplotlib import pyplot


# In[39]:

df1=pd.DataFrame(shuffled_df)
df2=pd.DataFrame(k_means.labels_,columns=['kmean.label'])
df_clustered=pd.concat([df1, df2], axis=1)
# df_clustered


# In[40]:

print("Grouping into clusters...")
grouped = df_clustered.groupby(['kmean.label'])

l_grouped = list(grouped)
   
# l_grouped[0][1]


# In[43]:

print("Exporting clusters as individual dataframes...")
count = 0
h_cluster =[]
for hierarchy_group in l_grouped:
    df_clustered = l_grouped[count][1]
    h_cluster.append(df_clustered)
    print("Cluster ",count," of " ,len(df_clustered), " rows!")
    csv_name = "K-means_Cluster_"+str(count)+".csv"
    df_clustered.to_csv(csv_name, index= False, encoding='cp1252')
#     put_file(credentials_1,csv_name) ## after to_csv
    count+=1

