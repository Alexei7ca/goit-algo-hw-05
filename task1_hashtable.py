from typing import List, Any

class HashTable:
    def __init__(self, size: int):
        self.size = size
        self.table: List[List[List[Any]]] = [[] for _ in range(self.size)]

    def hash_function(self, key: Any) -> int:
        return hash(key) % self.size

    def insert(self, key: Any, value: Any) -> bool:
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]

        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return True
        
        bucket.append([key, value])
        return True

    def get(self, key: Any) -> Any:
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]
        
        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return None

    def delete(self, key: Any) -> bool:
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]
        
        # Iterate through the bucket to find the key by index
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                # Remove the key-value pair from the bucket
                del bucket[i]
                return True
        return False

def run_task1():
    # Тest
    H = HashTable(5)
    H.insert("apple", 10)
    H.insert("orange", 20)
    H.insert("banana", 30)

    print(f"Initial 'apple' value: {H.get('apple')}")

    H.delete("apple")
    print(f"Value after deleting 'apple': {H.get('apple')}") # Should output: None

    H.insert("grape", 40)
    print(f"Initial 'grape' value: {H.get('grape')}") # Should output: 40
    H.delete("grape")
    print(f"Value after deleting 'grape': {H.get('grape')}") # Should output: None

if __name__ == "__main__":
    run_task1()