/**
 * API service for furniture recommendations
 */

import { API_URL } from '../constants/app.constants';

/**
 * Get furniture recommendations based on query and filters
 */
export const getRecommendations = async (query, filters = {}, topK = 5) => {
  const requestBody = {
    query,
    top_k: topK,
  };

  // Add filters if provided
  if (Object.keys(filters).length > 0) {
    requestBody.filters = filters;
  }

  const response = await fetch(`${API_URL}/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    throw new Error('Failed to get recommendations');
  }

  return response.json();
};

/**
 * Get analytics dashboard data
 */
export const getAnalytics = async () => {
  const response = await fetch(`${API_URL}/analytics`);

  if (!response.ok) {
    throw new Error('Failed to fetch analytics');
  }

  return response.json();
};

/**
 * Get paginated list of all products
 */
export const getAllProducts = async (skip = 0, limit = 50) => {
  const response = await fetch(`${API_URL}/products?skip=${skip}&limit=${limit}`);

  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }

  return response.json();
};

/**
 * Get specific product by ID
 */
export const getProductById = async (productId) => {
  const response = await fetch(`${API_URL}/product/${productId}`);

  if (!response.ok) {
    throw new Error('Product not found');
  }

  return response.json();
};

/**
 * Check API health
 */
export const checkHealth = async () => {
  const response = await fetch(`${API_URL}/health`);

  if (!response.ok) {
    throw new Error('API health check failed');
  }

  return response.json();
};
