import mysql.connector

import pandas as pd

from sklearn.linear_model import LinearRegression

from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score, f1_score, r2_score

cnx = mysql.connector.connect(user='root', password='@lexander8891',
                              host='127.0.0.1',
                              database='infoDB')

cursor = cnx.cursor(buffered=True)

df = pd.read_sql_query("SELECT * FROM cars", con=cnx)

#print(df.duplicated().sum())

df.drop_duplicates(inplace=True)

#I used multiple linear regression
mlr = LinearRegression()

#convert model and currentUse to dummy variable
df = pd.get_dummies(df, columns=['model', 'currentUse'], drop_first=True)

#print(df.tail(10))
#print(df.columns)

X = df[['mileage', 'yearMake', 'numOfAccidents', 'numOfOwners', 'model_Acura MDX', 'model_Acura NSX', 'model_Acura RDX',
       'model_Acura RL', 'model_Acura RLX', 'model_Acura TL',
       'model_Acura TLX', 'model_Acura TSX', 'model_Acura ZDX',
       'currentUse_ Personal use']]

y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

mlr.fit(X_train, y_train)

test_data_point = [[8101, 2022, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

prediction = mlr.predict(test_data_point)

print()
print("***Using Multiple Linear Regression***")
print()
print(f"The predicted y for test_data_point is: {prediction}")

print()

y_predicted = mlr.predict(X_test)

r2 = r2_score(y_test, y_predicted)

print("The accuracy of multiple linear regression model is {}%".format(round(r2, 2) *100))

print("--------------------------------------------------------")

print("***Using Decision Tree Classifier***")
print()

clf = DecisionTreeClassifier()

clf.fit(X_train, y_train)

prediction = clf.predict([[8101, 2022, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]])

print(f"The predicted y for test_data_point is: {prediction}")
print()
print("The accuracy of Decision Tree Classifier model is {}%".format(round(clf.score(X_test, y_test), 2) *100))

print("--------------------------------------------------------")

print("***Using Decision Tree Regressor***")
print()

from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor(random_state = 0)
regressor.fit(X_train, y_train)

y_pred = regressor.predict([[8101, 2022, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]])

print(f"The predicted y for test_data_point is: {y_pred}")
print()
print("The accuracy of Decision Tree Regressor model is {}%".format(round(regressor.score(X_test, y_test), 2) *100))

cnx.close()
