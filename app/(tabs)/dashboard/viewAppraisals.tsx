import React, { useState } from 'react';
import { View, Text, FlatList, Pressable, StyleSheet, Alert } from 'react-native';
import pastAppraisals from '../../past_appraisals.json';
import * as Clipboard from 'expo-clipboard';

interface Item {
  item: string;
  description: string;
  max_price: number;
  min_price: number;
  condition: string;
  appraisal_correct: string | null;
}

interface Appraisals {
  items: Item[];
}

export default function ItemTableView() {
  const [selectedItem, setSelectedItem] = useState<Item | null>(null);
  const [appraisalCorrect, setAppraisalCorrect] = useState<String | null>(null);

  const sampleData: Appraisals = pastAppraisals;

  const renderItem = ({ item }: { item: Item }) => (
    <Pressable
      onPress={() => setSelectedItem(item)}
      style={styles.row}>
      <Text style={styles.itemName}>{item.item}</Text>
      <Text style={styles.itemPrice}>${item.max_price}</Text>
    </Pressable>
  );

  const handleShare = () => {
    if (selectedItem) {
      const text = `Item: ${selectedItem.item}\nDescription: ${selectedItem.description}\nMax Price: $${selectedItem.max_price}\nMin Price: $${selectedItem.min_price}\nCondition: ${selectedItem.condition}`;
      Clipboard.setString(text);
      Alert.alert('Copied to Clipboard', 'Item details have been copied.');
    }
  };

  const handleConfirmAppraisal = async () => {
    console.log('test');
    if (selectedItem && appraisalCorrect !== null) {
      const updatedItems = pastAppraisals.items.map((item) =>
        item.item === selectedItem.item ? { ...item, appraisal_correct: appraisalCorrect } : item
      );

      const updatedData = { items: updatedItems };
      console.log('Updated appraisal data:', JSON.stringify(updatedData, null, 2));

      try {
        const response = await fetch('http://10.0.2.2:5000/updateAppraisal', {
          method: 'POST',
          body: JSON.stringify(updatedData, null, 2),
          headers: {
            'Content-Type': 'application/json',
          },
        });
    
        const result = await response.json();
        console.log(result);
      } catch (error) {
        console.error('Error updating .json file:', error);
      }
    };
  };

  return (
    <View style={styles.container}>
      {!selectedItem ? (
        <FlatList
          data={sampleData.items}
          keyExtractor={(_, index) => index.toString()}
          renderItem={renderItem}
          ListHeaderComponent={() => (
            <View style={styles.headerRow}>
              <Text style={styles.headerText}>Item</Text>
              <Text style={styles.headerText}>Max Price</Text>
            </View>
          )}
        />
      ) : (
        <View style={styles.detailContainer}>
          <Text style={styles.detailTitle}>{selectedItem.item}</Text>
          <Text style={styles.detailText}>Description: {selectedItem.description}</Text>
          <Text style={styles.detailText}>Max Price: ${selectedItem.max_price}</Text>
          <Text style={styles.detailText}>Min Price: ${selectedItem.min_price}</Text>
          <Text style={styles.detailText}>Condition: {selectedItem.condition}</Text>
          {selectedItem.appraisal_correct ? <Text style={styles.detailText}>Appraisal Correct: {selectedItem.appraisal_correct}</Text>
            : <Text style={styles.detailText}>Appraisal Correct: Not yet confirmed</Text>}
          <Text style={styles.detailText}></Text>
          <Text style={styles.detailTextAppraisal}>Is this appraisal correct?</Text>

          <View style={{ flexDirection: 'row', justifyContent: 'space-evenly', marginTop: 16 }}>
            <Pressable onPress={() => setAppraisalCorrect("Yes")} style={{ padding: 10, backgroundColor: appraisalCorrect === "Yes" ? '#4ade80' : '#e5e7eb', borderRadius: 8 }}>
              <Text style={{ textAlign: 'center' }}>Yes</Text>
            </Pressable>
            <Pressable onPress={() => setAppraisalCorrect("No")} style={{ padding: 10, backgroundColor: appraisalCorrect === "No" ? '#f87171' : '#e5e7eb', borderRadius: 8 }}>
              <Text style={{ textAlign: 'center' }}>No</Text>
            </Pressable>
            <Pressable onPress={handleConfirmAppraisal} style={{ padding: 10, backgroundColor: '#3b82f6', borderRadius: 8 }}>
              <Text style={{ color: 'white', textAlign: 'center' }}>Confirm</Text>
            </Pressable>
          </View>

          <Pressable
            onPress={handleShare}
            style={styles.shareButton}>
            <Text style={styles.shareButtonText}>Share To Marketplace</Text>
          </Pressable>

          <Pressable
            onPress={() => { setSelectedItem(null); }}
            style={styles.backButton}>
            <Text style={styles.backButtonText}>Back to List</Text>
          </Pressable>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f0f0f0',
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
    backgroundColor: '#e0e0e0',
  },
  headerText: {
    fontWeight: 'bold',
    fontSize: 16,
    width: '50%',
    textAlign: 'center',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 16,
    paddingHorizontal: 12,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderColor: '#ccc',
  },
  itemName: {
    fontSize: 16,
    width: '60%',
    textAlign: 'center',
  },
  itemPrice: {
    fontSize: 16,
    color: '#555',
    textAlign: 'center',
    width: '40%',
  },
  detailContainer: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  detailTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 12,
    textAlign: 'center',
  },
  detailText: {
    fontSize: 16,
    marginBottom: 8,
  },
  detailTextAppraisal: {
    fontSize: 16,
    marginBottom: 8,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  shareButton: {
    marginTop: 10,
    backgroundColor: '#28a745',
    paddingVertical: 10,
    borderRadius: 6,
  },
  shareButtonText: {
    color: '#fff',
    textAlign: 'center',
    fontSize: 16,
    fontWeight: '600',
  },
  backButton: {
    marginTop: 16,
    backgroundColor: '#007AFF',
    paddingVertical: 10,
    borderRadius: 6,
  },
  backButtonText: {
    color: '#fff',
    textAlign: 'center',
    fontSize: 16,
    fontWeight: '600',
  },
});
