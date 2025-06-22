from sklearn.metrics import mean_squared_error

def evaluate_model(test_df):
    return mean_squared_error(
        test_df["user_difficulty_score"],
        test_df["predicted_difficulty"]
    )
