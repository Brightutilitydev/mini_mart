import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Database, User, LogOut, ShoppingCart, Search, Grid, ShieldCheck, ShoppingBag, ChevronDown, Package, Settings, Code } from 'lucide-react';

export default function Storefront({ user, handleLogout, products, categories, addToCart, cartCount }) {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);

  // DEMO MODE: Always show the Admin button.
  const isAdmin = true; 

  const filteredProducts = products.filter(product => {
    const matchesCategory = selectedCategory ? product.category_id === selectedCategory : true;
    const matchesSearch = searchQuery
      ? product.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
        (product.brand && product.brand.toLowerCase().includes(searchQuery.toLowerCase()))
      : true;
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-[#f1f1f2] font-sans text-[#282828] flex flex-col">
      
      {/* 🛠️ DEVELOPER DEBUG BANNER */}
      <div className="bg-yellow-200 text-yellow-900 text-xs font-bold py-1.5 px-4 flex justify-center items-center gap-2 tracking-wide">
        <Code className="h-4 w-4" />
        DEMO MODE ACTIVE: SECURITY DISABLED FOR HOSTING
      </div>

      <nav className="bg-white shadow-sm p-4 flex justify-between items-center px-4 sm:px-8 sticky top-0 z-50">
        <Link to="/" className="font-black text-[#f68b1e] text-2xl tracking-tight">
          FOOD MART
        </Link>
        
        <div className="hidden md:flex flex-1 max-w-xl mx-8 relative">
          <input 
            type="text" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search products, brands and categories..." 
            className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#f68b1e] transition-all"
          />
          <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>

        <div className="flex items-center space-x-6">
          {isAdmin && (
            <Link to="/admin" className="text-xs font-bold text-gray-600 hover:text-[#f68b1e] border border-gray-200 px-3 py-1.5 rounded-lg hidden md:flex items-center gap-1.5 transition-colors shadow-sm">
              <Database className="h-3.5 w-3.5 text-[#f68b1e]" /> Enter Console
            </Link>
          )}

          {user ? (
            <div className="relative">
              <button 
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="flex items-center space-x-2 text-gray-700 hover:text-[#f68b1e] font-medium transition-colors cursor-pointer p-1"
              >
                <User className="h-5 w-5 text-[#f68b1e]" />
                <span className="text-sm">Hi, {user.first_name || 'User'}</span>
                <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${isUserMenuOpen ? 'rotate-180' : ''}`} />
              </button>

              {isUserMenuOpen && (
                <div className="absolute right-0 mt-3 w-56 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50 animate-fade-in">
                  <div className="p-4 border-b border-gray-50 bg-gray-50/50">
                    <p className="text-sm font-bold text-gray-900">{user.first_name || 'User'}</p>
                  </div>
                  <div className="p-2 border-t border-gray-50">
                    <button 
                      onClick={() => {
                        setIsUserMenuOpen(false);
                        handleLogout();
                      }} 
                      className="w-full flex items-center gap-3 px-3 py-2.5 text-sm font-bold text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <LogOut className="h-4 w-4" /> Logout
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <Link to="/auth" className="flex items-center space-x-2 text-gray-700 hover:text-[#f68b1e] font-medium transition-colors">
              <User className="h-6 w-6" />
              <span className="inline text-sm">Login / Register</span>
            </Link>
          )}
          
          <Link to="/cart" className="flex items-center space-x-1 text-gray-700 hover:text-[#f68b1e] transition-colors relative">
            <ShoppingCart className="h-6 w-6" />
            <span className="hidden md:inline font-medium text-sm">Cart</span>
            {cartCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-[#f68b1e] text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center shadow-sm">
                {cartCount}
              </span>
            )}
          </Link>
        </div>
      </nav>

      <main className="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        <div className="bg-gradient-to-r from-[#f68b1e] to-orange-400 rounded-2xl shadow-md p-8 mb-8 text-white flex flex-col md:flex-row items-center justify-between">
          <div className="max-w-xl">
            <span className="bg-white/20 text-white text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full">Ramadan Deals</span>
            <h2 className="text-3xl md:text-5xl font-black mb-3 mt-3 tracking-tight">Fresh Groceries, Fast Delivery!</h2>
            <p className="text-sm md:text-base text-orange-50 mb-4">Stock your home shelves with premium food items, beverages and household ingredients at wholesale prices.</p>
          </div>
          <div className="hidden md:block bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/10">
            <ShieldCheck className="h-20 w-20 text-white stroke-1" />
          </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          <div className="w-full lg:w-64 flex-shrink-0">
            <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm sticky top-24">
              <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
                <Grid className="h-4 w-4 text-[#f68b1e]" /> Categories
              </h3>
              
              <div className="relative">
                <select
                  value={selectedCategory || ''}
                  onChange={(e) => setSelectedCategory(e.target.value || null)}
                  className="w-full appearance-none bg-gray-50 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded-lg text-sm font-medium focus:outline-none focus:ring-2 focus:ring-[#f68b1e] focus:border-transparent transition-all cursor-pointer shadow-sm"
                >
                  <option value="">All Categories</option>
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <div className="flex-grow">
            <div className="mb-6 flex items-center justify-between border-b border-gray-100 pb-4">
              <h2 className="text-xl font-bold text-gray-800">
                {selectedCategory ? categories.find(c => c.id === selectedCategory)?.name : 'All Products'}
              </h2>
              <span className="text-sm text-gray-500 font-medium">{filteredProducts.length} Items found</span>
            </div>
            
            {filteredProducts.length === 0 ? (
              <div className="bg-white rounded-xl border border-gray-100 p-16 text-center shadow-sm">
                <ShoppingBag className="h-16 w-16 text-gray-300 mx-auto stroke-1 mb-4" />
                <h3 className="text-lg font-bold text-gray-700">No Products Found</h3>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredProducts.map(product => (
                  <div key={product.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-300 group flex flex-col">
                    <div className="relative h-48 overflow-hidden bg-gray-50 flex items-center justify-center">
                      {product.image_url ? (
                        <img src={product.image_url} alt={product.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                      ) : (
                        <ShoppingBag className="h-12 w-12 text-gray-300 stroke-1" />
                      )}
                    </div>
                    <div className="p-4 flex flex-col flex-grow">
                      <h3 className="text-sm font-semibold text-gray-800 line-clamp-2 h-10 leading-tight">{product.name}</h3>
                      <p className="text-xs text-gray-400 mt-1">{product.brand || 'Generic'}</p>
                      <div className="mt-auto pt-4 border-t border-gray-50 flex flex-col">
                        <span className="text-lg font-bold text-gray-900">₦{parseFloat(product.price).toLocaleString()}</span>
                        {product.stock <= 0 ? (
                          <span className="text-xs font-semibold text-red-500 mt-2 text-center bg-red-50 py-1.5 rounded-lg">Out Of Stock</span>
                        ) : (
                          <button 
                            onClick={() => addToCart(product)}
                            className="w-full mt-3 bg-[#f68b1e] text-white py-2 rounded-lg text-sm font-bold hover:bg-orange-600 transition-colors shadow-sm flex justify-center items-center gap-2"
                          >
                            <ShoppingCart className="h-4 w-4" /> ADD TO CART
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}