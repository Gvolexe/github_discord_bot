# persistence/data_persistence.py

import json
import threading
import logging

class DataPersistence:
    """
    Handles loading and saving of persistent data to a JSON file.
    Ensures thread-safe operations using a threading lock.
    """
    def __init__(self, file_path):
        """
        Initializes the DataPersistence instance.

        Parameters:
        - file_path (str): Path to the JSON file for data storage.
        """
        self.file_path = file_path
        self.DATA_STORE = {}
        self.MESSAGE_MAP = {}
        self.data_lock = threading.Lock()

    def load_data(self):
        """
        Loads DATA_STORE and MESSAGE_MAP from the JSON file.
        If the file doesn't exist, initializes empty structures.
        """
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.DATA_STORE = data.get("DATA_STORE", {})
                self.MESSAGE_MAP = data.get("MESSAGE_MAP", {})
            logging.info(f"Data loaded from {self.file_path}")
        except FileNotFoundError:
            logging.info(f"No existing {self.file_path} found. Starting with empty data stores.")
            self.DATA_STORE = {}
            self.MESSAGE_MAP = {}
            self.save_data()
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {self.file_path}: {e}")
            self.DATA_STORE = {}
            self.MESSAGE_MAP = {}
            self.save_data()

    def save_data(self):
        """
        Saves DATA_STORE and MESSAGE_MAP to the JSON file.
        Ensures thread-safe write operations.
        """
        with self.data_lock:
            with open(self.file_path, "w") as f:
                json.dump({
                    "DATA_STORE": self.DATA_STORE,
                    "MESSAGE_MAP": self.MESSAGE_MAP
                }, f, indent=2)
        logging.info(f"Data saved to {self.file_path}")

    def get_data_store(self):
        """
        Retrieves the DATA_STORE dictionary in a thread-safe manner.

        Returns:
        - dict: The DATA_STORE.
        """
        with self.data_lock:
            return self.DATA_STORE

    def get_message_map(self):
        """
        Retrieves the MESSAGE_MAP dictionary in a thread-safe manner.

        Returns:
        - dict: The MESSAGE_MAP.
        """
        with self.data_lock:
            return self.MESSAGE_MAP

    def update_data_store(self, key, value):
        """
        Updates the DATA_STORE with the given key and value.

        Parameters:
        - key (str): The unique key for the data entry.
        - value (dict): The data to store.
        """
        with self.data_lock:
            self.DATA_STORE[key] = value
        self.save_data()

    def update_message_map(self, key, message_id):
        """
        Updates the MESSAGE_MAP with the given key and Discord message ID.

        Parameters:
        - key (str): The unique key corresponding to the data entry.
        - message_id (int): The Discord message ID.
        """
        with self.data_lock:
            self.MESSAGE_MAP[key] = message_id
        self.save_data()
