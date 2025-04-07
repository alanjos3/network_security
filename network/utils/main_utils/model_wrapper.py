import pickle

def load_model(model_path, preprocessor_path):
    with open(preprocessor_path, "rb") as f:
        preprocessor = pickle.load(f)
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model, preprocessor

def predict_dataframe(preprocessor, model, df):
    X = preprocessor.transform(df)
    y_pred = model.predict(X)
    return y_pred
