from sklearn.linear_model import LinearRegression
import numpy as np

def predict_future_health(df):

    X = np.arange(len(df)).reshape(-1,1)
    y = df["health_score"]

    model = LinearRegression()
    model.fit(X,y)

    future = model.predict([[len(df)+3]])

    return round(future[0],2)
