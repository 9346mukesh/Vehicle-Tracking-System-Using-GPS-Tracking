// Analytics Page JavaScript with Charts
let distanceChart, durationChart, speedChart, hourlyChart;
let analyticsTrips = [];

function initCharts(payload) {
    const distanceCtx = document.getElementById('distanceChart');
    if (distanceCtx) {
        distanceChart = new Chart(distanceCtx, {
            type: 'bar',
            data: {
                labels: payload.distance_bins.labels,
                datasets: [{
                    label: 'Number of Trips',
                    data: payload.distance_bins.values,
                    backgroundColor: 'rgba(37, 99, 235, 0.8)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: { color: '#f8fafc' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#cbd5e1' },
                        grid: { color: 'rgba(51, 65, 85, 0.5)' }
                    },
                    x: {
                        ticks: { color: '#cbd5e1' },
                        grid: { color: 'rgba(51, 65, 85, 0.5)' }
                    }
                }
            }
        });
    }

    const durationCtx = document.getElementById('durationChart');
    if (durationCtx) {
        durationChart = new Chart(durationCtx, {
            type: 'line',
            data: {
                labels: payload.duration_bins.labels,
                datasets: [{
                    label: 'Trip Duration',
                    data: payload.duration_bins.values,
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: { color: '#f8fafc' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#cbd5e1' },
                        grid: { color: 'rgba(51, 65, 85, 0.5)' }
                    },
                    x: {
                        ticks: { color: '#cbd5e1' },
                        grid: { color: 'rgba(51, 65, 85, 0.5)' }
                    }
                }
            }
        });
    }

    const speedCtx = document.getElementById('speedChart');
    if (speedCtx) {
        speedChart = new Chart(speedCtx, {
            type: 'bar',
            data: {
                labels: payload.speed_bins.labels,
                datasets: [{
                    label: 'Speed Range (km/h)',
                    data: payload.speed_bins.values,
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(37, 99, 235, 0.8)',
                        'rgba(168, 85, 247, 0.8)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: { color: '#f8fafc' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#cbd5e1' },
                        grid: { color: 'rgba(51, 65, 85, 0.5)' }
                    },
                    x: {
                        ticks: { color: '#cbd5e1' },
                        grid: { color: 'rgba(51, 65, 85, 0.5)' }
                    }
                }
            }
        });
    }

    const hourlyCtx = document.getElementById('hourlyChart');
    if (hourlyCtx) {
        hourlyChart = new Chart(hourlyCtx, {
            type: 'line',
            data: {
                labels: payload.hourly.labels,
                datasets: [{
                    label: 'Trips per Hour',
                    data: payload.hourly.values,
                    backgroundColor: 'rgba(168, 85, 247, 0.2)',
                    borderColor: 'rgba(168, 85, 247, 1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: { color: '#f8fafc' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#cbd5e1' },
                        grid: { color: 'rgba(51, 65, 85, 0.5)' }
                    },
                    x: {
                        ticks: { color: '#cbd5e1' },
                        grid: { color: 'rgba(51, 65, 85, 0.5)' }
                    }
                }
            }
        });
    }
}

// Update statistics
function updateStatistics(summary) {
    document.getElementById('totalTrips').textContent = summary.total_trips;
    document.getElementById('totalKm').textContent = summary.total_distance_km.toFixed(1) + ' km';
    document.getElementById('totalTime').textContent = summary.total_time_hours.toFixed(1) + ' hrs';
    document.getElementById('avgSpeedStat').textContent = summary.avg_speed_kmh.toFixed(1) + ' km/h';
}

// Populate trip history table
function populateTripTable(trips) {
    const tbody = document.getElementById('tripTableBody');
    if (!tbody) return;

    if (!trips || trips.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No trip data available</td></tr>';
        return;
    }

    let html = '';
    trips.forEach(trip => {
        const statusLabel = trip.status ? trip.status.charAt(0).toUpperCase() + trip.status.slice(1) : 'Unknown';
        const statusColor = trip.status === 'completed' ? '#10b981' : trip.status === 'cancelled' ? '#ef4444' : '#f59e0b';
        html += `
            <tr>
                <td>${trip.vehicle_id || '-'}</td>
                <td>${trip.date}</td>
                <td>${trip.distance.toFixed(2)}</td>
                <td>${trip.duration.toFixed(1)}</td>
                <td>${trip.speed.toFixed(2)}</td>
                <td><span style="color: ${statusColor}; font-weight: 600;">${statusLabel}</span></td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}
async function loadAnalytics() {
    const response = await fetch('/api/analytics');
    const data = await response.json();

    analyticsTrips = data.trips || [];
    updateStatistics(data.summary);
    populateTripTable(analyticsTrips);

    if (!distanceChart) {
        initCharts(data.charts);
    } else {
        distanceChart.data.labels = data.charts.distance_bins.labels;
        distanceChart.data.datasets[0].data = data.charts.distance_bins.values;
        distanceChart.update();

        durationChart.data.labels = data.charts.duration_bins.labels;
        durationChart.data.datasets[0].data = data.charts.duration_bins.values;
        durationChart.update();

        speedChart.data.labels = data.charts.speed_bins.labels;
        speedChart.data.datasets[0].data = data.charts.speed_bins.values;
        speedChart.update();

        hourlyChart.data.labels = data.charts.hourly.labels;
        hourlyChart.data.datasets[0].data = data.charts.hourly.values;
        hourlyChart.update();
    }
}

// Add animation on scroll
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.stat-card, .chart-card, .analytics-section').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Animate statistics on load
function animateStats() {
    const statValues = document.querySelectorAll('.stat-content h3');
    
    statValues.forEach(stat => {
        const finalValue = stat.textContent;
        const isNumber = !isNaN(parseFloat(finalValue));
        
        if (isNumber) {
            const target = parseFloat(finalValue);
            let current = 0;
            const increment = target / 50;
            const unit = finalValue.match(/[a-z]+/gi)?.[0] || '';
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    stat.textContent = finalValue;
                    clearInterval(timer);
                } else {
                    stat.textContent = Math.floor(current) + (unit ? ' ' + unit : '');
                }
            }, 20);
        }
    });
}

// Export data functionality
function exportTripData() {
    let csv = 'Vehicle ID,Date & Time,Distance (km),Duration (min),Avg Speed (km/h),Status\n';
    
    analyticsTrips.forEach(trip => {
        csv += `${trip.vehicle_id || ''},${trip.date},${trip.distance},${trip.duration},${trip.speed},${trip.status}\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'trip_data.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// Initialize analytics page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Analytics page loading...');
    
    // Initialize all components
    loadAnalytics();
    addScrollAnimations();
    
    // Animate stats after a short delay
    setTimeout(animateStats, 300);
    
    console.log('Analytics page loaded successfully');
});

// Refresh data every 30 seconds (if connected to real-time data)
setInterval(() => {
    loadAnalytics();
}, 30000);
