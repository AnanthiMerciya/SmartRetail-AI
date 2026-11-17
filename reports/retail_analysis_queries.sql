-- ======================================================================
-- SMARTRETAIL AI: BUSINESS ANALYTICS & SALES FORECASTING
-- Database: MySQL / PostgreSQL / SQLite Compatible Analytical Queries
-- Document: SmartRetail_AI_Project_Documentation.docx
-- Date: 2026-11-05
-- Student: Ananthi Merciya M (Reg No: ASML24005)
-- ======================================================================

-- 1. MASTER KPI SUMMARY
-- Calculates overall sales, profit, orders, customers, quantity, and profit margin
SELECT 
    COUNT(DISTINCT `Order ID`) AS total_orders,
    COUNT(DISTINCT `Customer ID`) AS total_customers,
    SUM(`Quantity`) AS total_quantity,
    ROUND(SUM(`Sales`), 2) AS total_sales,
    ROUND(SUM(`Profit`), 2) AS total_profit,
    ROUND((SUM(`Profit`) / SUM(`Sales`)) * 100, 2) AS overall_profit_margin_pct
FROM superstore_cleaned;

-- 2. YEAR-OVER-YEAR SALES & PROFIT GROWTH
SELECT 
    `Year`,
    ROUND(SUM(`Sales`), 2) AS annual_sales,
    ROUND(SUM(`Profit`), 2) AS annual_profit,
    ROUND((SUM(`Profit`) / SUM(`Sales`)) * 100, 2) AS profit_margin_pct,
    COUNT(DISTINCT `Order ID`) AS annual_orders
FROM superstore_cleaned
GROUP BY `Year`
ORDER BY `Year` ASC;

-- 3. CATEGORY PROFITABILITY & REVENUE SHARE
SELECT 
    `Category`,
    ROUND(SUM(`Sales`), 2) AS total_sales,
    ROUND(SUM(`Profit`), 2) AS total_profit,
    ROUND((SUM(`Profit`) / SUM(`Sales`)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(`Sales`) / (SELECT SUM(`Sales`) FROM superstore_cleaned) * 100, 2) AS sales_share_pct,
    ROUND(SUM(`Profit`) / (SELECT SUM(`Profit`) FROM superstore_cleaned) * 100, 2) AS profit_share_pct
FROM superstore_cleaned
GROUP BY `Category`
ORDER BY total_profit DESC;

-- 4. REGIONAL PERFORMANCE RANKING
SELECT 
    `Region`,
    ROUND(SUM(`Sales`), 2) AS regional_sales,
    ROUND(SUM(`Profit`), 2) AS regional_profit,
    SUM(`Quantity`) AS total_quantity,
    ROUND((SUM(`Profit`) / SUM(`Sales`)) * 100, 2) AS profit_margin_pct
FROM superstore_cleaned
GROUP BY `Region`
ORDER BY regional_profit DESC;

-- 5. DISCOUNT SENSITIVITY & PROFIT DESTRUCTION AUDIT
-- Exposes that discounts >= 30% produce negative net earnings
SELECT 
    `Discount`,
    COUNT(*) AS total_transactions,
    SUM(`Quantity`) AS total_units_sold,
    ROUND(SUM(`Sales`), 2) AS total_sales,
    ROUND(SUM(`Profit`), 2) AS total_profit,
    ROUND((SUM(`Profit`) / SUM(`Sales`)) * 100, 2) AS profit_margin_pct,
    CASE 
        WHEN SUM(`Profit`) < 0 THEN 'CRITICAL ALERT: LOSS-MAKING DISCOUNT (RESTRICT)'
        WHEN SUM(`Profit`) >= 0 AND (SUM(`Profit`) / SUM(`Sales`)) < 0.10 THEN 'CAUTION: MARGINAL PROFIT'
        ELSE 'APPROVED: PROFITABLE DISCOUNT'
    END AS policy_recommendation
FROM superstore_cleaned
GROUP BY `Discount`
ORDER BY `Discount` ASC;

-- 6. TOP 10 PROFIT BLEEDERS (LOSS-MAKING PRODUCTS)
SELECT 
    `Product ID`,
    `Product Name`,
    `Category`,
    `Sub-Category`,
    ROUND(SUM(`Sales`), 2) AS total_sales,
    ROUND(SUM(`Profit`), 2) AS total_loss,
    ROUND(AVG(`Discount`) * 100, 1) AS avg_discount_pct
FROM superstore_cleaned
GROUP BY `Product ID`, `Product Name`, `Category`, `Sub-Category`
HAVING SUM(`Profit`) < 0
ORDER BY total_loss ASC
LIMIT 10;

-- 7. TOP 10 PROFIT GENERATORS (STAR SKUS)
SELECT 
    `Product ID`,
    `Product Name`,
    `Category`,
    ROUND(SUM(`Sales`), 2) AS total_sales,
    ROUND(SUM(`Profit`), 2) AS total_profit,
    ROUND((SUM(`Profit`) / SUM(`Sales`)) * 100, 2) AS profit_margin_pct
FROM superstore_cleaned
GROUP BY `Product ID`, `Product Name`, `Category`
ORDER BY total_profit DESC
LIMIT 10;

-- 8. MONTHLY SALES AGGREGATION FOR TIME-SERIES FORECASTING
SELECT 
    `Year`,
    `Month`,
    `Month Name`,
    ROUND(SUM(`Sales`), 2) AS monthly_sales,
    ROUND(SUM(`Profit`), 2) AS monthly_profit,
    SUM(`Quantity`) AS monthly_units
FROM superstore_cleaned
GROUP BY `Year`, `Month`, `Month Name`
ORDER BY `Year` ASC, `Month` ASC;

