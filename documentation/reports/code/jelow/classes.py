class Airport(object):
    def __init__(self, ground_planes, flying_planes):
        self.ground_planes= ground_planes
        self.flying_planes= flying_planes

class Human(object):
    pass

class Passenger(Human):
    pass
    
class Employee(Human):
    pass

class Plane(object):
    pass

class FlyingPlane(Plane):
    def __init__(self, passengers, employees):
        self.passengers= passengers
        self.employees= employees

class GroundPlane(Plane):
    pass


def build_airport():
    ground_planes= [GroundPlane() for i in range(10)]
    flying_planes= []
    for i in range(10):
        employees= [Employee() for i in range(10)]
        passengers= [Passenger() for i in range(10)]
        flying_planes.append(FlyingPlane(passengers, employees))
    
    airport= Airport(ground_planes, flying_planes)
    return airport
