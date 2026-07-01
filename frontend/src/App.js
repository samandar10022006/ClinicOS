import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { Toaster, toast } from 'react-hot-toast';
import Login from './components/Login';
import PatientRegistration from './components/PatientRegistration';
import WaitingList from './components/WaitingList';
import BedDashboard from './components/BedDashboard';
import AppointmentBooking from './components/AppointmentBooking';
import AdminPanel from './components/AdminPanel';
import { WebSocketService } from './services/websocket';
import { API_URL } from './services/api';
import './styles/global.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));

  useEffect(() => {
    if (isAuthenticated) {
      const wsUrl = API_URL.replace(/^http/, 'ws') + '/api/v1/patients/ws';
      const websocket = new WebSocketService(wsUrl);
      websocket.connect();
      websocket.onMessage((data) => {
        if (data.type === 'new_patient') {
          toast.success(`Yangi bemor: ${data.data.name}`);
        }
      });

      return () => {
        websocket.disconnect();
      };
    }
  }, [isAuthenticated]);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Toaster position="top-right" />
        <Routes>
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
          <Route path="/dashboard" element={isAuthenticated ? <WaitingList /> : <Navigate to="/login" />} />
          <Route path="/register" element={isAuthenticated ? <PatientRegistration /> : <Navigate to="/login" />} />
          <Route path="/beds" element={isAuthenticated ? <BedDashboard /> : <Navigate to="/login" />} />
          <Route path="/appointments" element={isAuthenticated ? <AppointmentBooking /> : <Navigate to="/login" />} />
          <Route path="/admin" element={isAuthenticated ? <AdminPanel /> : <Navigate to="/login" />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export function NavBar() {
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
        <Link to="/admin" className="text-blue-600 hover:underline">Admin</Link>
      </div>
      <button onClick={logout} className="text-red-600 hover:underline text-sm">Chiqish</button>
    </nav>
  );
}

export default App;
