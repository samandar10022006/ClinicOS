import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import axios from 'axios';
import { API_URL } from '../config';

export default function HomeScreen({ navigation }) {
  const [stats, setStats] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/patients/stats`);
      setStats(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchStats();
    setRefreshing(false);
  };

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.header}>
        <Text style={styles.title}>🏥 DMed</Text>
        <Text style={styles.subtitle}>Aqlli shifoxona tizimi</Text>
      </View>

      <View style={styles.statsGrid}>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>{stats?.waiting || 0}</Text>
          <Text style={styles.statLabel}>Navbatda</Text>
        </View>
        <View style={[styles.statCard, styles.urgentCard]}>
          <Text style={styles.statNumber}>{stats?.urgent || 0}</Text>
          <Text style={styles.statLabel}>Shoshilinch</Text>
        </View>
        <View style={[styles.statCard, styles.chronicCard]}>
          <Text style={styles.statNumber}>{stats?.chronic || 0}</Text>
          <Text style={styles.statLabel}>Surunkali</Text>
        </View>
        <View style={[styles.statCard, styles.fastCard]}>
          <Text style={styles.statNumber}>{stats?.fast || 0}</Text>
          <Text style={styles.statLabel}>Tez tibbiy</Text>
        </View>
      </View>

      <View style={styles.menuGrid}>
        <TouchableOpacity
          style={styles.menuItem}
          onPress={() => navigation.navigate('Register')}
        >
          <Text style={styles.menuIcon}>📋</Text>
          <Text style={styles.menuText}>Ro'yxatga olish</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.menuItem}
          onPress={() => navigation.navigate('Appointments')}
        >
          <Text style={styles.menuIcon}>📅</Text>
          <Text style={styles.menuText}>Qabulga yozilish</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.menuItem}>
          <Text style={styles.menuIcon}>🛏️</Text>
          <Text style={styles.menuText}>Palatalar</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.menuItem}
          onPress={() => navigation.navigate('Profile')}
        >
          <Text style={styles.menuIcon}>👤</Text>
          <Text style={styles.menuText}>Profil</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#0b3b5c',
    padding: 30,
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    color: 'white',
    fontWeight: 'bold',
  },
  subtitle: {
    fontSize: 16,
    color: '#a0c4d8',
    marginTop: 5,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 15,
    gap: 10,
  },
  statCard: {
    flex: 1,
    minWidth: '45%',
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  urgentCard: { borderLeftWidth: 4, borderLeftColor: '#e53e3e' },
  chronicCard: { borderLeftWidth: 4, borderLeftColor: '#3182ce' },
  fastCard: { borderLeftWidth: 4, borderLeftColor: '#38a169' },
  statNumber: {
    fontSize: 28,
    fontWeight: 'bold',
  },
  statLabel: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  menuGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 15,
    gap: 15,
  },
  menuItem: {
    flex: 1,
    minWidth: '40%',
    backgroundColor: 'white',
    padding: 25,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  menuIcon: {
    fontSize: 32,
  },
  menuText: {
    marginTop: 10,
    fontSize: 16,
    color: '#333',
  },
});