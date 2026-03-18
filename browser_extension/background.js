// ─────────────────────────────────────────
// Malicious Traffic Detector
// Background Service Worker
// ─────────────────────────────────────────

const API_URL = 'http://localhost:5000';

// Check for threats every 10 seconds
chrome.alarms.create('checkThreats', { periodInMinutes: 0.2 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'checkThreats') {
    checkForThreats();
  }
});

async function checkForThreats() {
  try {
    const response = await fetch(`${API_URL}/alerts`);
    const data = await response.json();

    if (data.total > 0) {
      const latest = data.alerts[data.alerts.length - 1];

      // Send notification
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icon.png',
        title: '🚨 Malicious Traffic Detected!',
        message: `Threat detected from IP: ${latest.ip}`
      });

      // Save to storage
      chrome.storage.local.set({
        alerts: data.alerts,
        total: data.total,
        lastChecked: new Date().toLocaleTimeString()
      });
    }
  } catch (error) {
    console.log('Backend not running:', error);
  }
}