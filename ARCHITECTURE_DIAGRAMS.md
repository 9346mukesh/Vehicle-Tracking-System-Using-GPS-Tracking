# SYSTEM ARCHITECTURE DIAGRAMS & VISUAL REPRESENTATIONS
## For IEEE Research Paper Publication

---

## DIAGRAM 1: Complete System Architecture Stack

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     GPS-BASED VEHICLE TRACKING SYSTEM                        ║
║                   WITH ML-ENHANCED ROUTE PREDICTION                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────┐
│ TIER-1: USER INTERFACE LAYER (Frontend - HTML/CSS/JavaScript)               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │  ADMIN          │  │  DRIVER         │  │  CUSTOMER       │            │
│  │  DASHBOARD      │  │  DASHBOARD      │  │  DASHBOARD      │            │
│  │                 │  │                 │  │                 │            │
│  │ • User Mgmt     │  │ • Live Location │  │ • Book Ride     │            │
│  │ • Analytics     │  │ • Earnings      │  │ • Track Driver  │            │
│  │ • Reports       │  │ • Rating        │  │ • Rate Driver   │            │
│  │ • Settings      │  │ • Rides History │  │ • View ETA      │            │
│  │ • Monitoring    │  │ • Statistics    │  │ • Payment       │            │
│  │ • Real-time     │  │                 │  │                 │            │
│  │   Fleet Map     │  │                 │  │                 │            │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘            │
│           │                   │                     │                       │
│           └───────────────────┼─────────────────────┘                       │
│                               │                                              │
│                  ┌────────────────────────┐                                 │
│                  │  HTML/CSS/JS Layer     │                                 │
│                  │  • Maps (Google Maps)  │                                 │
│                  │  • Real-time updates   │                                 │
│                  │  • WebSocket listener  │                                 │
│                  └────────────────────────┘                                 │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓ (HTTP/WebSocket)
┌──────────────────────────────────────────────────────────────────────────────┐
│ TIER-2: API & COMMUNICATION LAYER (Flask Application)                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                    REST API ENDPOINTS                             │    │
│  │  POST   /api/rides/create              (Customer books ride)     │    │
│  │  GET    /api/rides/{id}                (Get ride details)        │    │
│  │  PUT    /api/rides/{id}/accept         (Driver accepts)          │    │
│  │  PUT    /api/rides/{id}/complete       (Mark ride complete)      │    │
│  │  POST   /api/auth/login                (User authentication)     │    │
│  │  GET    /api/analytics/dashboard       (Admin analytics)         │    │
│  │  GET    /api/drivers/available         (Find nearby drivers)     │    │
│  │  POST   /api/ratings/create            (Submit rating/feedback)  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                  WEBSOCKET EVENTS (Real-time)                    │    │
│  │  'connect'              (Client connects to server)              │    │
│  │  'gps_update'           (Driver sends GPS location)              │    │
│  │  'location_broadcast'   (Server broadcasts to room)              │    │
│  │  'ride_accepted'        (Driver accepted notification)           │    │
│  │  'ride_completed'       (Trip finished event)                    │    │
│  │  'disconnect'           (Client disconnects)                     │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │             REQUEST PROCESSING PIPELINE                          │    │
│  │  1. Authentication & Authorization                               │    │
│  │  2. Input Validation & Sanitization                              │    │
│  │  3. Business Logic Execution                                     │    │
│  │  4. ML Model Inference                                           │    │
│  │  5. Database Transaction                                         │    │
│  │  6. Response Serialization & Broadcasting                        │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│ TIER-3: BUSINESS LOGIC LAYER (Core Processing)                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐                        │
│  │  RIDE MANAGEMENT     │  │  DRIVER MANAGEMENT   │                        │
│  │  Module              │  │  Module              │                        │
│  │                      │  │                      │                        │
│  │ • Create ride        │  │ • Find available     │                        │
│  │ • Update status      │  │   drivers            │                        │
│  │ • Calculate distance │  │ • Assign driver      │                        │
│  │ • Process payment    │  │ • Update location    │                        │
│  │ • Send notifications │  │ • Calculate earnings │                        │
│  │ • Store in DB        │  │ • Update rating      │                        │
│  └──────────────────────┘  └──────────────────────┘                        │
│                                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐                        │
│  │  ROUTE ENGINE        │  │  ANALYTICS ENGINE    │                        │
│  │  Module              │  │  Module              │                        │
│  │                      │  │                      │                        │
│  │ • Haversine distance │  │ • Trip statistics    │                        │
│  │ • Bearing calc       │  │ • Revenue tracking   │                        │
│  │ • Route interpolate  │  │ • User metrics       │                        │
│  │ • ETA calculation    │  │ • Heatmap gen        │                        │
│  │ • Path optimization  │  │ • Trend analysis     │                        │
│  │ • Traffic handling   │  │ • Performance KPIs   │                        │
│  └──────────────────────┘  └──────────────────────┘                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│ TIER-4: MACHINE LEARNING INFERENCE LAYER                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐        │
│  │  XGBoost Model               │  │  Random Forest Model         │        │
│  │  (ETA & Distance Prediction) │  │  (Fare Prediction)          │        │
│  │                              │  │                              │        │
│  │  Input Features:             │  │  Input Features:             │        │
│  │  • pickup_lat, pickup_lon    │  │  • distance                 │        │
│  │  • dropoff_lat, dropoff_lon  │  │  • duration                 │        │
│  │  • hour_of_day               │  │  • hour_of_day              │        │
│  │  • day_of_week               │  │  • is_rush_hour             │        │
│  │  • traffic_level             │  │  • day_of_week              │        │
│  │  • weather_condition         │  │  • city                     │        │
│  │                              │  │                              │        │
│  │  Output:                     │  │  Output:                     │        │
│  │  • eta_minutes (float)       │  │  • base_fare (float)        │        │
│  │  • distance_km (float)       │  │  • adjusted_fare (float)    │        │
│  │  • confidence_score          │  │  • confidence_score         │        │
│  └──────────────────────────────┘  └──────────────────────────────┘        │
│                                                                              │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐        │
│  │  K-Means (Pickup Cluster)    │  │  K-Means (Dropoff Cluster)   │        │
│  │  (Start Point Prediction)    │  │  (Destination Prediction)    │        │
│  │                              │  │                              │        │
│  │  Input:                      │  │  Input:                      │        │
│  │  • Historical pickup points  │  │  • Historical dropoff points │        │
│  │  • 150+ clusters trained     │  │  • 180+ clusters trained     │        │
│  │                              │  │                              │        │
│  │  Output:                     │  │  Output:                     │        │
│  │  • Cluster ID                │  │  • Cluster ID                │        │
│  │  • Cluster center (lat, lon) │  │  • Cluster center (lat, lon) │        │
│  │  • Distance to center        │  │  • Distance to center        │        │
│  │  • Density score             │  │  • Density score             │        │
│  └──────────────────────────────┘  └──────────────────────────────┘        │
│                                                                              │
│  Feature Engineering & Preprocessing:                                       │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ • Normalize coordinates to [0,1] range                            │    │
│  │ • Extract temporal features (hour, day, month)                    │    │
│  │ • Encode categorical variables (city, day_of_week)               │    │
│  │ • Calculate derived features (distance, bearing)                  │    │
│  │ • Handle missing values & outliers                                │    │
│  │ • Scale features using fitted scaler                              │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│ TIER-5: DATA PERSISTENCE LAYER (SQLAlchemy ORM)                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────┐  ┌───────────────────────┐                      │
│  │  USER MODEL           │  │  VEHICLE MODEL        │                      │
│  │  ┌─────────────────┐  │  │  ┌─────────────────┐  │                      │
│  │  │ id (PK)         │  │  │  │ id (PK)         │  │                      │
│  │  │ username (U)    │  │  │  │ driver_id (FK)  │  │                      │
│  │  │ email (U)       │  │  │  │ vehicle_number  │  │                      │
│  │  │ password_hash   │  │  │  │ vehicle_type    │  │                      │
│  │  │ role (enum)     │  │  │  │ status          │  │                      │
│  │  │ full_name       │  │  │  │ current_lat     │  │                      │
│  │  │ phone           │  │  │  │ current_lon     │  │                      │
│  │  │ created_at (I)  │  │  │  │ rating          │  │                      │
│  │  │ is_active       │  │  │  │ total_trips     │  │                      │
│  │  └─────────────────┘  │  │  └─────────────────┘  │                      │
│  └───────────────────────┘  └───────────────────────┘                      │
│                                                                              │
│  ┌───────────────────────┐  ┌───────────────────────┐                      │
│  │  RIDE MODEL           │  │  SYSTEM SETTINGS      │                      │
│  │  ┌─────────────────┐  │  │  ┌─────────────────┐  │                      │
│  │  │ id (PK)         │  │  │  │ id (PK)         │  │                      │
│  │  │ customer_id (FK)│  │  │  │ key (U)         │  │                      │
│  │  │ driver_id (FK)  │  │  │  │ value           │  │                      │
│  │  │ pickup_lat      │  │  │  │ description     │  │                      │
│  │  │ pickup_lon      │  │  │  └─────────────────┘  │                      │
│  │  │ dropoff_lat     │  │  │                       │                      │
│  │  │ dropoff_lon     │  │  │  KEY SETTINGS:        │                      │
│  │  │ distance        │  │  │  • max_distance_km   │                      │
│  │  │ duration        │  │  │  • min_rating        │                      │
│  │  │ fare            │  │  │  • base_fare         │                      │
│  │  │ status          │  │  │  • per_km_rate       │                      │
│  │  │ rating          │  │  │  • surge_multiplier  │                      │
│  │  │ feedback        │  │  │  • default_city      │                      │
│  │  │ created_at (I)  │  │  │                       │                      │
│  │  │ completed_at    │  │  │                       │                      │
│  │  └─────────────────┘  │  └─────────────────────┘  │                      │
│  └───────────────────────┘  └───────────────────────┘                      │
│                                                                              │
│  Database: SQLite (instance/vehicle_tracking.db)                            │
│  ORM: SQLAlchemy                                                            │
│  Indexes: (username, email, vehicle_number, created_at)                    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│ TIER-6: EXTERNAL SERVICES & UTILITIES                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐  │
│  │ GEOGRAPHIC UTILS   │  │ CRYPTOGRAPHY       │  │ SERIALIZATION      │  │
│  │                    │  │                    │  │                    │  │
│  │ • Haversine        │  │ • Password hashing │  │ • JSON encoder     │  │
│  │   distance         │  │   (Werkzeug)       │  │ • Pickle for ML    │  │
│  │ • Bearing          │  │ • Password verify  │  │ • DataFrame I/O    │  │
│  │   calculation      │  │                    │  │                    │  │
│  │ • Route            │  │                    │  │                    │  │
│  │   interpolation    │  │                    │  │                    │  │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘  │
│                                                                              │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐  │
│  │ NOTIFICATIONS      │  │ LOGGING            │  │ CACHING (Optional) │  │
│  │                    │  │                    │  │                    │  │
│  │ • Email alerts     │  │ • Application logs │  │ • Redis cache      │  │
│  │ • SMS (SMS API)    │  │ • Error tracking   │  │ • Session storage  │  │
│  │ • Push notif       │  │ • Audit trail      │  │ • Model cache      │  │
│  │ • In-app messages  │  │                    │  │                    │  │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## DIAGRAM 2: Ride Lifecycle State Machine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          RIDE STATUS FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

                              START
                                │
                                ↓
                    ┌──────────────────────┐
                    │  PENDING             │
                    │  [Waiting for Driver]│
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ↓                     ↓
           ┌────────────────┐   ┌─────────────────┐
           │ ACCEPTED       │   │ CANCELLED       │ (End)
           │ [Driver agreed]│   │ [No driver]     │
           └────────┬───────┘   └─────────────────┘
                    │
                    ↓
           ┌────────────────┐
           │ IN_PROGRESS    │
           │ [Trip ongoing] │
           └────────┬───────┘
                    │
                    ↓
           ┌────────────────┐
           │ COMPLETED      │ (End)
           │ [Trip finished]│
           └────────────────┘
                    │
                    ↓
           ┌────────────────┐
           │ RATED          │
           │ [Feedback done]│
           └────────────────┘ (End)


Timestamps Recorded at Each Stage:
┌──────────────┬──────────────────────────────────────────────┐
│ Status       │ Timestamp Field(s)                          │
├──────────────┼──────────────────────────────────────────────┤
│ PENDING      │ created_at                                   │
│ ACCEPTED     │ accepted_at                                  │
│ IN_PROGRESS  │ started_at                                   │
│ COMPLETED    │ completed_at                                 │
│ RATED        │ feedback recorded at completed_at + delta    │
└──────────────┴──────────────────────────────────────────────┘
```

---

## DIAGRAM 3: GPS Tracking & Real-time Update Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      REAL-TIME GPS STREAMING                                │
│                         (1 SECOND CYCLE)                                    │
└─────────────────────────────────────────────────────────────────────────────┘

DRIVER CLIENT                    SERVER                    CUSTOMER CLIENT
┌──────────────┐            ┌──────────────┐             ┌──────────────┐
│              │            │              │             │              │
│  GPS Sensor  │            │              │             │              │
│      ↓       │            │              │             │              │
│ ┌────────┐   │            │              │             │              │
│ │Get Loc │   │            │              │             │              │
│ │Lat/Lon │   │            │              │             │              │
│ │Speed   │   │            │              │             │              │
│ │Bearing │   │            │              │             │              │
│ └────────┘   │            │              │             │              │
│      │       │            │              │             │              │
│      ↓       │            │              │             │              │
│ Package GPS  │            │              │             │              │
│  as JSON     │            │              │             │              │
│      │       │            │              │             │              │
│      │       │ Emit       │              │             │              │
│      └───────┤ gps_update │              │             │              │
│              │────────────→              │             │              │
│              │            │              │             │              │
│              │            │ Step 7a:     │             │              │
│              │            │ Validate     │             │              │
│              │            │ Accuracy     │             │              │
│              │            ├→ [dev<50m]   │             │              │
│              │            │              │             │              │
│              │            │ Step 7b:     │             │              │
│              │            │ Distance     │             │              │
│              │            │ Calculation  │             │              │
│              │            ├→ haversine() │             │              │
│              │            │              │             │              │
│              │            │ Step 7c:     │             │              │
│              │            │ Bearing      │             │              │
│              │            │ Calculation  │             │              │
│              │            ├→ atan2()     │             │              │
│              │            │              │             │              │
│              │            │ Step 7d:     │             │              │
│              │            │ ETA Calc     │             │              │
│              │            │ ML Predict   │             │              │
│              │            ├→ xgb_model   │             │              │
│              │            │              │             │              │
│              │            │ Step 7e:     │             │              │
│              │            │ DB Update    │             │              │
│              │            ├→ INSERT gps  │             │              │
│              │            │ UPDATE ride  │             │              │
│              │            │              │             │              │
│              │            │ Step 7f:     │             │              │
│              │            │ Broadcast    │             │              │
│              │            │ to Room      │             │              │
│              │            │ ride_12345   │             │              │
│              │            │              │ Emit       │              │
│              │            │              │─────────────→ Display      │
│              │            │              │ location_  │ • Map update │
│              │            │              │ broadcast  │ • ETA update │
│              │            │              │            │ • Distance   │
│              │            │              │            │ • Speed      │
│              │            │              │            └──────────────┘
│              │            │              │
│              │ ← ← ← ← ← ← ← ← ← ← ← ← ←  REPEATS EVERY 1 SECOND
│              │            │              │
│              │            │              │
│              │            ├→ Step 7g:    │
│              │            │ Check        │
│              │            │ Conditions   │
│              │            │              │
│              │            │ IF dist<100m │
│              │            │ → Step 8     │
│              │            │   (Pickup)   │
│              │            │              │
│              │            │ ELSE         │
│              │            │ → Continue   │
│              │            │   tracking   │
│              │            │              │
│              │            │              │
└──────────────┘            └──────────────┘             └──────────────┘

Total Cycle Time: ~1000 ms
  - GPS reading: 50-100 ms
  - Network transmission: 50-100 ms
  - Server processing: 200-300 ms
  - Database write: 100-200 ms
  - WebSocket broadcast: 100-150 ms
  - Client rendering: 200-300 ms
  
Latency to Customer: 500-1000 ms (typically <800ms)
```

---

## DIAGRAM 4: Machine Learning Inference Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     ML MODEL INFERENCE SEQUENCE                             │
└─────────────────────────────────────────────────────────────────────────────┘

INPUT: Ride Booking Request
┌─────────────────────────────────────┐
│ Customer Inputs:                    │
│ • pickup_lat, pickup_lon            │
│ • dropoff_lat, dropoff_lon          │
│ • current_time                      │
│ • city ('bangalore' or 'porto')     │
└─────────────────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ FEATURE EXTRACTION                  │
│                                     │
│ ├─ Distance Calculation:            │
│ │  d = haversine(lat_p, lon_p,     │
│ │       lat_d, lon_d)               │
│ │  Range: [0.1, 50] km              │
│ │                                   │
│ ├─ Temporal Features:               │
│ │  hour = current_time.hour()       │
│ │  day_of_week = current_time.weekday()
│ │  is_rush_hour = bool              │
│ │  month = current_time.month()     │
│ │                                   │
│ ├─ Location Clustering:             │
│ │  start_cluster = kmeans_start    │
│ │                  .predict([lat_p,lon_p])
│ │  end_cluster = kmeans_end        │
│ │                .predict([lat_d,lon_d])
│ │                                   │
│ ├─ Traffic Pattern:                 │
│ │  traffic_level = get_traffic()    │
│ │  Values: [0.5, 1.0, 1.5, 2.0]     │
│ │                                   │
│ ├─ City-specific:                   │
│ │  currency = city_config[city]     │
│ │  base_fare = city_config[base_fare]
│ │  per_km_rate = city_config[rate]  │
│ └─────────────────────────────────  │
└─────────────────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ FEATURE NORMALIZATION               │
│                                     │
│ Features scaled to [0,1] range:     │
│ • Coordinates normalized           │
│ • Distance scaled                  │
│ • Time features encoded            │
│ • Categorical vars one-hot encoded │
│                                     │
│ Shape: [n_samples, n_features]     │
│ Total features: ~25-30             │
└─────────────────────────────────────┘
          ↓
      ┌────┴────┐
      ↓         ↓
┌──────────┐  ┌──────────┐
│ XGBoost  │  │ RandomFr │
│ Model    │  │ Forest   │
│          │  │ Model    │
│ INPUT:   │  │ INPUT:   │
│ • coords │  │ • dist   │
│ • time   │  │ • time   │
│ • traffic│  │ • hour   │
│          │  │ • cluster│
│          │  │          │
│ PROCESS: │  │ PROCESS: │
│ 100+     │  │ 100+     │
│ trees    │  │ trees    │
│          │  │          │
│ OUTPUT:  │  │ OUTPUT:  │
│ ETA (min)│  │ Base Fare│
└────┬─────┘  └────┬─────┘
     │             │
     ↓             ↓
  ┌────────────────────┐
  │ XGBoost Result     │ XGBoost Result
  │ eta_pred = 22.5   │ (ETA Minutes)
  │ conf_score = 0.87 │
  └────────────────────┘
     
  ┌────────────────────┐
  │ RF Result          │ RandomForest Result
  │ fare_pred = 220.5 │ (Base Fare)
  │ conf_score = 0.92 │
  └────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ PRICING CALCULATION                 │
│                                     │
│ base_fare = 220.5 (from RF)        │
│ distance_charge = 12 * 15 = 180    │
│ subtotal = 220.5 + 180 = 400.5     │
│                                     │
│ traffic_multiplier = 2.0 (rush)    │
│ final_fare = 400.5 * 2.0 = 801     │
│                                     │
│ surge_multiplier = 1.0 (normal)    │
│ FINAL_FARE = 801 * 1.0 = ₹801      │
└─────────────────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│ OUTPUT PACKAGE                      │
│                                     │
│ {                                   │
│   "ride_id": 12345,                │
│   "eta_minutes": 22.5,             │
│   "fare_estimate": 801,            │
│   "distance": 15.0,                │
│   "confidence_score": 0.90,        │
│   "pickup_cluster": 5,             │
│   "dropoff_cluster": 12,           │
│   "base_fare": 220.5,              │
│   "breakdown": {                   │
│     "base": 220.5,                │
│     "distance_charge": 180,       │
│     "traffic_multiplier": 2.0,    │
│     "surge_multiplier": 1.0       │
│   }                                │
│ }                                  │
└─────────────────────────────────────┘
          ↓
       TO CLIENT: Display to customer
```

---

## DIAGRAM 5: Database Schema & Relationships

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DATABASE SCHEMA (ER MODEL)                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐                      ┌─────────────────────┐
│    USERS            │      1    ╱╲    N   │    VEHICLES         │
│  ┌────────────────┐ │      ├───→ HAS ←───┤  ┌────────────────┐ │
│  │ id (PK)        │ │      │              │  │ id (PK)        │ │
│  │ username (UQ)  │ │      │              │  │ driver_id (FK) │ │
│  │ email (UQ)     │ │      │              │  │ vehicle_number │ │
│  │ password_hash  │ │      │              │  │ vehicle_type   │ │
│  │ role (enum)    │ │      │              │  │ status (enum)  │ │
│  │ full_name      │ │      │              │  │ current_lat    │ │
│  │ phone          │ │      │              │  │ current_lon    │ │
│  │ created_at (I) │ │      │              │  │ rating         │ │
│  │ is_active      │ │      │              │  │ total_trips    │ │
│  └────────────────┘ │      │              │  └────────────────┘ │
└─────────────────────┘      │              └─────────────────────┘
         │                   │
         │        ╱╲         │
         │    M   HAS (as    │
         │ ─────→    Customer)
         │        ╲╱         │
         │                   │
         │        ╱╲         │        ╱╲
         │    M   HAS (as    │    N   ASSIGNS
         │ ─────→    Driver) ├────────→ DRIVER
         │        ╲╱         │        ╲╱
         │                   │
         └────────┬──────────┘
                  │
                  ↓
        ┌─────────────────────┐
        │    RIDES            │
        │  ┌────────────────┐ │
        │  │ id (PK)        │ │
        │  │ customer_id(FK)│ │
        │  │ driver_id(FK)  │ │
        │  │ pickup_lat     │ │
        │  │ pickup_lon     │ │
        │  │ dropoff_lat    │ │
        │  │ dropoff_lon    │ │
        │  │ distance (I)   │ │
        │  │ duration       │ │
        │  │ fare           │ │
        │  │ status (enum)  │ │
        │  │ city           │ │
        │  │ created_at (I) │ │
        │  │ accepted_at    │ │
        │  │ started_at     │ │
        │  │ completed_at   │ │
        │  │ rating         │ │
        │  │ feedback       │ │
        │  └────────────────┘ │
        └─────────────────────┘


INDEXES (Performance Optimization):
┌────────────────────────────────────────────────┐
│ TABLE        │ INDEX_NAME      │ COLUMNS      │
├──────────────┼─────────────────┼──────────────┤
│ users        │ idx_username    │ username     │
│              │ idx_email       │ email        │
│              │ idx_created     │ created_at   │
│              │                 │              │
│ vehicles     │ idx_driver      │ driver_id    │
│              │ idx_vehicle_no  │ vehicle_no   │
│              │ idx_status      │ status       │
│              │                 │              │
│ rides        │ idx_customer    │ customer_id  │
│              │ idx_driver      │ driver_id    │
│              │ idx_created     │ created_at   │
│              │ idx_status      │ status       │
│              │ idx_city        │ city         │
└────────────────────────────────────────────────┘

CONSTRAINT RULES:
┌──────────────────────────────────────────────────┐
│ • Foreign key integrity checks                   │
│ • NOT NULL constraints on critical fields        │
│ • UNIQUE constraints on username, email          │
│ • ENUM constraints on role, status, city         │
│ • Default values for timestamps                  │
│ • Cascading deletes (optional) for sensitive ops │
└──────────────────────────────────────────────────┘
```

---

## DIAGRAM 6: Data Flow - Complete Ride Simulation

```
                    ┌────────────────────────────────┐
                    │   RIDE BOOKING SEQUENCE         │
                    │   (Time in ms)                  │
                    └────────────────────────────────┘

T=0ms   ┌────────────────────────────────────────────┐
        │ Customer clicks "Book Ride"                │
        │ API: POST /api/rides/create                │
        │ Payload: {pickup, dropoff, city}           │
        └────────────────────────────────────────────┘
           │
           ↓
T=100ms ┌────────────────────────────────────────────┐
        │ Server Validates Input                     │
        │ • Check coordinates in bounds              │
        │ • Validate customer exists                 │
        │ • Check not duplicate ride                 │
        └────────────────────────────────────────────┘
           │
           ↓
T=200ms ┌────────────────────────────────────────────┐
        │ Feature Extraction & ML Inference          │
        │ • Calculate distance (haversine)           │
        │ • Extract time features                    │
        │ • Run XGBoost (ETA prediction) → 22.5 min │
        │ • Run RandomForest (fare) → ₹220.5        │
        │ • Run K-means (clusters) → id:5, id:12    │
        └────────────────────────────────────────────┘
           │
           ↓
T=400ms ┌────────────────────────────────────────────┐
        │ Calculate Final Pricing                    │
        │ • Base: ₹220.5                             │
        │ • Distance: ₹180 (12×15)                   │
        │ • Traffic multiplier: 2.0x (rush hour)     │
        │ • Final: ₹801                              │
        └────────────────────────────────────────────┘
           │
           ↓
T=500ms ┌────────────────────────────────────────────┐
        │ Create Ride Record (DB)                    │
        │ INSERT into rides table                    │
        │ status='pending'                           │
        │ created_at=current_timestamp               │
        └────────────────────────────────────────────┘
           │
           ↓
T=600ms ┌────────────────────────────────────────────┐
        │ Find & Assign Available Drivers            │
        │ • Query: status='available', dist<5km      │
        │ • Rank by proximity + rating               │
        │ • Assign top driver (ID: 42)               │
        │ • UPDATE rides SET driver_id=42            │
        └────────────────────────────────────────────┘
           │
           ↓
T=700ms ┌────────────────────────────────────────────┐
        │ Send Driver Notification                   │
        │ WebSocket: 'new_ride_available'            │
        │ Driver name: John, Rating: 4.8/5.0         │
        │ Estimated pickup: 5 minutes                │
        └────────────────────────────────────────────┘
           │
           ↓
T=800ms ┌────────────────────────────────────────────┐
        │ Return Response to Customer                │
        │ HTTP 200 OK                                │
        │ {ride_id: 12345, eta: 22.5, fare: 801}    │
        └────────────────────────────────────────────┘
           │
           ↓
T=1000ms ┌───────────────────────────────────────────┐
        │ Driver Accepts Ride (30s decision window)  │
        │ UPDATE rides SET status='accepted'         │
        │ accepted_at=current_timestamp              │
        │ WebSocket: 'ride_accepted' → Customer     │
        └───────────────────────────────────────────┘
           │
           ↓
T=2000ms ┌───────────────────────────────────────────┐
        │ Driver Initiates Navigation                │
        │ GPS tracking starts                        │
        │ WebSocket room created: 'ride_12345'      │
        │ Customer joined to room                   │
        └───────────────────────────────────────────┘
           │
           ↓ (Every 1 second)
T=3000ms ┌───────────────────────────────────────────┐
T=4000ms │ GPS Stream: Driver → Server → Customer    │
T=5000ms │ [50 GPS points for this segment]          │
...      │ Each point: distance calc, ETA recalc    │
T=25000ms│ Real-time map updates on customer app    │
        └───────────────────────────────────────────┘
           │
           ↓
T=26000ms ┌───────────────────────────────────────────┐
        │ Driver Arrives at Pickup                   │
        │ distance_remaining < 100m detected         │
        │ Step 8: Pickup completion                  │
        │ Ride status: 'in_progress'                 │
        │ started_at=current_timestamp               │
        └───────────────────────────────────────────┘
           │
           ↓ (Every 1 second)
T=27000ms ┌───────────────────────────────────────────┐
T=28000ms │ Continue GPS Streaming (to dropoff)       │
...       │ [Another 50+ GPS points]                  │
T=47000ms │ Real-time tracking continues             │
        └───────────────────────────────────────────┘
           │
           ↓
T=48000ms ┌───────────────────────────────────────────┐
        │ Driver Arrives at Dropoff                  │
        │ distance_remaining < 100m detected         │
        │ Step 9: Trip completion                    │
        │ Ride status: 'completed'                   │
        │ completed_at=current_timestamp             │
        │ Final fare: ₹801                           │
        └───────────────────────────────────────────┘
           │
           ↓
T=49000ms ┌───────────────────────────────────────────┐
        │ Show Rating & Feedback Screen              │
        │ Customer rates driver 1-5 stars            │
        │ Optional feedback text                     │
        └───────────────────────────────────────────┘
           │
           ↓
T=50000ms ┌───────────────────────────────────────────┐
        │ Submit Rating (Step 10)                    │
        │ POST /api/ratings/create                   │
        │ UPDATE rides SET rating=4.5, feedback=...  │
        │ UPDATE vehicles SET rating=avg(...)        │
        └───────────────────────────────────────────┘
           │
           ↓
T=51000ms ┌───────────────────────────────────────────┐
        │ Analytics Update (Step 11)                 │
        │ • Increment trip count                     │
        │ • Add to revenue                           │
        │ • Update driver statistics                 │
        │ • Refresh dashboard                        │
        └───────────────────────────────────────────┘
           │
           ↓
T=52000ms ┌───────────────────────────────────────────┐
        │ ✓ RIDE COMPLETE & CLOSED                   │
        │ Both user & driver can start new rides     │
        └───────────────────────────────────────────┘

TOTAL TIME: ~52 seconds (simulation)
REAL TIME SIMULATED: ~25 minutes
COMPRESSION RATIO: 28.8x
```

---

**Document Version**: 1.0
**Content**: Comprehensive visual diagrams for IEEE publication
**Last Updated**: February 2026
