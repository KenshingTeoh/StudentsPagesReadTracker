# For School Library Program that we keep on track of the students on how many pages that they have read
# And saved it in a csv file that user enter the file name so we can keep the data
# 4/8/2023 Kenshing Teoh

# 4/18/2023 Adding new features: 30 secs auto save, and let user add new column.

import os
import csv
import time
import threading

# Global variables
fileName = ''
studentDict = {}
columns = []


# Load the data from existing file
def loadData(fileName):
    global studentDict, columns
    with open(fileName, "r") as file:
        lines = file.readlines()
        if len(lines) == 0:
            return {}
        headers = lines[0].strip().split(",")
        columns = headers[1:]
        studentDict = {}
        for line in lines[1:]:
            data = line.strip().split(",")
            studentDict[data[0]] = {headers[i]: data[i] for i in range(1, len(headers))}
        return studentDict


# Add student data
# Check if user enter 'exit' will back to main menu
# Check if the student's name already exist if it does check every keys for missing value will ask user to enter it
def addData():
    global studentDict
    while True:
        userIn = input('Enter student name (or type "exit" to return to main menu): ')
        if userIn == 'exit':
            break

        if not userIn:
            print('Student name cannot be empty. Please try again.')
            continue

        if userIn in studentDict:
            print(f"Student '{userIn}' already exists.")

            # check if the student has any missing values
            missingValues = []
            for column in columns:
                if not studentDict[userIn].get(column):
                    missingValues.append(column)

            if missingValues:
                print(f"The following fields for student '{userIn}' are missing values: {', '.join(missingValues)}")
                for column in missingValues:
                    while True:
                        data = input(f'Enter {column} for {userIn}: ')
                        if not data:
                            print(f'{column} cannot be empty. Please try again.')
                            continue
                        else:
                            studentDict[userIn][column] = data
                            break
            else:
                print(f"Student '{userIn}' already has all values.")

        else:
            studentDict[userIn] = {}
            for column in columns:
                while True:
                    data = input(f'Enter {column} for {userIn}: ')
                    if not data:
                        print(f'{column} cannot be empty. Please try again.')
                        continue
                    else:
                        studentDict[userIn][column] = data
                        break


# Add Column function
def addColumn(fileName):
    global columns

    while True:
        columnName = input('Enter column name: ')
        if not columnName:
            print('Column name cannot be empty. Please try again.')
        else:
            break

    if os.path.getsize(fileName) == 0:
        header = []
    else:
        with open(fileName, 'r') as file:
            reader = csv.reader(file)
            header = next(reader, [])
    # If the column already exist
    if columnName in header:
        print(f"Column '{columnName}' already exists.")
        return

    # remove 'Name' column from header before checking if column exists
    if 'Name' in header:
        header.remove('Name')

    if columnName in header:
        print(f"Column '{columnName}' already exists.")
        header.insert(0, 'Name')  # add 'Name' column back to header
        return

    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header + [columnName])
        columns = header + [columnName]

    print(f"Column '{columnName}' added successfully.")


# Save Data Function
def saveData(fileName):
    global studentDict
    with open(fileName, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # write header row
        header = ['Name'] + columns
        writer.writerow(header)
        # write student data rows
        for key, value in studentDict.items():
            row = [key] + [value.get(column, '') for column in columns]
            writer.writerow(row)


# Auto Save feature every 30 secs
def autoSave():
    global studentDict
    # Set timer for 30 secs
    saveInterval = 30
    # Every 30 secs after autoSave got call
    threading.Timer(saveInterval, autoSave).start()
    if studentDict:
        saveData(fileName)


# Main
def main():
    global studentDict  # add this line to access the global variable

    fileName = input('Enter CSV file name: ')
    if not fileName.endswith('.csv'):
        fileName += '.csv'

    if os.path.exists(fileName):
        studentDict = loadData(fileName)
        if not studentDict:
            columns = []
        else:
            columns = list(studentDict[next(iter(studentDict))].keys())
            print(f"Columns found in CSV file: {', '.join(columns)}")
    else:
        print(f"CSV file '{fileName}' does not exist. Created new file!")
        columns = []
        with open(fileName, 'w') as file:
            pass

    autoSave()

    while True:
        print()
        print('\n-----------------------')
        print('     MENU OPTIONS')
        print('-----------------------')
        print('1. Enter student data')
        print('2. Add column (No need to create the name column!!)')
        print('3. Save and Exit\n')

        choice = input('Enter choice: ')

        if choice == '1':
            addData()

        elif choice == '2':
            addColumn(fileName)

        elif choice == '3':
            saveData(fileName)
            exit()

        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()
