import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from preprocess import load_and_preprocess_data

def train_and_save_model():
    # Load and preprocess the data
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    
    # Limit the tree's complexity
# Use a very simple decision tree
    clf = DecisionTreeClassifier(max_depth=5, min_samples_split=5, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate the model on the test data
    accuracy = clf.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # Save the trained model
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    model_path = os.path.join(model_dir, 'delay_model.pkl')
    with open(model_path, 'wb') as model_file:
        pickle.dump(clf, model_file)
    
    print("Model trained and saved successfully!")
    
    # Return the trained classifier
    return clf

def show_feature_importance(clf, X_train):
    # Get feature importance from the decision tree
    feature_importance = clf.feature_importances_
    
    # Sort the features by importance
    sorted_idx = np.argsort(feature_importance)
    features = X_train.columns[sorted_idx]
    importance = feature_importance[sorted_idx]

    # Plot the feature importance
    plt.barh(features, importance)
    plt.xlabel("Feature Importance")
    plt.title("Feature Importance in Decision Tree")
    plt.show()

if __name__ == "__main__":
    # Train the model and save it
    clf = train_and_save_model()  # Now it returns the trained classifier
    
    # Reload the training data for analysis (without splitting it again)
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    
    # Show feature importance to understand which factors are influencing predictions
    show_feature_importance(clf, X_train)
