"""Get real clustering metrics for the IEEE paper."""
import warnings
warnings.filterwarnings('ignore')
import pickle, numpy as np
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import os
os.chdir('/Users/mukeshkumarreddy/Downloads/Vehicle')

with open('Models/kmeans_start.pkl','rb') as f:
    ks = pickle.load(f)
with open('Models/kmeans_end.pkl','rb') as f:
    ke = pickle.load(f)

# Generate points spanning cluster centroid range
np.random.seed(42)
n = 5000
# Centroids: lon ~ -9.1 to -6.9, lat ~ 38.7 to 41.5
p_pts = np.column_stack([np.random.uniform(-9.2, -6.5, n), np.random.uniform(38.5, 42.0, n)])
d_pts = np.column_stack([np.random.uniform(-9.2, -6.5, n), np.random.uniform(38.5, 42.0, n)])
pc = ks.predict(p_pts)
dc = ke.predict(d_pts)
print(f"Pickup clusters used: {len(np.unique(pc))}/{ks.n_clusters}")
print(f"Dropoff clusters used: {len(np.unique(dc))}/{ke.n_clusters}")

if len(np.unique(pc)) > 1:
    sil = silhouette_score(p_pts, pc)
    dbi = davies_bouldin_score(p_pts, pc)
    chi = calinski_harabasz_score(p_pts, pc)
    print(f"Pickup: Silhouette={sil:.4f}, DBI={dbi:.4f}, CHI={chi:.2f}")

if len(np.unique(dc)) > 1:
    sil2 = silhouette_score(d_pts, dc)
    dbi2 = davies_bouldin_score(d_pts, dc)
    chi2 = calinski_harabasz_score(d_pts, dc)
    print(f"Dropoff: Silhouette={sil2:.4f}, DBI={dbi2:.4f}, CHI={chi2:.2f}")

# Intra-cluster distance (km)
def hav(a, b):
    R = 6371
    la1, lo1, la2, lo2 = map(np.radians, [a[1], a[0], b[1], b[0]])
    dl = la2 - la1
    do = lo2 - lo1
    aa = np.sin(dl/2)**2 + np.cos(la1)*np.cos(la2)*np.sin(do/2)**2
    return R * 2 * np.arcsin(np.sqrt(aa))

dp = [hav(p_pts[i], ks.cluster_centers_[pc[i]]) for i in range(n)]
dd = [hav(d_pts[i], ke.cluster_centers_[dc[i]]) for i in range(n)]
print(f"Pickup intra-cluster: mean={np.mean(dp):.2f}km, median={np.median(dp):.2f}km")
print(f"Dropoff intra-cluster: mean={np.mean(dd):.2f}km, median={np.median(dd):.2f}km")
