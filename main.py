# Author: Jacob Campbell
# Student ID: 011079787
# Title: C950 WGUPS PROGRAM
import csv
import datetime
import truck

from builtins import ValueError

from hashmap import HashMap
from package import Package

# Read the file of distance information
with open("csv/distances.csv") as csvfile:
    csv_distances = csv.reader(csvfile)
    csv_distances = list(csv_distances)

# Read the file of address information
with open("csv/addresses.csv") as csvfile1:
    csv_addresses = csv.reader(csvfile1)
    csv_addresses = list(csv_addresses)

# Read the file of package information
with open("csv/packages.csv") as csvfile2:
    csv_packages = csv.reader(csvfile2)
    csv_packages = list(csv_packages)


# Create package objects from the CSV package file
# Load package objects into the hash table: package_hash_table
def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            package_id = int(package[0])
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zipcode = package[4]
            package_deadline_time = package[5]
            package_weight = package[6]
            package_status = "At Hub"

            # Package object
            p = Package(package_id, package_address, package_city, package_state, package_zipcode, package_deadline_time, package_weight, package_status)

            # Insert data into hash table
            package_hash_table.insert(package_id, p)


# Method for finding distance between two addresses
def distance_in_between(x_value, y_value):
    distance = csv_distances[x_value][y_value]
    if distance == '':
        distance = csv_distances[y_value][x_value]

    return float(distance)


# Method to get address number from string literal of address
def extract_address(address):
    for row in csv_addresses:
        if address in row[2]:
            return int(row[0])


# Create truck object truck1
truck1 = truck.Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8))

# Create truck object truck2
truck2 = truck.Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

# Create truck object truck3
truck3 = truck.Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=9, minutes=5))

# Create hash table
package_hash_table = HashMap()

# Load packages into hash table
load_package_data("csv/packages.csv", package_hash_table)


# Method for ordering packages on a given truck using the nearest neighbor algo
# This method also calculates the distance a given truck drives once the packages are sorted
def delivering_packages(truck):
    # Place all packages into array of not delivered
    not_delivered = []
    for package_id in truck.packages:
        package = package_hash_table.lookup(package_id)
        not_delivered.append(package)
    # Clear the package list of a given truck so the packages can be placed back into the truck in the order
    # of the nearest neighbor
    truck.packages.clear()

    # Cycle through the list of not_delivered until none remain in the list
    # Adds the nearest package into the truck.packages list one by one
    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None
        for package in not_delivered:
            if distance_in_between(extract_address(truck.address), extract_address(package.address)) <= next_address:
                next_address = distance_in_between(extract_address(truck.address), extract_address(package.address))
                next_package = package
        # Adds next closest package to the truck package list
        truck.packages.append(next_package.id)
        # Removes the same package from the not_delivered list
        not_delivered.remove(next_package)
        # Takes the mileage driven to this packaged into the truck.mileage attribute
        truck.mileage += next_address
        # Updates truck's current address attribute to the package it drove to
        truck.address = next_package.address
        # Updates the time it took for the truck to drive to the nearest package
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time


# Put the trucks through the loading process
delivering_packages(truck1)
delivering_packages(truck2)
# The below line of code ensures that truck 3 does not leave until either of the first two trucks are finished delivering their packages
truck3.depart_time = min(truck1.time, truck2.time)
delivering_packages(truck3)


class Main:
    # User Interface
    print("Western Governors University Parcel Service (WGUPS)")
    print("The total mileage for the route is:")
    print(truck1.mileage + truck2.mileage + truck3.mileage)  # Print total mileage for all trucks
    # The user will be asked to start the process by entering the word "time"
    text = input("To start please type the word 'begin'.\n")
    # If the user doesn't type "leave" the program will ask for a specific time in regard to checking packages
    if text == "begin":
        try:
            # The user will be asked to enter a specific time
            user_time = input("Please enter a time to check status of package(s). Use the following format, HH:MM:SS\n")
            (h, m, s) = user_time.split(":")
            convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            # The user will be asked if they want to see the status of all packages or only one
            second_input = input("To view the status of an individual package please type 'single'. To view the status of all"
                                 " packages please type 'all'.\n")
            # If the user enters "single" the program will ask for one package ID
            if second_input == "single":
                try:
                    # The user will be asked to input a package ID. Invalid entry will cause the program to quit
                    single_input = input("Enter the numeric package ID\n")
                    package = package_hash_table.lookup(int(single_input))
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
    elif text != "begin":
        print("Entry invalid. Closing program.")
        exit()