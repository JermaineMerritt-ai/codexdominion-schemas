import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';

const SocialScreen = () => {
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Social Media</Text>
      <Text style={styles.subtitle}>Content coming soon...</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
  },
});

export default SocialScreen;
