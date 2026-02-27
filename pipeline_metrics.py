"""Get pipeline timing and RF vs XGB comparison for the IEEE paper."""
import warnings
warnings.filterwarnings('ignore')
import pickle, numpy as np, pandas as pd, time
import os
os.chdir('/Users/mukeshkumarreddy/Downloads/Vehicle')

with open('Models/kmeans_start.pkl','rb') as f: ks = pickle.load(f)
with open('Models/kmeans_end.pkl','rb') as f: ke = pickle.load(f)
with open('Models/xgboost_model.pkl','rb') as f: xgb = pickle.load(f)
with open('Models/random_forest_model (1).pkl','rb') as f: rf = pickle.load(f)
with open('Models/feature_columns.pkl','rb') as f: fc = pickle.load(f)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    la1, lo1, la2, lo2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dl = la2 - la1
    do = lo2 - lo1
    a = np.sin(dl/2)**2 + np.cos(la1)*np.cos(la2)*np.sin(do/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def bearing(lat1, lon1, lat2, lon2):
    la1, lo1, la2, lo2 = map(np.radians, [lat1, lon1, lat2, lon2])
    do = lo2 - lo1
    x = np.sin(do) * np.cos(la2)
    y = np.cos(la1)*np.sin(la2) - np.sin(la1)*np.cos(la2)*np.cos(do)
    return (np.degrees(np.arctan2(x, y)) + 360) % 360

# Porto test routes
routes = [
    ("City Center-Beach", 41.1579, -8.6291, 41.1496, -8.6810),
    ("Airport-Downtown", 41.2480, -8.6813, 41.1579, -8.6291),
    ("University-Hospital", 41.1525, -8.6397, 41.1630, -8.5847),
    ("Boavista-Matosinhos", 41.1585, -8.6392, 41.1820, -8.6940),
    ("Porto-Braga", 41.1579, -8.6291, 41.5518, -8.4229),
    ("Porto-Gaia", 41.1579, -8.6291, 41.1239, -8.6118),
    ("Campanha-SBento", 41.1484, -8.5854, 41.1455, -8.6100),
    ("Ribeira-Foz", 41.1402, -8.6132, 41.1519, -8.6785),
]

print("=== XGBoost vs RF on Porto routes ===")
xgb_preds = []
rf_preds = []
xgb_times = []
rf_times = []

for name, lat1, lon1, lat2, lon2 in routes:
    dist = haversine(lat1, lon1, lat2, lon2)
    bear = bearing(lat1, lon1, lat2, lon2)
    sc = int(ks.predict([[lat1, lon1]])[0])
    ec = int(ke.predict([[lat2, lon2]])[0])
    npts = max(2, int(dist*10))
    
    for h in [6, 8, 12, 17, 22]:
        for d in [0, 2, 5]:
            is_wk = 1 if d in [5,6] else 0
            is_rush = 1 if h in [7,8,9,17,18,19] else 0
            feat = pd.DataFrame([[lat1, lon1, lat2, lon2, dist, bear, 0.8, npts,
                h, d, 2, is_wk, is_rush, sc, ec]], columns=fc)
            
            t0 = time.time()
            xp = xgb.predict(feat)[0]
            t1 = time.time()
            xgb_times.append((t1-t0)*1000)
            
            t0 = time.time()
            rp = rf.predict(feat)[0]
            t1 = time.time()
            rf_times.append((t1-t0)*1000)
            
            xgb_preds.append(xp)
            rf_preds.append(rp)

xp = np.array(xgb_preds)
rp = np.array(rf_preds)
diff = xp - rp

print(f"Tests: {len(xp)}")
print(f"XGBoost: mean={xp.mean()/60:.1f}min, range={xp.min()/60:.1f}-{xp.max()/60:.1f}min")
print(f"RF:      mean={rp.mean()/60:.1f}min, range={rp.min()/60:.1f}-{rp.max()/60:.1f}min")
print(f"XGB vs RF RMSE: {np.sqrt(np.mean(diff**2))/60:.2f} min")
print(f"XGB vs RF MAE: {np.mean(np.abs(diff))/60:.2f} min")
print(f"Correlation: {np.corrcoef(xp, rp)[0,1]:.4f}")
print(f"XGB inference: mean={np.mean(xgb_times):.3f}ms, p95={np.percentile(xgb_times,95):.3f}ms")
print(f"RF inference: mean={np.mean(rf_times):.3f}ms, p95={np.percentile(rf_times,95):.3f}ms")

# Full pipeline timing
print("\n=== Full Pipeline Timing (200 runs) ===")
pipe_times = []
for _ in range(200):
    name, lat1, lon1, lat2, lon2 = routes[np.random.randint(len(routes))]
    h = np.random.choice([6,8,12,17,22])
    d = np.random.choice([0,2,5])
    
    t0 = time.time()
    dist = haversine(lat1, lon1, lat2, lon2)
    bear = bearing(lat1, lon1, lat2, lon2)
    sc = int(ks.predict([[lat1, lon1]])[0])
    ec = int(ke.predict([[lat2, lon2]])[0])
    npts = max(2, int(dist*10))
    is_wk = 1 if d in [5,6] else 0
    is_rush = 1 if h in [7,8,9,17,18,19] else 0
    feat = pd.DataFrame([[lat1, lon1, lat2, lon2, dist, bear, 0.8, npts,
        h, d, 2, is_wk, is_rush, sc, ec]], columns=fc)
    xgb.predict(feat)
    rf.predict(feat)
    t1 = time.time()
    pipe_times.append((t1-t0)*1000)

print(f"Mean: {np.mean(pipe_times):.2f}ms")
print(f"Median: {np.median(pipe_times):.2f}ms")
print(f"P95: {np.percentile(pipe_times,95):.2f}ms")
print(f"P99: {np.percentile(pipe_times,99):.2f}ms")
print(f"Std: {np.std(pipe_times):.2f}ms")

# Model properties
print("\n=== Model Properties ===")
p = xgb.get_params()
print(f"XGBoost: n_estimators={p['n_estimators']}, max_depth={p['max_depth']}, lr={p['learning_rate']}, objective={p['objective']}")
print(f"RF: n_estimators={rf.n_estimators}, max_depth={rf.max_depth}, n_features={rf.n_features_in_}")
print(f"K-Means pickup: k={ks.n_clusters}, inertia={ks.inertia_:.4f}, iters={ks.n_iter_}")
print(f"K-Means dropoff: k={ke.n_clusters}, inertia={ke.inertia_:.4f}, iters={ke.n_iter_}")
print(f"Features: {fc}")

# Fare calculation test
from city_config import calculate_fare
print("\n=== Fare Calculation (Deterministic) ===")
for d in [5, 10, 15, 20, 30]:
    fn = calculate_fare(d, 'bangalore', 12)
    fr = calculate_fare(d, 'bangalore', 8)
    fln = calculate_fare(d, 'bangalore', 23)
    print(f"  {d}km: normal=INR{fn}, rush=INR{fr}, night=INR{fln}")
