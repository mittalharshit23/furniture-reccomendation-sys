/**
 * Utility functions for the application
 */

/**
 * Format price as currency string
 */
export const formatPrice = (price) => {
  return `$${parseFloat(price).toFixed(2)}`;
};

/**
 * Format large numbers with commas
 */
export const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

/**
 * Truncate text to specified length
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text || text.length <= maxLength) return text;
  return text.substring(0, maxLength).trim() + '...';
};

/**
 * Check if filters are active
 */
export const hasActiveFilters = (filters) => {
  return Object.values(filters).some((value) => value !== '' && value !== null && value !== undefined);
};

/**
 * Parse filter values for API request
 */
export const parseFilters = (filters) => {
  const activeFilters = {};

  if (filters.maxPrice) {
    activeFilters.max_price = parseFloat(filters.maxPrice);
  }

  if (filters.minPrice) {
    activeFilters.min_price = parseFloat(filters.minPrice);
  }

  if (filters.categories) {
    activeFilters.categories = filters.categories
      .split(',')
      .map((c) => c.trim())
      .filter((c) => c);
  }

  if (filters.material) {
    activeFilters.material = filters.material;
  }

  if (filters.color) {
    activeFilters.color = filters.color;
  }

  return activeFilters;
};

/**
 * Handle image load errors
 */
export const handleImageError = (e) => {
  e.target.src = 'https://via.placeholder.com/150?text=No+Image';
};

/**
 * Debounce function calls
 */
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};
