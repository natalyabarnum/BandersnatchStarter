import pandas as pd
from pandas import DataFrame
import joblib
import numpy as np
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from app.data import Database

db = Database()
df = db.dataframe()

class Machine:

    def __init__(self, df: DataFrame):
        self.name = 'Random Forest Classifier'
        self.df = df.drop(columns=['Damage', 'Timestamp', 'Name', 'Type'])
        self.le = LabelEncoder()
        self.df['Rarity'] = self.le.fit_transform(df['Rarity'])


        target = 'Rarity'
        self.y = self.df[target]
        self.X = self.df.drop(columns=target)
        print(self.y)
        self.model = make_pipeline(
                        SimpleImputer(strategy='median'), 
                        RandomForestClassifier(random_state=42, n_jobs=-1,n_estimators=75)
                        )
        self.model.fit(self.X, self.y)

    def __call__(self, feature_basis):
        features = pd.DataFrame(feature_basis, columns=self.X.columns)
        prediction_proba = self.model.predict_proba(features)
        prediction = np.argmax(prediction_proba, axis=1)
        confidence = np.max(prediction_proba, axis=1)[0]
        prediction_label = self.le.inverse_transform(prediction)[0]
        return prediction_label, confidence

    def save(self, filepath):
        state = {'model': self.model, 'label_encoder': self.le}
        joblib.dump(state, filepath)

    @staticmethod
    def open(filepath):
        state = joblib.load(filepath)
        machine = Machine(df)
        machine.model = state['model']
        machine.le = state['label_encoder']
        return machine

    def info(self):
        info_str = f"Base Model: {self.name}<br>Timestamp: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}"
        return info_str

        

if __name__ == '__main__':
    machine = Machine(df)