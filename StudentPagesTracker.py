# For School Library Program that we keep on track of the students on how many pages that they have read
# And saved it in a csv file that user enter the file name so we can keep the data
# 4/8/2023 Kenshing Teoh

import csv
import os

# global students dictionary
students = {}


# Load data function that load the data from user wanted file in order to keep on track of the pages read
def load_data(fileName):
    # file doesn't exist, so no data to load
    if not os.path.isfile(fileName):
        return
    # if file exist read the data to the students dictionary in order to keep on the students that already entered later
    with open(fileName, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            pages = int(row['Pages Read'])
            students[name] = pages


# Add student function that check if the student already exist in the dictionary so won't repeat the student
def add_student(name, pages):
    if name in students:
        # update page count for existing student
        students[name] += pages
    else:
        # else add the student
        students[name] = pages


# Save the data to the user want file name
def save_data(file_name):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Pages Read'])
        for name, pages in students.items():
            writer.writerow([name, pages])


# Return user wanted how many top readers
# Extra functionality that return the top readers, but probably not that useful since is in a excel sheet
# can easily sort the data, keep it for user need later.
def get_top_readers(studentsNum):
    sorted_students = sorted(students.items(), key=lambda x: x[1], reverse=True)
    top_students = sorted_students[:studentsNum]
    return top_students


# Display welcome message and how to use the program
def welcome_message():
    print("\n** Thank you for using the student's pages read tracker! **")
    print("** Need more function please contact Kenshing Teoh! **\n")
    print("\n** This program will ask for students name (Please keep the student's name format consistent).**")
    print("** For example: Lastname Firstname or Lastname, Firstname. As long as all the name are in the same format.")
    print("** And you will enter the file name that you want to save the data in.**\n")


def main():
    welcome_message()

    # Prompt user for CSV file name
    fileName = input("Enter Excel file name: ")
    # Check if the file has .csv extension
    if not fileName.endswith('.csv'):
        fileName += '.csv'

    # Load existing student data from CSV file, if it exists
    load_data(fileName)

    # Loop the program
    while True:
        name = input("\nEnter student name (or 'exit' to save and quit): ")
        if name.lower() == 'exit':
            save_data(fileName)
            print(f"Student data saved to {fileName}")
            break
        while True:
            pages_input = input("Enter pages read: ")
            try:
                pages = int(pages_input)
                break
            except ValueError:
                print("Invalid input: pages read must be an integer")
        add_student(name, pages)

    # To return the top readers data
    try:
        studentsNum = int(input("\nHow many top readers you want: "))
    except ValueError:
        print("Invalid input: pages read must be an integer")
    top_students = get_top_readers(studentsNum)
    print(f"Top {studentsNum} readers are:")
    for i, (name, pages) in enumerate(top_students):
        print(f"{i + 1}. {name}: {pages} pages")
    input("Press Any key to continue...")

if __name__ == "__main__":
    main()
