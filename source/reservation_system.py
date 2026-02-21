"""Módulo que contiene las abstracciones para el sistema de reservaciones."""

class Hotel:
    """Clase que representa la abstracción de un Hotel."""
    def __init__(self, hotel_id, name, total_rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.total_rooms = total_rooms

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