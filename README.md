# 🚗 RideShare Pro - Vehicle Tracking System

## 🔧 QUICK FIX FOR LOGIN ISSUES

### Problem
You cannot login with the credentials shown on the login page.

### Solution (Choose ONE method)

#### Method 1: Using Batch File (EASIEST - Windows Only)
1. **Double-click** `FIX_DATABASE.bat`
2. Wait for it to complete
3. **Double-click** `START_APP.bat`
4. Open browser to http://localhost:5000

#### Method 2: Using Command Line
```bash
# Step 1: Fix the database
python complete_fix.py

# Step 2: Start the application
python app_complete.py
```

---

## 🎯 Login Credentials (After Running Fix)

### Admin Dashboard
- **Username:** `admin`
- **Password:** `admin123`
- **URL:** http://localhost:5001/admin_dashboard

### Driver Dashboard
- **Username:** `driver1`
- **Password:** `password123`
- **URL:** http://localhost:5001/driver_dashboard

### Customer Dashboard
- **Username:** `customer1`
- **Password:** `password123`
- **URL:** http://localhost:5001/customer_dashboard

---

## 📋 What the Fix Does

The `complete_fix.py` script will:

1. ✅ Check if database exists at `instance/rideshare.db`
2. ✅ Create database if it doesn't exist
3. ✅ Create all necessary tables (users, vehicles, rides, system_settings)
4. ✅ Delete any existing users (to prevent conflicts)
5. ✅ Create fresh users with correct passwords:
   - Admin (username: admin, password: admin123)
   - Driver (username: driver1, password: password123)
   - Customer (username: customer1, password: password123)
6. ✅ Verify all passwords work correctly

---

## 🚀 How to Use the Application

### Starting the Server

**Option 1: Using Batch File (Windows)**
```
Double-click START_APP.bat
```

**Option 2: Using Command Line**
```bash
python app_complete.py
```

The server will start on: **http://localhost:5000**

### Accessing Different Dashboards

1. Go to http://localhost:5000
2. Click "Get Started" or "Login"
3. Enter credentials based on which dashboard you want:
   - **Admin** → username: `admin`, password: `admin123`
   - **Driver** → username: `driver1`, password: `password123`
   - **Customer** → username: `customer1`, password: `password123`

---

## 🎨 Application Features

### For Customers 👤
- Book rides with real-time fare estimation
- Track driver location in real-time
- View ride history
- Rate and review drivers
- Voice command support

### For Drivers 🚗
- View and accept ride requests
- Navigate to pickup/dropoff locations
- Update availability status
- Track earnings and trips
- Real-time GPS tracking

### For Admins 📊
- Monitor all active rides
- Track all vehicles in real-time
- View system statistics
- Manage users and vehicles
- Analytics dashboard

---

## 🗂️ Project Structure

```
Vehicle/
├── app_complete.py          # Main application (USE THIS)
├── complete_fix.py          # Database fix script
├── FIX_DATABASE.bat         # Quick fix (Windows)
├── START_APP.bat            # Quick start (Windows)
├── models.py                # Database models
├── city_config.py           # City configurations
├── instance/                # Database folder
│   └── rideshare.db         # SQLite database (created by fix script)
├── Models/                  # ML models
│   ├── xgboost_model.pkl
│   ├── random_forest_model (1).pkl
│   ├── kmeans_start.pkl
│   ├── kmeans_end.pkl
│   └── feature_columns.pkl
├── templates/               # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── customer_dashboard.html
│   ├── driver_dashboard.html
│   └── admin_dashboard.html
└── static/                  # CSS and JavaScript
    ├── css/
    └── js/
```

---

## 🐛 Troubleshooting

### Issue: "Unable to open database file"
**Solution:** Run `python complete_fix.py` first

### Issue: "Invalid credentials" when logging in
**Solution:** 
1. Make sure you ran `complete_fix.py`
2. Use the exact credentials (case-sensitive):
   - admin / admin123
   - driver1 / password123
   - customer1 / password123

### Issue: "Module not found" errors
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution:** 
1. Stop any other Flask applications
2. Or change port in `app_complete.py` (line ~580):
   ```python
   socketio.run(app, debug=True, host='0.0.0.0', port=5001)
   ```

### Issue: Database is locked
**Solution:**
1. Stop all running instances of `app_complete.py`
2. Delete `instance/rideshare.db`
3. Run `python complete_fix.py` again

---

## 📝 Important Notes

1. **Always run `complete_fix.py` first** if you're having login issues
2. **Use `app_complete.py`** to start the application (not app.py or app_new.py)
3. **Passwords are case-sensitive**
4. **Make sure port 5000 is available** before starting

---

## ✅ Success Checklist

- [ ] Ran `complete_fix.py` successfully
- [ ] Saw "SETUP COMPLETED SUCCESSFULLY!" message
- [ ] Started `app_complete.py`
- [ ] Opened http://localhost:5000 in browser
- [ ] Successfully logged in with demo credentials

---

## 🆘 Still Having Issues?

If you're still having problems after running the fix script:

1. **Check the database file exists:**
   - Path: `C:\Users\VAIBHAVRAI\OneDrive\Desktop\Vehicle\instance\rideshare.db`
   
2. **Check for error messages** in the console when running `complete_fix.py`

3. **Try deleting everything and starting fresh:**
   ```bash
   # Delete the instance folder
   rmdir /s instance
   
   # Run fix script
   python complete_fix.py
   
   # Start application
   python app_complete.py
   ```

---

## 📞 Quick Commands Reference

```bash
# Fix database and reset passwords
python complete_fix.py

# Start the application
python app_complete.py

# Check what users exist in database
python fix_passwords.py

# Initialize fresh database (alternative)
python setup_database.py
```

---

**Created by:** RideShare Pro Team  
**Last Updated:** January 2026  
**Version:** 1.0.0
