import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

function AdminPanel() {
  const [dashboard, setDashboard] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [dashRes, statsRes] = await Promise.all([
        api.get('/api/v1/admin/dashboard'),
        api.get('/api/v1/patients/stats'),
      ]);
      setDashboard(dashRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching admin data:', error);
    }
  };

  return (
    <div className="p-6">
      <NavBar />
      <h2 className="text-2xl font-bold text-gray-800 mb-6">📊 Admin panel</h2>

      {dashboard && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatCard label="Jami palatalar" value={dashboard.total_beds} icon="🛏" />
          <StatCard label="Bo'sh palatalar" value={dashboard.available_beds} icon="🟢" />
          <StatCard label="Bandlik darajasi" value={`${dashboard.occupancy_rate}%`} icon="📈" />
          <StatCard label="Jami bemorlar" value={dashboard.total_patients} icon="👥" />
        </div>
      )}

      {stats && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-semibold mb-4">Bemorlar statistikasi</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <p className="text-2xl font-bold">{stats.waiting}</p>
              <p className="text-sm text-gray-600">Navbatda</p>
            </div>
            <div className="text-center p-4 bg-red-50 rounded-lg">
              <p className="text-2xl font-bold text-red-600">{stats.urgent}</p>
              <p className="text-sm text-gray-600">Shoshilinch</p>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <p className="text-2xl font-bold text-blue-600">{stats.chronic}</p>
              <p className="text-sm text-gray-600">Surunkali</p>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <p className="text-2xl font-bold text-green-600">{stats.fast}</p>
              <p className="text-sm text-gray-600">Tez tibbiy</p>
            </div>
          </div>
          <p className="mt-4 text-gray-600">
            Navbatda: {dashboard?.waiting_patients || 0} ta bemor
          </p>
        </div>
      )}
    </div>
  );
}

function StatCard({ label, value, icon }) {
  return (
    <div className="bg-white rounded-lg shadow p-6 text-center">
      <p className="text-3xl mb-2">{icon}</p>
      <p className="text-2xl font-bold text-gray-800">{value}</p>
      <p className="text-sm text-gray-600">{label}</p>
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
        <Link to="/beds" className="text-blue-600 hover:underline">Palatalar</Link>
        <Link to="/appointments" className="text-blue-600 hover:underline">Qabul</Link>
        <Link to="/admin" className="text-blue-600 hover:underline font-bold">Admin</Link>
      </div>
      <button onClick={logout} className="text-red-600 hover:underline text-sm">Chiqish</button>
    </nav>
  );
}

export default AdminPanel;
