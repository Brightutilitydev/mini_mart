import React, { useState, useEffect } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { ArrowLeft, Package, Clock, CheckCircle2 } from 'lucide-react';
import apiClient from '../api/client';

export default function Orders({ user }) {
  const [orders, setOrders] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Safely count items regardless of how backend serializes the "items" relationship
  const getItemsCount = (order) => {
    // The Python backend (order.py) defines the relationship as "order_items"
    // We check both order.order_items and order.items to be safe!
    const items = order.order_items || order.items;
    if (!items) return 0;
    if (Array.isArray(items)) return items.length;
    if (typeof items === 'object') return Object.keys(items).length;
    return 0;
  };

  useEffect(() => {
    if (!user) return;
    const fetchOrders = async () => {
      try {
        const userId = user.id || user.user_id || user.uuid || (user.user && user.user.id);
        const response = await apiClient.get('/orders');
        
        const myOrders = Array.isArray(response.data) 
          ? response.data.filter(o => o.user_id === userId) 
          : [];
        
        setOrders(myOrders.reverse());
      } catch (error) {
        console.error("Failed to fetch orders:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchOrders();
  }, [user]);

  if (!user) return <Navigate to="/auth" />;

  return (
    <div className="min-h-screen bg-[#f1f1f2] font-sans text-[#282828] flex flex-col">
      <nav className="bg-white shadow-sm p-4 sticky top-0 z-50">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-gray-500 hover:text-[#f68b1e] font-medium transition-colors">
            <ArrowLeft className="h-5 w-5" /> Back to Storefront
          </Link>
          <span className="font-black text-[#f68b1e] text-2xl tracking-tight">FOOD MART</span>
        </div>
      </nav>

      <main className="flex-grow max-w-5xl mx-auto px-4 py-8 w-full">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
          <Package className="h-6 w-6 text-[#f68b1e]" /> My Orders
        </h2>

        {isLoading ? (
          <div className="text-center py-20 text-gray-500 font-medium">Fetching your order history...</div>
        ) : orders.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-100 p-12 text-center shadow-sm">
            <Package className="h-16 w-16 text-gray-200 mx-auto mb-4 stroke-1" />
            <h3 className="text-xl font-bold text-gray-700 mb-1">No orders yet!</h3>
            <p className="text-gray-400 text-sm mb-6">You haven't placed any orders. Start shopping to see them here.</p>
            <Link to="/" className="inline-block bg-[#f68b1e] text-white px-8 py-3 rounded-lg font-bold hover:bg-orange-600 transition-colors shadow-sm">
              START SHOPPING
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {orders.map((order, idx) => (
              <div key={order.id || idx} className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start border-b border-gray-50 pb-4 mb-4">
                  <div>
                    <p className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Order ID: {order.id?.substring(0, 8) || 'N/A'}</p>
                    <p className="text-sm font-medium text-gray-800 flex items-center gap-1.5">
                      <Clock className="h-4 w-4 text-gray-400" /> Placed successfully
                    </p>
                  </div>
                  <span className="bg-green-50 text-green-700 border border-green-100 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1.5 shadow-sm">
                    <CheckCircle2 className="h-3.5 w-3.5" /> Confirmed
                  </span>
                </div>
                <div className="flex justify-between items-end">
                  <div className="text-sm text-gray-500">
                    {/* Utilizing the robust counting function */}
                    Total Types of Items: <span className="font-bold text-gray-800">{getItemsCount(order)} Products</span>
                  </div>
                  <button className="text-sm font-bold text-[#f68b1e] hover:text-orange-600 transition-colors">
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
