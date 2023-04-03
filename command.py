import argparse
import pyodbc
from tabulate import tabulate
import sys
import keyboard

def connect(username, password):
    #connection_string = f'DRIVER={DESKTOP-TEFQKFL};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(f'DRIVER={{SQL Server}}; SERVER=DESKTOP-TEFQKFL; DATABASE=parkingWinnipeg; UID = {username}; PWD={password}; Trusted_Connection=yes')
    return conn

def query_database(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    formatted_result = tabulate(result, headers=column_names, tablefmt='grid')

    print(formatted_result)

    cursor.close()

def find_ticket_by_street(conn, street):
    query = f'select * from parking where street = {street};'
    print(street)
    query_database(conn, query)

def fetch_all_tickets(conn):
    query = 'SELECT * FROM parking;'
    query_database(conn, query)

def fetch_ticket_by_id(conn, ticket_id):
    query = f'SELECT * FROM parking WHERE ticketNo = {ticket_id};'
    query_database(conn, query)

def main_menu():
    print('Choose an action:')
    print('1. Fetch all tickets')
    print('2. Fetch ticket by ID')
    print('3. Find ticket by street')
    print('4. Exit')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A command-line database application for connecting to SQL Server')
    #parser.add_argument('-server', required=True, help='The SQL Server address')
    #parser.add_argument('-database', required=True, help='The database name')
    parser.add_argument('-username', required=True, help='The username for the SQL Server connection')
    parser.add_argument('-password', required=True, help='The password for the SQL Server connection')

    args = parser.parse_args()

    conn = connect(args.username, args.password)

    while True:
        main_menu()
        choice = input('Enter your choice (1, 2, or 3): ')

        if choice == '1':
            fetch_all_tickets(conn)
        elif choice == '2':
            ticket_id = int(input('Enter the ticket ID: '))
            fetch_ticket_by_id(conn, ticket_id)
        elif choice == '3':
            street = "'" + input('Enter the street name: ') + "'"
            find_ticket_by_street(conn, street)
        elif choice == '4':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please try again.')

    conn.close()

