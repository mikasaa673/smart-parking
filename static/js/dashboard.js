/**
 * dashboard.js
 * ------------
 * Frontend logic for the Admin Dashboard page.
 * Loads dashboard data, renders Chart.js graphs, overstay alerts,
 * reservation table, and slot map.
 */

// ─── Configuration ───────────────────────────────────────────────────────
const API_BASE = '';

// ─── Chart instances ─────────────────────────────────────────────────────
let occupancyChart = null;
let peakChart = null;
let predictionChart = null;

// ─── Chart.js Defaults ──────────────────────────────────────────────────
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255,255,255,0.06)';
Chart.defaults.font.family = "'Inter', sans-serif";

// ─── Color helpers ───────────────────────────────────────────────────────
const COLORS = {
    accent: '#6366f1',
    accentLight: '#818cf8',
    green: '#22c55e',
    red: '#ef4444',
    orange: '#f59e0b',
    cyan: '#06b6d4',
};

function gradient(ctx, c1, c2) {
    const g = ctx.createLinearGradient(0, 0, 0, 300);
    g.addColorStop(0, c1);
    g.addColorStop(1, c2);
    return g;
}

// ─── Load Dashboard Data ─────────────────────────────────────────────────
async function loadDashboard() {
    try {
        const res = await fetch(`${API_BASE}/dashboard-data`);
        const data = await res.json();
        if (!data.success) throw new Error(data.error);

        renderSummary(data.summary);
        renderOccupancyChart(data.history);
        renderPeakChart(data.peak_hours);
        renderOverstays(data.overstays);
        renderReservations(data.reservations);
        renderSlotMap(data.slots);
    } catch (err) {
        console.error('loadDashboard:', err);
    }
}

// ─── Load Predictions ────────────────────────────────────────────────────
async function loadPredictions() {
    try {
        const res = await fetch(`${API_BASE}/predict?hours=8`);
        const data = await res.json();
        if (!data.success) return;
        renderPredictionChart(data.predictions, data.total_slots);
    } catch (err) {
        console.error('loadPredictions:', err);
    }
}

// ─── Summary Cards ───────────────────────────────────────────────────────
function renderSummary(s) {
    animateNumber(document.getElementById('summTotal'), s.total);
    animateNumber(document.getElementById('summAvailable'), s.available);
    animateNumber(document.getElementById('summOccupied'), s.occupied);
}

// ─── Occupancy Chart (line) ──────────────────────────────────────────────
function renderOccupancyChart(history) {
    const ctx = document.getElementById('occupancyChart').getContext('2d');

    // Take the last 24 records (1 day)
    const recent = history.slice(0, 24).reverse();
    const labels = recent.map(r => {
        const h = r.hour_of_day !== undefined ? r.hour_of_day : '--';
        return `${String(h).padStart(2, '0')}:00`;
    });
    const occupied = recent.map(r => r.occupied_slots);
    const available = recent.map(r => r.available_slots);

    if (occupancyChart) occupancyChart.destroy();
    occupancyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Occupied',
                    data: occupied,
                    borderColor: COLORS.red,
                    backgroundColor: gradient(ctx, 'rgba(239,68,68,.25)', 'rgba(239,68,68,.01)'),
                    fill: true, tension: .4, pointRadius: 3,
                },
                {
                    label: 'Available',
                    data: available,
                    borderColor: COLORS.green,
                    backgroundColor: gradient(ctx, 'rgba(34,197,94,.2)', 'rgba(34,197,94,.01)'),
                    fill: true, tension: .4, pointRadius: 3,
                }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { position: 'top' } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,.04)' } },
                x: { grid: { display: false } }
            }
        }
    });
}

// ─── Peak Hours Chart (bar) ──────────────────────────────────────────────
function renderPeakChart(peakHours) {
    const ctx = document.getElementById('peakChart').getContext('2d');

    // Show top 10 hours sorted by time for readability
    const sorted = [...peakHours].slice(0, 12).sort((a, b) => a.hour.localeCompare(b.hour));
    const labels = sorted.map(p => p.hour);
    const data = sorted.map(p => p.avg_occupied);
    const colors = data.map(d => d > 9 ? COLORS.red : d > 6 ? COLORS.orange : COLORS.green);

    if (peakChart) peakChart.destroy();
    peakChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Avg Occupied',
                data,
                backgroundColor: colors.map(c => c + '99'),
                borderColor: colors,
                borderWidth: 1,
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,.04)' } },
                x: { grid: { display: false } }
            }
        }
    });
}

// ─── Prediction Chart (line) ─────────────────────────────────────────────
function renderPredictionChart(predictions, totalSlots) {
    const ctx = document.getElementById('predictionChart').getContext('2d');

    const labels = predictions.map(p => p.hour);
    const predicted = predictions.map(p => p.predicted_occupied);
    const avail = predictions.map(p => p.predicted_available);

    if (predictionChart) predictionChart.destroy();
    predictionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Predicted Occupied',
                    data: predicted,
                    borderColor: COLORS.accent,
                    backgroundColor: gradient(ctx, 'rgba(99,102,241,.25)', 'rgba(99,102,241,.02)'),
                    fill: true, tension: .4, borderWidth: 2.5, pointRadius: 5,
                    pointBackgroundColor: COLORS.accent,
                },
                {
                    label: 'Predicted Available',
                    data: avail,
                    borderColor: COLORS.cyan,
                    backgroundColor: gradient(ctx, 'rgba(6,182,212,.2)', 'rgba(6,182,212,.02)'),
                    fill: true, tension: .4, borderWidth: 2, pointRadius: 4,
                    borderDash: [6, 3],
                }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    callbacks: {
                        afterBody: (items) => {
                            const idx = items[0].dataIndex;
                            return `Occupancy: ${predictions[idx].occupancy_pct}%`;
                        }
                    }
                }
            },
            scales: {
                y: { beginAtZero: true, max: totalSlots + 1, grid: { color: 'rgba(255,255,255,.04)' } },
                x: { grid: { display: false } }
            }
        }
    });
}

// ─── Overstay Alerts ─────────────────────────────────────────────────────
function renderOverstays(overstays) {
    const container = document.getElementById('alertsContainer');
    const counter = document.getElementById('summOverstays');

    animateNumber(counter, overstays.length);

    if (!overstays.length) {
        container.innerHTML = '<p class="no-data">No overstays detected. All clear!</p>';
        return;
    }

    container.innerHTML = overstays.map(o => `
        <div class="alert-item">
            <span class="alert-icon"><i class="material-icons">warning</i></span>
            <div class="alert-text">
                <div class="alert-name">${o.user_name}</div>
                <div class="alert-detail">Slot ${o.slot_label} — Expected end: ${o.expected_end}</div>
            </div>
            <div class="alert-duration">+${o.overstay_minutes} min</div>
        </div>
    `).join('');
}

// ─── Reservations Table ──────────────────────────────────────────────────
function renderReservations(reservations) {
    const tbody = document.getElementById('reservationsBody');

    if (!reservations.length) {
        tbody.innerHTML = '<tr><td colspan="9" class="no-data">No active reservations.</td></tr>';
        return;
    }

    tbody.innerHTML = reservations.map(r => `
        <tr>
            <td>#${r.reservation_id}</td>
            <td>${r.user_name}</td>
            <td>
                <span style="font-family:monospace;font-weight:600;letter-spacing:.5px">
                    ${r.car_plate || '—'}
                </span>
            </td>
            <td>
                <a href="mailto:${r.user_email || ''}" style="color:var(--accent,#6366f1);text-decoration:none">
                    ${r.user_email || '—'}
                </a>
            </td>
            <td>${r.slot_label || 'Slot ' + r.slot_id}</td>
            <td>${r.start_time}</td>
            <td>${r.end_time}</td>
            <td><span class="status-badge ${r.status}">${r.status}</span></td>
            <td>${r.status === 'active' ? `<button class="btn-cancel" onclick="cancelReservation(${r.reservation_id})">✕ Cancel</button>` : '—'}</td>
        </tr>
    `).join('');
}

// ─── Cancel Reservation ──────────────────────────────────────────────────
async function cancelReservation(id) {
    if (!confirm(`Cancel reservation #${id}?`)) return;
    try {
        const res = await fetch(`${API_BASE}/cancel-reservation/${id}`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            loadDashboard();
            loadPredictions();
        } else {
            alert(data.error || 'Failed to cancel.');
        }
    } catch (err) {
        console.error('cancelReservation:', err);
        alert('Network error.');
    }
}

// ─── Slot Map ────────────────────────────────────────────────────────────
function renderSlotMap(slots) {
    const grid = document.getElementById('dashSlotGrid');
    if (!grid) return;

    grid.innerHTML = '';
    slots.forEach(s => {
        const status = s.reservation_status || (s.is_occupied ? 'occupied' : 'available');
        let cls, statusText, icon;
        if (status === 'grace') {
            cls = 'reserved';
            statusText = `Reserved · ${s.grace_minutes_left}m`;
            icon = '';
        } else if (status === 'occupied') {
            cls = 'occupied';
            statusText = 'Occupied';
            icon = '';
        } else {
            cls = 'available';
            statusText = 'Free';
            icon = '';
        }
        const card = document.createElement('div');
        card.className = `slot-card ${cls}`;
        card.innerHTML = `
            <div class="slot-label">${s.slot_label || 'S' + s.slot_id}</div>
            <span class="slot-status">${statusText}</span>
            ${status === 'grace' ? `<span class="slot-reserved-by">${s.reserved_by}</span>` : ''}
            <span class="slot-car-icon">${icon}</span>
        `;
        grid.appendChild(card);
    });
}

// ─── Utilities ───────────────────────────────────────────────────────────
function animateNumber(el, target) {
    if (!el) return;
    const start = parseInt(el.textContent) || 0;
    const diff = target - start;
    const dur = 600;
    const t0 = performance.now();
    function step(now) {
        const p = Math.min((now - t0) / dur, 1);
        el.textContent = Math.round(start + diff * easeOut(p));
        if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}
function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

// ─── Init ────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    loadPredictions();

    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadDashboard();
        loadPredictions();
    }, 30000);
});
