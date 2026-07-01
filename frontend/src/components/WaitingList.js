import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { NavBar } from '../App';

function WaitingList() {
  const [patients, setPatients] = useState([]);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [patientsRes, statsRes] = await Promise.all([
        api.get('/api/v1/patients/waiting'),
        api.get('/api/v1/patients/stats'),
      ]);
      setPatients(patientsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const treatPatient = async (id) => {
    try {
      await api.put(`/api/v1/patients/${id}/status?status=treated`);
      fetchData();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      urgent: 'bg-red-500',
      chronic: 'bg-blue-500',
      fast: 'bg-green-500',
    };
    return colors[category] || 'bg-gray-500';
  };

  return (
    <div className="p-6">
      <NavBar />
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-sm text-gray-600">Navbatdagi bemorlar</p>
          <p className="text-2xl font-bold">{stats?.waiting || 0}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow border-l-4 border-red-500">
          <p className="text-sm text-gray-600">Shoshilinch</p>
          <p className="text-2xl font-bold text-red-600">{stats?.urgent || 0}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow border-l-4 border-blue-500">
          <p className="text-sm text-gray-600">Surunkali</p>
          <p className="text-2xl font-bold text-blue-600">{stats?.chronic || 0}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow border-l-4 border-green-500">
          <p className="text-sm text-gray-600">Tez tibbiy</p>
          <p className="text-2xl font-bold text-green-600">{stats?.fast || 0}</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-4 border-b">
          <h3 className="font-semibold">Navbat ro'yxati</h3>
        </div>
        <div className="divide-y">
          {patients.map((patient) => (
            <div key={patient.id} className="p-4 flex justify-between items-center hover:bg-gray-50">
              <div>
                <p className="font-medium">{patient.full_name}</p>
                <p className="text-sm text-gray-600">{patient.complaint}</p>
              </div>
              <div className="flex items-center space-x-4">
                <span className={`px-3 py-1 rounded-full text-white text-sm ${getCategoryColor(patient.category)}`}>
                  {patient.category.toUpperCase()}
                </span>
                <span className="text-sm text-gray-600">
                  {patient.estimated_wait} daqiqa
                </span>
                <button
                  onClick={() => treatPatient(patient.id)}
                  className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
                >
                  Davolandi
                </button>
              </div>
            </div>
          ))}
          {patients.length === 0 && (
            <div className="p-8 text-center text-gray-500">
              Navbat bo'sh
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default WaitingList;
