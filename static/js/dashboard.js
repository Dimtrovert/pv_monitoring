console.log("Loading dashboard.js (Final Synchronized Version)");

// ==========================================
// 1. KONFIGURASI EMQX
// ==========================================
const brokerUrl = 'wss://b792c9ff.ala.asia-southeast1.emqxsl.com:8084/mqtt';
const topic = 'pv/data';
const options = {
    clientId: `pv-dashboard-${Math.random().toString(16).slice(2, 10)}`,
    username: 'Rsi123', 
    password: 'Rsi123',
    clean: true
};

// ==========================================
// 2. LOGIKA UI
// ==========================================
function conditionClass(condition) {
    if (!condition) return "status-unknown";
    const normalized = condition.toString().trim().toLowerCase();
    if (normalized.includes("short")) return "status-short";
    if (normalized.includes("open")) return "status-open";
    if (normalized.includes("shaded")) return "status-shaded";
    if (normalized.includes("normal")) return "status-normal";
    return "status-unknown";
}

function updateDashboard(data) {
    if (!data) return;
    document.getElementById("lux").innerText = `${data.lux ?? "--"} lx`;
    document.getElementById("temperature").innerText = `${data.temperature ?? "--"} °C`;
    document.getElementById("voltage").innerText = `${data.voltage ?? "--"} V`;
    document.getElementById("current").innerText = `${data.current ?? "--"} A`;
    document.getElementById("power").innerText = `${data.power ?? "--"} W`;
    
    const conditionText = document.getElementById("condition-text");
    const conditionBox = document.getElementById("condition-box");
    if (conditionText && conditionBox) {
        conditionText.innerText = data.condition || "Tidak diketahui";
        conditionBox.className = `metric-value condition-value ${conditionClass(data.condition)}`;
    }
    const elConf = document.getElementById("confidence");
    if (elConf && data.confidence !== undefined) elConf.innerText = `${(data.confidence * 100).toFixed(2)} %`;
}

// ==========================================
// 3. LOGIKA CHART (PONDASI SUPABASE + REALTIME)
// ==========================================
let pvChart = null;

function initChart(period = '1h') {
    fetch(`/api/historical-data?period=${period}&_t=${Date.now()}`)
        .then(res => res.json())
        .then(payload => {
            const canvas = document.getElementById('pvChart');
            if (pvChart) pvChart.destroy();

            pvChart = new Chart(canvas.getContext('2d'), {
                type: 'line',
                data: {
                    labels: payload.labels.map(iso => new Date(iso).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit', second: '2-digit' }).replace(/\./g, ':')),
                    datasets: [
                        { label: 'Tegangan (V)', data: payload.voltage, borderColor: '#38bdf8', borderWidth: 2, tension: 0.35 },
                        { label: 'Daya (W)', data: payload.power, borderColor: '#a855f7', borderWidth: 2, tension: 0.35 },
                        { label: 'Arus (A)', data: payload.current, borderColor: '#10b981', borderWidth: 2, tension: 0.35 }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        });
}

window.changeChartPeriod = () => initChart(document.getElementById('timeRange').value);
window.addEventListener('DOMContentLoaded', () => initChart('1h'));

// ==========================================
// 4. MQTT REAL-TIME
// ==========================================
const client = mqtt.connect(brokerUrl, options);
client.on('connect', () => client.subscribe(topic));

client.on('message', (t, msg) => {
    const payload = JSON.parse(msg.toString());
    updateDashboard(payload);

    if (pvChart) {
        const now = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit', second: '2-digit' }).replace(/\./g, ':');
        
        pvChart.data.labels.push(now);
        pvChart.data.datasets[0].data.push(payload.voltage);
        pvChart.data.datasets[1].data.push(payload.power);
        pvChart.data.datasets[2].data.push(payload.current);

        if (pvChart.data.labels.length > 100) {
            pvChart.data.labels.shift();
            pvChart.data.datasets.forEach(ds => ds.data.shift());
        }
        pvChart.update();
    }
});