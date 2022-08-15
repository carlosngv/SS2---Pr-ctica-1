import time
import curses
from db import connection

menu = ["Clear model", "Create model", "Extract data", "Load data", "Queries", "Exit"]
global loop
loop = 1

def join(iterator, seperator):
    it = map(str, iterator)
    seperator = str(seperator)
    string = next(it, '')
    for s in it:
        string += seperator + s
    return string

def process_query():
    try:
        with connection.cursor() as cursor:

            query = '''
                SELECT d.[year] as Year, COUNT(*) as 'Tsunami Count' FROM Tsunamis t
                INNER JOIN Dates d on t.idDates = d.idDates
                GROUP BY d.year
                ORDER BY d.year DESC;
            '''

            cursor.execute(query)

            results = cursor.fetchall()
            data = [list(rows) for rows in results] # this one

            columns = [column[0] for column in cursor.description]
            columns = ' | '.join(columns)

            formated_data = ''
            for item in data:
                formated_data = formated_data + join(item, '       |       ') + '\n'

            query_result = "{}\n {}".format(columns, formated_data)
            print(query_result)

    except Exception as e:

        print("Ocurrió un error al insertar: ", e)

    finally:
        connection.close()




def print_menu(stdscr, selected_item):
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    for index, item in enumerate(menu):
        x = w//2 - len(item)//2
        y = h//2 - len(menu)//2 + index
        if index == selected_item:
            # Only colors the current row selected
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, item)

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    current_item = 0

    print_menu(stdscr, current_item)

    while loop:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and current_item > 0:
            current_item -= 1
        elif key == curses.KEY_DOWN and current_item < len(menu) - 1:
            current_item += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()


            if current_item == len(menu) - 1:
                break
            else:
                evaluate_selection(current_item, stdscr)

            stdscr.refresh()
            stdscr.getch()

        print_menu(stdscr, current_item)
        stdscr.refresh()

def evaluate_selection(current_selection, stdscr):
    if current_selection == 0:
        stdscr.addstr(0, 0, "You've selected: {}".format(menu[current_selection]))
    elif current_selection == 1:
        stdscr.addstr(0, 0, "You've selected: {}".format(menu[current_selection]))
    elif current_selection == 2:
        stdscr.addstr(0, 0, "You've selected: {}".format(menu[current_selection]))
    elif current_selection == 3:
        stdscr.addstr(0, 0, "You've selected: {}".format(menu[current_selection]))
    elif current_selection == 4:
        stdscr.addstr(0, 0, "You've selected: {}".format(menu[current_selection]))


if __name__ == '__main__':
    curses.wrapper(main)
