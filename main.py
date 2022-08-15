import time
import curses
from db import connect_db
from data import DDL, queries, insert_bulk, table_drop

menu = ["Queries", "Clear model", "Create model", "Load CSV", "Exit"]
query_menu = ["Query 1", "Query 2", "Query 3", "Query 4", "Query 5", "Query 6", "Query 7", "Query 8", "Query 9", "Query 10", "Exit Queries"]
current_menu = []

global loop
loop = 1

def join(iterator, seperator):
    it = map(str, iterator)
    seperator = str(seperator)
    string = next(it, '')
    for s in it:
        string += seperator + s
    return string

def clear_model():
    connection = connect_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute(table_drop)
    except Exception as e:
        print(e)

def load_data():
    connection = connect_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_bulk)
    except Exception as e:
        print(e)

def create_model():
    connection = connect_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute(DDL)
    except Exception as e:
        print(e)

def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()

def process_query(stdscr, query):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)


            results = cursor.fetchall()
            data = [list(rows) for rows in results] # this one

            columns = [column[0] for column in cursor.description]
            columns = ' | '.join(columns)

            query_result = []
            query_result.append(columns)

            for item in data:
                query_result.append(join(item, '       |       '))

            return query_result

    except Exception as e:
        print_center(stdscr, "Something went wrong... :(")
        time.sleep(2)
    finally:
        connection.close()

def print_query(stdscr, query):
    try:
        stdscr.clear()
        for i in query:
            stdscr.addstr(str(i) + '\n')
    except:
        pass
    stdscr.refresh()

def print_menu(stdscr, selected_item):
    global current_menu
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    try:

        for index, item in enumerate(current_menu):
            x = w//2 - len(item)//2
            y = h//2 - len(current_menu)//2 + index
            if index == selected_item:
                # Only colors the current row selected
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, item)
        stdscr.refresh()
    except Exception as e:
        print(e)

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    global current_menu
    current_menu = menu
    current_item = 0

    print_menu(stdscr, current_item)

    while loop:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and current_item > 0:
            current_item -= 1
        elif key == curses.KEY_DOWN and current_item < len(current_menu) - 1:
            current_item += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()


            if current_menu[current_item] == 'Exit':
                break
            else:
                evaluate_selection(current_item, stdscr)

            stdscr.refresh()
            stdscr.getch()

        print_menu(stdscr, current_item)
        stdscr.refresh()

def evaluate_selection(current_selection, stdscr):
    global current_menu
    if current_menu[current_selection] == "Clear model":
        clear_model()
        print_center(stdscr, "Model successfully cleared")
    elif current_menu[current_selection] == "Create model":
        create_model()
        print_center(stdscr, "Model successfully created")
    elif current_menu[current_selection] == "Load CSV":
        load_data()
        print_center(stdscr, "Data successfully loaded")
    elif current_menu[current_selection] == "Queries":
        current_menu = query_menu
        print_menu(stdscr, current_selection)
    elif current_menu[current_selection] == "Exit Queries":
        current_menu = menu
        main(stdscr)
    elif current_menu[current_selection] == "Query 1":
        query_result = process_query(stdscr, queries[0])
        print_query(stdscr, query_result)
        #print_center(stdscr, query_result)
    elif current_menu[current_selection] == "Query 2":
        query_result = process_query(stdscr, queries[1])
        print_query(stdscr, query_result)
    elif current_menu[current_selection] == "Query 3":
        query_result = process_query(stdscr, queries[2])
        print_query(stdscr, query_result)
    elif current_menu[current_selection] == "Query 4":
        query_result = process_query(stdscr, queries[3])
        print_query(stdscr, query_result)
    elif current_menu[current_selection] == "Query 5":
        query_result = process_query(stdscr, queries[4])
        print_query(stdscr, query_result)
    elif current_menu[current_selection] == "Query 6":
        query_result = process_query(stdscr, queries[5])
        print_query(stdscr, query_result)
    elif current_menu[current_selection] == "Query 7":
        query_result = process_query(stdscr, queries[6])
        print_query(stdscr, query_result)
    elif current_menu[current_selection] == "Query 8":
        query_result = process_query(stdscr, queries[7])
        print_query(stdscr, query_result)
    elif current_menu[current_selection] == "Query 9":
        query_result = process_query(stdscr, queries[8])
        print_query(stdscr, query_result)
    elif current_menu[current_selection] == "Query 10":
        query_result = process_query(stdscr, queries[9])
        print_query(stdscr, query_result)



if __name__ == '__main__':
    curses.wrapper(main)
