# Hash Map class
class HashMap:
    def __init__(self, initial_capacity=20):
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])

    # Inserts a new item into the hash table
    # Citing source: WGU code repository W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
    def insert(self, key, item):  # Inserts or updates a key-value pair
        # Get the bucket where this item will go.
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # Update the key if it is already in the bucket
        for kv in bucket_list:  # O(N) CPU time
            if kv[0] == key:
                kv[1] = item
                return True

        # If not, insert the item at the end of the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Lookup items in the hash table
    def lookup(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None  # No pair[0] matches the key

    # Remove method - removes an item from the hash table
    def remove(self, key):
        slot = hash(key) % len(self.list)
        destination = self.list[slot]

        # If the key is found in the hash table, then remove the item
        for pair in destination:
            if key == pair[0]:
                destination.remove(pair)
                return
