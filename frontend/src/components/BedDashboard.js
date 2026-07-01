import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

function BedDashboard() {
  const [beds, setBeds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBeds();
    const interval = setInterval(fetchBeds, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchBeds = async () => {
    try {
      const response = await api.get('/api/v1/admin/beds');
      setBeds(response.data);
    } catch (error) {
      console.error('Error fetching beds:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      urgent: 'border-red-500 bg-red-50',
      chronic: 'border-blue-500 bg-blue-50',
      fast: 'border-green-500 bg-green-50',
    };
    return colors[category] || 'border-gray-300 bg-gray-50';
  };

  return (
    <div className="p-6">
      <NavBar />
      <h2 className="text-2xl font-bold text-gray-800 mb-6">🛏 Palatalar holati</h2>

      {loading ? (
        <p className="text-gray-500">Yuklanmoqda...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {beds.map((bed) => (
            <div
              key={bed.id}
              className={`p-4 rounded-lg border-l-4 shadow ${getCategoryColor(bed.category)}`}
            >
              <div className="flex justify-between items-center">
                <span className="font-bold text-lg">{bed.room_number}</span>
                <span className={`px-2 py-1 rounded text-xs font-bold ${
                  bed.is_available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {bed.is_available ? 'Bo\'sh' : 'Band'}
                </span>
              </div>
              <p className="text-sm text-gray-600 mt-2">Bo'lim: {bed.ward}</p>
              <p className="text-sm text-gray-600">Kategoriya: {bed.category}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function NavBar() {
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };

  return (
    <nav className="bg-white shadow mb-6 rounded-lg p-4 flex flex-wrap gap-4 items-center justify-between">
      <div className="flex flex-wrap gap-4">
        <Link to="/dashboard" className="text-blue-600 hover:underline">Navbat</Link>
        <Link to="/register" className="text-blue-600 hover:underline">Ro'yxat</Link>
        <Link to="/beds" className="text-blue-600 hover:underline font-bold">Palatalar</Link>
        <Link to="/appointments" className="text-blue-600 hover:underline">Qabul</Link>
        <Link to="/admin" className="text-blue-600 hover:underline">Admin</Link>
      </div>
      <button onClick={logout} className="text-red-600 hover:underline text-sm">Chiqish</button>
    </nav>
  );
}

export default BedDashboard;
