

# -*- coding: utf-8 -*-
"""pcoddetection.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1cnKiIydjQTc4ux9U3ZyfCB3Won_lz-x5
"""



import numpy as np #create arrays
import pandas.util.testing as tm
import pandas as pd
import matplotlib.pyplot as plt #plot data
import seaborn as sns #plot data
import missingno as ms #plot missing data


import warnings
warnings.filterwarnings('ignore')
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV              #For selecting best parameter values from the given set
from sklearn.linear_model import SGDClassifier                #For supporting loss functions

# from mlxtend.classifier import StackingClassifier
from sklearn.ensemble import VotingClassifier                 #To weight the occurrences of predicted class


# df = pd.read_csv('https://raw.githubusercontent.com/hiyabose/hackout-app/master/pcos.csv?token=AMDBGXCLZMVYM53W756SYXK7V3JFW', sep=',' , encoding='latin-1')
df = pd.read_csv('pcos.csv')

df.info()

df[[' Age (yrs)','Blood Group','Cycle length(days)','PCOS (Y/N)','Cycle(months)','Bloated','facial hair','chest hair','difficult to loose weight','mood swings','anxiety/depression/stress','Irregular_sleep','Fast food (Y/N)','Pregnant(Y/N)','No of aborptions','Hip(inch)','Waist(inch)','Weight gain(Y/N)','hair growth(Y/N)','Skin darkening (Y/N)','Hair loss(Y/N)','Pimples(Y/N)','Reg Exercise(Y/N)','Waist/Hip Ratio']] = df[[' Age (yrs)','Blood Group','Cycle length(days)','PCOS (Y/N)','Cycle(months)','Bloated','facial hair','chest hair','difficult to loose weight','mood swings','anxiety/depression/stress','Irregular_sleep','Fast food (Y/N)','Pregnant(Y/N)','No of aborptions','Hip(inch)','Waist(inch)','Weight gain(Y/N)','hair growth(Y/N)','Skin darkening (Y/N)','Hair loss(Y/N)','Pimples(Y/N)','Reg Exercise(Y/N)','Waist/Hip Ratio']].astype(float)

df.info()

# from sklearn import svm
##from sklearn.ensemble import RandomForestClassifier  
# from sklearn.linear_model import LogisticRegression
##from sklearn.model_selection import train_test_split

train = df.drop(['Sl No','Patient File No','PCOS (Y/N)','Pulse rate(bpm) '], axis=1)
train= np.asarray(train, dtype='int64')
test = df['PCOS (Y/N)']
test= np.asarray(test, dtype='int64')

test.shape

##X_train, X_test, y_train, y_test = train_test_split(train,test, test_size=0.2, random_state=2)
x_train, x_test, y_train, y_test = train_test_split(train,test, test_size=0.2,random_state=2)

# clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
# clf.fit(X_train, y_train)

#Predict the response for test dataset
# y_pred = clf.predict(X_test)

# y_train.shape,y_test.shape

# reg = LogisticRegression()
# reg = LogisticRegression( solver='lbfgs', max_iter=290)


# reg.fit(X_train, y_train)

# pred = reg.predict(X_test)

# pred

# reg.score(X_test, y_test)
from sklearn.neighbors import KNeighborsClassifier

warnings.simplefilter('ignore')
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train,y_train)

rf = RandomForestClassifier(n_estimators = 100,n_jobs=-1)
rf.fit(x_train, y_train)

from sklearn.ensemble import GradientBoostingClassifier
gb = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1)
gb.fit(x_train,y_train)

from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression

estimator_list = [
    ('knn',knn),
    ('rf',rf),
    ('gb',gb)
]

stack_model = StackingClassifier(
    estimators=estimator_list, final_estimator=LogisticRegression()
)

stack_model.fit(x_train, y_train)

#ypredtr = stack_model.predict(x_train)
pred = stack_model.predict(x_test)
pred
stack_model.score(x_test, y_test)
x_test.shape



##classifier= RandomForestClassifier(n_estimators= 290, criterion="entropy") 
##classifier.fit(X_train, y_train)
##pred= classifier.predict(X_test)     
##pred
##classifier.score(X_test, y_test)
"""With an excellant accuracy of 99.38 %"""

##X_test.shape

# x=[[28,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,44,152,19.3,15,1,5,7,36,30,0.833333333]]
# x=[[33,	1,	0,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	1,	1,	1,	0,	68.8,	165,	25.27089073,	11,		2,	5,	10,	40,	36,	0.9,	18,	11.8,	5.54,	0.88,	6.295454545,	2.54,	10.52,	13,	15,	18,	20,	10,	14.9,	16.4]]
x=[[30,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,85,165,31.22130395,16,4,7,7,44,42,0.954545455]]
# x=[[25,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,74,125,32.02909,17,4,2,7,45,40,0.888889]]

o = stack_model.predict(x)


print (o)

import pickle
pickle.dump(stack_model,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split
