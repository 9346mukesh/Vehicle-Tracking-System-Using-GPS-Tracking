"""Quick script to inspect the actual ML models and get real metrics."""
import warnings
warnings.filterwarnings('ignore')
import pickle, numpy as np, pandas as pd, time
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import os
os.chdir('/Users/mukeshkumarreddy/Downloads/Vehicle')

# Load models
with open('Models/kmeans_start.pkl', 'rb') as f: ks = pickle.load(f)
with open('Models/kmeans_end.pkl', 'rb') as f: ke = pickle.load(f)
with open('Models/xgboost_model.pkl', 'rb') as f: xgb = pickle.load(f)
with open('Models/random_forest_model (1).pkl', 'rb') as f: rf = pickle.load(f)
with open('Models/feature_columns.pkl', 'rb') as f: fc = pickle.load(f)

print("=== K-MEANS PICKUP ===")
print(f"n_clusters: {ks.n_clusters}")
for i, c in enumerate(ks.cluster_centers_):
    print(f"  Cluster {i}: ({c[0]:.4f}, {c[1]:.4f})")

print("\n=== K-MEANS DROPOFF ===")
print(f"n_clusters: {ke.n_clusters}")
for i, c in enumerate(ke.cluster_centers_):
    print(f"  Cluster {i}: ({c[0]:.4f}, {c[1]:.4f})")

# Generate Porto-area points for clustering evaluation
np.random.seed(42)
n = 2000
# Porto coordinates: ~41.14-41.18, -8.68 to -8.58
p_lats = np.random.uniform(41.10, 41.20, n)
p_lons = np.random.uniform(-8.70, -8.55, n)
pickup_pts = np.column_stack([p_lats, p_lons])

d_lats = np.random.uniform(41.10, 41.20, n)
d_lons = np.random.uniform(-8.70, -8.55, n)
dropoff_pts = np.column_stack([d_lats, d_lons])

pc = ks.predict(pickup_pts)
dc = ke.predict(dropoff_pts)

print(f"\n=== CLUSTERING QUALITY (Porto-area points, n={n}) ===")
print(f"Unique pickup clusters used: {len(np.unique(pc))}/{ks.n_clusters}")
print(f"Unique dropoff clusters used: {len(np.unique(dc))}/{ke.n_clusters}")

try:
    sil_p = silhouette_score(pickup_pts, pc)
    print(f"Pickup Silhouette Score: {sil_p:.4f}")
except Exception as e:
    print(f"Pickup Silhouette: {e}")

try:
    sil_d = silhouette_score(dropoff_pts, dc)
    print(f"Dropoff Silhouette Score: {sil_d:.4f}")
except Exception as e:
    print(f"Dropoff Silhouette: {e}")

try:
    dbi_p = davies_bouldin_score(pickup_pts, pc)
    print(f"Pickup Davies-Bouldin Index: {dbi_p:.4f}")
except Exception as e:
    print(f"Pickup DBI: {e}")

try:
    dbi_d = davies_bouldin_score(dropoff_pts, dc)
    print(f"Dropoff Davies-Bouldin Index: {dbi_d:.4f}")
except Exception as e:
    print(f"Dropoff DBI: {e}")

try:
    chi_p = calinski_harabasz_score(pickup_pts, pc)
    print(f"Pickup Calinski-Harabasz: {chi_p:.2f}")
except Exception as e:
    print(f"Pickup CHI: {e}")

try:
    chi_d = calinski_harabasz_score(dropoff_pts, dc)
    print(f"Dropoff Calinski-Harabasz: {chi_d:.2f}")
except Exception as e:
    print(f"Dropoff CHI: {e}")

# Intra-cluster distances (haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    la1, lo1, la2, lo2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dl = la2 - la1; do = lo2 - lo1
    a = np.sin(dl/2)**2 + np.cos(la1)*np.cos(la2)*np.sin(do/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

dists_p = [haversine(p[0], p[1], ks.cluster_centers_[l][0], ks.cluster_centers_[l][1]) for p, l in zip(pickup_pts, pc)]
dists_d = [haversine(p[0], p[1], ke.cluster_centers_[l][0], ke.cluster_centers_[l][1]) for p, l in zip(dropoff_pts, dc)]
print(f"\nPickup intra-cluster: mean={np.mean(dists_p):.3f}km, max={np.max(dists_p):.3f}km")
print(f"Dropoff intra-cluster: mean={np.mean(dists_d):.3f}km, max={np.max(dists_d):.3f}km")

# RF model: what does it predict?
print("\n=== RF MODEL OUTPUT TEST ===")
# Porto trip ~1.5km
feat_porto = pd.DataFrame([[41.15, -8.63, 41.16, -8.62, 1.5, 45.0, 0.8, 15, 10, 2, 2, 0, 0, 
    int(ks.predict([[41.15, -8.63]])[0]), int(ke.predict([[41.16, -8.62]])[0])]], columns=fc)
xgb_pred = xgb.predict(feat_porto)[0]
rf_pred = rf.predict(feat_porto)[0]
print(f"Porto 1.5km trip: XGBoost={xgb_pred:.1f}s ({xgb_pred/60:.1f}min), RF={rf_pred:.1f}s ({rf_pred/60:.1f}min)")

# Bangalore trip ~16km
feat_blr = pd.DataFrame([[12.97, 77.59, 12.85, 77.66, 15.7, 150.0, 0.8, 157, 10, 2, 2, 0, 0,
    int(ks.predict([[12.97, 77.59]])[0]), int(ke.predict([[12.85, 77.66]])[0])]], columns=fc)
xgb_blr = xgb.predict(feat_blr)[0]
rf_blr = rf.predict(feat_blr)[0]
print(f"Bangalore 16km trip: XGBoost={xgb_blr:.1f}s ({xgb_blr/60:.1f}min), RF={rf_blr:.1f}s ({rf_blr/60:.1f}min)")

# Compare XGBoost vs RF on same dataset
print("\n=== XGBOOST vs RANDOM FOREST COMPARISON ===")
from city_config import get_city_config
blr = get_city_config('bangalore')
locations = {k: v for k, v in blr['locations'].items()}
loc_names = list(locations.keys())

xgb_preds = []
rf_preds = []
distances = []
for i in range(min(10, len(loc_names))):
    for j in range(i+1, min(10, len(loc_names))):
        s = locations[loc_names[i]]
        e = locations[loc_names[j]]
        dist = haversine(s[0], s[1], e[0], e[1])
        sc = int(ks.predict([[s[0], s[1]]])[0])
        ec = int(ke.predict([[e[0], e[1]]])[0])
        feat = pd.DataFrame([[s[0], s[1], e[0], e[1], dist, 
            float(np.degrees(np.arctan2(np.sin(np.radians(e[1]-s[1]))*np.cos(np.radians(e[0])),
            np.cos(np.radians(s[0]))*np.sin(np.radians(e[0]))-np.sin(np.radians(s[0]))*np.cos(np.radians(e[0]))*np.cos(np.radians(e[1]-s[1]))))+360)%360,
            0.8, max(2,int(dist*10)), 10, 2, 2, 0, 0, sc, ec]], columns=fc)
        xp = xgb.predict(feat)[0]
        rp = rf.predict(feat)[0]
        xgb_preds.append(xp)
        rf_preds.append(rp)
        distances.append(dist)

xgb_preds = np.array(xgb_preds)
rf_preds = np.array(rf_preds)
errors = xgb_preds - rf_preds

print(f"Routes tested: {len(xgb_preds)}")
print(f"XGBoost mean: {xgb_preds.mean():.1f}s ({xgb_preds.mean()/60:.1f}min)")
print(f"RF mean: {rf_preds.mean():.1f}s ({rf_preds.mean()/60:.1f}min)")
print(f"XGB vs RF RMSE: {np.sqrt(np.mean(errors**2)):.1f}s")
print(f"XGB vs RF MAE: {np.mean(np.abs(errors)):.1f}s")
print(f"Correlation: {np.corrcoef(xgb_preds, rf_preds)[0,1]:.4f}")

# Both models predict DURATION (seconds). The RF is a SECOND ETA estimator.
# For the paper, we should report RF as an alternative ETA model, not fare.
# Fare is computed deterministically via city_config.calculate_fare()

print("\n=== DETERMINISTIC FARE CALCULATION ===")
from city_config import calculate_fare
for d in [5, 10, 15, 20, 30]:
    fare_normal = calculate_fare(d, 'bangalore', 12)
    fare_rush = calculate_fare(d, 'bangalore', 8)
    fare_night = calculate_fare(d, 'bangalore', 23)
    print(f"  {d}km: normal=INR{fare_normal}, rush_am=INR{fare_rush}, late_night=INR{fare_night}")

# End-to-end pipeline timing (100 runs)
print("\n=== PIPELINE TIMING (100 runs) ===")
times = []
for _ in range(100):
    t0 = time.time()
    dist = haversine(12.97, 77.59, 12.85, 77.66)
    bearing = (np.degrees(np.arctan2(
        np.sin(np.radians(77.66-77.59))*np.cos(np.radians(12.85)),
        np.cos(np.radians(12.97))*np.sin(np.radians(12.85))-np.sin(np.radians(12.97))*np.cos(np.radians(12.85))*np.cos(np.radians(77.66-77.59))))+360)%360
    sc = int(ks.predict([[12.97, 77.59]])[0])
    ec = int(ke.predict([[12.85, 77.66]])[0])
    feat = pd.DataFrame([[12.97, 77.59, 12.85, 77.66, dist, bearing, 0.8, max(2,int(dist*10)), 
        10, 2, 2, 0, 0, sc, ec]], columns=fc)
    xgb.predict(feat)
    rf.predict(feat)
    t1 = time.time()
    times.append((t1-t0)*1000)
print(f"  Mean: {np.mean(times):.2f} ms")
print(f"  Median: {np.median(times):.2f} ms")
print(f"  P95: {np.percentile(times, 95):.2f} ms")
print(f"  P99: {np.percentile(times, 99):.2f} ms")

print("\n=== XGBoost MODEL PARAMS ===")
p = xgb.get_params()
for k in ['n_estimators', 'max_depth', 'learning_rate', 'objective', 'reg_alpha', 'reg_lambda', 'subsample', 'colsample_bytree']:
    print(f"  {k}: {p.get(k)}")
print(f"\n=== RF MODEL PARAMS ===")
print(f"  n_estimators: {rf.n_estimators}")
print(f"  max_depth: {rf.max_depth}")
print(f"  n_features: {rf.n_features_in_}")
