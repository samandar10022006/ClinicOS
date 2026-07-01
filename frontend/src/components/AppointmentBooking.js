import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import api from '../services/api';

function AppointmentBooking() {
  const { register, handleSubmit, reset } = useForm();
  const [loading, setLoading] = useState(false);
  const [appointments, setAppointments] = useState([]);
  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
    fetchAppointments();
    fetchDoctors();
  }, []);

  const fetchAppointments = async () => {
    try {
      const response = await api.get('/api/v1/appointments');
      setAppointments(response.data);
    } catch (error) {
      console.error('Error fetching appointments:', error);
    }
  };

  const fetchDoctors = async () => {
    try {
      const response = await api.get('/api/v1/admin/doctors');
      setDoctors(response.data);
    } catch (error) {
      console.error('Error fetching doctors:', error);
    }
  };

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      const patientRes = await api.post('/api/v1/patients/register', {
        full_name: data.full_name,
        phone: data.phone,
        complaint: 'Onlayn qabul',
        is_online: true,
      });

      await api.post('/api/v1/appointments/book', {
        patient_id: patientRes.data.id,
        doctor_id: parseInt(data.doctor_id, 10) || doctors[0]?.id || 1,
        datetime: data.datetime,
      });

      toast.success('Qabulga muvaffaqiyatli yozildingiz!');
      reset();
      fetchAppointments();
    } catch (error) {
      toast.error('Xatolik yuz berdi');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <NavBar />
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">📅 Onlayn qabulga yozilish</h2>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <input
              {...register('full_name', { required: true })}
              className="w-full px-4 py-2 border rounded-lg"
              placeholder="To'liq ism"
            />
            <input
              {...register('phone', { required: true })}
              className="w-full px-4 py-2 border rounded-lg"
              placeholder="Telefon"
            />
            <select
              {...register('doctor_id')}
              className="w-full px-4 py-2 border rounded-lg"
            >
              {doctors.map((doc) => (
                <option key={doc.id} value={doc.id}>{doc.full_name} — {doc.specialty}</option>
              ))}
            </select>
            <input
              type="datetime-local"
              {...register('datetime', { required: true })}
              className="w-full px-4 py-2 border rounded-lg"
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Yozilmoqda...' : 'Yozilish'}
            </button>
          </form>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="font-semibold mb-4">Rejalashtirilgan qabullar</h3>
          {appointments.length === 0 ? (
            <p className="text-gray-500">Qabullar yo'q</p>
          ) : (
            appointments.map((appt) => (
              <div key={appt.id} className="border-b py-3 last:border-0">
                <p className="font-medium">{appt.patient_name}</p>
                <p className="text-sm text-gray-600">
                  {appt.doctor_name} — {new Date(appt.datetime).toLocaleString()}
                </p>
              </div>
            ))
          )}
        </div>
      </div>
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
        <Link to="/appointments" className="text-blue-600 hover:underline font-bold">Qabul</Link>
        <Link to="/admin" className="text-blue-600 hover:underline">Admin</Link>
      </div>
      <button onClick={logout} className="text-red-600 hover:underline text-sm">Chiqish</button>
    </nav>
  );
}

export default AppointmentBooking;
