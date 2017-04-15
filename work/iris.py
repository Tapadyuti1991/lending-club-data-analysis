
# coding: utf-8

# In[ ]:

from tsne import bh_sne


# In[ ]:

from sklearn.datasets import load_iris


# In[ ]:

iris = load_iris()


# In[ ]:

X = iris.data


# In[ ]:

y = iris.target


# In[ ]:

X_2d = bh_sne(X)


# In[ ]:

scatter(X_2d[:, 0], X_2d[:, 1], c=y)


# In[ ]:



