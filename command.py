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

def get_all_boundary():

def fetch_all_tickets(conn):
    query = 'SELECT * FROM parking;'
    query_database(conn, query)

def fetch_ticket_by_id(conn, ticket_id):
    query = f'SELECT * FROM parking WHERE ticketNo = {ticket_id};'
    query_database(conn, query)

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

def boundary_menu():
    print('Choose an option:')
    print('1. get all the boundary information')
    print('2. get a list of boundary names ')

# do task when user select option under the age menu
def age_choice():
    ageChoice = input('Enter your choice (1-9): ')
    if ageChoice == '1':
        get_all_ages(conn)
    elif ageChoice == '2':
        age = int(input('Enter the age: '))
        area = "'" + input('Enter the boundary name: ') + "'"
        get_population_belowAges_area(conn, age, area)

# do task when user select option under the age menu
def boundary_choice():
    boundary_chocie = input('Enter your choice (1-9): ')
    if boundary_chocie == '1':


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
            while True:
                age_menu()
                age_choice()
        elif choice == '2':
            ticket_id = int(input('Enter the ticket ID: '))
            fetch_ticket_by_id(conn, ticket_id)
        elif choice == '3':
            street = "'" + input('Enter the street name: ') + "'"
        elif choice == '4':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please try again.')

    conn.close()

