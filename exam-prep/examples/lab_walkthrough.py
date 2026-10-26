"""Reference practice solutions for P01-P05; preserve original notebooks.
Run from any working directory. Produces results in exam-prep/results.
"""
from pathlib import Path
import json, platform
import numpy as np
import pandas as pd
import sklearn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array, check_is_fitted

BASE = Path(__file__).resolve().parents[2]
OUT = BASE / 'exam-prep' / 'results'
OUT.mkdir(exist_ok=True)

def rmse(y, pred): return float(np.sqrt(mean_squared_error(y, pred)))
def metrics(y, pred):
    return {'MAE': float(mean_absolute_error(y, pred)), 'RMSE': rmse(y, pred),
            'R2': float(r2_score(y, pred))}

def features(df, quadratic=False):
    X = df[['temp_forecast_c', 'working_day']].copy()
    if quadratic: X['temp_squared'] = X.temp_forecast_c ** 2
    return X

def energy_lab():
    dev = pd.read_csv(BASE / 'quiz' / 'regression_development.csv', parse_dates=['date'])
    assert dev.date.is_monotonic_increasing and len(dev) == 90
    train, val = dev.iloc[:72], dev.iloc[72:]
    p01 = []
    for name, cols in [('Simple', ['temp_forecast_c']),
                       ('Multiple', ['temp_forecast_c', 'working_day'])]:
        model = LinearRegression().fit(train[cols], train.energy_kwh)
        p01.append({'model': name, **metrics(val.energy_kwh, model.predict(val[cols]))})
    pd.DataFrame(p01).to_csv(OUT / 'p01.csv', index=False)
    specs = [('A', False, LinearRegression()), ('B', True, LinearRegression()),
             ('C', True, make_pipeline(StandardScaler(), Ridge(alpha=.1))),
             ('D', True, make_pipeline(StandardScaler(), Ridge(alpha=10)))]
    rows = []
    for name, quadratic, model in specs:
        model.fit(features(train, quadratic), train.energy_kwh)
        rows.append({'model': name, **metrics(val.energy_kwh, model.predict(features(val, quadratic)))})
    # Protocol: within <0.01 kWh of the best, prefer simpler; then lower alpha.
    best = min(r['RMSE'] for r in rows)
    chosen = next(r['model'] for r in rows if r['RMSE'] - best < .01)
    pd.DataFrame(rows).to_csv(OUT / 'p03_validation.csv', index=False)
    pred_a = specs[0][2].predict(features(val))
    residual = val.energy_kwh.to_numpy() - pred_a
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(pred_a, residual)
    axes[0].set(xlabel='Fitted energy (kWh)', ylabel='Residual = actual - predicted', title='Validation residuals: model A')
    axes[1].plot(val.date, residual, marker='o')
    axes[1].set(xlabel='Date', ylabel='Residual (kWh)', title='Residuals over time')
    for ax in axes: ax.axhline(0, color='black', linewidth=.8)
    fig.autofmt_xdate(); fig.tight_layout(); fig.savefig(OUT / 'p03_residuals.png', dpi=140); plt.close(fig)
    # Only now open final-test data, refit chosen model, and report once.
    name, quadratic, model = next(s for s in specs if s[0] == chosen)
    model.fit(features(dev, quadratic), dev.energy_kwh)
    test = pd.read_csv(BASE / 'quiz' / 'regression_final_test.csv', parse_dates=['date'])
    assert len(test) == 30 and dev.date.max() < test.date.min()
    final = {'chosen': chosen, **metrics(test.energy_kwh, model.predict(features(test, quadratic)))}
    (OUT / 'p03_final.json').write_text(json.dumps(final, indent=2), encoding='utf-8')
    # P04: each method starts its own generator with the same specified seed.
    boot = []
    X, y, n = features(dev), dev.energy_kwh, len(dev)
    for method in ['ordinary', 'moving_block']:
        rng = np.random.default_rng(20260922)
        values = []
        for _ in range(300):
            if method == 'ordinary': indices = rng.integers(0, n, size=n)
            else:
                starts = rng.integers(0, n - 7 + 1, size=int(np.ceil(n / 7)))
                indices = np.concatenate([np.arange(s, s + 7) for s in starts])[:n]
            fit = LinearRegression().fit(X.iloc[indices], y.iloc[indices])
            values.append(fit.coef_[0])
        lo, hi = np.percentile(values, [2.5, 97.5])
        boot.append({'method': method, 'lower_2.5': lo, 'upper_97.5': hi})
    pd.DataFrame(boot).to_csv(OUT / 'p04.csv', index=False)
    print('P01', p01, '\nP03 validation', rows, '\nP03 final', final, '\nP04', boot)

def bias_variance_lab():
    def sine(seed, n):
        rng = np.random.default_rng(seed)
        x = rng.uniform(0, 6, (n, 1))
        return x, np.sin(x[:, 0]) + rng.normal(0, .25, n)
    xv, yv = sine(2026, 200)
    rows = []
    for seed in [11, 22, 33]:
        x, y = sine(seed, 35)
        for degree in [1, 3, 12]:
            model = make_pipeline(PolynomialFeatures(degree=degree, include_bias=False),
                                  StandardScaler(), LinearRegression()).fit(x, y)
            rows.append({'seed': seed, 'degree': degree, 'train_RMSE': rmse(y, model.predict(x)),
                         'val_RMSE': rmse(yv, model.predict(xv)),
                         'prediction_at_2': float(model.predict([[2.]])[0])})
    pd.DataFrame(rows).to_csv(OUT / 'p02.csv', index=False)
    print('P02\n', pd.DataFrame(rows).to_string(index=False))

class GaussianFeatures(TransformerMixin, BaseEstimator):
    def __init__(self, N=12, width_factor=.8):
        self.N = N
        self.width_factor = width_factor
    def fit(self, X, y=None):
        X = check_array(X)
        if X.shape[1] != 1 or not isinstance(self.N, (int, np.integer)) or self.N < 2:
            raise ValueError('One feature and integer N >= 2 required')
        if not np.isfinite(self.width_factor) or self.width_factor <= 0 or X.max() <= X.min():
            raise ValueError('Positive finite width and nonconstant training X required')
        self.n_features_in_ = 1
        self.centers_ = np.linspace(X.min(), X.max(), self.N)
        self.sigma_ = self.width_factor * (self.centers_[1] - self.centers_[0])
        return self
    def transform(self, X):
        check_is_fitted(self, ['centers_', 'sigma_'])
        X = check_array(X)
        if X.shape[1] != 1: raise ValueError('One feature required')
        return np.exp(-.5 * ((X[:, 0, None] - self.centers_[None, :]) / self.sigma_) ** 2)

def gaussian_lab():
    def data(seed, n):
        rng = np.random.default_rng(seed)
        X = rng.uniform(0, 10, (n, 1))
        return X, np.sin(X[:, 0]) + rng.normal(0, .15, n)
    x, y = data(41, 50); xv, yv = data(42, 100)
    poly = PolynomialFeatures(degree=3, include_bias=False).fit_transform(x[:3])
    basis = GaussianFeatures(N=12, width_factor=.8)
    B = basis.fit_transform(x)
    scaler = StandardScaler()
    Z = scaler.fit_transform(B); Zv = scaler.transform(basis.transform(xv))
    models = [('OLS', LinearRegression()), ('Ridge', Ridge(alpha=.1)),
              ('Lasso', Lasso(alpha=.001, max_iter=100000, tol=1e-6))]
    rows = []
    for name, model in models:
        model.fit(Z, y)
        rows.append({'model': name, 'train_RMSE': rmse(y, model.predict(Z)),
                     'val_RMSE': rmse(yv, model.predict(Zv)),
                     'zero_coefficients': int(np.sum(model.coef_ == 0))})
    best = min(r['val_RMSE'] for r in rows)
    index = next(i for i, r in enumerate(rows) if r['val_RMSE'] - best <= 1e-6)
    name, model = models[index]
    # P05 explicitly forbids refitting; retain train-fitted model, centers and scale.
    xt, yt = data(43, 100)
    final = {'chosen': name, 'test_RMSE': rmse(yt, model.predict(scaler.transform(basis.transform(xt)))),
             'centers': basis.centers_.tolist(), 'sigma': float(basis.sigma_),
             'train_basis_shape': list(B.shape), 'polynomial_first_three': poly.tolist()}
    pd.DataFrame(rows).to_csv(OUT / 'p05_validation.csv', index=False)
    (OUT / 'p05_final.json').write_text(json.dumps(final, indent=2), encoding='utf-8')
    grid = np.linspace(0, 10, 300)[:, None]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(grid[:, 0], basis.transform(grid)); axes[0].set(title='12 train-fitted Gaussian bases', xlabel='x')
    axes[1].scatter(x[:, 0], y, s=15, alpha=.5, label='train')
    axes[1].plot(grid[:, 0], np.sin(grid[:, 0]), label='true mean')
    axes[1].plot(grid[:, 0], model.predict(scaler.transform(basis.transform(grid))), label=name)
    axes[1].set(title='Selected model (no refit)', xlabel='x'); axes[1].legend()
    fig.tight_layout(); fig.savefig(OUT / 'p05_basis.png', dpi=140); plt.close(fig)
    print('P05', rows, '\nP05 final', final)

if __name__ == '__main__':
    versions = {'python': platform.python_version(), 'numpy': np.__version__,
                'pandas': pd.__version__, 'sklearn': sklearn.__version__}
    (OUT / 'versions.json').write_text(json.dumps(versions, indent=2), encoding='utf-8')
    energy_lab(); bias_variance_lab(); gaussian_lab()
