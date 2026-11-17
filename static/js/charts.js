/**
 * SmartRetail AI - Chart.js Theme & Rendering Factory
 * Author: Ananthi Merciya M (Reg No: ASML24005)
 */

// Global Dark Theme Configuration for Chart.js
if (window.Chart) {
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    Chart.defaults.font.size = 11;
    Chart.defaults.plugins.tooltip.backgroundColor = '#1e293b';
    Chart.defaults.plugins.tooltip.titleColor = '#ffffff';
    Chart.defaults.plugins.tooltip.bodyColor = '#cbd5e1';
    Chart.defaults.plugins.tooltip.borderColor = '#334155';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.boxPadding = 4;
    Chart.defaults.plugins.tooltip.usePointStyle = true;
}

window.ChartFactory = {
    // 1. Monthly Sales & Profit Area Chart
    renderMonthlyTrend: function(canvasId, labels, sales, profit) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        
        // Destroy existing chart if present
        if (Chart.getChart(ctx)) { Chart.getChart(ctx).destroy(); }
        
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Gross Sales ($)',
                        data: sales,
                        borderColor: '#14b8a6',
                        backgroundColor: 'rgba(20, 184, 166, 0.12)',
                        fill: true,
                        tension: 0.35,
                        pointRadius: 2.5,
                        pointHoverRadius: 6,
                        pointBackgroundColor: '#14b8a6',
                        borderWidth: 2.5
                    },
                    {
                        label: 'Net Profit ($)',
                        data: profit,
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56, 189, 248, 0.05)',
                        fill: true,
                        tension: 0.35,
                        pointRadius: 2,
                        pointHoverRadius: 5,
                        pointBackgroundColor: '#38bdf8',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.04)' },
                        ticks: { maxRotation: 45, maxTicksLimit: 16 }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.06)' },
                        ticks: {
                            callback: function(val) { return '$' + (val >= 1000 ? (val/1000) + 'k' : val); }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { usePointStyle: true, boxWidth: 8, padding: 15 }
                    }
                }
            }
        });
    },

    // 2. Year-over-Year Grouped Bar Chart
    renderYearlyBar: function(canvasId, years, sales, profit) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        if (Chart.getChart(ctx)) { Chart.getChart(ctx).destroy(); }

        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: years,
                datasets: [
                    {
                        label: 'Sales Revenue ($)',
                        data: sales,
                        backgroundColor: '#0d9488',
                        borderRadius: 6,
                        barPercentage: 0.65
                    },
                    {
                        label: 'Net Profit ($)',
                        data: profit,
                        backgroundColor: '#3b82f6',
                        borderRadius: 6,
                        barPercentage: 0.65
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { display: false } },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.06)' },
                        ticks: {
                            callback: function(val) { return '$' + (val/1000) + 'k'; }
                        }
                    }
                },
                plugins: {
                    legend: { position: 'top', labels: { usePointStyle: true, padding: 12 } }
                }
            }
        });
    },

    // 3. Category Donut Chart
    renderCategoryDonut: function(canvasId, categories, sales) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        if (Chart.getChart(ctx)) { Chart.getChart(ctx).destroy(); }

        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: categories,
                datasets: [{
                    data: sales,
                    backgroundColor: ['#0d9488', '#3b82f6', '#f59e0b'],
                    borderColor: '#1e293b',
                    borderWidth: 3,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: { position: 'bottom', labels: { usePointStyle: true, padding: 15 } }
                }
            }
        });
    },

    // 4. Regional Performance Horizontal Bar Chart
    renderRegionBar: function(canvasId, regions, sales, profit) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        if (Chart.getChart(ctx)) { Chart.getChart(ctx).destroy(); }

        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: regions,
                datasets: [
                    {
                        label: 'Regional Sales ($)',
                        data: sales,
                        backgroundColor: '#06b6d4',
                        borderRadius: 4
                    },
                    {
                        label: 'Regional Profit ($)',
                        data: profit,
                        backgroundColor: '#10b981',
                        borderRadius: 4
                    }
                ]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.06)' },
                        ticks: {
                            callback: function(val) { return '$' + (val/1000) + 'k'; }
                        }
                    },
                    y: { grid: { display: false } }
                },
                plugins: {
                    legend: { position: 'top', labels: { usePointStyle: true, padding: 12 } }
                }
            }
        });
    },

    // 5. Discount vs Profit Sensitivity Line Chart
    renderDiscountCurve: function(canvasId, discounts, profit) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        if (Chart.getChart(ctx)) { Chart.getChart(ctx).destroy(); }

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: discounts,
                datasets: [{
                    label: 'Net Profit ($)',
                    data: profit,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    fill: {
                        target: 'origin',
                        above: 'rgba(16, 185, 129, 0.15)', // Green when profitable
                        below: 'rgba(239, 68, 68, 0.25)'   // Red when loss-making
                    },
                    tension: 0.3,
                    pointRadius: 4,
                    pointBackgroundColor: profit.map(p => p >= 0 ? '#10b981' : '#ef4444'),
                    borderWidth: 2.5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: { display: true, text: 'Promotional Discount Depth', color: '#94a3b8' },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    },
                    y: {
                        title: { display: true, text: 'Net Operating Profit ($)', color: '#94a3b8' },
                        grid: { color: 'rgba(255, 255, 255, 0.06)' },
                        ticks: {
                            callback: function(val) { return '$' + val.toLocaleString(); }
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const val = context.raw;
                                return (val >= 0 ? 'Profit: +$' : 'Loss: -$') + Math.abs(val).toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    },

    // 6. Forecast Actual vs Predicted Chart
    renderForecastOverlay: function(canvasId, months, actual, predicted) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        if (Chart.getChart(ctx)) { Chart.getChart(ctx).destroy(); }

        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [
                    {
                        label: 'Actual Historical Sales ($)',
                        data: actual,
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56, 189, 248, 0.15)',
                        fill: false,
                        tension: 0.2,
                        pointRadius: 4,
                        borderWidth: 2.5
                    },
                    {
                        label: 'Model Predicted Sales ($)',
                        data: predicted,
                        borderColor: '#f59e0b',
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.2,
                        pointRadius: 4,
                        pointStyle: 'rectRot',
                        borderWidth: 2.5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                scales: {
                    x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.06)' },
                        ticks: {
                            callback: function(val) { return '$' + (val/1000) + 'k'; }
                        }
                    }
                },
                plugins: {
                    legend: { position: 'top', labels: { usePointStyle: true, padding: 12 } }
                }
            }
        });
    }
};

