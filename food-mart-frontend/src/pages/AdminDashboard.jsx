import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  Database, Store, PlusCircle, Tag, Package, Trash2, 
  Edit3, CheckCircle2, AlertCircle, X, Layers 
} from 'lucide-react';
import apiClient from '../api/client';

export default function AdminDashboard({ categories, products, triggerReload }) {
  const [status, setStatus] = useState({ type: '', message: '' });
  const [activeTab, setActiveTab] = useState('products');
  
  const [catName, setCatName] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [prodForm, setProdForm] = useState({
    name: '', price: '', brand: '', category_id: '', stock: 20, package_size: '', description: ''
  });

  const displayAlert = (type, message) => {
    setStatus({ type, message });
    setTimeout(() => setStatus({ type: '', message: '' }), 4000);
  };

  const handleCategorySubmit = async (e) => {
    e.preventDefault();
    if (!catName.trim()) return;
    try {
      if (editingId) {
        await apiClient.put(`/categories/${editingId}`, { name: catName });
        displayAlert('success', `Category updated successfully!`);
      } else {
        await apiClient.post('/categories', { name: catName });
        displayAlert('success', `Category "${catName}" added successfully!`);
      }
      setCatName('');
      setEditingId(null);
      triggerReload();
    } catch (err) {
      displayAlert('error', err.response?.data?.error || 'Category operation failed.');
    }
  };

  const handleDeleteCategory = async (id) => {
    if (!window.confirm("Are you sure? Deleting this category might impact linked products!")) return;
    try {
      await apiClient.delete(`/categories/${id}`);
      displayAlert('success', 'Category deleted from database.');
      triggerReload();
    } catch (err) {
      displayAlert('error', err.response?.data?.error || 'Failed to delete category.');
    }
  };

  const handleProductSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('name', prodForm.name);
    formData.append('price', prodForm.price);
    formData.append('category_id', prodForm.category_id);
    formData.append('stock', prodForm.stock);
    if (prodForm.brand) formData.append('brand', prodForm.brand);
    if (prodForm.package_size) formData.append('package_size', prodForm.package_size);
    if (prodForm.description) formData.append('description', prodForm.description);

    try {
      if (editingId) {
        await apiClient.put(`/products/${editingId}`, formData, { headers: { 'Content-Type': 'multipart/form-data' }});
        displayAlert('success', 'Product updated successfully!');
      } else {
        await apiClient.post('/products', formData, { headers: { 'Content-Type': 'multipart/form-data' }});
        displayAlert('success', `Product "${prodForm.name}" created!`);
      }
      setEditingId(null);
      setProdForm({ name: '', price: '', brand: '', category_id: '', stock: 20, package_size: '', description: '' });
      triggerReload();
    } catch (err) {
      displayAlert('error', err.response?.data?.error || 'Product operation failed.');
    }
  };

  const handleEditProductClick = (product) => {
    setEditingId(product.id);
    setProdForm({
      name: product.name, price: product.price, brand: product.brand || '',
      category_id: product.category_id || '', stock: product.stock,
      package_size: product.package_size || '', description: product.description || ''
    });
    setActiveTab('products');
  };

  const handleDeleteProduct = async (id) => {
    if (!window.confirm("Delete this product permanently?")) return;
    try {
      await apiClient.delete(`/products/${id}`);
      displayAlert('success', 'Product dropped from inventory.');
      triggerReload();
    } catch (err) {
      displayAlert('error', err.response?.data?.error || 'Failed to delete product.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
      {/* Isolated Admin Top-Bar (Dark Mode) */}
      <nav className="bg-gray-950 text-white shadow-md p-4 flex justify-between items-center px-4 sm:px-8 sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <Database className="h-6 w-6 text-[#f68b1e]" />
          <div>
            <span className="block font-black tracking-widest uppercase text-sm leading-none">FoodMart Console</span>
            <span className="block text-[10px] text-gray-400 font-mono mt-1">v1.0.0 (Authorized Access)</span>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <button 
            onClick={async () => {
              // Gracefully handle the missing /logout route without crashing
              try { await apiClient.post('/logout'); } catch(e) {} 
              localStorage.removeItem('foodMartUser');
              window.location.href = '/';
            }} 
            className="flex items-center gap-2 text-xs font-bold text-red-400 hover:text-white hover:bg-red-500/20 px-3 py-2 rounded-lg transition-colors"
          >
            End Session
          </button>
          
          <Link to="/" className="flex items-center gap-2 text-xs font-bold bg-white/10 hover:bg-white/20 px-4 py-2.5 rounded-lg transition-colors border border-white/5">
            <Store className="h-4 w-4" /> Storefront
          </Link>
        </div>
      </nav>

      {/* Main Admin Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-gray-200 pb-5 mb-8 gap-4">
          <div>
            <h1 className="text-2xl font-black text-gray-950 tracking-tight">Database Administration</h1>
            <p className="text-sm text-gray-500">Manage products, categories, and inventory via active APIs.</p>
          </div>
          
          <div className="flex bg-gray-100 p-1 rounded-xl w-full md:w-auto">
            <button onClick={() => { setActiveTab('products'); setEditingId(null); }} className={`flex-1 md:flex-none px-5 py-2 rounded-lg text-sm font-bold transition-all flex items-center justify-center gap-2 ${activeTab === 'products' ? 'bg-white text-[#f68b1e] shadow-sm' : 'text-gray-600 hover:text-gray-900'}`}>
              <Package className="h-4 w-4" /> Products Inventory
            </button>
            <button onClick={() => { setActiveTab('categories'); setEditingId(null); }} className={`flex-1 md:flex-none px-5 py-2 rounded-lg text-sm font-bold transition-all flex items-center justify-center gap-2 ${activeTab === 'categories' ? 'bg-white text-[#f68b1e] shadow-sm' : 'text-gray-600 hover:text-gray-900'}`}>
              <Layers className="h-4 w-4" /> Categories
            </button>
          </div>
        </div>

        {status.message && (
          <div className={`p-4 rounded-xl flex items-start gap-3 text-sm mb-6 max-w-2xl animate-fade-in shadow-sm ${status.type === 'success' ? 'bg-green-50 text-green-700 border border-green-100' : 'bg-red-50 text-red-700 border border-red-100'}`}>
            {status.type === 'success' ? <CheckCircle2 className="h-5 w-5 mt-0.5" /> : <AlertCircle className="h-5 w-5 mt-0.5" />}
            <span className="font-medium">{status.message}</span>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm sticky top-24">
              {activeTab === 'categories' ? (
                <>
                  <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <PlusCircle className="h-5 w-5 text-[#f68b1e]" /> 
                    {editingId ? 'Modify Category' : 'Create Category'}
                  </h3>
                  <form onSubmit={handleCategorySubmit} className="space-y-4">
                    <div>
                      <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Name</label>
                      <input type="text" required placeholder="e.g. Beverages" className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#f68b1e] text-sm" value={catName} onChange={e => setCatName(e.target.value)} />
                    </div>
                    <div className="flex gap-2">
                      <button type="submit" className="flex-1 bg-[#f68b1e] text-white py-2 rounded-lg text-sm font-bold hover:bg-orange-600 transition-colors">
                        {editingId ? 'Update Category' : 'Save Category'}
                      </button>
                      {editingId && (
                        <button type="button" onClick={() => { setEditingId(null); setCatName(''); }} className="p-2 bg-gray-100 rounded-lg text-gray-500 hover:bg-gray-200">
                          <X className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                  </form>
                </>
              ) : (
                <>
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                      <PlusCircle className="h-5 w-5 text-[#f68b1e]" /> 
                      {editingId ? 'Modify Product' : 'Add Product'}
                    </h3>
                    {editingId && (
                      <button onClick={() => { setEditingId(null); setProdForm({ name: '', price: '', brand: '', category_id: '', stock: 20, package_size: '', description: '' }); }} className="text-xs font-bold text-gray-400 hover:text-gray-600 flex items-center gap-1">
                        <X className="h-3.5 w-3.5" /> Clear Edit
                      </button>
                    )}
                  </div>
                  <form onSubmit={handleProductSubmit} className="space-y-3.5">
                    <div>
                      <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Product Title *</label>
                      <input required type="text" className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#f68b1e]" value={prodForm.name} onChange={e => setProdForm({...prodForm, name: e.target.value})} />
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Price (₦) *</label>
                        <input required type="number" step="0.01" className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#f68b1e]" value={prodForm.price} onChange={e => setProdForm({...prodForm, price: e.target.value})} />
                      </div>
                      <div>
                        <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Stock Vol *</label>
                        <input required type="number" className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#f68b1e]" value={prodForm.stock} onChange={e => setProdForm({...prodForm, stock: e.target.value})} />
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Category Link *</label>
                        <select required className="w-full px-2 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#f68b1e]" value={prodForm.category_id} onChange={e => setProdForm({...prodForm, category_id: e.target.value})}>
                          <option value="">Select...</option>
                          {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                        </select>
                      </div>
                      <div>
                        <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Brand</label>
                        <input type="text" className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#f68b1e]" value={prodForm.brand} onChange={e => setProdForm({...prodForm, brand: e.target.value})} />
                      </div>
                    </div>
                    <div>
                      <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Package Sizing</label>
                      <input type="text" placeholder="e.g. 50cl, 1kg" className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#f68b1e]" value={prodForm.package_size} onChange={e => setProdForm({...prodForm, package_size: e.target.value})} />
                    </div>
                    <button type="submit" className="w-full bg-[#f68b1e] text-white py-2.5 rounded-lg text-sm font-bold hover:bg-orange-600 transition-colors shadow-sm mt-2">
                      {editingId ? 'Apply Database Changes' : 'Commit to Storage'}
                    </button>
                  </form>
                </>
              )}
            </div>
          </div>

          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              {activeTab === 'categories' ? (
                <div>
                  <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">Database Categories Records</h3>
                  <div className="divide-y divide-gray-100">
                    {categories.map(cat => (
                      <div key={cat.id} className="py-3 flex justify-between items-center group">
                        <div className="flex items-center gap-2">
                          <Tag className="h-4 w-4 text-[#f68b1e]" />
                          <span className="font-medium text-gray-800 text-sm">{cat.name}</span>
                          <span className="text-[10px] text-gray-300 font-mono">({cat.id.substring(0,8)})</span>
                        </div>
                        <div className="flex items-center gap-1 opacity-80 group-hover:opacity-100 transition-opacity">
                          <button onClick={() => { setEditingId(cat.id); setCatName(cat.name); }} className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-md">
                            <Edit3 className="h-4 w-4" />
                          </button>
                          <button onClick={() => handleDeleteCategory(cat.id)} className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md">
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div>
                  <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">Warehouse SKU Records</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse text-sm">
                      <thead>
                        <tr className="border-b border-gray-100 text-gray-400 font-semibold">
                          <th className="pb-3">Product</th>
                          <th className="pb-3">Category</th>
                          <th className="pb-3">Price</th>
                          <th className="pb-3">Stock</th>
                          <th className="pb-3 text-right">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-100">
                        {products.map(prod => (
                          <tr key={prod.id} className="hover:bg-gray-50/50 transition-colors group">
                            <td className="py-3.5 font-medium text-gray-900">
                              <div>{prod.name}</div>
                              <div className="text-xs text-gray-400 font-normal">{prod.brand || 'No Brand'}</div>
                            </td>
                            <td className="py-3.5 text-gray-500">
                              {categories.find(c => c.id === prod.category_id)?.name || 'Unlinked'}
                            </td>
                            <td className="py-3.5 font-bold text-gray-800">₦{parseFloat(prod.price).toLocaleString()}</td>
                            <td className="py-3.5">
                              <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${prod.stock > 5 ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                                {prod.stock} units
                              </span>
                            </td>
                            <td className="py-3.5 text-right">
                              <div className="flex justify-end gap-1">
                                <button onClick={() => handleEditProductClick(prod)} className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-md">
                                  <Edit3 className="h-4 w-4" />
                                </button>
                                <button onClick={() => handleDeleteProduct(prod.id)} className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md">
                                  <Trash2 className="h-4 w-4" />
                                </button>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
