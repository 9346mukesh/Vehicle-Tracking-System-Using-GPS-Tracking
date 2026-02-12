// Tracking Page JavaScript with Real-time GPS Updates
let map;
let socket;
let vehicleMarkers = {};
let vehiclePolylines = {};
let activeVehicles = new Set();

// Initialize map
function initMap() {
    map = L.map('map').setView([41.1579, -8.6291], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    console.log('Map initialized');
}

// Initialize Socket.IO connection
function initSocket() {
    socket = io();
    
    socket.on('connect', function() {
        console.log('Connected to server');
    });

    socket.on('gps_update', function(data) {
        updateVehicleOnMap(data);
    });

    socket.on('vehicle_completed', function(data) {
        handleVehicleCompletion(data.vehicle_id);
    });

    socket.on('disconnect', function() {
        console.log('Disconnected from server');
    });
}

// Create custom vehicle icon
function createVehicleIcon(vehicleId) {
    return L.divIcon({
        className: 'vehicle-marker',
        html: `<div style="background: #2563eb; color: white; padding: 8px 12px; border-radius: 20px; font-weight: bold; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4); white-space: nowrap;">
                <i class="fas fa-car" style="margin-right: 5px;"></i>${vehicleId}
               </div>`,
        iconSize: [100, 40],
        iconAnchor: [50, 20]
    });
}

// Update vehicle on map
function updateVehicleOnMap(data) {
    const vehicleId = data.vehicle_id;
    const latLng = [data.latitude, data.longitude];

    // Create or update marker
    if (!vehicleMarkers[vehicleId]) {
        vehicleMarkers[vehicleId] = L.marker(latLng, {
            icon: createVehicleIcon(vehicleId)
        }).addTo(map);

        vehicleMarkers[vehicleId].bindPopup(`
            <div style="color: #0f172a; min-width: 200px;">
                <h4 style="margin-bottom: 10px; color: #2563eb;">
                    <i class="fas fa-car"></i> ${vehicleId}
                </h4>
                <p><strong>Speed:</strong> ${data.speed.toFixed(2)} km/h</p>
                <p><strong>Progress:</strong> ${data.progress.toFixed(1)}%</p>
                <p><strong>Distance:</strong> ${data.distance_covered.toFixed(2)} km</p>
                <p><strong>Time:</strong> ${formatTime(data.elapsed_time)}</p>
            </div>
        `);

        // Initialize polyline
        vehiclePolylines[vehicleId] = L.polyline([], {
            color: '#2563eb',
            weight: 4,
            opacity: 0.7
        }).addTo(map);
    } else {
        vehicleMarkers[vehicleId].setLatLng(latLng);
        vehicleMarkers[vehicleId].getPopup().setContent(`
            <div style="color: #0f172a; min-width: 200px;">
                <h4 style="margin-bottom: 10px; color: #2563eb;">
                    <i class="fas fa-car"></i> ${vehicleId}
                </h4>
                <p><strong>Speed:</strong> ${data.speed.toFixed(2)} km/h</p>
                <p><strong>Progress:</strong> ${data.progress.toFixed(1)}%</p>
                <p><strong>Distance:</strong> ${data.distance_covered.toFixed(2)} km</p>
                <p><strong>Time:</strong> ${formatTime(data.elapsed_time)}</p>
            </div>
        `);
    }

    // Update polyline
    vehiclePolylines[vehicleId].addLatLng(latLng);

    // Update active vehicles list
    updateActiveVehiclesList(vehicleId, data);

    // Update metrics
    updateMetrics();
}

// Handle vehicle completion
function handleVehicleCompletion(vehicleId) {
    if (vehicleMarkers[vehicleId]) {
        setTimeout(() => {
            map.removeLayer(vehicleMarkers[vehicleId]);
            delete vehicleMarkers[vehicleId];
            
            if (vehiclePolylines[vehicleId]) {
                map.removeLayer(vehiclePolylines[vehicleId]);
                delete vehiclePolylines[vehicleId];
            }
            
            activeVehicles.delete(vehicleId);
            updateActiveVehiclesList();
            updateMetrics();
        }, 3000);
    }
}

// Update active vehicles list in sidebar
function updateActiveVehiclesList(vehicleId, data) {
    activeVehicles.add(vehicleId);
    
    const container = document.getElementById('activeVehicles');
    
    if (activeVehicles.size === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-car"></i>
                <p>No active vehicles</p>
            </div>
        `;
        return;
    }

    let html = '';
    activeVehicles.forEach(vid => {
        const progress = data && vid === vehicleId ? data.progress : 0;
        html += `
            <div class="vehicle-item" onclick="focusVehicle('${vid}')">
                <div class="vehicle-header">
                    <span class="vehicle-id">${vid}</span>
                    <span class="vehicle-status active">Active</span>
                </div>
                <div class="vehicle-progress">
                    <div class="progress-bar" style="width: ${progress}%"></div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Focus on specific vehicle
function focusVehicle(vehicleId) {
    if (vehicleMarkers[vehicleId]) {
        map.setView(vehicleMarkers[vehicleId].getLatLng(), 15);
        vehicleMarkers[vehicleId].openPopup();
    }
}

// Update metrics panel
function updateMetrics() {
    document.getElementById('totalVehicles').textContent = activeVehicles.size;
    
    let totalDistance = 0;
    Object.values(vehiclePolylines).forEach(polyline => {
        const latlngs = polyline.getLatLngs();
        for (let i = 1; i < latlngs.length; i++) {
            totalDistance += latlngs[i-1].distanceTo(latlngs[i]) / 1000;
        }
    });
    
    document.getElementById('totalDistance').textContent = totalDistance.toFixed(2) + ' km';
}

// Format time helper
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}m ${secs}s`;
}

// Handle preset selection
document.getElementById('presetSelect')?.addEventListener('change', function(e) {
    const presets = {
        'porto1': {
            startLat: 41.1579,
            startLon: -8.6291,
            endLat: 41.1496,
            endLon: -8.6109
        },
        'porto2': {
            startLat: 41.2481,
            startLon: -8.6814,
            endLat: 41.1621,
            endLon: -8.6531
        },
        'porto3': {
            startLat: 41.1773,
            startLon: -8.5960,
            endLat: 41.1579,
            endLon: -8.6291
        }
    };

    const preset = presets[e.target.value];
    if (preset) {
        document.getElementById('startLat').value = preset.startLat;
        document.getElementById('startLon').value = preset.startLon;
        document.getElementById('endLat').value = preset.endLat;
        document.getElementById('endLon').value = preset.endLon;
    }
});

// Get ML prediction
document.getElementById('getPredictionBtn')?.addEventListener('click', async function() {
    const startLat = parseFloat(document.getElementById('startLat').value);
    const startLon = parseFloat(document.getElementById('startLon').value);
    const endLat = parseFloat(document.getElementById('endLat').value);
    const endLon = parseFloat(document.getElementById('endLon').value);

    if (!startLat || !startLon || !endLat || !endLon) {
        alert('Please fill in all location fields');
        return;
    }

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_lat: startLat,
                start_lon: startLon,
                end_lat: endLat,
                end_lon: endLon
            })
        });

        const data = await response.json();
        
        if (data.success) {
            document.getElementById('predDistance').textContent = data.distance_km.toFixed(2) + ' km';
            document.getElementById('predDuration').textContent = data.duration_minutes.toFixed(1) + ' min';
            document.getElementById('predSpeed').textContent = data.avg_speed_kmh.toFixed(1) + ' km/h';
            
            const etaDate = new Date(data.eta);
            document.getElementById('predETA').textContent = etaDate.toLocaleTimeString();
        }
    } catch (error) {
        console.error('Error getting prediction:', error);
        alert('Error getting prediction. Please try again.');
    }
});

// Start tracking
document.getElementById('tripForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const vehicleId = document.getElementById('vehicleId').value;
    const startLat = parseFloat(document.getElementById('startLat').value);
    const startLon = parseFloat(document.getElementById('startLon').value);
    const endLat = parseFloat(document.getElementById('endLat').value);
    const endLon = parseFloat(document.getElementById('endLon').value);

    if (!vehicleId || !startLat || !startLon || !endLat || !endLon) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const response = await fetch('/api/start_simulation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                vehicle_id: vehicleId,
                start_lat: startLat,
                start_lon: startLon,
                end_lat: endLat,
                end_lon: endLon
            })
        });

        const data = await response.json();
        
        if (data.success) {
            alert(`Tracking started for ${vehicleId}!\nEstimated duration: ${data.estimated_duration.toFixed(1)} minutes`);
            
            // Generate new vehicle ID for next trip
            const currentNum = parseInt(vehicleId.split('-')[1]) || 1;
            document.getElementById('vehicleId').value = `VEH-${String(currentNum + 1).padStart(3, '0')}`;
        }
    } catch (error) {
        console.error('Error starting tracking:', error);
        alert('Error starting tracking. Please try again.');
    }
});

// Center map button
document.getElementById('centerMapBtn')?.addEventListener('click', function() {
    if (Object.keys(vehicleMarkers).length > 0) {
        const bounds = L.latLngBounds(
            Object.values(vehicleMarkers).map(marker => marker.getLatLng())
        );
        map.fitBounds(bounds, { padding: [50, 50] });
    } else {
        map.setView([41.1579, -8.6291], 13);
    }
});

// Clear all vehicles
document.getElementById('clearMapBtn')?.addEventListener('click', function() {
    if (confirm('Are you sure you want to clear all vehicles?')) {
        Object.keys(vehicleMarkers).forEach(vehicleId => {
            if (vehicleMarkers[vehicleId]) {
                map.removeLayer(vehicleMarkers[vehicleId]);
            }
            if (vehiclePolylines[vehicleId]) {
                map.removeLayer(vehiclePolylines[vehicleId]);
            }
        });
        
        vehicleMarkers = {};
        vehiclePolylines = {};
        activeVehicles.clear();
        
        updateActiveVehiclesList();
        updateMetrics();
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    initSocket();
    
    // Generate initial vehicle ID
    document.getElementById('vehicleId').value = 'VEH-001';
    
    console.log('GPS Tracking System initialized');
});
