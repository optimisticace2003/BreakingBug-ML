
# 1. To handle the data
import pandas as pd
import numpy as np

# 2. To visualize the data
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from yellowbrick.cluster import KElbowVisualizer
from matplotlib.colors import ListedColormap

# 3. To preprocess the data
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer

# 4. Import Iterative imputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# 5. Machine Learning  //*************sklearn importing
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score

# 6. For Classification task
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
import xgboost as xgb
import lightgbm as lgb
from sklearn.naive_bayes import GaussianNB

# 7. Metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

df = pd.read_csv("/content/drive/MyDrive/hari-bug/dataset.csv")

# print the first 5 rows of the dataframe
df.head()

# Exploring the data type of each column
df.info()

# Checking the data shape
df.shape

# Id column
df['id'].min(), df['id'].max()

# age column
df['age'].min(), df['age'].max()

# lets summerize the age column
df['age'].describe()

import seaborn as sns

# Define custom colors
custom_colors = ["#FF5733", "#3366FF", "#33FF57"]  # Example colors, you can adjust as needed

# Plot the histogram with custom colors
sns.histplot(df['age'], kde=True, color="#FF5733", palette=custom_colors)

# Plot the mean, Median and mode of age column using sns
sns.histplot(df['age'], kde=True)
plt.axvline(df['age'].mean(), color='Red')
plt.axvline(df['age'].median(), color= 'Green')
plt.axvline(df['age'].mode()[0], color='Blue')

# print the value of mean, median and mode of age column
print('Mean', df['age'].mean())
print('Median', df['age'].median())
print('Mode', df['age'].mode())


# plot the histogram of age column using plotly and coloring this by sex

fig = px.histogram(data_frame=df, x='age', color= 'sex')
fig.show()

# Find the values of sex column
df['sex'].value_counts()

# calculating the percentage fo male and female value counts in the data

male_count = 726
female_count = 194

total_count = male_count + female_count

# calculate percentages
male_percentage = (male_count/total_count)*100
female_percentages = (female_count/total_count)*100

# display the results
print(f'Male percentage i the data: {male_percentage:.2f}%')
print(f'Female percentage in the data : {female_percentages:.2f}%')

# Difference
difference_percentage = ((male_count - female_count)/female_count) * 100
print(f'Males are {difference_percentage:.2f}% more than female in the data.')


726/194

# Find the values count of age column grouping by sex column
df.groupby('sex')['age'].value_counts()

# find the unique values in the dataset column
df['dataset'].value_counts()                      #**************counts to value_counts , dataseet to dataset

# plot the countplot of dataset column
fig =px.bar(df, x='dataset', color='sex')
fig.show()

# print the values of dataset column groupes by sex
print (df.groupby('sex')['dataset'].value_counts())

# make a plot of age column using plotly and coloring by dataset

fig = px.histogram(data_frame=df, x='age', color= 'dataset')
fig.show()

print("___________________________________________________________")
print("Mean of the dataset: ")
print(df.groupby('dataset')['age'].mean())
print("___________________________________________________________")
print("Median of the dataset: ")
print(df.groupby('dataset')['age'].median())
print("___________________________________________________________")
print("Mode of the dataset: ")
print(df.groupby('dataset')['age'].apply(pd.Series.mode))  #****************groupby need to be added
print("___________________________________________________________")

#value count of cp column
df['cp'].value_counts()

# count plot of cp column by sex column
sns.countplot(df, x='cp', hue= 'sex')

# count plot of cp column by dataset column
sns.countplot(df,x='cp',hue='dataset')

# Draw the plot of age column group by cp column

fig = px.histogram(data_frame=df, x='age', color='cp')
fig.show()

# lets summerize the trestbps column
df['trestbps'].describe()

# Dealing with Missing values in trestbps column.
# find the percentage of misssing values in trestbps column
print(f"Percentage of missing values in trestbps column: {df['trestbps'].isnull().sum() /len(df) *100:.2f}%")

# Impute the missing values of trestbps column using iterative imputer
# create an object of iteratvie imputer
imputer1 = IterativeImputer(max_iter=10, random_state=42)

# Fit the imputer on trestbps column
imputer1.fit(df[['trestbps']])

# Transform the data
df['trestbps'] = imputer1.transform(df[['trestbps']])

# Check the missing values in trestbps column
print(f"Missing values in trestbps column: {df['trestbps'].isnull().sum()}")

# Create an object of Iterative Imputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
# First lets see data types or category of columns
df.info()

# let's see which columns has missing values
(df.isnull().sum()/ len(df)* 100).sort_values(ascending=False)

# create an object of iterative imputer
imputer2 = IterativeImputer(max_iter=10, random_state=42)

# fit transform on ca,oldpeak, thal,chol and thalch columns
# Fit and transform on ca, oldpeak, chol, and thalch columns
df[['ca', 'oldpeak', 'chol', 'thalch']] = imputer2.fit_transform(df[['ca', 'oldpeak', 'chol', 'thalch']])   #*********** change imputer to imputer2.fit_transformer.Applied fit_transform to the subset of columns rather than individual columns.



# let's check again for missing values
(df.isnull().sum()/ len(df)* 100).sort_values(ascending=False)

print(f"The missing values in thal column are: {df['thal'].isnull().sum()}")

df['thal'].value_counts()

df.tail()

# find missing values.
missing_values = df.isnull().sum()
print("Missing values:")                    #*******************Replaced null to isnull, Removed the incorrect expression, changed to sort_values(ascending=True)
print(missing_values[missing_values > 0].sort_values(ascending=True))

def impute_continuous_missing_data(passed_col):

    # Separate data into rows with missing and non-missing values for the specified column
    df_null = df[df[passed_col].isnull()]
    df_not_null = df[df[passed_col].notnull()]

    X = df_not_null.drop(passed_col, axis=1)
    y = df_not_null[passed_col]

    other_missing_cols = [col for col in missing_data_cols if col != passed_col]

    # Initialize LabelEncoder (not used in this code)
    # label_encoder = LabelEncoder()  # Removed as it's not used

    # OneHotEncoder needs to be initialized
    onehotencoder = OneHotEncoder(sparse=False, drop='first')

    # Apply one-hot encoding to categorical columns in X
    categorical_cols = X.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        X[col] = onehotencoder.fit_transform(X[[col]].astype(str))

    # Initialize IterativeImputer with RandomForestRegressor
    imputer = IterativeImputer(estimator=RandomForestRegressor(random_state=16), add_indicator=True)

    # Train-test split for evaluating RandomForestRegressor
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf_regressor = RandomForestRegressor()
    rf_regressor.fit(X_train, y_train)
    y_pred = rf_regressor.predict(X_test)

    print("MAE =", mean_absolute_error(y_test, y_pred), "\n")
    print("RMSE =", mean_squared_error(y_test, y_pred, squared=False), "\n")
    print("R2 =", r2_score(y_test, y_pred), "\n")

    # Prepare df_null for imputation
    X_null = df_null.drop(passed_col, axis=1)

    # Apply one-hot encoding to categorical columns in X_null
    categorical_cols_null = X_null.select_dtypes(include=['object']).columns
    for col in categorical_cols_null:
        X_null[col] = onehotencoder.transform(X_null[[col]].astype(str))

    # Impute missing values using IterativeImputer
    X_null_imputed = imputer.transform(X_null)

    # Predict missing values using trained RandomForestRegressor
    if len(df_null) > 0:
        df_null[passed_col] = rf_regressor.predict(X_null_imputed)

    # Combine the imputed df_null back with df_not_null
    df_combined = pd.concat([df_not_null, df_null])

    return df_combined[passed_col]

# def impute_continuous_missing_data(passed_col):

#     df_null = df[df[passed_col].isnull()]
#     df_not_null = df[df[passed_col].notnull()]

#     X = df_not_null.drop(passed_col, axis=1)
#     y = df_not_null[passed_col]

#     other_missing_cols = [col for col in missing_data_cols if col != passed_col]

#     label_encoder = LabelEncoder()

#     for cols in Y.columns:
#         if Y[col].dtype == 'object' :
#             Y[col] = onehotencoder.fit_transform(Y[col].astype(str))

#     imputer = Imputer(estimator=RandomForestRegressor(random_state=16), add_indicator=True)

#     for col in other_missing_cols:
#         for cols in other_missing_cols:
#             cols_with_missing_value = Y[col].value.reshape(-100, 100)

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     rf_regressor = RandomForestRegressor()

#     rf_regressor.fit(X_train, y_train)

#     y_pred = rf_regressor.predict(X_test)

#     print("MAE =", mean_absolute_error(y_test, y_pred), "\n")
#     print("RMSE =", mean_squared_error(y_test, y_pred, squared=False), "\n")
#     print("R2 =", r2_score(y_test, y_pred), "\n")

#     X = df_null.drop(passed_col, axis=1)

#     for cols in Y.columns:
#         if Y[col].dtype == 'object' :
#             Y[col] = onehotencoder.fit_transform(Y[col].astype(str))

#     for cols in other_missing_cols:
#             cols_with_missing_value = Y[col].value.reshape(-100, 100)
#             imputed_values = iterative_imputer.fit_transform(col_with_missing_values)
#             X[col] = imputed_values[:, 0]
#         else:
#             pass

#     if len(df_null) > 0:
#         df_not_null[wrong_col] = rf_classifer.predict(X_train)
#     else:
#         pass

#     df_combined = pd.concat([df_not_null, df_null])

#     return df_combined[passed_col]

# List of numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# List of categorical columns
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

df.isnull().sum().sort_values(ascending=False)

# remove warning
import warnings
warnings.filterwarnings('ignore')

def impute_categorical_missing_data(col):
    most_frequent = df[col].mode()[0]
    df[col].fillna(most_frequent, inplace=True)
    return df[col]

def impute_continuous_missing_data(col):
    imputer = IterativeImputer(max_iter=10, random_state=42)
    df[[col]] = imputer.fit_transform(df[[col]])
    return df[col]

# impute missing values using our functions

for col in missing_data_cols:
    print("Missing Values", col, ":", str(round((df[col].isnull().sum() / len(df)) * 100, 2)) + "%")
    if col in categorical_cols:
        df[col] = impute_categorical_missing_data(col)
    elif col in numeric_cols:
        df[col] = impute_continuous_missing_data(col)
    else:
        pass

df.isnull().sum().sort_values(ascending=False)


print("_________________________________________________________________________________________________________________________________________________")

# Define columns to plot (you can choose specific columns to visualize or plot all)
cols = ['age', 'trestbps', 'chol', 'fbs', 'thalch', 'oldpeak', 'slope', 'ca', 'thal']  # Example columns, update as needed

# Set initial background color
sns.set(rc={"axes.facecolor": "#87CEEB", "figure.facecolor": "#EEE8AA"})

# Define color palette and colormap
palette = ["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#9F8A78", "#F3AB60"]
cmap = ListedColormap(palette)

# Plot the boxen plots
plt.figure(figsize=(12, 10))

for i, col in enumerate(cols):
    plt.subplot(3, 3, i + 1)  # Adjust the grid size (3 rows x 3 columns) as needed
    sns.boxenplot(data=df, x=col, color=palette[i % len(palette)])  # Plot data
    plt.title(col)

plt.tight_layout()
plt.show()

# Print rows where 'trestbps' is 0
print(df[df['trestbps'] == 0])

# Remove rows where 'trestbps' is 0
df = df[df['trestbps'] != 0]

# Set new background color
sns.set(rc={"axes.facecolor": "#B76E79", "figure.facecolor": "#C0C0C0"})

# Define new color palette
modified_palette = ["#C44D53", "#B76E79", "#DDA4A5", "#B3BCC4", "#A2867E", "#F3AB60"]
cmap = ListedColormap(modified_palette)

# Plot the updated boxen plots
plt.figure(figsize=(12, 10))

for i, col in enumerate(cols):
    plt.subplot(3, 3, i + 1)  # Adjust the grid size (3 rows x 3 columns) as needed
    sns.boxenplot(data=df, x=col, color=modified_palette[i % len(modified_palette)])  # Plot data
    plt.title(col)

plt.tight_layout()
plt.show()

# Print descriptive statistics
print(df['trestbps'].describe())
print(df.describe())

print("___________________________________________________________________________________________________________________________________________________________________")

# Define columns to plot
cols = ['age', 'trestbps', 'chol', 'fbs', 'thalch', 'oldpeak', 'slope', 'ca', 'thal']

# Set facecolors
sns.set(rc={"axes.facecolor": "#FFF9ED", "figure.facecolor": "#FFF9ED"})

# Define the "night vision" color palette
night_vision_palette = ["#00FF00", "#FF00FF", "#00FFFF", "#FFFF00", "#FF0000", "#0000FF"]

# Use the "night vision" palette for the plots
plt.figure(figsize=(12, 10))
for i, col in enumerate(cols):
    plt.subplot(3, 3, i + 1)  # Create a subplot in a 3x3 grid
    sns.boxenplot(data=df, x=col, color=night_vision_palette[i % len(night_vision_palette)])  # Use modulo to cycle through colors
    plt.title(col)

plt.tight_layout()
plt.show()

# Descriptive statistics for 'age'
print(df.age.describe())

# Define a new palette for histogram plots
palette = ["#999999", "#666666", "#333333"]

# Plot histogram for 'trestbps'
sns.histplot(data=df, x='trestbps', kde=True, color=palette[0])
plt.title('Resting Blood Pressure')
plt.xlabel('Pressure (mmHg)')
plt.ylabel('Count')
plt.show()

# Plot histogram for 'trestbps' with respect to 'sex'
sns.histplot(df, x='trestbps', kde=True, palette="Spectral", hue='sex')
plt.show()

# Display DataFrame info and head
print(df.info())
print(df.columns)
print(df.head())

# Split the data into X and y
X = df.drop('num', axis=1)
y = df['num']

# Initialize OneHotEncoder
encoder = OneHotEncoder(sparse=False, drop='first')
X_encoded = X.copy()

# Apply OneHotEncoder to categorical columns
categorical_cols = ['thal']  # Replace with your actual categorical columns

for col in categorical_cols:
    # Fit and transform the data using OneHotEncoder
    encoded = encoder.fit_transform(X[[col]])
    # Create DataFrame from encoded array
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out([col]))
    # Concatenate the encoded columns with the original DataFrame
    X_encoded = pd.concat([X_encoded, encoded_df], axis=1)
    # Drop the original categorical column
    X_encoded.drop(col, axis=1, inplace=True)

# Split the data into train and test
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.1, random_state=42)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.naive_bayes import GaussianNB as Gaussian
from sklearn.svm import SVC as SVC_Classifier
from sklearn.tree import DecisionTreeClassifier as DecisionTree
from sklearn.ensemble import RandomForestClassifier as RandomForest
from xgboost import XGBClassifier as XG
from sklearn.ensemble import GradientBoostingClassifier as GradientBoost
from sklearn.ensemble import AdaBoostClassifier as AdaBoost
from sklearn.metrics import accuracy_score
import pandas as pd

# Sample data creation (replace with your data)
X, y = make_classification(n_samples=100, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define models
models = [
    ('Logistic Regression', LogisticRegression(random_state=42)),
    ('Gradient Boosting', GradientBoostingClassifier(random_state=42)),
    ('KNeighbors Classifier', KNeighborsClassifier()),
    ('Decision Tree Classifier', DecisionTreeClassifier(random_state=42)),
    ('AdaBoost Classifier', AdaBoostClassifier(random_state=42)),
    ('Random Forest', RandomForestClassifier(random_state=42)),
    ('XGboost Classifier', XGBClassifier(random_state=42)),
    ('Support Vector Machine', SVC(random_state=42)),
    ('Naive Bayes Classifier', GaussianNB())
]

# Define the preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='most_frequent'), list(range(X.shape[1]))),  # Adjust for numerical features
        # ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)  # Comment this out if not using categorical features
    ],
    remainder='passthrough'
)

best_model = None
best_accuracy = 0.0

# Iterate over the models and evaluate their performance
for name, model in models:
    # Create a pipeline for each model
    pipeline = Pipeline([
        ('preprocessor', preprocessor),  # Apply preprocessing
        ('model', model)  # The model to be evaluated
    ])

    # Perform cross-validation on training data
    scores = cross_val_score(pipeline, X_train, y_train, cv=5)  # Use X_train and y_train for cross-validation

    # Calculate mean accuracy
    mean_accuracy = scores.mean()  # Use mean() instead of avg()

    # Fit the pipeline on the training data
    pipeline.fit(X_train, y_train)  # Fit on X_train and y_train

    # Make predictions on the test data
    y_pred = pipeline.predict(X_test)

    # Calculate accuracy score
    accuracy = accuracy_score(y_test, y_pred)

    # Print the performance metrics
    print("Model:", name)
    print("Cross Validation Accuracy:", mean_accuracy)
    print("Test Accuracy:", accuracy)
    print()

    # Check if the current model has the best accuracy
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = pipeline

# Retrieve the best model
print("Best Model:", best_model)

def evaluate_classification_models(X, y, categorical_columns):
    # Encode categorical columns
    X_encoded = X.copy()
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

    # Apply one-hot encoding to categorical columns
    X_encoded = pd.get_dummies(X_encoded, columns=categorical_columns)

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # Define models
    models = {
        "Logistic Regression": LogisticRegression(),
        "KNN": KNN(),
        "NB": Gaussian(),
        "SVM": SVC_Classifier(),
        "Decision Tree": DecisionTree(),
        "Random Forest": RandomForest(),
        "XGBoost": XG(),
        "GradientBoosting": GradientBoost(),
        "AdaBoost": AdaBoost()
    }

    # Train and evaluate models
    results = {}
    best_model = None
    best_accuracy = 0.0
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = accuracy
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = name

    return results, best_model

# Example usage:
# Assuming df is your DataFrame
categorical_cols = ['thal', 'ca', 'slope', 'exang', 'restecg', 'fbs', 'cp', 'sex', 'num']
X = df[categorical_cols]  # Select the categorical columns as input features
y = df['num']  # Select the target variable

results, best_model = evaluate_classification_models(X, y, categorical_cols)
print("Model accuracies:", results)
print("Best model:", best_model)



from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

def hyperparameter_tuning(X, y, categorical_columns, models):
    # Initialize the encoder
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)  # Changed from 'onehotencoder' to 'OneHotEncoder'

    # Encode categorical columns
    X_encoded = X.copy()
    for col in categorical_columns:
        X_encoded = X_encoded.join(pd.DataFrame(encoder.fit_transform(X[[col]]), columns=encoder.get_feature_names_out([col])))  # Correct encoding and joining

    # Split data into train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X_encoded, y, test_size=0.2, random_state=42)  # Changed 'val_size' to 'test_size'

    # Define dictionary to store results
    results = {}

    # Perform hyperparameter tuning for each model
    for model_name, model in models.items():
        # Define parameter grid for hyperparameter tuning
        param_grid = {}
        if model_name == 'Logistic Regression':
            param_grid = {'C': [0.1, 1, 10, 100]}
        elif model_name == 'KNN':
            param_grid = {'n_neighbors': [3, 5, 7, 9]}
        elif model_name == 'NB':
            param_grid = {'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6]}
        elif model_name == 'SVM':
            param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [0.1, 1, 10, 100]}
        elif model_name == 'Decision Tree':
            param_grid = {'max_depth': [None, 10, 20, 30], 'min_samples_split': [2, 5, 10]}
        elif model_name == 'Random Forest':
            param_grid = {'n_estimators': [100, 200, 300], 'max_depth': [None, 10, 20, 30], 'min_samples_split': [2, 5, 10]}
        elif model_name == 'XGBoost':
            param_grid = {'learning_rate': [0.01, 0.1, 0.2], 'n_estimators': [100, 200, 300], 'max_depth': [3, 5, 7]}  # Changed 'parameter_grid' to 'param_grid'
        elif model_name == 'GradientBoosting':
            param_grid = {'learning_rate': [0.01, 0.1, 0.2], 'n_estimators': [100, 200, 300], 'max_depth': [3, 5, 7]}
        elif model_name == 'AdaBoost':
            param_grid = {'learning_rate': [0.01, 0.1, 0.2], 'n_estimators': [50, 100, 200]}

        # Perform hyperparameter tuning using GridSearchCV
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        # Get best hyperparameters and evaluate on validation set
        best_params = grid_search.best_params_
        best_model = grid_search.best_estimator_
        y_pred = best_model.predict(X_val)  # Changed from 'X_test' to 'X_val'
        accuracy = accuracy_score(y_val, y_pred)  # Changed from 'y_test' to 'y_val'

        # Store results in dictionary
        results[model_name] = {'best_params': best_params, 'accuracy': accuracy}

    return results

from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint
import pandas as pd

def hyperparameter_tuning(X, y, categorical_columns, models):
    # Initialize the encoder
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

    # Encode categorical columns
    X_encoded = X.copy()
    for col in categorical_columns:
        # Apply one-hot encoding and convert to DataFrame
        encoded_cols = encoder.fit_transform(X[[col]])
        encoded_df = pd.DataFrame(encoded_cols, columns=encoder.get_feature_names_out([col]))
        X_encoded = X_encoded.join(encoded_df).drop(columns=[col])

    # Split data into train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # Define dictionary to store results
    results = {}

    # Perform hyperparameter tuning for each model
    for model_name, model in models.items():
        # Define parameter grid for hyperparameter tuning
        param_distributions = {}
        if model_name == 'Logistic Regression':
            param_distributions = {'C': uniform(0.1, 100)}
        elif model_name == 'KNN':
            param_distributions = {'n_neighbors': randint(3, 10)}
        elif model_name == 'NB':
            param_distributions = {'var_smoothing': uniform(1e-9, 1e-6)}
        elif model_name == 'SVM':
            param_distributions = {'C': uniform(0.1, 100), 'gamma': uniform(0.1, 100)}
        elif model_name == 'Decision Tree':
            param_distributions = {'max_depth': [None, 10, 20, 30], 'min_samples_split': randint(2, 11)}
        elif model_name == 'Random Forest':
            param_distributions = {'n_estimators': [100, 200], 'max_depth': [None, 10, 20], 'min_samples_split': randint(2, 11)}
        elif model_name == 'XGBoost':
            param_distributions = {'learning_rate': uniform(0.01, 0.2), 'n_estimators': [100, 200], 'max_depth': randint(3, 6)}
        elif model_name == 'GradientBoosting':
            param_distributions = {'learning_rate': uniform(0.01, 0.2), 'n_estimators': [100, 200], 'max_depth': randint(3, 6)}
        elif model_name == 'AdaBoost':
            param_distributions = {'learning_rate': uniform(0.01, 0.2), 'n_estimators': randint(50, 100)}

        # Perform hyperparameter tuning using RandomizedSearchCV
        randomized_search = RandomizedSearchCV(
            model, param_distributions, n_iter=5, cv=3, scoring='accuracy', random_state=42, n_jobs=-1
        )
        randomized_search.fit(X_train, y_train)

        # Get best hyperparameters and evaluate on validation set
        best_params = randomized_search.best_params_
        best_model = randomized_search.best_estimator_
        y_pred = best_model.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred)

        # Store results in dictionary
        results[model_name] = {'best_params': best_params, 'accuracy': accuracy}

    return results

# Example usage:
results = hyperparameter_tuning(X, y, categorical_cols, models)
for model_name, result in results.items():
    print("Model:", model_name)
    print("Best hyperparameters:", result['best_params'])
    print("Accuracy:", result['accuracy'])
    print()
