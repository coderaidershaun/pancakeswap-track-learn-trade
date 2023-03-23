from xgboost import XGBClassifier

# Predict to go short or long
def xgb_predict_ratio(X_data):

  # Make predictions
  xbg_classifier = XGBClassifier()
  xbg_classifier.load_model(f"model.json")
  preds = xbg_classifier.predict(X_data)
  preds_proba = xbg_classifier.predict_proba(X_data)

  # Return probability of 1
  return preds_proba.tolist()[0][1]
