"""Pruebas unitarias para el sistema de reservaciones."""
import unittest
import json
from source.reservation_system import Hotel, Customer, Reservation


class TestReservationSystem(unittest.TestCase):
    """Clase de pruebas para validar Hotel, Customer y Reservation."""

    def setUp(self):
        """Configura un estado limpio antes de cada prueba."""
        self.hotel_file = "data/hotels.json"
        self.customer_file = "data/customers.json"
        self.res_file = "data/reservations.json"

        # Inicializar archivos con listas vacías
        for file in [self.hotel_file, self.customer_file, self.res_file]:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def test_hotel_operations(self):
        """Prueba de la creación, modificación y eliminación de hoteles."""
        hotel = Hotel(1, "Hotel Test", 10)
        hotel.create_hotel()

        # Verificar creación
        info = Hotel.display_info(1)
        self.assertEqual(info['name'], "Hotel Test")

        # Verificar modificación
        Hotel.modify_hotel_info(1, new_name="Updated Name")
        self.assertEqual(Hotel.display_info(1)['name'], "Updated Name")

        # Verificar reserva de habitación
        Hotel.reserve_room(1)
        self.assertEqual(Hotel.display_info(1)['total_rooms'], 9)

        # Verificar eliminación
        Hotel.delete_hotel(1)
        self.assertIsNone(Hotel.display_info(1))

    def test_hotel_reserve_no_rooms(self):
        """Prueba de reservar en hotel sin disponibilidad."""
        hotel = Hotel(2, "Hotel Sin Cuartos", 0)
        hotel.create_hotel()
        result = Hotel.reserve_room(2)
        self.assertFalse(result)

    def test_modify_nonexistent_hotel(self):
        """Prueba modificar hotel inexistente."""
        result = Hotel.modify_hotel_info(999, new_name="No existe")
        self.assertFalse(result)

    def test_customer_operations(self):
        """Prueba de la gestión de clientes."""
        customer = Customer(101, "Jose Diaz", "jose@test.com")
        customer.create_customer()

        # Verificar modificación
        Customer.modify_customer_info(101, new_email="new_jose@test.com")
        info = Customer.display_info(101)
        self.assertEqual(info['email'], "new_jose@test.com")

    def test_reservation_creation_and_cancel(self):
        """Prueba del flujo de reservaciones."""
        res = Reservation(500, 101, 1)
        res.create_reservation()

        # Verificar que existe en el archivo
        with open(self.res_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)

        # Cancelar reservación (Req 2.3b)
        Reservation.cancel_reservation(500)
        with open(self.res_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data), 0)

    def test_invalid_json_handling(self):
        """Validación del sistema de manejar archivos corruptos."""
        with open(self.hotel_file, 'w', encoding='utf-8') as f:
            f.write("ESTO_NO_ES_JSON")

        # El sistema debe mostrar el error y devolver una lista vacía
        result = Hotel.safe_load_data()  # wrapper público
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
