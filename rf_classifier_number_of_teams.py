import pandas as pd

dataset = pd.read_csv('TPD-CSV/dados_prospecao.csv', encoding='cp850')
to_predict = pd.read_csv('TPD-CSV/dados_previsao.csv', encoding='cp850')
to_predict = to_predict.iloc[:, 3:9].values
new_data = []
for i in range(len(dataset['equipas_seguinte'])):
    if dataset['equipas_seguinte'][i] < 7:
         new_data.append(str(dataset['equipas_seguinte'][i]))
    else:
        new_data.append('>6')
        
dataset['class']=new_data
dataset['gender']=[x.strip() for x in dataset['gender']]

X = dataset.iloc[:, 3:9].values  
y = dataset.iloc[:, 11].values

print(y)

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
for i in range(6):
    X[:,i] = le.fit_transform(X[:,i])
y=le.fit_transform(y)
for i in range(6):
    to_predict[:,i] = le.fit_transform(to_predict[:,i])

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()  
X_train = sc.fit_transform(X_train)  
X_test = sc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(n_estimators=100, random_state=0)  
classifier.fit(X_train, y_train)  
y_pred = classifier.predict(X_test)

predictions = classifier.predict(to_predict)
print(predictions)