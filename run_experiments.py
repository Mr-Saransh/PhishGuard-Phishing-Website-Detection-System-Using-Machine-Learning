"""
PhishGuard Experiment & Model Training Runner
Trains models on UCI Phishing Websites (ID 327) and saves exact metrics, models, and evaluation plots.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve
)

def run_pipeline():
    os.makedirs('charts', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # 1. Load Dataset
    csv_path = 'data/phishing_websites_uci_327.csv'
    if os.path.exists(csv_path):
        print(f"Loading local cached dataset from {csv_path}...")
        df = pd.read_csv(csv_path)
    else:
        print("Fetching dataset from UCI ML Repository (ID=327)...")
        from ucimlrepo import fetch_ucirepo
        ds = fetch_ucirepo(id=327)
        df = pd.concat([ds.data.features, ds.data.targets], axis=1)
        df.to_csv(csv_path, index=False)
        
    print(f"Dataset shape: {df.shape}")
    
    # Identify target and features
    target_col = 'result' if 'result' in df.columns else 'Result'
    feature_cols = [c for c in df.columns if c != target_col]
    
    X = df[feature_cols].copy()
    y_raw = df[target_col].copy()
    
    # In original UCI 327: 1 = Legitimate, -1 = Phishing
    # For standard binary classification in cybersecurity:
    # 1 = Phishing (Malicious / Alert), 0 = Legitimate (Benign)
    # This aligns Precision/Recall with catching phishing websites!
    y = (y_raw == -1).astype(int)
    
    # Check duplicates and missing values
    missing_count = int(df.isnull().sum().sum())
    duplicate_count = int(df.duplicated().sum())
    total_samples = len(df)
    phishing_count = int(y.sum())
    legit_count = int(total_samples - phishing_count)
    
    print(f"Total samples: {total_samples}")
    print(f"Missing values: {missing_count}")
    print(f"Duplicates: {duplicate_count}")
    print(f"Class distribution: Phishing (-1 -> 1) = {phishing_count} ({phishing_count/total_samples*100:.2f}%), Legitimate (1 -> 0) = {legit_count} ({legit_count/total_samples*100:.2f}%)")
    
    # Visual 1: Target Class Distribution
    plt.figure(figsize=(7, 4.5), dpi=300)
    palette = ['#2b5c8f', '#d9534f']
    counts = [legit_count, phishing_count]
    labels = ['Legitimate (Safe)', 'Phishing (Malicious)']
    bars = plt.bar(labels, counts, color=palette, width=0.5, edgecolor='#333333', linewidth=1)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 100, f"{yval:,} ({yval/total_samples*100:.1f}%)", ha='center', va='bottom', fontsize=11, fontweight='bold')
    plt.title('UCI Phishing Websites Dataset — Class Distribution (N=11,055)', fontsize=13, fontweight='bold', pad=15)
    plt.ylabel('Number of Websites', fontsize=11)
    plt.ylim(0, 7500)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('charts/class_distribution.png')
    plt.close()
    
    # 2. Stratified Train-Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Train set: {X_train.shape[0]} samples, Test set: {X_test.shape[0]} samples")
    
    # 3. Model Training
    models = {
        "Dummy (Baseline)": DummyClassifier(strategy="most_frequent"),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs'),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    }
    
    results = {}
    roc_data = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Probabilities for ROC
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)[:, 1]
            roc_auc = roc_auc_score(y_test, y_proba)
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            roc_data[name] = (fpr, tpr, roc_auc)
        else:
            y_proba = None
            roc_auc = 0.5
            roc_data[name] = ([0, 1], [0, 1], 0.5)
            
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()
        report = classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing'], output_dict=True)
        
        results[name] = {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1),
            "roc_auc": float(roc_auc),
            "confusion_matrix": cm,
            "classification_report": report
        }
        print(f"{name} -> Accuracy: {acc*100:.2f}%, Precision: {prec*100:.2f}%, Recall: {rec*100:.2f}%, F1: {f1*100:.2f}%, ROC-AUC: {roc_auc:.4f}")
        
    # Visual 2: Confusion Matrices
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5), dpi=300)
    for i, (name, res) in enumerate(results.items()):
        cm = np.array(res["confusion_matrix"])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i],
                    cbar=False, annot_kws={"size": 13, "weight": "bold"},
                    xticklabels=['Legitimate (0)', 'Phishing (1)'],
                    yticklabels=['Legitimate (0)', 'Phishing (1)'])
        axes[i].set_title(f"{name}\nAcc: {res['accuracy']*100:.2f}% | F1: {res['f1_score']*100:.2f}%", fontsize=11, fontweight='bold')
        axes[i].set_xlabel('Predicted Label', fontsize=10)
        axes[i].set_ylabel('True Label', fontsize=10)
    plt.suptitle('Confusion Matrix Comparison on Test Set (N=2,211)', fontsize=14, fontweight='bold', y=1.03)
    plt.tight_layout()
    plt.savefig('charts/confusion_matrices.png', bbox_inches='tight')
    plt.close()
    
    # Visual 3: Model Metrics Comparison Bar Chart
    metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
    df_metrics = pd.DataFrame({
        m_name: [results[m_name]['accuracy'],
                 results[m_name]['precision'],
                 results[m_name]['recall'],
                 results[m_name]['f1_score'],
                 results[m_name]['roc_auc']]
        for m_name in results
    }, index=metrics_names)
    
    plt.figure(figsize=(9, 5), dpi=300)
    bar_width = 0.25
    x_indices = np.arange(len(metrics_names))
    colors = ['#888888', '#2e7d32', '#1565c0']
    
    for idx, (m_name, color) in enumerate(zip(results.keys(), colors)):
        vals = [results[m_name]['accuracy'],
                results[m_name]['precision'],
                results[m_name]['recall'],
                results[m_name]['f1_score'],
                results[m_name]['roc_auc']]
        bars = plt.bar(x_indices + idx * bar_width, vals, bar_width, label=m_name, color=color, edgecolor='#222', linewidth=0.8)
        for bar in bars:
            h = bar.get_height()
            if h > 0.05:
                plt.text(bar.get_x() + bar.get_width()/2.0, h + 0.015, f"{h*100:.1f}%", ha='center', va='bottom', fontsize=8, rotation=90)
                
    plt.xlabel('Evaluation Metrics', fontsize=12, fontweight='bold', labelpad=10)
    plt.ylabel('Score (0.0 to 1.0)', fontsize=12, fontweight='bold')
    plt.title('Performance Comparison Across Evaluated Classifiers', fontsize=13, fontweight='bold', pad=15)
    plt.xticks(x_indices + bar_width, metrics_names, fontsize=11)
    plt.ylim(0, 1.15)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig('charts/model_comparison.png')
    plt.close()
    
    # Visual 4: ROC Curves
    plt.figure(figsize=(7, 5.5), dpi=300)
    for m_name, (fpr, tpr, auc_val) in roc_data.items():
        if m_name == "Dummy (Baseline)":
            plt.plot(fpr, tpr, linestyle='--', color='gray', label=f'{m_name} (AUC = {auc_val:.2f})')
        elif m_name == "Logistic Regression":
            plt.plot(fpr, tpr, color='#2e7d32', lw=2, label=f'{m_name} (AUC = {auc_val:.4f})')
        else:
            plt.plot(fpr, tpr, color='#1565c0', lw=2.5, label=f'{m_name} (AUC = {auc_val:.4f})')
    plt.plot([0, 1], [0, 1], 'k:', alpha=0.5)
    plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=11, fontweight='bold')
    plt.ylabel('True Positive Rate (Sensitivity / Recall)', fontsize=11, fontweight='bold')
    plt.title('Receiver Operating Characteristic (ROC) Curves', fontsize=13, fontweight='bold', pad=15)
    plt.legend(loc='lower right', frameon=True)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('charts/roc_curves.png')
    plt.close()
    
    # Visual 5: Feature Importances from Random Forest
    rf_model = models["Random Forest"]
    importances = rf_model.feature_importances_
    feat_names = X.columns
    sorted_idx = np.argsort(importances)[::-1]
    
    # Top 12 features
    top_n = 12
    top_indices = sorted_idx[:top_n]
    top_feats = [feat_names[i] for i in top_indices]
    top_scores = [importances[i] for i in top_indices]
    
    plt.figure(figsize=(9, 5.5), dpi=300)
    colors = plt.cm.Blues(np.linspace(0.85, 0.45, top_n))
    y_pos = np.arange(top_n)
    plt.barh(y_pos, top_scores[::-1], color=colors[::-1], edgecolor='#333333', linewidth=0.8)
    plt.yticks(y_pos, top_feats[::-1], fontsize=10)
    plt.xlabel('Gini Feature Importance Score', fontsize=11, fontweight='bold')
    plt.title('Top 12 Most Influential Features (Random Forest)', fontsize=13, fontweight='bold', pad=15)
    for i, v in enumerate(top_scores[::-1]):
        plt.text(v + 0.003, i, f"{v:.4f}", va='center', fontsize=9, fontweight='bold')
    plt.xlim(0, max(top_scores) * 1.15)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('charts/feature_importance.png')
    plt.close()
    
    # Save results json
    summary_data = {
        "dataset": {
            "total_instances": total_samples,
            "total_features": len(feature_cols),
            "missing_values": missing_count,
            "duplicate_records": duplicate_count,
            "phishing_count": phishing_count,
            "legitimate_count": legit_count,
            "test_size": len(y_test),
            "train_size": len(y_train)
        },
        "models": results,
        "top_features": list(zip(top_feats, [float(s) for s in top_scores]))
    }
    
    with open('experiment_results.json', 'w') as f:
        json.dump(summary_data, f, indent=4)
        
    print("\nExperiment completed successfully! Results written to experiment_results.json.")
    print("Generated charts: class_distribution.png, confusion_matrices.png, model_comparison.png, roc_curves.png, feature_importance.png")

if __name__ == "__main__":
    run_pipeline()
