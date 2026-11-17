/**
 * SmartRetail AI - Machine Learning Forecasting Client Script
 * Author: Ananthi Merciya M (Reg No: ASML24005)
 */

document.addEventListener('DOMContentLoaded', function () {
    const modelSelect = document.getElementById('forecastModel');
    const horizonSelect = document.getElementById('forecastHorizon');
    const runBtn = document.getElementById('runForecastBtn');
    const downloadCsvBtn = document.getElementById('downloadForecastCsvBtn');

    const formatCurrency = (val) => '$' + Number(val || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const formatPercent = (val) => Number(val || 0).toFixed(2) + '%';

    let futureChartInstance = null;

    function updateDownloadLink() {
        const model = modelSelect.value;
        const horizon = horizonSelect.value;
        downloadCsvBtn.href = `/download/forecast-csv?model=${encodeURIComponent(model)}&horizon=${encodeURIComponent(horizon)}`;
    }

    function loadActualVsPredicted(model) {
        fetch(`/api/actual-vs-predicted?model=${encodeURIComponent(model)}`)
            .then(res => res.json())
            .then(json => {
                if (!json.success) throw new Error(json.error || 'Failed to fetch actual vs predicted data');
                const d = json.data;
                ChartFactory.renderForecastOverlay('actualVsPredictedChart', d.months, d.actual, d.predicted);
            })
            .catch(err => {
                console.error('Actual vs predicted error:', err);
                if (window.showToast) window.showToast('Validation chart error: ' + err.message, 'error');
            });
    }

    function executeForecast(model, horizon) {
        runBtn.disabled = true;
        runBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Projecting...';

        fetch('/api/forecast', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model: model, horizon: parseInt(horizon) })
        })
        .then(res => res.json())
        .then(json => {
            runBtn.disabled = false;
            runBtn.innerHTML = '<i class="bi bi-stars"></i> Compute Forecast Projections';

            if (!json.success) throw new Error(json.error || 'Forecasting computation failed');

            const fc = json.forecast;
            updateForecastUI(fc);
            if (window.showToast) {
                window.showToast(`Forecast generated successfully for ${horizon} months!`, 'success');
            }
        })
        .catch(err => {
            runBtn.disabled = false;
            runBtn.innerHTML = '<i class="bi bi-stars"></i> Compute Forecast Projections';
            console.error('Forecast error:', err);
            if (window.showToast) window.showToast('Forecasting error: ' + err.message, 'error');
        });
    }

    function updateForecastUI(fc) {
        // Update KPIs
        document.getElementById('kpiForecastTotal').textContent = formatCurrency(fc.total_predicted_sales);
        document.getElementById('kpiForecastHorizonText').textContent = `${fc.horizon_months}-Month Cumulative Total`;
        document.getElementById('kpiForecastAvg').textContent = formatCurrency(fc.average_monthly_sales);
        document.getElementById('kpiForecastPeak').textContent = formatCurrency(fc.highest_sales);
        document.getElementById('kpiForecastPeakMonth').textContent = `Peak Month: ${fc.highest_month}`;
        document.getElementById('kpiForecastTrough').textContent = formatCurrency(fc.lowest_sales);
        document.getElementById('kpiForecastTroughMonth').textContent = `Trough Month: ${fc.lowest_month}`;

        document.getElementById('chartModelBadge').textContent = fc.model_used === 'linear_regression' ? 'Linear Regression' : 'Random Forest';
        document.getElementById('tableHorizonBadge').textContent = `${fc.horizon_months} Future Months`;

        // Render Future Forecast Chart
        const futureCtx = document.getElementById('futureForecastChart');
        if (futureCtx) {
            if (futureChartInstance) futureChartInstance.destroy();

            futureChartInstance = new Chart(futureCtx, {
                type: 'line',
                data: {
                    labels: fc.chart.labels,
                    datasets: [{
                        label: 'Projected Sales ($)',
                        data: fc.chart.values,
                        borderColor: '#14b8a6',
                        backgroundColor: 'rgba(20, 184, 166, 0.15)',
                        fill: true,
                        tension: 0.35,
                        pointRadius: 5,
                        pointHoverRadius: 8,
                        pointBackgroundColor: '#14b8a6',
                        borderWidth: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' } },
                        y: {
                            grid: { color: 'rgba(255,255,255,0.06)' },
                            ticks: {
                                callback: val => '$' + (val >= 1000 ? (val/1000) + 'k' : val)
                            }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: ctx => 'Projected Sales: $' + Number(ctx.raw).toLocaleString()
                            }
                        }
                    }
                }
            });
        }

        // Populate Granular Table
        const tbody = document.getElementById('forecastTableBody');
        tbody.innerHTML = '';
        const total = fc.total_predicted_sales;

        fc.table.forEach((row, idx) => {
            const share = (row.predicted_sales / total) * 100;
            let phase = 'Standard Run-Rate';
            let badgeClass = 'bg-secondary';
            if (row.month_name === 'November' || row.month_name === 'December') {
                phase = 'Holiday Surge Peak';
                badgeClass = 'bg-success';
            } else if (row.month_name === 'September') {
                phase = 'Q3 Seasonal Surge';
                badgeClass = 'bg-teal';
            } else if (row.month_name === 'January' || row.month_name === 'February') {
                phase = 'Post-Holiday Reset';
                badgeClass = 'bg-warning text-dark';
            }

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><code>${row.month}</code></td>
                <td><strong>${row.month_name}</strong></td>
                <td>${row.year}</td>
                <td class="text-teal-light fw-bold">${formatCurrency(row.predicted_sales)}</td>
                <td>
                    <div class="d-flex align-items-center gap-2">
                        <span>${formatPercent(share)}</span>
                        <div class="progress flex-grow-1" style="height: 4px; background: rgba(255,255,255,0.1);">
                            <div class="progress-bar bg-teal" style="width: ${share * 5}%"></div>
                        </div>
                    </div>
                </td>
                <td><span class="badge ${badgeClass}">${phase}</span></td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Event Listeners
    if (runBtn) {
        runBtn.addEventListener('click', function () {
            const model = modelSelect.value;
            const horizon = horizonSelect.value;
            updateDownloadLink();
            loadActualVsPredicted(model);
            executeForecast(model, horizon);
        });
    }

    if (modelSelect) {
        modelSelect.addEventListener('change', function () {
            updateDownloadLink();
            loadActualVsPredicted(this.value);
        });
    }

    if (horizonSelect) {
        horizonSelect.addEventListener('change', updateDownloadLink);
    }

    // Initialize on page load
    updateDownloadLink();
    loadActualVsPredicted(modelSelect.value);
    executeForecast(modelSelect.value, horizonSelect.value);
});

