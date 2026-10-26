"""Runnable teaching examples. Synthetic data only; no downloads."""
import numpy as np
import pandas as pd
from sklearn.datasets import make_regression, make_classification, make_blobs
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, StratifiedKFold
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
    classification_report, confusion_matrix, roc_auc_score, silhouette_score)

def regression():
    X, y = make_regression(n_samples=240, n_features=3, noise=15, random_state=42)
    X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=.2, random_state=42)
    pipe = Pipeline([('poly', PolynomialFeatures(include_bias=False)),
                     ('scale', StandardScaler()), ('model', Ridge())])
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    search = GridSearchCV(pipe, {'poly__degree': [1, 2], 'model__alpha': [.1, 1, 10]},
                          cv=cv, scoring='neg_mean_squared_error')
    search.fit(X_dev, y_dev)
    # GridSearchCV refits the chosen pipeline on all development data by default.
    pred = search.predict(X_test)
    print('REGRESSION best:', search.best_params_)
    print('Final test:', {'MAE': mean_absolute_error(y_test, pred),
          'RMSE': np.sqrt(mean_squared_error(y_test, pred)), 'R2': r2_score(y_test, pred)})

def classification():
    X, y = make_classification(n_samples=600, n_features=8, n_informative=5,
                               weights=[.8, .2], random_state=42)
    X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=.2,
                                                   stratify=y, random_state=42)
    pipe = Pipeline([('scale', StandardScaler()), ('model', LogisticRegression(max_iter=2000))])
    # Compare all candidates on the SAME folds; use macro F1 for this exercise.
    candidates = [
        {'model': [LogisticRegression(max_iter=2000)], 'model__C': [.1, 1, 10]},
        {'model': [KNeighborsClassifier()], 'model__n_neighbors': [3, 7, 15]},
        {'model': [DecisionTreeClassifier(random_state=42)], 'model__max_depth': [3, 6]},
        {'model': [RandomForestClassifier(n_estimators=100, random_state=42)],
         'model__max_depth': [4, None]},
        {'model': [GradientBoostingClassifier(random_state=42)],
         'model__n_estimators': [50, 100], 'model__learning_rate': [.05]},
    ]
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    search = GridSearchCV(pipe, candidates, cv=cv, scoring='f1_macro')
    search.fit(X_dev, y_dev)
    pred = search.predict(X_test)
    positive_index = list(search.classes_).index(1)
    probability = search.predict_proba(X_test)[:, positive_index]
    print('CLASSIFICATION best:', search.best_params_)
    print(confusion_matrix(y_test, pred, labels=[0, 1]))
    print(classification_report(y_test, pred, zero_division=0))
    print('ROC-AUC:', roc_auc_score(y_test, probability))

def clustering():
    X, _ = make_blobs(n_samples=240, centers=3, cluster_std=.8, random_state=42)
    # This is descriptive clustering of this dataset, not a future-data score.
    scaler = StandardScaler()
    Z = scaler.fit_transform(X)
    rows, models = [], {}
    for k in range(2, 7):
        model = KMeans(n_clusters=k, n_init=10, random_state=42).fit(Z)
        rows.append({'k': k, 'inertia': model.inertia_,
                     'silhouette': silhouette_score(Z, model.labels_)})
        models[k] = model
    results = pd.DataFrame(rows)
    chosen_k = int(results.loc[results.silhouette.idxmax(), 'k'])
    model = models[chosen_k]
    print('CLUSTERING descriptive metrics:\n', results.to_string(index=False))
    print('Suggested K (check domain usefulness too):', chosen_k)
    print('Centers in original units:\n', scaler.inverse_transform(model.cluster_centers_))
    profile = pd.DataFrame(X, columns=['x1', 'x2']).assign(cluster=model.labels_)
    print(profile.groupby('cluster').agg(['size', 'mean', 'median']))

if __name__ == '__main__':
    regression()
    classification()
    clustering()
