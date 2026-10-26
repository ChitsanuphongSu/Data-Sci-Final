"""Additional runnable chapter 7/12 patterns: mixed columns and learning curves."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.model_selection import (train_test_split, KFold, RandomizedSearchCV,
                                      learning_curve, TimeSeriesSplit, GroupKFold)
from sklearn.metrics import mean_squared_error
from scipy.stats import loguniform

rng = np.random.default_rng(42)
X = pd.DataFrame({'temperature': rng.normal(28, 4, 180),
                  'day_type': rng.choice(['workday', 'holiday'], 180)})
y = 20 + 2 * X.temperature.to_numpy() + 8 * (X.day_type == 'workday') + rng.normal(0, 2, 180)
X.loc[::17, 'temperature'] = np.nan
X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=.2, random_state=42)

numeric = Pipeline([('impute', SimpleImputer(strategy='median')),
                    ('scale', StandardScaler())])
categorical = Pipeline([('impute', SimpleImputer(strategy='most_frequent')),
                        ('encode', OneHotEncoder(handle_unknown='ignore'))])
preprocess = ColumnTransformer([('numeric', numeric, ['temperature']),
                                ('categorical', categorical, ['day_type'])])
pipe = Pipeline([('prepare', preprocess), ('model', Ridge())])
cv = KFold(n_splits=4, shuffle=True, random_state=42)
search = RandomizedSearchCV(pipe, {'model__alpha': loguniform(.01, 100)},
                            n_iter=8, cv=cv, scoring='neg_mean_squared_error', random_state=42)
search.fit(X_dev, y_dev)
print('Best alpha:', search.best_params_)

# Diagnostic curves remain on development, never on final-test data.
sizes, train_scores, val_scores = learning_curve(
    search.best_estimator_, X_dev, y_dev, cv=cv,
    train_sizes=[.3, .6, 1.], scoring='neg_mean_squared_error')
print(pd.DataFrame({'training_rows': sizes,
                    'mean_train_RMSE': np.sqrt(-train_scores).mean(axis=1),
                    'mean_val_RMSE': np.sqrt(-val_scores).mean(axis=1)}))
print('Final test RMSE:', np.sqrt(mean_squared_error(y_test, search.predict(X_test))))

# Split examples only: the synthetic regression above is not a time series.
ordered_X = np.arange(60).reshape(-1, 1)
for train_index, val_index in TimeSeriesSplit(n_splits=3, gap=2).split(ordered_X):
    assert train_index.max() < val_index.min()
    print('Temporal fold:', (train_index.min(), train_index.max()),
          '->', (val_index.min(), val_index.max()))
groups = np.repeat(np.arange(12), 5)
for train_index, val_index in GroupKFold(n_splits=3).split(ordered_X, groups=groups):
    assert not set(groups[train_index]) & set(groups[val_index])
print('Group folds: no person/group appears on both sides.')
