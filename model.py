import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def create_model(csv_path):

    df = pd.read_csv(csv_path)

    # Select features and target
    features = ['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year']
    target = 'Life Expectancy (IHME)'

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)

    return model, score
