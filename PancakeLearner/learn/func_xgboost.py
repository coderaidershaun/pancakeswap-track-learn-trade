from sklearn.model_selection import train_test_split, cross_val_score, RepeatedStratifiedKFold
from sklearn.metrics import classification_report
from xgboost import XGBClassifier, plot_tree
from func_utils import structure_probabilities
from scipy.stats import binom_test
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from pprint import pprint

def run_xgboost(columns, X_data, y_data, proba_thresh):
  ne = 25
  md = 2
  lr = 0.1
  gm = 0.03
  test_size_rate = 0.8

  # Train Test Split
  X_train, X_test, y_train, y_test = train_test_split(
      X_data,
      y_data,
      random_state=0,
      test_size=test_size_rate,
      shuffle=True)
  
  # For binary classification
  objective = "binary:logistic"
  eval_metric = "logloss"
  eval_metric_list = ["error", "logloss"]

  # Evaluation
  eval_metric = "aucpr"
  eval_metric_list.append(eval_metric)
  scoring = 'precision'

  # Build Classification Model with Initial Hyperparams
  classifier = XGBClassifier(
    objective=objective,
    booster="gbtree",
    n_estimators=ne,
    learning_rate=lr,
    max_depth=md,
    subsample=0.8,
    colsample_bytree=1,
    gamma=gm,
    random_state=1,
  )

  # Fit Model
  eval_set = [(X_train, y_train), (X_test, y_test)]
  classifier.fit(
    X_train,
    y_train,
    eval_metric=eval_metric_list,
    eval_set=eval_set,
    verbose=False,
  )

  # Extract predictions
  train_yhat_preds = classifier.predict(X_train)
  test_yhat_preds = classifier.predict(X_test)
  train_yhat_proba = classifier.predict_proba(X_train)
  test_yhat_proba = classifier.predict_proba(X_test)

  # Set K-Fold Cross Validation levels
  cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=1)

  # Training Results
  train_cross_val_score = cross_val_score(classifier, X_train, y_train, scoring=scoring, cv=cv, n_jobs=-1)
  train_summary_report = classification_report(y_train, train_yhat_preds, output_dict=True, zero_division=False)
  test_summary_report = classification_report(y_test, test_yhat_preds, output_dict=True, zero_division=False)

  # Standard deviation
  std_dev_perc = train_cross_val_score.std() * 100
  avg_score_perc = train_cross_val_score.mean() * 100

  # Show key metrics
  print("")
  print("Std Deviation %: ", round(std_dev_perc, 1))
  print("Avg Accuracy %: ", round(avg_score_perc, 1))
  print("Train Precision %: ", round(train_summary_report["1.0"]["precision"] * 100, 1))
  print("Test Precision %: ", round(test_summary_report["1.0"]["precision"] * 100, 1))
  print("")

  # Structure predictions
  preds_list = []

  preds_list_train = structure_probabilities(
    train_yhat_proba, train_yhat_preds, y_train, preds_list, "train", proba_thresh)
  
  preds_list_full = structure_probabilities(
    test_yhat_proba, test_yhat_preds, y_test, preds_list_train, "test", proba_thresh)
  
  # Create predictions dataframe
  df_preds = pd.DataFrame(preds_list_full)

  # Create Winner Column and default to 0
  df_preds["WINNER"] = 0

  # Confirm winners
  df_preds.loc[df_preds["actual_y"] == df_preds["pred_y"] & (df_preds["pred_y"] == 1), "WINNER"] = 1

  # Sum winners
  winner_count = df_preds["WINNER"].sum()
  winner_perc = round(winner_count / len(df_preds) * 100, 1)

  print("")
  print("Results including Training data:")
  print("Count: ", winner_count)
  print("Win Rate %: ", winner_perc)
  print("")

  # Filter only for test items
  df_preds = df_preds[df_preds["index"].str.contains("test")]

  # Sum winners again
  winner_count = df_preds["WINNER"].sum()
  winner_perc = round(winner_count / len(df_preds) * 100, 1)

  print("")
  print("Results including Test data:")
  print("Count: ", winner_count)
  print("Win Rate %: ", winner_perc)
  print("")

  # Calculate p value of test result
  x = winner_count,
  n = len(df_preds)
  p = 0.5
  alternative = "greater"
  p_value = round(binom_test(x, n, p, alternative), 3)

  # Show final stats
  print("")
  print("p-value: ", p_value, p_value <= 0.05)
  print("")

  # Save model
  classifier.save_model("model.json")

  """
    Other useful code
    Helps to evaluate and seek out overfitting
  """

  # Feature importance
  importance_features = classifier.feature_importances_
  plt.title('Feature Importance')
  plt.bar(columns, importance_features)
  plt.savefig('PancakeLearner/learn/img/feature_importance.png')
  plt.clf()

  # Plot tree
  plot_tree(classifier, num_trees=0)
  plt.savefig('PancakeLearner/learn/img/decision_tree.png')
  plt.clf()

  # Other useful plots
  training_results = classifier.evals_result()
  validation_0_error = training_results['validation_0'][eval_metric_list[0]]
  validation_1_error = training_results['validation_1'][eval_metric_list[0]]

  # Plots
  plt.title('Error')
  plt.plot(validation_0_error)
  plt.plot(validation_1_error)
  plt.savefig('PancakeLearner/learn/img/error_train_v_test.png')
  plt.clf()
