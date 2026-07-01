import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';
import axios from 'axios';
import { API_URL } from '../config';

export default function RegisterScreen({ navigation }) {
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [complaint, setComplaint] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRegister = async () => {
    if (!fullName || !phone || !complaint) {
      Alert.alert('Xatolik', 'Barcha maydonlarni to\'ldiring');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/v1/patients/register`, {
        full_name: fullName,
        phone,
        complaint,
        is_online: false,
      });
      setResult(response.data);
      setFullName('');
      setPhone('');
      setComplaint('');
      Alert.alert('Muvaffaqiyat', `${response.data.full_name} ro'yxatga olindi`);
    } catch (error) {
      Alert.alert('Xatolik', 'Ro\'yxatga olishda xatolik yuz berdi');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Bemor ro'yxatga olish</Text>

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
        style={[styles.input, styles.textarea]}
        placeholder="Shikoyat"
        value={complaint}
        onChangeText={setComplaint}
        multiline
      />

      <TouchableOpacity
        style={[styles.button, loading && styles.buttonDisabled]}
        onPress={handleRegister}
        disabled={loading}
      >
        <Text style={styles.buttonText}>
          {loading ? 'Ro\'yxatga olinmoqda...' : 'Ro\'yxatga olish'}
        </Text>
      </TouchableOpacity>

      {result && (
        <View style={styles.result}>
          <Text style={styles.resultTitle}>{result.full_name}</Text>
          <Text>Kategoriya: {result.category}</Text>
          <Text>Kutish: {result.estimated_wait} daqiqa</Text>
        </View>
      )}
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
  textarea: { height: 100, textAlignVertical: 'top' },
  button: {
    backgroundColor: '#0b3b5c',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonDisabled: { opacity: 0.5 },
  buttonText: { color: 'white', fontWeight: 'bold', fontSize: 16 },
  result: {
    marginTop: 20,
    padding: 15,
    backgroundColor: '#e6fffa',
    borderRadius: 10,
  },
  resultTitle: { fontWeight: 'bold', marginBottom: 5 },
});
