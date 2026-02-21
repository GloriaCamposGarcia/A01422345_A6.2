import json
import os

"""Módulo que contiene las abstracciones para el sistema de reservaciones."""

class Hotel:
    """Clase que representa la abstracción de un Hotel."""
    FILE_PATH = "data/hotels.json"

    def __init__(self, hotel_id, name, total_rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.total_rooms = total_rooms

    @staticmethod
    def _load_data():
        """Carga datos del archivo manejando errores de formato."""
        try:
            if not os.path.exists(Hotel.FILE_PATH):
                return []
            with open(Hotel.FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al leer datos de hoteles: {e}. Continuando...")
            return []

    @staticmethod
    def _save_data(data):
        """Guarda la lista de hoteles en el archivo JSON."""
        with open(Hotel.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def create_hotel(self):
        """Agrega un nuevo hotel."""
        hotels = self._load_data()
        hotels.append(self.__dict__)
        self._save_data(hotels)

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Elimina un hotel por su ID."""
        hotels = [h for h in cls._load_data() if h['hotel_id'] != hotel_id]
        cls._save_data(hotels)

    @classmethod
    def display_info(cls, hotel_id):
        """Muestra la información de un hotel."""
        hotels = cls._load_data()
        for h in hotels:
            if h['hotel_id'] == hotel_id:
                print(f"Hotel: {h['name']}, Habitaciones: {h['total_rooms']}")
                return h
        return None
    @classmethod
    def modify_hotel_info(cls, hotel_id, new_name=None, new_rooms=None):
        """Modifica la información de un hotel existente."""
        hotels = cls._load_data()
        for h in hotels:
            if h['hotel_id'] == hotel_id:
                if new_name:
                    h['name'] = new_name
                if new_rooms is not None:
                    h['total_rooms'] = new_rooms
                cls._save_data(hotels)
                return True
        return False

    @classmethod
    def reserve_room(cls, hotel_id):
        """Reduce en 1 el total de habitaciones disponibles."""
        hotels = cls._load_data()
        for h in hotels:
            if h['hotel_id'] == hotel_id and h['total_rooms'] > 0:
                h['total_rooms'] -= 1
                cls._save_data(hotels)
                return True
        print(f"No hay habitaciones disponibles en el hotel {hotel_id}.")
        return False

    @classmethod
    def cancel_reservation(cls, hotel_id):
        """Incrementa en 1 el total de habitaciones disponibles."""
        hotels = cls._load_data()
        for h in hotels:
            if h['hotel_id'] == hotel_id:
                h['total_rooms'] += 1
                cls._save_data(hotels)
                return True
        return False

class Customer:
    """Clase que representa la abstracción de un Cliente."""
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

class Reservation:
    """Clase que vincula un Cliente con un Hotel."""
    def __init__(self, reservation_id, customer_id, hotel_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id