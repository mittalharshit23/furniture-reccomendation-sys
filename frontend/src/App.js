import React, { useState, useEffect, useRef } from 'react';
import { Send, TrendingUp, Package, DollarSign, Tag, ShoppingCart, Filter, X } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

// API Configuration
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [currentPage, setCurrentPage] = useState('recommendation');
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your AI furniture assistant. Describe what you\'re looking for, and I\'ll recommend the perfect pieces for you!'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    maxPrice: '',
    minPrice: '',
    categories: '',
    material: '',
    color: ''
  });
  const [analyticsData, setAnalyticsData] = useState(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load analytics data when switching to analytics page
  useEffect(() => {
    if (currentPage === 'analytics' && !analyticsData) {
      fetchAnalytics();
    }
  }, [currentPage]);

  // Fetch analytics from backend
  const fetchAnalytics = async () => {
    try {
      const response = await fetch(`${API_URL}/analytics`);
      if (response.ok) {
        const data = await response.json();
        setAnalyticsData(data);
      } else {
        console.error('Failed to fetch analytics');
        // Use mock data as fallback
        setAnalyticsData(getMockAnalytics());
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
      // Use mock data as fallback
      setAnalyticsData(getMockAnalytics());
    }
  };

  // Mock analytics data (fallback if backend not available)
  const getMockAnalytics = () => ({
    total_products: 365,
    avg_price: 847.50,
    price_distribution: {
      '$0-200': 45,
      '$200-500': 78,
      '$500-1000': 92,
      '$1000-2000': 56,
      '$2000+': 29
    },
    category_breakdown: {
      'Living Room': 120,
      'Bedroom': 95,
      'Dining Room': 67,
      'Office': 48,
      'Outdoor': 35
    },
    top_brands: [
      { brand: 'ComfortLux', count: 42 },
      { brand: 'WoodCraft', count: 38 },
      { brand: 'ModernHome', count: 35 },
      { brand: 'UrbanStyle', count: 28 },
      { brand: 'ClassicDesign', count: 22 }
    ],
    material_distribution: {
      'Wood': 150,
      'Metal': 80,
      'Fabric': 120,
      'Leather': 45,
      'Glass': 30
    }
  });

  // Handle sending message
  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Prepare request body
      const requestBody = {
        query: input,
        top_k: 5
      };

      // Add filters if any are set
      const activeFilters = {};
      if (filters.maxPrice) activeFilters.max_price = parseFloat(filters.maxPrice);
      if (filters.minPrice) activeFilters.min_price = parseFloat(filters.minPrice);
      if (filters.categories) activeFilters.categories = filters.categories.split(',').map(c => c.trim());
      if (filters.material) activeFilters.material = filters.material;
      if (filters.color) activeFilters.color = filters.color;

      if (Object.keys(activeFilters).length > 0) {
        requestBody.filters = activeFilters;
        console.log('Applying filters:', activeFilters);
      }

      console.log('Sending request:', requestBody);

      // Call backend API
      const response = await fetch(`${API_URL}/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (response.ok) {
        const data = await response.json();
        
        const assistantMessage = {
          role: 'assistant',
          content: data.generated_description || 'Here are my recommendations for you:',
          products: data.products || []
        };
        
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        throw new Error('Failed to get recommendations');
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      
      // Fallback to mock data
      const mockProducts = [
        {
          uniq_id: '1',
          title: 'Modern Velvet Sofa',
          brand: 'ComfortLux',
          price: 899.99,
          description: 'Elegant 3-seater sofa with premium velvet upholstery',
          categories: ['Living Room', 'Sofas'],
          color: 'Navy Blue',
          material: 'Velvet',
          images: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400'
        },
        {
          uniq_id: '2',
          title: 'Rustic Dining Table',
          brand: 'WoodCraft',
          price: 1299.99,
          description: 'Solid oak dining table with natural finish',
          categories: ['Dining Room', 'Tables'],
          color: 'Natural Wood',
          material: 'Oak',
          images: 'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=400'
        }
      ];

      const assistantMessage = {
        role: 'assistant',
        content: 'Based on your preferences, here are some great options:',
        products: mockProducts
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearFilters = () => {
    setFilters({
      maxPrice: '',
      minPrice: '',
      categories: '',
      material: '',
      color: ''
    });
  };

  // Check if any filters are active
  const hasActiveFilters = () => {
    return filters.maxPrice || filters.minPrice || filters.categories || filters.material || filters.color;
  };

  // Format price distribution for charts
  const getPriceDistributionData = () => {
    if (!analyticsData) return [];
    return Object.entries(analyticsData.price_distribution).map(([range, count]) => ({
      range,
      count
    }));
  };

  // Format category breakdown for pie chart
  const getCategoryData = () => {
    if (!analyticsData) return [];
    const colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'];
    return Object.entries(analyticsData.category_breakdown).map(([name, value], index) => ({
      name,
      value,
      color: colors[index % colors.length]
    }));
  };

  // Format material distribution
  const getMaterialData = () => {
    if (!analyticsData) return [];
    return Object.entries(analyticsData.material_distribution).map(([material, count]) => ({
      material,
      count
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center space-x-3">
              <Package className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">FurniMatch AI</h1>
                <p className="text-xs text-gray-500">Powered by Machine Learning</p>
              </div>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => setCurrentPage('recommendation')}
                className={`px-4 py-2 rounded-lg font-medium transition flex items-center space-x-2 ${currentPage === 'recommendation' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
              >
                <ShoppingCart className="w-4 h-4" />
                <span>Recommendations</span>
              </button>
              <button
                onClick={() => setCurrentPage('analytics')}
                className={`px-4 py-2 rounded-lg font-medium transition flex items-center space-x-2 ${currentPage === 'analytics' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
              >
                <TrendingUp className="w-4 h-4" />
                <span>Analytics</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      {currentPage === 'recommendation' ? (
        <div className="max-w-6xl mx-auto p-4 h-[calc(100vh-5rem)] flex gap-4">
          {/* Filters Sidebar */}
          <div className={`${showFilters ? 'w-64' : 'w-0'} transition-all duration-300 overflow-hidden`}>
            <div className="bg-white rounded-lg shadow p-4 h-full">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold text-gray-900 flex items-center gap-2">
                  <Filter className="w-4 h-4" />
                  Filters
                  {hasActiveFilters() && (
                    <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">
                      Active
                    </span>
                  )}
                </h3>
                <button
                  onClick={() => setShowFilters(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Max Price ($)
                  </label>
                  <input
                    type="number"
                    value={filters.maxPrice}
                    onChange={(e) => setFilters({...filters, maxPrice: e.target.value})}
                    placeholder="e.g., 1500"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Min Price ($)
                  </label>
                  <input
                    type="number"
                    value={filters.minPrice}
                    onChange={(e) => setFilters({...filters, minPrice: e.target.value})}
                    placeholder="e.g., 100"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Categories
                  </label>
                  <input
                    type="text"
                    value={filters.categories}
                    onChange={(e) => setFilters({...filters, categories: e.target.value})}
                    placeholder="e.g., Living Room"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Material
                  </label>
                  <input
                    type="text"
                    value={filters.material}
                    onChange={(e) => setFilters({...filters, material: e.target.value})}
                    placeholder="e.g., Wood"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Color
                  </label>
                  <input
                    type="text"
                    value={filters.color}
                    onChange={(e) => setFilters({...filters, color: e.target.value})}
                    placeholder="e.g., Blue"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <button
                  onClick={clearFilters}
                  className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
                >
                  Clear Filters
                </button>
              </div>
            </div>
          </div>

          {/* Chat Interface */}
          <div className="flex-1 flex flex-col">
            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto mb-4 space-y-4 bg-white rounded-lg shadow p-6">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-3xl ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-900'} rounded-2xl px-4 py-3`}>
                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                    {msg.products && msg.products.length > 0 && (
                      <div className="mt-4 space-y-4">
                        {msg.products.map((product) => (
                          <div key={product.uniq_id} className="bg-white rounded-lg p-4 shadow-sm">
                            <div className="flex space-x-4">
                              <img
                                src={product.images || 'https://via.placeholder.com/150'}
                                alt={product.title}
                                className="w-32 h-32 object-cover rounded-lg flex-shrink-0"
                                onError={(e) => {
                                  e.target.src = 'https://via.placeholder.com/150?text=No+Image';
                                }}
                              />
                              <div className="flex-1 min-w-0">
                                <h3 className="font-bold text-gray-900 text-lg truncate">{product.title}</h3>
                                <p className="text-sm text-gray-600 mb-2">{product.brand}</p>
                                <p className="text-sm text-gray-700 mb-2 line-clamp-2">{product.description}</p>
                                <div className="flex flex-wrap items-center gap-3">
                                  <span className="text-lg font-bold text-blue-600">${parseFloat(product.price).toFixed(2)}</span>
                                  {product.material && (
                                    <span className="text-xs bg-gray-200 px-2 py-1 rounded">{product.material}</span>
                                  )}
                                  {product.color && (
                                    <span className="text-xs bg-gray-200 px-2 py-1 rounded">{product.color}</span>
                                  )}
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-2xl px-4 py-3">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="bg-white rounded-lg shadow-lg p-4">
              <div className="flex space-x-2">
                {!showFilters && (
                  <button
                    onClick={() => setShowFilters(true)}
                    className={`px-4 py-3 border rounded-lg transition relative ${
                      hasActiveFilters() 
                        ? 'border-blue-500 bg-blue-50 hover:bg-blue-100' 
                        : 'border-gray-300 hover:bg-gray-100'
                    }`}
                    title="Show Filters"
                  >
                    <Filter className={`w-5 h-5 ${hasActiveFilters() ? 'text-blue-600' : 'text-gray-600'}`} />
                    {hasActiveFilters() && (
                      <span className="absolute -top-1 -right-1 w-3 h-3 bg-blue-600 rounded-full"></span>
                    )}
                  </button>
                )}
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Describe your ideal furniture... (e.g., 'modern blue sofa for small living room')"
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!input.trim() || loading}
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center space-x-2"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      ) : (
        // Analytics Dashboard
        <div className="max-w-7xl mx-auto p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Product Analytics Dashboard</h1>
          
          {!analyticsData ? (
            <div className="flex justify-center items-center h-64">
              <div className="text-gray-500">Loading analytics...</div>
            </div>
          ) : (
            <>
              {/* Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Products</p>
                      <p className="text-3xl font-bold text-gray-900">{analyticsData.total_products}</p>
                    </div>
                    <Package className="w-12 h-12 text-blue-600 opacity-80" />
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Avg Price</p>
                      <p className="text-3xl font-bold text-gray-900">${analyticsData.avg_price.toFixed(0)}</p>
                    </div>
                    <DollarSign className="w-12 h-12 text-green-600 opacity-80" />
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Categories</p>
                      <p className="text-3xl font-bold text-gray-900">{Object.keys(analyticsData.category_breakdown).length}</p>
                    </div>
                    <Tag className="w-12 h-12 text-purple-600 opacity-80" />
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Brands</p>
                      <p className="text-3xl font-bold text-gray-900">{analyticsData.top_brands.length}</p>
                    </div>
                    <TrendingUp className="w-12 h-12 text-orange-600 opacity-80" />
                  </div>
                </div>
              </div>

              {/* Charts */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                {/* Price Distribution */}
                <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-lg font-bold text-gray-900 mb-4">Price Distribution</h2>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={getPriceDistributionData()}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="range" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#3b82f6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* Category Breakdown */}
                <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-lg font-bold text-gray-900 mb-4">Category Breakdown</h2>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={getCategoryData()}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                        outerRadius={100}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {getCategoryData().map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>

                {/* Material Distribution */}
                <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-lg font-bold text-gray-900 mb-4">Material Distribution</h2>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={getMaterialData()} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" />
                      <YAxis dataKey="material" type="category" width={100} />
                      <Tooltip />
                      <Bar dataKey="count" fill="#10b981" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* Top Brands */}
                <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-lg font-bold text-gray-900 mb-4">Top Brands</h2>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={analyticsData.top_brands}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="brand" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#8b5cf6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
