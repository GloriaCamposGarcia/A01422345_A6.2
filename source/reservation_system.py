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
    FILE_PATH = "data/customers.json"

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    @staticmethod
    def _load_data():
        """Carga datos de clientes manejando errores de archivo."""
        try:
            if not os.path.exists(Customer.FILE_PATH):
                return []
            with open(Customer.FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error en datos de clientes: {e}. Continuando...")
            return []

    @staticmethod
    def _save_data(data):
        """Guarda la lista de clientes en el archivo JSON."""
        with open(Customer.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def create_customer(self):
        """Crea un nuevo registro de cliente."""
        customers = self._load_data()
        customers.append(self.__dict__)
        self._save_data(customers)

    @classmethod
    def delete_customer(cls, customer_id):
        """Elimina un cliente por su ID."""
        customers = [
            c for c in cls._load_data()
            if c['customer_id'] != customer_id
        ]
        cls._save_data(customers)

    @classmethod
    def display_info(cls, customer_id):
        """Muestra información de un cliente específico."""
        customers = cls._load_data()
        for c in customers:
            if c['customer_id'] == customer_id:
                print(f"Cliente: {c['name']}, Email: {c['email']}")
                return c
        return None

    @classmethod
    def modify_customer_info(cls, customer_id, new_name=None, new_email=None):
        """Modifica los datos de un cliente existente."""
        customers = cls._load_data()
        for c in customers:
            if c['customer_id'] == customer_id:
                if new_name:
                    c['name'] = new_name
                if new_email:
                    c['email'] = new_email
                cls._save_data(customers)
                return True
        return False


class Reservation:
    """Clase que vincula un Cliente con un Hotel."""
    FILE_PATH = "data/reservations.json"

    def __init__(self, reservation_id, customer_id, hotel_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    @staticmethod
    def _load_data():
        """Carga reservaciones manejando errores de formato."""
        try:
            if not os.path.exists(Reservation.FILE_PATH):
                return []
            with open(Reservation.FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error en datos de reservaciones: {e}. Continuando...")
            return []

    @staticmethod
    def _save_data(data):
        """Guarda la lista de reservaciones en JSON."""
        with open(Reservation.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def create_reservation(self):
        """Crea una reservación vinculando Cliente y Hotel."""
        # Se asume que el hotel tiene disponibilidad (Hotel.reserve_room)
        reservations = self._load_data()
        reservations.append(self.__dict__)
        self._save_data(reservations)

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """Cancela una reservación existente."""
        reservations = [
            r for r in cls._load_data()
            if r['reservation_id'] != reservation_id]
        cls._save_data(reservations)
