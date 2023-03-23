# Structure and clarify probabilities with percentage expectation
def structure_probabilities(yhat_proba, yhat_preds, y_actual, preds_list, pred_type, proba_thresh):

  # Go through each prediction
  for index, item in enumerate(yhat_proba):
    pred_0 = item[0]
    pred_1 = item[1]
    pred_y = yhat_preds[index]
    actual_y = y_actual.values[index]
    data_obj = {
      "index": f"{pred_type}_{index}",
      "actual_y": actual_y,
      "pred_y": pred_y,
      "pred_0_proba": pred_0,
      "pred_1_proba": pred_1,
    }

    # Append to list of predictions
    if pred_1 >= proba_thresh:
      preds_list.append(data_obj)

  # Return list of predicitons
  return preds_list
