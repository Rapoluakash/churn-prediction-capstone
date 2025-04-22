# Importing Libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from xgboost import XGBClassifier

# Load Dataset
data = pd.read_csv(r"C:\Users\rapol\Downloads\DATA SCIENCE\4. Dec\16th, 17th - ENSAMBLE LEARNING\7.XGBOOST\Churn_Modelling.csv")

# Split features and target
x = data.iloc[:, 3:-1].values  # Exclude RowNumber, CustomerId, Surname, and Exited
y = data.iloc[:, -1].values    # Exited column

# Label Encoding for Gender column
le = LabelEncoder()
x[:, 2] = le.fit_transform(x[:, 2])  # Gender: Male=1, Female=0

# One-Hot Encoding for Geography column
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
x = np.array(ct.fit_transform(x))

# Feature Scaling (optional but helps with convergence)
sc = StandardScaler()
x = sc.fit_transform(x)

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=0)

# XGBoost Model
xgb = XGBClassifier(
    learning_rate=0.08,
    n_estimators=100,
    max_depth=3,
    random_state=0
)
xgb.fit(x_train, y_train)

# Prediction
y_pred = xgb.predict(x_test)

# Evaluation
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", cm)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy Score:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Bias & Variance
bias = xgb.score(x_train, y_train)
variance = xgb.score(x_test, y_test)

print("Training Score (Bias):", bias)
print("Testing Score (Variance):", variance)
