# For School Library Program

# ** Updated History **
# 4/8/2023 Kenshing Teoh
# 4/18/2023 Adding new features: 30 secs auto save, and let user add new column.
# 4/21/2023 Adding new features: Updated existing student's data based on user entered column name.
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
    with open(fileName, "r") as csvFile:
        lines = csvFile.readlines()
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
        print("\n---------------- For Entering Student's Data ----------------")
        userIn = input('Enter student name (or "exit" to return to main menu): ')
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
                print(f"The following data for student '{userIn}' are missing values: {', '.join(missingValues)}")
                for column in missingValues:
                    while True:
                        data = input(f'Enter {column} for {userIn}: ')
                        if not data:
                            print(f'{column} will be empty.')
                            break
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
                        print(f'{column} will be empty.')
                        break
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
        with open(fileName, 'r') as csvFile:
            reader = csv.reader(csvFile)
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

    with open(fileName, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(header + [columnName])
        columns = header + [columnName]

    print(f"Column '{columnName}' added successfully.")


# Update Column Function
def updateColumn():
    global studentDict, columns
    while True:
        print("\n---------------- For Updating Student's Data ----------------")
        userIn = input('Enter student name (or "exit" to return to main menu): ')
        if userIn == 'exit':
            break

        if userIn in studentDict:
            column = input('Enter the column to update the data: ')
            if column in columns:
                value = input(f'Enter {column} for {userIn}: ')
                studentDict[userIn][column] = value
                print('Data updated successfully.')

            else:
                print('Column does not exist.')

        else:
            print('Student does not exist.')


# Save Data Function
def saveData(fileName):
    global studentDict
    with open(fileName, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        # write header row
        header = ['Name'] + columns
        writer.writerow(header)
        # write student data rows
        for key, value in studentDict.items():
            row = [key] + [value.get(column, '') for column in columns]
            writer.writerow(row)


# Save and Quit Function
def saveQuit(fileName):
    global studentDict
    with open(fileName, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        # write header row
        header = ['Name'] + columns
        writer.writerow(header)
        # write student data rows
        for key, value in studentDict.items():
            row = [key] + [value.get(column, '') for column in columns]
            writer.writerow(row)
    quit()


# Auto Save feature every 30 secs
def autoSave():
    global studentDict
    # Set timer for 30 secs
    saveInterval = 30
    # Every 30 secs after autoSave got call
    threading.Timer(saveInterval, autoSave).start()
    if studentDict:
        saveData(fileName)


# Main Function
def main():
    global studentDict, fileName

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
        print('3. Update Column')
        print('4. Save and Exit\n')

        choice = input('Enter choice: ')

        if choice == '1':
            addData()

        elif choice == '2':
            addColumn(fileName)

        elif choice == '3':
            updateColumn()

        elif choice == '4':
            saveQuit(fileName)
            exit()

        else:
            print('** Invalid options. Please try again. **')


if __name__ == '__main__':
    main()
