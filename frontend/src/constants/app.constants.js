/**
 * Application-wide constants
 */

// API Configuration
export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// App Metadata
export const APP_NAME = 'FurniMatch AI';
export const APP_VERSION = '2.0.0';

// Default Values
export const DEFAULT_TOP_K = 5;
export const MAX_PRODUCTS_PER_PAGE = 50;

// Chart Colors
export const CHART_COLORS = {
  primary: '#3b82f6',
  secondary: '#8b5cf6',
  tertiary: '#ec4899',
  quaternary: '#f59e0b',
  quinary: '#10b981',
};

// Price Ranges for Filters
export const PRICE_RANGES = [
  { label: 'Under $100', value: { max: 100 } },
  { label: '$100 - $500', value: { min: 100, max: 500 } },
  { label: '$500 - $1000', value: { min: 500, max: 1000 } },
  { label: 'Over $1000', value: { min: 1000 } },
];

// Popular Materials
export const COMMON_MATERIALS = ['Wood', 'Metal', 'Fabric', 'Leather', 'Glass', 'Plastic'];

// Popular Colors
export const COMMON_COLORS = ['Black', 'White', 'Brown', 'Gray', 'Blue', 'Beige'];
