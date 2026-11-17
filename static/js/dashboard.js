/**
 * SmartRetail AI - Dashboard Client Script
 * Author: Ananthi Merciya M (Reg No: ASML24005)
 */

document.addEventListener('DOMContentLoaded', function () {
    const yearSelect = document.getElementById('filterYear');
    const categorySelect = document.getElementById('filterCategory');
    const applyBtn = document.getElementById('applyFilterBtn');
    const resetBtn = document.getElementById('resetFilterBtn');

    // Number Formatters
    const formatCurrency = (val) => {
        return '$' + Number(val || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    };
    const formatInteger = (val) => {
        return Number(val || 0).toLocaleString('en-US');
    };
    const formatPercent = (val) => {
        return Number(val || 0).toFixed(2) + '%';
    };

    function loadDashboardData(year = 'all', category = 'all') {
        const queryParams = new URLSearchParams();
        if (year && year !== 'all') queryParams.append('year', year);
        if (category && category !== 'all') queryParams.append('category', category);

        const url = `/api/dashboard?${queryParams.toString()}`;

        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return response.json();
            })
            .then(res => {
                if (!res.success) {
                    throw new Error(res.error || 'Failed to fetch dashboard metrics');
                }

                const kpis = res.kpis;
                // Update KPI Cards
                document.getElementById('kpiSales').textContent = formatCurrency(kpis.total_sales);
                
                const profitEl = document.getElementById('kpiProfit');
                profitEl.textContent = formatCurrency(kpis.total_profit);
                if (kpis.total_profit < 0) {
                    profitEl.className = 'kpi-value text-danger';
                } else {
                    profitEl.className = 'kpi-value text-success';
                }

                document.getElementById('kpiMargin').textContent = formatPercent(kpis.profit_margin);
                document.getElementById('kpiOrders').textContent = formatInteger(kpis.total_orders);
                document.getElementById('kpiCustomers').textContent = formatInteger(kpis.total_customers);
                document.getElementById('kpiQuantity').textContent = formatInteger(kpis.total_quantity);

                // 1. Monthly Trends
                if (res.monthly_trend && res.monthly_trend.months) {
                    ChartFactory.renderMonthlyTrend(
                        'monthlyTrendChart',
                        res.monthly_trend.months,
                        res.monthly_trend.sales,
                        res.monthly_trend.profit
                    );
                }

                // 2. Yearly YoY Chart
                if (res.yearly_data && res.yearly_data.years) {
                    ChartFactory.renderYearlyBar(
                        'yearlyChart',
                        res.yearly_data.years,
                        res.yearly_data.sales,
                        res.yearly_data.profit
                    );
                }

                // 3. Category Breakdown
                if (res.category_data && res.category_data.categories) {
                    ChartFactory.renderCategoryDonut(
                        'categoryChart',
                        res.category_data.categories,
                        res.category_data.sales
                    );
                }

                // 4. Regional Breakdown
                if (res.region_data && res.region_data.regions) {
                    ChartFactory.renderRegionBar(
                        'regionChart',
                        res.region_data.regions,
                        res.region_data.sales,
                        res.region_data.profit
                    );
                }

                // 5. Discount Sensitivity
                if (res.discount_data && res.discount_data.buckets) {
                    ChartFactory.renderDiscountCurve(
                        'discountImpactChart',
                        res.discount_data.buckets,
                        res.discount_data.profit
                    );
                }
            })
            .catch(err => {
                console.error('Error loading dashboard:', err);
                if (window.showToast) {
                    window.showToast('Failed to load dashboard data: ' + err.message, 'error');
                }
            });
    }

    // Filter event listeners
    if (applyBtn) {
        applyBtn.addEventListener('click', function () {
            const yr = yearSelect.value;
            const cat = categorySelect.value;
            loadDashboardData(yr, cat);
            if (window.showToast) {
                window.showToast(`Applied filters: Year [${yr}], Category [${cat}]`, 'info');
            }
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', function () {
            yearSelect.value = 'all';
            categorySelect.value = 'all';
            loadDashboardData('all', 'all');
            if (window.showToast) {
                window.showToast('Dashboard filters reset to defaults.', 'info');
            }
        });
    }

    // Initial load
    loadDashboardData('all', 'all');
});

