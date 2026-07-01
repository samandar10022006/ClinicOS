import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useAuth } from '../context/AuthContext';

export default function ProfileScreen() {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    Alert.alert('Chiqish', 'Tizimdan chiqmoqchimisiz?', [
      { text: 'Bekor qilish', style: 'cancel' },
      {
        text: 'Chiqish',
        style: 'destructive',
        onPress: logout,
      },
    ]);
  };

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.avatar}>👤</Text>
        <Text style={styles.name}>{user?.full_name || 'Mehmon'}</Text>
        <Text style={styles.role}>{user?.role || 'Foydalanuvchi'}</Text>
        {user?.username && (
          <Text style={styles.detail}>Login: {user.username}</Text>
        )}
      </View>

      <View style={styles.infoCard}>
        <Text style={styles.infoTitle}>DMed Mobile</Text>
        <Text style={styles.infoText}>
          Aqlli shifoxona tizimi mobil ilovasi. Bemorlarni ro'yxatga olish,
          qabulga yozilish va statistikani ko'rish imkoniyati.
        </Text>
      </View>

      {user && (
        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Text style={styles.logoutText}>Chiqish</Text>
        </TouchableOpacity>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5', padding: 20 },
  card: {
    backgroundColor: 'white',
    padding: 30,
    borderRadius: 16,
    alignItems: 'center',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  avatar: { fontSize: 48, marginBottom: 10 },
  name: { fontSize: 22, fontWeight: 'bold', color: '#0b3b5c' },
  role: { fontSize: 16, color: '#666', marginTop: 5 },
  detail: { fontSize: 14, color: '#999', marginTop: 10 },
  infoCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    marginBottom: 20,
  },
  infoTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
  infoText: { color: '#666', lineHeight: 22 },
  logoutButton: {
    backgroundColor: '#e53e3e',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  logoutText: { color: 'white', fontWeight: 'bold' },
});
