import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import api from '../services/api';
import { NavBar } from '../App';

function PatientRegistration() {
  const { register, handleSubmit, reset } = useForm();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      const response = await api.post('/api/v1/patients/register', data);
      setResult(response.data);
      toast.success('Bemor muvaffaqiyatli ro\'yxatga olindi!');
      reset();
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
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Bemor ro'yxatga olish</h2>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">To'liq ism</label>
              <input
                {...register('full_name', { required: true })}
                className="mt-1 w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="Ism Familiya"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Telefon</label>
              <input
                {...register('phone', { required: true })}
                className="mt-1 w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="+998 90 123 45 67"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Shikoyat</label>
              <textarea
                {...register('complaint', { required: true })}
                className="mt-1 w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                rows="4"
                placeholder="Kasallik haqida qisqacha..."
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {loading ? 'Ro\'yxatga olinmoqda...' : 'Ro\'yxatga olish'}
            </button>
          </form>

          {result && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="font-semibold">{result.full_name}</p>
              <p>Kategoriya: <span className="font-bold text-blue-600">{result.category.toUpperCase()}</span></p>
              <p>Kutish vaqti: {result.estimated_wait} daqiqa</p>
              <p>Palata: {result.bed_id || 'Kutilmoqda'}</p>
              <p>Shifokor: {result.doctor_id || 'Kutilmoqda'}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default PatientRegistration;
