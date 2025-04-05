import { useState } from 'react';
import { View, TextInput, TouchableOpacity, Text, StyleSheet, Image } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { ThemedView } from '@/components/ThemedView';

export default function FormSubmissionScreen() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState<string | null>(null);

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  const handleSubmit = async () => {
    console.log('Form submitted!');
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
  
    if (image) {
      formData.append('image', {
        uri: image,
        name: 'upload.jpg',
        type: 'image/jpeg'
      } as any);
    }
  
    try {
      const response = await fetch('http://10.0.2.2:5000/submit', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
  
      const result = await response.json();
      console.log(result);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  return (
    <ThemedView style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Title"
        value={title}
        onChangeText={setTitle}
      />
      <TextInput
        style={styles.input}
        placeholder="Description"
        value={description}
        onChangeText={setDescription}
        multiline
      />
      <TouchableOpacity style={styles.imageUploadButton} onPress={pickImage}>
        <Text style={styles.buttonText}>Upload Image</Text>
      </TouchableOpacity>
      {image && <Image source={{ uri: image }} style={styles.image} />}
      <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
        <Text style={styles.buttonText}>Submit</Text>
      </TouchableOpacity>
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
  input: {
    width: '80%',
    padding: 12,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    marginBottom: 12,
    backgroundColor: '#fff',
  },
  imageUploadButton: {
    width: '80%',
    paddingVertical: 15,
    backgroundColor: '#007AFF',
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 12,
  },
  submitButton: {
    width: '80%',
    paddingVertical: 15,
    backgroundColor: '#28a745',
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 12,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  image: {
    width: 200,
    height: 200,
    marginTop: 10,
    borderRadius: 8,
  },
});