import { Image, StyleSheet, View, TouchableOpacity, Text } from 'react-native';
import { useRouter } from 'expo-router';
import { ThemedView } from '@/components/ThemedView';

export default function LandingScreen() {
  const router = useRouter();

  return (
    <ThemedView style={styles.container}>
      <Image source={require('@/assets/images/partial-react-logo.png')} style={styles.logo} />
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={() => router.navigate('./submitAppraisal')}>
          <Text style={styles.buttonText}>Submit Appraisal Request</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={() => router.navigate('./viewAppraisals')}>
          <Text style={styles.buttonText}>View Past Appraisals</Text>
        </TouchableOpacity>
      </View>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5F5F5',
  },
  logo: {
    width: 150,
    height: 150,
    marginBottom: 40,
  },
  buttonContainer: {
    width: '80%',
    alignItems: 'center',
  },
  button: {
    width: '100%',
    paddingVertical: 15,
    backgroundColor: '#007AFF',
    borderRadius: 8,
    marginVertical: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
});