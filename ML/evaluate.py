from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt

def evaluate_model(y_true, y_pred, title="Confusion Matrix"):
    """
    Evaluates ML models with common metrics and plots confusion matrix.
    """
    print(f"--- Evaluation: {title} ---")
    
    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:")
    print(cm)
    
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, zero_division=0))
    print(f"Accuracy Score: {accuracy_score(y_true, y_pred):.4f}")
    
    # Plotting
    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()
    
    return classification_report(y_true, y_pred, output_dict=True, zero_division=0)
