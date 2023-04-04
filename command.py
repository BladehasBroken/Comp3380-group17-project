import argparse
import pyodbc
from tabulate import tabulate
import sys
import keyboard

def connect():
    #connection_string = f'DRIVER={DESKTOP-TEFQKFL};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(f'DRIVER={{SQL Server}}; SERVER=localhost; DATABASE=group_project; Trusted_Connection=yes')
    return conn

def query_database(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    formatted_result = tabulate(result, headers=column_names, tablefmt='grid')

    print(formatted_result)

    cursor.close()

def get_all_ages(conn):
    query = f'select * from Ages'
    query_database(conn, query)

def get_population_belowAges_area(conn, age, area):
    query = f'select boundary_name, male, female from Boundary join Response on Boundary.boundary_id = Response.boundary join Ages on Response.response_id = Ages.response_id where max <= {age} and boundary_name = {area}'
    query_database(conn,query)

def get_all_boundary(conn):
    query = 'select * from Boundary'
    query_database(conn,query)

def get_all_boundary_name(conn):
    query = 'select distinct Boundary_name from Boundary'
    query_database(conn,query)

def get_all_education(conn):
    query = 'select * from Education'
    query_database(conn,query)

def get_all_faith(conn):
    query = 'select * from Faith'
    query_database(conn,query)

def get_all_language(conn):
    query = 'select * from Language'
    query_database(conn,query)

def get_all_non_response_rate(conn):
    query = 'select * from Non_Response_Rate'
    query_database(conn,query)

def get_all_response(conn):
    query = 'select * from Response'
    query_database(conn,query)

def get_all_topic(conn):
    query = 'select * from Topic'
    query_database(conn,query)

def main_menu():
    print('Choose an option:')
    print('1. Ages')
    print('2. Boundary')
    print('3. Education')
    print('4. Faith')
    print('5. Language')
    print('6. Non_Response_Rate')
    print('7. Response')
    print('8. Topic')

def age_menu():
    print('Choose an option:')
    print('1. get all the age information')
    print('2. get population that below some age in one area ')
    print('"b". Back to main menu')

def boundary_menu():
    print('Choose an option:')
    print('1. get all the boundary information')
    print('2. get a list of boundary names ')
    print('"b". Back to main menu')

def educaiton_menu():
    print('Choose an option:')
    print('1. get all the education information')

def faith_menu():
    print('Choose an option:')
    print('1. get all the faith information')

def language_menu():
    print('Choose an option:')
    print('1. get all the language information')

def non_response_rate_menu():
    print('Choose an option:')
    print('1. get all the non resposne rate information')

def response_menu():
    print('Choose an option:')
    print('1. get all the response information')

def topic_menu():
    print('Choose an option:')
    print('1. get all the topic information')

# do task when user select option under the age menu
def age_choice():
    while True:
        age_menu()
        ageChoice = input('Enter your choice (1-9): ')
        if ageChoice == '1':
            get_all_ages(conn)
        elif ageChoice == '2':
            age = int(input('Enter the age: '))
            area = "'" + input('Enter the boundary name: ') + "'"
            get_population_belowAges_area(conn, age, area)
        elif ageChoice == 'b':
            print("Back to main...")
            break

# do task when user select option under the age menu
def boundary_choice():
    while True:
        boundary_menu()
        boundaryChoice = input('Enter your choice (1-9): ')
        if boundaryChoice == '1':
            get_all_boundary(conn)
        elif boundaryChoice == '2':
            get_all_boundary_name(conn)
        elif boundaryChoice == 'b':
            print("Back to main...")
            break


def education_choice():
    while True:
        educaiton_menu()
        educationChoice = input('Enter your choice (1-9): ')
        if educationChoice == '1':
            get_all_education(conn)
        elif educationChoice == 'b':
            print("Back to main...")
            break

def faith_choice():
    while True:
        faith_menu()
        faithChoice = input('Enter your choice (1-9): ')
        if faithChoice == '1':
            get_all_faith(conn)
        elif faithChoice == 'b':
            print("Back to main...")
            break

def language_choice():
    while True:
        language_menu()
        languageChoice = input('Enter your choice (1-9): ')
        if languageChoice == '1':
            get_all_language(conn)
        elif languageChoice == 'b':
            print("Back to main...")
            break

def non_response_rate_choice():
    while True:
        non_response_rate_menu()
        nonResponseRateChoice = input('Enter your choice (1-9): ')
        if nonResponseRateChoice == '1':
            get_all_non_response_rate(conn)
        elif nonResponseRateChoice == 'b':
            print("Back to main...")
            break

def response_choice():
    while True:
        response_menu()
        responseChoice = input('Enter your choice (1-9): ')
        if responseChoice == '1':
            get_all_response(conn)
        elif responseChoice == 'b':
            print("Back to main...")
            break

def topic_choice():
    while True:
        topic_menu()
        topicChoice = input('Enter your choice (1-9): ')
        if topicChoice == '1':
            get_all_topic(conn)
        elif topicChoice == 'b':
            print("Back to main...")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A command-line database application for connecting to SQL Server')
    #parser.add_argument('-server', required=True, help='The SQL Server address')
    #parser.add_argument('-database', required=True, help='The database name')
    #parser.add_argument('-username', required=True, help='The username for the SQL Server connection')
    #parser.add_argument('-password', required=True, help='The password for the SQL Server connection')

    args = parser.parse_args()

    conn = connect()

    while True:
        main_menu()
        choice = input('Enter your choice (1-9): ')

        if choice == '1':
            age_choice()
        elif choice == '2':
            boundary_choice()
        elif choice == '3':
            education_choice()
        elif choice == '4':
            faith_choice()
        elif choice == '5':
            language_choice()
        elif choice == '6':
            non_response_rate_choice()
        elif choice == '7':
            response_choice()
        elif choice == '8':
            topic_choice()
        elif choice == '9':
            break
        else:
            print('Not a valid input, please try again')

    conn.close()

