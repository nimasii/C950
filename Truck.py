class Truck:
    def __init__(self, capacity, speed, load, packages, mileage, address, depart_time):
        self.capacity = capacity      # Maximum package capacity of the truck
        self.speed = speed            # Speed of the truck (miles per hour)
        self.load = load              # Current load of the truck
        self.packages = packages      # List of packages on the truck
        self.mileage = mileage        # Total mileage covered by the truck
        self.address = address        # Current address of the truck
        self.depart_time = depart_time  # Time when the truck departs from the hub
        self.time = depart_time       # Current time of the truck's route

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.load, self.packages, self.mileage,
                                               self.address, self.depart_time)
