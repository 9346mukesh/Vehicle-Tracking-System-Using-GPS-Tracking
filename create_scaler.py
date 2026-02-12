"""
Simple script to create a scaler.pkl file for the project
Run this if scaler.pkl is missing from the Models folder
"""
import pickle
from sklearn.preprocessing import StandardScaler

# Create a dummy scaler (it will be fit with actual data during prediction)
scaler = StandardScaler()

# Save to Models folder
with open('Models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("✓ scaler.pkl created successfully in Models folder")
