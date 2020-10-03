import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error


# Fonksiyonlar
def rmse_hesapla(y_test,y_pred):
    return np.sqrt(mean_squared_error(y_test,y_pred))


def ciz (y_test,y_pred):
    
    plt.scatter(range(len(y_pred)),y_pred,color="red")
    plt.plot(range(len(y_pred)),y_test)
    plt.show()
    




data = pd.read_excel("son.xlsx",index_col='Unnamed: 0')

X, y = data.iloc[:,7:], data['ortalamaPuani']






# Puan dağılımını görmek için histogram çizdiriyorum.
sns.distplot(y)
plt.show()




# Train-test split
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test= train_test_split(X,y,
                                                test_size = .33 ,
                                                random_state= 42)



# Lineer Regresyon   (0.71834)

'''
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X_train,y_train)


y_pred= model.predict(X_test)


from sklearn.metrics import mean_squared_error

# RMSE
print(rmse_hesapla(y_test, y_pred))

ciz(y_test, y_pred)

# Tahmin edilen uç değerler dışında fena değil açıkçası
'''

# Polynomial Regression (0.3056937)
'''

from sklearn.linear_model import LinearRegression

# Fitting Polynomial Regression to the dataset
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree=2)
X_poly = poly_reg.fit_transform(X)
pol_reg = LinearRegression()
pol_reg.fit(X_poly, y)

# Visualizing the Polymonial Regression results

plt.scatter(range(len(y)), y, color='red')
plt.plot(range(len(y)), pol_reg.predict(poly_reg.fit_transform(X)), color='blue')
plt.title('Yorumlardan Restoran Puanı Tahmin Etme (Polynomial Regression)')
plt.xlabel("Restoran")
plt.ylabel('ortalamaPuan')
plt.show()

print(np.sqrt(mean_squared_error(y, pol_reg.predict(poly_reg.fit_transform(X)))))
'''


# SVR  (0.48553)

'''
from sklearn.svm import SVR

model = SVR(kernel="rbf").fit(X_train,y_train)

y_pred= model.predict(X_test)

print(rmse_hesapla(y_test, y_pred))

ciz(y_test, y_pred)
'''


# Decision Tree (0.8199)
'''
from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor().fit(X_train,y_train)

y_pred= model.predict(X_test)

print(rmse_hesapla(y_test, y_pred))

ciz(y_test, y_pred)
'''