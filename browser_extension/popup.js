// ─────────────────────────────────────────
// Malicious Traffic Detector
// Popup Script
// ─────────────────────────────────────────

const API_URL = 'http://localhost:5000';

async function loadData() {
  await checkStatus();
  await loadAlerts();
  await loadBlocked();
}

// Check if backend is running
async function checkStatus() {
  try {
    const response = await fetch(`${API_URL}/status`);
    const data = await response.json();

    document.getElementById('statusText').innerHTML =
      '<span class="status-dot dot-green"></span>Monitor Active';
    document.getElementById('lastChecked').textContent =
      new Date().toLocaleTimeString();

  } catch (error) {
    document.getElementById('statusText').innerHTML =
      '<span class="status-dot dot-red"></span>Backend Offline';
  }
}

// Load alerts
async function loadAlerts() {
  try {
    const response = await fetch(`${API_URL}/alerts`);
    const data = await response.json();

    document.getElementById('totalAlerts').textContent = data.total || 0;

    const alertsList = document.getElementById('alertsList');

    if (!data.alerts || data.alerts.length === 0) {
      alertsList.innerHTML = '<div class="no-alerts">✅ No threats detected</div>';
      return;
    }

    alertsList.innerHTML = '';
    data.alerts.reverse().forEach(alert => {
      const card = document.createElement('div');
      card.className = 'alert-card';
      card.innerHTML = `
        <div class="alert-ip">⚠️ ${alert.ip}</div>
        <div class="alert-time">${alert.timestamp}</div>
        <button class="btn btn-red" onclick="blockIP('${alert.ip}')">🚫 Block</button>
        <button class="btn btn-gray" onclick="explainThreat('${alert.ip}', this)">🤖 Explain</button>
        <div class="alert-explanation" id="exp-${alert.ip.replace(/\./g,'-')}"></div>
      `;
      alertsList.appendChild(card);
    });

  } catch (error) {
    document.getElementById('alertsList').innerHTML =
      '<div class="no-alerts" style="color:#f85149">❌ Cannot connect to backend</div>';
  }
}

// Load blocked IPs count
async function loadBlocked() {
  try {
    const response = await fetch(`${API_URL}/blocked`);
    const data = await response.json();
    document.getElementById('totalBlocked').textContent = data.total || 0;
  } catch (error) {
    console.log('Error loading blocked:', error);
  }
}

// Block an IP
async function blockIP(ip) {
  try {
    const response = await fetch(`${API_URL}/block/${ip}`, { method: 'POST' });
    const data = await response.json();
    if (data.success) {
      alert(`✅ IP ${ip} has been blocked!`);
      loadData();
    }
  } catch (error) {
    alert('❌ Could not block IP. Is backend running?');
  }
}

// Explain threat using Gemini
async function explainThreat(ip, btn) {
  const expDiv = document.getElementById(`exp-${ip.replace(/\./g,'-')}`);
  expDiv.textContent = '🤖 Analyzing...';

  try {
    const response = await fetch(`${API_URL}/explain/${ip}`);
    const data = await response.json();
    expDiv.textContent = data.explanation;
  } catch (error) {
    expDiv.textContent = '❌ Could not get explanation';
  }
}

// Load on open
loadData();
