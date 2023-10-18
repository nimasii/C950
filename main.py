# Author: Jacob Campbell
# Student ID: 011079787
# Title: C950 WGUPS Program
import csv
import datetime

from truck import Truck
from hashmap import CreateHashMap
from package import Package

# Read the file of distance information
with open("csv/distances.csv") as csvfile:
    csv_distances = csv.reader(csvfile)
    distances = list(csv_distances)

# Read the file of address information
with open("csv/addresses.csv") as csvfile1:
    csv_addresses = csv.reader(csvfile1)
    addresses = list(csv_addresses)

# Read the file of package information
with open("csv/packages.csv") as csvfile2:
    csv_packages = csv.reader(csvfile2)
    packages = list(csv_packages)

# Create package objects from the CSV package file
# Load package objects into the hash table: package_hash_table
def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package_row in package_data:
            package_id = int(package_row[0])
            package_address = package_row[1]
            package_city = package_row[2]
            package_state = package_row[3]
            package_zipcode = package_row[4]
            package_deadline_time = package_row[5]
            package_weight = package_row[6]
            package_status = "At Hub"

            # Package object
            p = Package(package_id, package_address, package_city, package_state, package_zipcode, package_deadline_time, package_weight, package_status)

            # Insert data into the hash table
            package_hash_table.insert(package_id, p)

# Method for finding distance between two addresses
def distance_in_between(x_value, y_value):
    distance = distances[x_value][y_value]
    if distance == '':
        distance = distances[y_value][x_value]
    return float(distance)

# Method to get address number from string literal of address
def extract_address(address):
    for row in addresses:
        if address in row[2]:
            return int(row[0])

# Create truck objects
truck1 = Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8))
truck2 = Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
truck3 = Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=9, minutes=5))

# Create a hash table
package_hash_table = HashMap()

# Load packages into the hash table
load_package_data("csv/packages.csv", package_hash_table)

# Method for ordering packages on a given truck using the nearest neighbor algo
# This method also calculates the distance a given truck drives once the packages are sorted
def delivering_packages(truck):
    not_delivered = []
    for package_id in truck.packages:
        package = package_hash_table.lookup(package_id)
        not_delivered.append(package)
    truck.packages.clear()

    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None
        for package in not_delivered:
            if distance_in_between(extract_address(truck.address), extract_address(package.address)) <= next_address:
                next_address = distance_in_between(extract_address(truck.address), extract_address(package.address))
                next_package = package
        truck.packages.append(next_package.ID)
        not_delivered.remove(next_package)
        truck.mileage += next_address
        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

# Put the trucks through the loading process
delivering_packages(truck1)
delivering_packages(truck2)
truck3.depart_time = min(truck1.time, truck2.time)
delivering_packages(truck3)

# User Interface
# Upon running the program, the below message will appear.
print("Western Governors University Parcel Service (WGUPS)")
print("The mileage for the route is:")
print(truck1.mileage + truck2.mileage + truck3.mileage)  # Print total mileage for all trucks

# The user will be asked to start the process by entering the word "time"
text = input("To start please type the word 'time' (All else will cause the program to quit).")

# If the user doesn't type "leave" the program will ask for a specific time in regard to checking packages
if text == "time":
    try:
        # The user will be asked to enter a specific time
        user_time = input("Please enter a time to check status of package(s). Use the following format, HH:MM:SS")
        (h, m, s) = user_time.split(":")
        convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        # The user will be asked if they want to see the status of all packages or only one
        second_input = input("To view the status of an individual package please type 'solo'. For a rundown of all"
                             " packages please type 'all'.")
        # If the user enters "solo" the program will ask for one package ID
        if second_input == "solo":
            try:
                # The user will be asked to input a package ID. Invalid entry will cause the program to quit
                solo_input = input("Enter the numeric package ID")
                package = package_hash_table.lookup(int(solo_input))
                package.update_status(convert_timedelta)
                print(str(package))
            except ValueError:
                print("Entry invalid. Closing program.")
                exit()
        # If the user types "all" the program will display all package information at once
        elif second_input == "all":
            try:
                for package_id in range(1, 41):
                    package = package_hash_table.lookup(package_id)
                    package.update_status(convert_timedelta)
                    print(str(package))
            except ValueError:
                print("Entry invalid. Closing program.")
                exit()
        else:
            exit()
    except ValueError:
        print("Entry invalid. Closing program.")
        exit()
elif text != "time":
    print("Entry invalid. Closing program.")
    exit()
