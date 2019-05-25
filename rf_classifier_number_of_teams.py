import pandas as pd
import numpy as np
dataset = pd.read_csv('TPD-CSV/dados_prospecao.csv', encoding='cp850')
to_predict = pd.read_csv('TPD-CSV/dados_previsao.csv', encoding='cp850')
new_data_teams = []
new_data_teams_following_season = []
for i in range(len(dataset['equipas_epoca_seguinte'])):
    if dataset['equipas_epoca_seguinte'][i] < 7:
         new_data_teams_following_season.append(str(dataset['equipas_epoca_seguinte'][i]))
    else:
        new_data_teams_following_season.append('>6')
        
for i in range(len(dataset['equipas'])):
    if dataset['equipas'][i] < 7:
         new_data_teams.append(str(dataset['equipas'][i]))
    else:
        new_data_teams.append('>6')
    
dataset['prev_class']=new_data_teams
dataset['class']=new_data_teams_following_season
del dataset['equipas_epoca_seguinte']
del dataset['equipas']
new_data_teams = []
        
for i in range(len(to_predict['equipas'])):
    if to_predict['equipas'][i] < 7:
         new_data_teams.append(str(to_predict['equipas'][i]))
    else:
        new_data_teams.append('>6')
        
dataset['gender']=[x.strip() for x in dataset['gender']]

to_predict['prev_class']=new_data_teams
del to_predict['equipas']

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
dataset['agegroup']=le.fit_transform(dataset['agegroup'])
dataset['gender']=le.fit_transform(dataset['gender'])
dataset['club']=le.fit_transform(dataset['club'])
dataset['district']=le.fit_transform(dataset['district'])
dataset['prev_class']=le.fit_transform(dataset['prev_class'])

to_predict['agegroup']=le.fit_transform(to_predict['agegroup'])
to_predict['gender']=le.fit_transform(to_predict['gender'])
to_predict['club']=le.fit_transform(to_predict['club'])
to_predict['district']=le.fit_transform(to_predict['district'])
to_predict['prev_class']=le.fit_transform(to_predict['prev_class'])

X = dataset.iloc[:, 0:7].values  
y = dataset.iloc[:, 7].values
to_predict = to_predict.iloc[:,:].values

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(n_estimators=1000, criterion='gini')  
classifier.fit(X_train, y_train)  
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn import metrics
pscore = metrics.accuracy_score(y_test, y_pred)
print("Accuracy: " + str(pscore))
print(pd.crosstab(y_test, y_pred, rownames=['Actual Class'], colnames=['Predicted Class']))

predictions = classifier.predict(to_predict)
print(predictions)