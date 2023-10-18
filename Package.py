# Create a class for packages
class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline_time, weight, status):
        self.ID = ID               # Unique package identifier
        self.address = address     # Delivery address
        self.city = city           # City of delivery
        self.state = state         # State of delivery
        self.zipcode = zipcode     # Zip code of delivery
        self.deadline_time = deadline_time  # Delivery deadline time
        self.weight = weight       # Weight of the package
        self.status = status       # Delivery status (e.g., 'At Hub', 'En Route', 'Delivered')
        self.departure_time = None  # Time when the package departs from the hub
        self.delivery_time = None  # Time when the package is delivered

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode,
                                                       self.deadline_time, self.weight, self.delivery_time,
                                                       self.status)

    def update_status(self, convert_timedelta):
        # Update the status based on the current time (convert_timedelta)
        if self.delivery_time is not None and self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time is not None and self.departure_time > convert_timedelta:
            self.status = "En Route"
        else:
            self.status = "At Hub"
