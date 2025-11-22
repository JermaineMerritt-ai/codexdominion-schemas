
-- IONOS Analytics Platform Database Schema

CREATE DATABASE IF NOT EXISTS analytics_platform;
USE analytics_platform;

-- Stock Analytics Tables
CREATE TABLE stock_picks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    current_price DECIMAL(10,2),
    target_price DECIMAL(10,2),
    stop_loss DECIMAL(10,2),
    confidence_score DECIMAL(5,2),
    ai_reasoning TEXT,
    sector VARCHAR(100),
    risk_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_symbol (symbol),
    INDEX idx_created_at (created_at)
);

CREATE TABLE customer_portfolios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(100) NOT NULL,
    investment_amount DECIMAL(12,2),
    risk_tolerance VARCHAR(50),
    allocation JSON,
    expected_return VARCHAR(20),
    diversification_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer (customer_id),
    INDEX idx_risk (risk_tolerance)
);

CREATE TABLE portfolio_holdings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id INT,
    symbol VARCHAR(10) NOT NULL,
    shares DECIMAL(12,4),
    purchase_price DECIMAL(10,2),
    current_value DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES customer_portfolios(id),
    INDEX idx_portfolio (portfolio_id),
    INDEX idx_symbol (symbol)
);

CREATE TABLE amm_pools (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pool_name VARCHAR(50) NOT NULL,
    apy DECIMAL(5,2),
    tvl DECIMAL(15,2),
    daily_volume DECIMAL(15,2),
    risk_level VARCHAR(50),
    minimum_deposit DECIMAL(10,2),
    impermanent_loss_risk DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_pool_name (pool_name)
);

-- Data Analytics Tables
CREATE TABLE business_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    business_type VARCHAR(100),
    metric_name VARCHAR(100),
    metric_value DECIMAL(12,4),
    metric_unit VARCHAR(50),
    analysis_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_business_type (business_type),
    INDEX idx_metric_name (metric_name),
    INDEX idx_date (analysis_date)
);

CREATE TABLE customer_analytics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_segment VARCHAR(100),
    avg_age INT,
    income_range VARCHAR(100),
    purchase_frequency DECIMAL(5,2),
    avg_order_value DECIMAL(10,2),
    lifetime_value DECIMAL(12,2),
    retention_probability DECIMAL(5,2),
    analysis_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_segment (customer_segment),
    INDEX idx_date (analysis_date)
);

CREATE TABLE market_research (
    id INT AUTO_INCREMENT PRIMARY KEY,
    industry VARCHAR(100),
    market_size_tam DECIMAL(15,2),
    market_size_sam DECIMAL(15,2),
    market_size_som DECIMAL(15,2),
    growth_rate DECIMAL(5,2),
    research_insights JSON,
    analysis_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_industry (industry),
    INDEX idx_date (analysis_date)
);

CREATE TABLE kpi_dashboard (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kpi_name VARCHAR(100),
    current_value DECIMAL(10,4),
    target_value DECIMAL(10,4),
    unit VARCHAR(50),
    category VARCHAR(100),
    measurement_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_kpi_name (kpi_name),
    INDEX idx_category (category),
    INDEX idx_date (measurement_date)
);

-- User management and authentication
CREATE TABLE platform_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_role VARCHAR(50) DEFAULT 'customer',
    subscription_tier VARCHAR(50) DEFAULT 'basic',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- API usage tracking
CREATE TABLE api_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    endpoint VARCHAR(255),
    request_count INT DEFAULT 1,
    usage_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES platform_users(id),
    INDEX idx_user_date (user_id, usage_date),
    INDEX idx_endpoint (endpoint)
);

-- Sample data insertion
INSERT INTO stock_picks (symbol, company_name, current_price, target_price, stop_loss, confidence_score, ai_reasoning, sector, risk_level) VALUES
('AAPL', 'Apple Inc.', 175.50, 185.00, 168.00, 92.5, 'Technical analysis shows bullish breakout pattern with strong momentum indicators', 'Technology', 'Medium'),
('MSFT', 'Microsoft Corp.', 420.25, 445.00, 405.00, 89.8, 'Fundamental analysis reveals undervalued metrics with strong earnings growth potential', 'Technology', 'Low'),
('TSLA', 'Tesla Inc.', 245.75, 265.00, 235.00, 87.3, 'Sentiment analysis indicates positive market sentiment shift and institutional interest', 'Automotive', 'High');

INSERT INTO amm_pools (pool_name, apy, tvl, daily_volume, risk_level, minimum_deposit, impermanent_loss_risk) VALUES
('ETH/USDC', 12.4, 850000, 120000, 'Medium', 1000, 4.2),
('BTC/USDC', 8.9, 1200000, 95000, 'Low', 2000, 2.8),
('AAPL/USDC', 15.6, 450000, 65000, 'High', 500, 7.1);
