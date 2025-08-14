import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

def _create_model(csv_path):

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

    model_data = {
        'model': model,
        'score': score
    }

    joblib.dump(model_data, 'life_expectancy_model.pkl')

    return model, score

def _load_model():
    """Load the pre-trained model and its score"""

    model_data = joblib.load('life_expectancy_model.pkl')
    return model_data['model'], model_data['score']

def get_or_create_model(csv_path, force_retrain=False):
    model_path = 'life_expectancy_model.pkl'

    # Load existing model if available
    if os.path.exists(model_path) and not force_retrain:
        print("Loading existing model...")
        model, score = _load_model()
        return model, score  # No score since we didn't retrain

    print("Training new model...")
    model, score = _create_model(csv_path)
    return model, score