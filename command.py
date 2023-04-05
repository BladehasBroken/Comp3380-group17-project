import argparse
import pyodbc
from tabulate import tabulate
import sys
import keyboard

def connect():
    #connection_string = f'DRIVER={DESKTOP-TEFQKFL};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(f'DRIVER={{SQL Server}}; SERVER=localhost; DATABASE=group_project; Trusted_Connection=yes')
    return conn

# execute the query and formatted result
def query_database(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)

    print('execute the query...')

    result = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    formatted_result = tabulate(result, headers=column_names, tablefmt='grid')

    print(formatted_result)
    if result == []:
        print('Sorry, no result found!')

    cursor.close()

# execute the query with parameter and formatted result
def query_para_database(conn, query, para):
    cursor = conn.cursor()
    cursor.execute(query, para)

    print('execute the query...')

    result = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    formatted_result = tabulate(result, headers=column_names, tablefmt='grid')

    print(formatted_result)
    if result == []:
        print('Sorry, no result found!')

    cursor.close()

def get_all_ages(conn):
    query = f'select * from Ages'
    query_database(conn, query)

def get_population_belowAges_area(conn, age, area):
    query = f'select boundary_name, male, female from Boundary join Response on Boundary.boundary_id = Response.boundary join Ages on Response.response_id = Ages.response_id where max <= ? and boundary_name = ?'
    para = age, area
    query_para_database(conn,query, para)

def get_population_belowAges_gender(conn, age):
    query = 'SELECT A.male, A.female, A.min AS min_age, A.max AS max_age ' \
            'FROM Ages A JOIN Response R ON A.response_id = R.response_id ' \
            'WHERE A.max < ? ' \
            'GROUP BY A.male, A.female, A.min, A.max;'
    para = age
    query_para_database(conn, query, para)

def get_all_boundary(conn):
    query = 'select * from Boundary'
    query_database(conn,query)

def get_all_boundary_name(conn):
    query = 'select distinct Boundary_name from Boundary'
    query_database(conn,query)

def get_top5_response_boundary(conn):
    query = 'SELECT TOP 5 Boundary.boundary_name, Boundary.boundary_type, COUNT(Response.boundary) AS Responses ' \
            'FROM Boundary INNER JOIN Response ON Boundary.boundary_id = Response.boundary ' \
            'GROUP BY Boundary.boundary_name,  Boundary.boundary_type ' \
            'ORDER BY Responses DESC'
    query_database(conn, query)

def get_all_education(conn):
    query = 'select * from Education'
    query_database(conn,query)

def get_total_response_bydegree(conn):
    query = 'SELECT l.type, SUM(e.responses) AS ResponseNumber ' \
            'FROM Level l INNER JOIN Education e ON l.education_id = e.education_id ' \
            'GROUP BY l.type;'
    query_database(conn, query)

def get_response_number_degreeType_gender(conn):
    query = 'SELECT D.type, D.gender, COUNT(E.responses) as total_responses ' \
'FROM Education E JOIN Degree D ON E.education_id = D.education_id ' \
'GROUP BY D.type, D.gender;'
    query_database(conn,query)

def get_all_faith(conn):
    query = 'select * from Faith'
    query_database(conn,query)

def get_population_faith(conn):
    query = 'SELECT F.type, SUM(F.responses) as total_responses ' \
            'FROM Faith F ' \
            'GROUP BY F.type;'
    query_database(conn,query)

def get_all_language(conn):
    query = 'select * from Language'
    query_database(conn,query)

def get_population_langugae(conn, para):
    query = 'SELECT b.boundary_name, b.boundary_type, l.english, l.french, l.french_and_english, sl.type, sl.amount AS Secondary_Language_Amount ' \
            'FROM Boundary b INNER JOIN Response r ON r.boundary = b.boundary_id INNER JOIN Language l ON l.response_id = r.response_id INNER JOIN Secondary_Language sl ON sl.response_id = r.response_id ' \
            'WHERE b.boundary_name = ?'
    para = para
    query_para_database(conn,query,para)


def get_all_non_response_rate(conn):
    query = 'select * from Non_Response_Rate'
    query_database(conn,query)

def get_non_response_rate_peryear(conn):
    query = 'SELECT year, AVG(non_response_rate) as avg_non_response_rate ' \
            'FROM Non_Response_Rate ' \
            'GROUP BY year;'
    query_database(conn,query)

def get_top5_boundaries_non_response_rate(conn):
    query = 'SELECT TOP 5 B.boundary_name, N.year, N.non_response_rate ' \
            'FROM Boundary B JOIN Non_Response_Rate N ON B.boundary_id = N.boundary_id ' \
            'ORDER BY N.non_response_rate DESC'
    query_database(conn,query)

def get_all_response(conn):
    query = 'select * from Response'
    query_database(conn,query)

def get_all_topic(conn):
    query = 'select * from Topic'
    query_database(conn,query)

def get_topic_number_byresponse(conn):
    query = 'SELECT t.topic_name, COUNT(r.response_id) AS Number ' \
            'FROM Topic t INNER JOIN Response r ON t.id = r.topic ' \
            'GROUP BY t.topic_name'
    query_database(conn,query)

def get_list_topic_name(conn):
    query = 'select t.topic_name from Topic t'
    query_database(conn,query)

def get_boundary_responseNumber_byTopic(conn, para):
    query = 'SELECT B.boundary_name, COUNT(R.response_id) as num_responses ' \
            'FROM Response R JOIN Boundary B ON R.boundary = B.boundary_id ' \
            'WHERE R.topic = (SELECT id FROM Topic WHERE topic_name = ?) ' \
            'GROUP BY B.boundary_name ' \
            'ORDER BY num_responses DESC'
    query_para_database(conn,query,para)

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
    print('9. Exit the program')

def age_menu():
    print('Choose an option:')
    print('1. get all the age information')
    print('2. get population that below some age in one area ')
    print('3. get responses number that below some age and grouped by gender')
    print('b. Back to main menu')

def boundary_menu():
    print('Choose an option:')
    print('1. get all the boundary information')
    print('2. get a list of boundary names ')
    print('3. Boundaries with top 5 amount of responses')
    print('b. Back to main menu')

def educaiton_menu():
    print('Choose an option:')
    print('1. get all the education information')
    print('2. total number of responses by degree')
    print('3. get number of responses by degree type and gender')
    print('b. Back to main menu')

def faith_menu():
    print('Choose an option:')
    print('1. get all the faith information')
    print('2. get population by faith')
    print('b. Back to main menu')

def language_menu():
    print('Choose an option:')
    print('1. get all the language information')
    print('2. get population by languages')
    print('b. Back to main menu')

def non_response_rate_menu():
    print('Choose an option:')
    print('1. get all the non resposne rate information')
    print('2. get the average non-response rate per year')
    print('3. get the top 5 boundareis with highest non response rate')
    print('b. Back to main menu')

def response_menu():
    print('Choose an option:')
    print('1. get all the response information')
    print('b. Back to main menu')

def topic_menu():
    print('Choose an option:')
    print('1. get all the topic information')
    print('2. amount of topic by with responses')
    print('3. get a list of topic name')
    print('4. get boundaries with number of responses for specific topic')
    print('b. Back to main menu')

# do task when user select option under the age menu
def age_choice():
    while True:
        age_menu()
        ageChoice = input('Enter your choice (1-9): ')
        if ageChoice == '1':
            get_all_ages(conn)
        elif ageChoice == '2':
            age = int(input('Enter the age: '))
            area = input('Enter the boundary name: ')
            get_population_belowAges_area(conn, age, area)
        elif ageChoice == '3':
            age = int(input('Enter the age: '))
            get_population_belowAges_gender(conn, age)
        elif ageChoice == 'b':
            print("Back to main...")
            break
        else:
            print('Not a valid input! Please try again')

# do task when user select option under the age menu
def boundary_choice():
    while True:
        boundary_menu()
        boundaryChoice = input('Enter your choice (1-9): ')
        if boundaryChoice == '1':
            get_all_boundary(conn)
        elif boundaryChoice == '2':
            get_all_boundary_name(conn)
        elif boundaryChoice == '3':
            get_top5_response_boundary(conn)
        elif boundaryChoice == 'b':
            print("Back to main...")
            break
        else:
            print('Not a valid input! Please try again')


def education_choice():
    while True:
        educaiton_menu()
        educationChoice = input('Enter your choice (1-9): ')
        if educationChoice == '1':
            get_all_education(conn)
        elif educationChoice == '2':
            get_total_response_bydegree(conn)
        elif educationChoice == '3':
            get_response_number_degreeType_gender(conn)
        elif educationChoice == 'b':
            print("Back to main...")
            break
        else:
            print('Not a valid input! Please try again')

def faith_choice():
    while True:
        faith_menu()
        faithChoice = input('Enter your choice (1-9): ')
        if faithChoice == '1':
            get_all_faith(conn)
        elif faithChoice == '2':
            get_population_faith(conn)
        elif faithChoice == 'b':
            print("Back to main...")
            break
        else:
            print('Not a valid input! Please try again')

def language_choice():
    while True:
        language_menu()
        languageChoice = input('Enter your choice (1-9): ')
        if languageChoice == '1':
            get_all_language(conn)
        elif languageChoice == '2':
            para = input('Enter the boundary name: ')
            get_population_langugae(conn,para)
        elif languageChoice == 'b':
            print("Back to main...")
            break
        else:
            print('Not a valid input! Please try again')

def non_response_rate_choice():
    while True:
        non_response_rate_menu()
        nonResponseRateChoice = input('Enter your choice (1-9): ')
        if nonResponseRateChoice == '1':
            get_all_non_response_rate(conn)
        elif nonResponseRateChoice == '2':
            get_non_response_rate_peryear(conn)
        elif nonResponseRateChoice == '3':
            get_top5_boundaries_non_response_rate(conn)
        elif nonResponseRateChoice == 'b':
            print("Back to main...")
            break
        else:
            print('Not a valid input! Please try again')

def response_choice():
    while True:
        response_menu()
        responseChoice = input('Enter your choice (1-9): ')
        if responseChoice == '1':
            get_all_response(conn)
        elif responseChoice == 'b':
            print("Back to main...")
            break
        else:
            print('Not a valid input! Please try again')

def topic_choice():
    while True:
        topic_menu()
        topicChoice = input('Enter your choice (1-9): ')
        if topicChoice == '1':
            get_all_topic(conn)
        elif topicChoice == '2':
            get_topic_number_byresponse(conn)
        elif topicChoice == '3':
            get_list_topic_name(conn)
        elif topicChoice == '4':
            para = input('Enter the topic name: ')
            get_boundary_responseNumber_byTopic(conn,para)
        elif topicChoice == 'b':
            print("Back to main...")
            break
        else:
            print('Not a valid input! Please try again')

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
            print('Exiting...')
            break
        else:
            print('Not a valid input! Please try again')

    conn.close()

