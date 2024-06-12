import re
import ABS
class Passenger:
    @staticmethod
    def is_valid_name(name):
        if re.search(r"^[A-Za-z]+ (\s+[A-Za-z]) +$", name):
            return True
        return False
    
    def __init__(self,id,name,money):
        if self.is_valid_name(name):
            self.__name = name
        else:
            raise ValueError(f"Name is not valid")
        self.id = id
        self.money = money
    
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,new_name):
        if self.is_valid_name(new_name):
            self.__name = new_name
        else:
            raise ValueError(f"Name is not valid")
    
class Vehicle(ABS):
    def __init__(self,license_plate,amount_of_seats):
        self.license_plate = license_plate
        self.amount_of_seats = amount_of_seats
        self.__occupants = {}
    
    @property
    def number_of_occupants(self):
        return self.__occupants

    @property
    def maximum_occupants(self):
        ...
    
    @property
    def occupant_names(self):
        return self.__occupants[Passenger.name]
    
    def add_passenger(self,passenger):
        self.amount_of_seats -= 1
        self.__occupants[passenger.name] = passenger
    
    def remove_passenger(self,passenger):
        self.amount_of_seats += 1
        del self.__occupants[passenger]
        
    def remove_all_passengers(self):
        self.__occupants.clear()
    
    
class Bus(Vehicle):
    def __init__(self, license_plate, amount_of_seats):
        super().__init__(license_plate, amount_of_seats)
        self.maximum_occupants = 2 * amount_of_seats
        
    def board(self,passenger):
        tarief = 2
        if Bus.number_of_occupants == self.maximum_occupants:
            raise RuntimeError
        elif Passenger.money < tarief:
            raise RuntimeError
        else:
            Passenger.money -= tarief
            self.add_passenger(passenger)
    
    def disembark(self,passenger):
        if passenger in self.occupant_names:
            self.remove_passenger(passenger)
        



class Taxi(Vehicle):
    def __init__(self, license_plate, amount_of_seats):
        super().__init__(license_plate, amount_of_seats)
        self.maximum_occupants = self.amount_of_seats
    
    
    @property
    def is_available(self):
        return self.amount_of_seats >= 1
    
    def pickup(self,passengers,distance):
        tarief = 1 + distance
        passenger = passengers[0]
        
        if not self.is_available(Taxi):
            raise ValueError(f"Not available")
        elif tarief <= 5:
            if not passenger.money < tarief:
                self.add_passenger(passengers)
                passenger.money -= tarief
            else: 
                raise RuntimeError
            
            
    def dropoff(self):
        if not Taxi.number_of_occupants == 0:
            self.remove_all_passengers()
            
    



