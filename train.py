import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import os

# 1. Create dummy data
# X = Years of Experience, y = Salary
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([30000, 35000, 40000, 50000, 60000, 65000, 70000, 85000, 90000, 105000])

# 2. Train Model
model = LinearRegression()
model.fit(X, y)

# 3. Create directory if not exists
if not os.path.exists('model'):
    os.makedirs('model')

# 4. Save the model
joblib.dump(model, 'model/linear_model.pkl')
print("Model trained and saved to model/linear_model.pkl")