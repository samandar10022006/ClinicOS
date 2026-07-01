import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Alert,
} from 'react-native';
import axios from 'axios';
import { API_URL } from '../config';

export default function AppointmentScreen() {
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [datetime, setDatetime] = useState('');
  const [doctors, setDoctors] = useState([]);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDoctors();
    fetchAppointments();
  }, []);

  const fetchDoctors = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/admin/doctors`);
      setDoctors(response.data);
      if (response.data.length > 0) {
        setSelectedDoctor(response.data[0].id);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const fetchAppointments = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/appointments`);
      setAppointments(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleBook = async () => {
    if (!fullName || !phone || !datetime) {
      Alert.alert('Xatolik', 'Barcha maydonlarni to\'ldiring');
      return;
    }

    setLoading(true);
    try {
      const patientRes = await axios.post(`${API_URL}/api/v1/patients/register`, {
        full_name: fullName,
        phone,
        complaint: 'Onlayn qabul',
        is_online: true,
      });

      await axios.post(`${API_URL}/api/v1/appointments/book`, {
        patient_id: patientRes.data.id,
        doctor_id: selectedDoctor || 1,
        datetime,
      });

      Alert.alert('Muvaffaqiyat', 'Qabulga yozildingiz!');
      setFullName('');
      setPhone('');
      setDatetime('');
      fetchAppointments();
    } catch (error) {
      Alert.alert('Xatolik', 'Qabulga yozishda xatolik');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Onlayn qabul</Text>

      <TextInput
        style={styles.input}
        placeholder="To'liq ism"
        value={fullName}
        onChangeText={setFullName}
      />
      <TextInput
        style={styles.input}
        placeholder="Telefon"
        value={phone}
        onChangeText={setPhone}
        keyboardType="phone-pad"
      />
      <TextInput
        style={styles.input}
        placeholder="Sana va vaqt (2026-07-01T10:00)"
        value={datetime}
        onChangeText={setDatetime}
      />

      <TouchableOpacity
        style={[styles.button, loading && styles.buttonDisabled]}
        onPress={handleBook}
        disabled={loading}
      >
        <Text style={styles.buttonText}>
          {loading ? 'Yozilmoqda...' : 'Yozilish'}
        </Text>
      </TouchableOpacity>

      <Text style={styles.sectionTitle}>Rejalashtirilgan qabullar</Text>
      {appointments.map((appt) => (
        <View key={appt.id} style={styles.apptCard}>
          <Text style={styles.apptName}>{appt.patient_name}</Text>
          <Text style={styles.apptDetail}>{appt.doctor_name}</Text>
          <Text style={styles.apptDetail}>{appt.datetime}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#0b3b5c', marginBottom: 20 },
  input: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 10,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#dce1e8',
  },
  button: {
    backgroundColor: '#0b3b5c',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 20,
  },
  buttonDisabled: { opacity: 0.5 },
  buttonText: { color: 'white', fontWeight: 'bold' },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
  apptCard: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
  },
  apptName: { fontWeight: 'bold' },
  apptDetail: { color: '#666', fontSize: 14 },
});
