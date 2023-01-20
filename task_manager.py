from datetime import datetime
from tabulate import tabulate

# Variables used for highlighting parts of various outputs.
red = '\033[91m'
pink = '\033[95m'
blue = '\033[94m'
cyan = '\033[96m'
green = '\033[92m'
yellow = '\033[93m'
underline = '\033[4m'
bold = '\033[1m'
end = '\033[0m'


def read_external_user_file():
    """ Reads the "user.txt" file and loops over each line, separating usernames and passwords into two lists.
    :return: (list) A list containing each user's username.
    :return: (list) A list containing each user's password.
    """
    user_file = open("user.txt", "r", encoding="utf-8")
    stored_login_details = user_file.readlines()
    user_file.close()
    usernames = []
    passwords = []

    for each_user in stored_login_details:
        strip_user = each_user.strip("\n").split(", ")
        usernames.append(strip_user[0]), passwords.append(strip_user[1])
    return usernames, passwords


def read_external_task_file():
    """ Opens, reads and stores the tasks from "tasks.txt".
    :return (list) Each task is stored as an item within the list.
    """
    task_file = open("tasks.txt", "r", encoding="utf-8")
    stored_tasks = task_file.readlines()
    task_file.close()
    return stored_tasks


# ###########################
def tab(quantity):
    """ Increases and uniforms the spacing between the border and text outputs.
    :param quantity: (int) How many tab spaces to insert.
    :return: (str) Increases the distance between the page border and outputs.
    """
    return "\t" * quantity


def dividing_line(line_colour=blue):
    """ A line to separate different displays.
    :param line_colour: The colour of each dividing line.
    """
    print(f"{line_colour}{bold}{underline}─────────────────────────────────────────────────────────────────────{end}"*2)


def register_user():
    """ A new user can be added to the system if the "admin" is logged in. The username is checked to see if it is
    already in use and if not, password can be written to the "user.txt" file and a password check is added to ensure
    it is entered correctly and the stored usernames and passwords are updated with each additional entry.
    """
    if username == "admin":
        print(f"\n   \t\t\t   {underline}{bold}Register New User{end}\n")
        while True:
            new_user = input(" \t Which username would you like to add to the system: ")

            # Option to return to the main menu.
            if new_user == "-1":
                break

            # Checking if the username is already in use. If so, a message is displayed giving the option to enter a
            # new username or return to the menu.
            elif new_user in stored_usernames:
                print(f"\n{red}{bold} \t Unfortunately that username has already been taken. Please choose a new "
                      f"username.{end}"
                      f"{bold}\n \t Alternatively you can to return to the main menu by entering {yellow}-1{end}"
                      f".{end}\n")
                continue

            # Password input with secondary input required.
            new_password = input(" \t Now enter their password: ")
            password_check = input(" \t Please confirm the password: ")

            # Password check to ensure they match and if so, the users details are written to the "user.txt" file.
            if new_password == password_check:
                user_file = open("user.txt", "a+", encoding="utf-8")
                user_file.write(f"\n{new_user}, {new_password}")
                user_file.close()
                print(f"\n{green}{bold} \t Thank you, the new user has been added to the system.{end}")

                # Login details in "user.txt" are updated so that users cannot be duplicated.
                read_external_user_file()
                break

            # To catch any errors and return you to the password input stage.
            else:
                print(f"{red}{bold} \t I'm sorry, the passwords did not match. Please try again.{end}\n")

    else:
        print(f"\n{red}{bold} \t I'm sorry but only the admin is allowed to register new users.{end}")


def assign_task():
    """ Function for adding new tasks to the "tasks.txt" file. A valid username input is required as well as: task name,
    task description and due date. Today's date is added automatically as the assignment date.
    """
    # Updates the lists in "stored_usernames" and "stored_passwords" so that any new users can be assigned tasks.
    read_external_user_file()
    task_title = ""
    task_description = ""
    date_assigned = datetime.today().strftime('%d %b %Y')
    due_date_string = None
    task_complete = "No"
    print(f" \n \t\t\t    {underline}{bold}Assign A Task{end}")

    while True:
        task_username = input("\n \t Who is the new task for: ")

        if task_username not in stored_usernames:
            show_usernames = input(f"{red}{bold} \t I'm sorry, there is no user on the system with that name. Please "
                                   f"enter a valid username.{end}\n"
                                   f" \t To see a list of users who you can assign a task to, type {yellow}yes{end}."
                                   f"\n \t Otherwise press the {yellow}enter{end} key: ").lower()

            # Displays the registered usernames so the admin can allocate the task to a valid user.
            if "yes" in show_usernames:
                username_list = [i for i in stored_usernames]
                print(f" \t \n{pink}{username_list}{end}")
            continue

        task_title = input("     What is the title for the task: ")
        task_description = input("     Please describe the task: ")

        while True:
            try:
                task_due_date = datetime.strptime(input(f" \t Enter the new due date for the new task using the "
                                                        f"{yellow}yyyy mm dd {end}format: "), '%Y %m %d')
                due_date_string = datetime.strftime(task_due_date, "%d %b %Y")

                if task_due_date < datetime.now():
                    print(f"\n{red}{bold} \t This date has already passed. Please set a future date.{end}")
                    continue

            except (ValueError, TypeError):
                print(f"{red}{bold} \t Please enter the new due date in the correct format."
                      f" For example, today's date is {yellow}{datetime.now().strftime('%Y %m %d')}{end}.\n")
                continue
            break
        break

    task_file = open("tasks.txt", "a", encoding="utf-8")
    task_file.write(f"\n{task_username}, {task_title.capitalize()}, {task_description.capitalize()},"
                    f" {date_assigned}, {due_date_string.title()}, {task_complete}")
    task_file.close()

    print(f"\n{green}{bold} \t Successfully added {task_username}'s task to the system.{end}")


def task_display(line_colour, count, task_detail):
    """ Outputs tasks in a readable manner.
    :param line_colour: Choose a colour for the "dividing_line".
    :param count: Which task number is being displayed.
    :param task_detail: Task information spliced into relevant items.
    """
    dividing_line(line_colour)
    print(f"\n                   {underline}{bold}Task {count}{end}\n"
          f"\n  \t Task:                   {task_detail[1]}"
          f"\n  \t Assigned to:            {task_detail[0]}"
          f"\n  \t Date assigned:          {task_detail[3]}"
          f"\n  \t Due date:               {task_detail[4]}"
          f"\n  \t Task complete:          {task_detail[5]}"
          f"  \t Task description:"
          f"\n \t {task_detail[2]}\n")


def dictionary_of_all_tasks():
    """ A dictionary allocating an index position to each task from the "tasks.txt" file.
    :return: (dict) Task index positions as keys with the tasks as values.
    """
    stored_tasks = read_external_task_file()
    count_list, task_list = [], []
    index_and_all_tasks = {}

    for task, count in enumerate(stored_tasks):
        count_list.append(count), task_list.append(task)
        index_and_all_tasks = dict(zip(count_list, task_list))
    return index_and_all_tasks


def view_all_tasks():
    """ All tasks are displayed from the "tasks.txt" file."""
    stored_tasks = read_external_task_file()
    print(f"\n \t\t\t   {underline}{bold}View All Tasks{end}\n")

    # Loops through each task and prints out the information in order of appearance along with a task number.
    for task_index, task in enumerate(stored_tasks, start=1):
        extracted_information = task.split(", ")
        task_display(cyan, task_index, extracted_information)
        dividing_line(cyan)


def view_mine():
    """ Only displays tasks assigned to the user logged in and allows an update for if the task has been
    completed. There is also an option to modify a tasks deadline and reassign it to another user.
    """
    stored_tasks = read_external_task_file()
    print(f"\n \t\t\t   {underline}{bold}View My Tasks{end}\n")

    index_and_all_tasks = dictionary_of_all_tasks()

    number_of_tasks = 0  # The number of tasks assigned to the user logged in.
    task_index = []
    task_values = []
    dictionary_index_and_tasks = {}  # Dictionary for task numbers (keys) and tasks (values).

    for task in stored_tasks:
        split_task = task.split(", ")

        # Only iterates over tasks relevant to the user.
        if split_task[0] == username:
            number_of_tasks += 1

            # Stores a task number as a key with each task being the value. This is so each task can be
            # called by number later on.
            task_index.append(number_of_tasks), task_values.append(split_task)
            dictionary_index_and_tasks = dict(zip(task_index, task_values))

            # Prints out each user specific task.
            task_display(pink, number_of_tasks, split_task)

    dividing_line(cyan)
    print(f" \t There are {yellow}{bold}{number_of_tasks}{end} tasks assigned to {yellow}{bold}{username}{end}.")
    dividing_line(cyan)

    task_to_edit = []       # For the users chosen task to edit.
    string_to_edit = ""
    edited_task = None
    original_index = 0

    # The first loop is for task selection and the nested second loop is for the editing menus and processes.
    while True:
        # An error message is printed and the input loops if a data type other than an integer is entered.
        try:
            task_select_input = int(input("\n \t Which task number would you like to edit: "))
        except ValueError:
            print(f"{red}{bold} \t This input is expecting a digit and instead you entered an incorrect character.{end}"
                  f"\n \t Please enter a {yellow}{bold}valid{end} task number or alternatively, you can return to the "
                  f"main menu by entering {yellow}{bold}-1{end}.")
            continue

        # By taking the users task selection as the dictionary key, it returns the allocated task.
        task_to_edit = dictionary_index_and_tasks.get(task_select_input)

        # Returns to the main menu.
        if task_select_input == -1:
            print(f"\n \t {green}{bold}Returning to the main menu.{end}")
            break

        # Users task selection does not match with one of their valid tasks.
        elif task_select_input < -1 or task_select_input == 0 or task_select_input > number_of_tasks:
            print(f"{red} \t Please enter a valid task number, Task {bold}{task_select_input} is not a valid option."
                  f"{end}\n \t Please enter a {yellow}{bold}valid{end} task number or alternatively, you can return "
                  f"to the main menu by entering {yellow}{bold}-1{end}.")
            continue

        # Checks if the task is already complete.
        elif "Yes" in task_to_edit[5]:
            print(f"{red}{bold} \t You can not edit a task that is already complete, please select another.{end}")
            continue

        # If the task choice is valid.
        elif 0 < task_select_input <= number_of_tasks:
            string_to_edit = ", ".join(task_to_edit)
            task_display(yellow, task_select_input, task_to_edit)

            # Loop for the task editing process.
            while True:
                dividing_line(yellow)

                # Task completion menu.
                update_task_progress_menu = str(input(f"\n \t\t\t {underline}{bold}Update Task Progress{end}\n"
                                                      f"\n        -1. Return to the main menu."
                                                      f"\n         1. Mark the task as complete."
                                                      f"\n         2. Edit the selected task."
                                                      f"\n\n     How would you like to modify the task: "))

                # Return to the main menu.
                if update_task_progress_menu == "-1":
                    dividing_line(yellow)
                    print(f"\n \t {green}{bold}All information has been updated."
                          f"\n \t Returning to the main menu.{end}")
                    break

                # Option to mark the task as complete.
                elif update_task_progress_menu == "1":
                    task_to_edit.pop(5)
                    task_to_edit.insert(5, "Yes\n")
                    edited_task = True
                    print(f"\n \t{green}{bold} Task {task_select_input} marked as complete.{end}"
                          f"\n \t Return to the main menu to update the system.{end}")

                # Task editing menu.
                elif update_task_progress_menu == "2":
                    dividing_line(red)
                    modify_task_menu = str(input(f"\n \t\t\t\t {underline}{bold}Modify Task{end}\n"
                                                 f"\n        -1. Return to update task progress menu."
                                                 f"\n         1. Change who the task is assigned to."
                                                 f"\n         2. Modify the due date of the task."
                                                 f"\n\n     What would you like to edit: "))
                    dividing_line(red)

                    # Return to the Update Task Progress.
                    if modify_task_menu == "-1":
                        print(f"\n \t {green}{bold}Returning to the update task progress menu.{end}")
                        break

                    # Changes the assigned task user.
                    elif modify_task_menu == "1":
                        print(f"\n \t\t\t    {underline}{bold}Reassign Task{end}")
                        while True:
                            newly_assigned_user = str(input("\n \t Who is the new user: "))
                            if newly_assigned_user in stored_usernames:
                                task_to_edit.pop(0)
                                task_to_edit.insert(0, newly_assigned_user)
                                print(f"\n{green}{bold} \t This task has been reassigned to {newly_assigned_user}.{end}"
                                      f"\nReturn to the main menu to update the system.")
                                break
                            elif newly_assigned_user not in stored_usernames:
                                print(f"\n{red}{bold} \t I'm sorry, there is no user on the system with that name. "
                                      f"Please enter a valid username.{end}")
                                show_usernames = input(
                                    f" \t To see a list of users who you can assign a task to, type {yellow}yes{end}."
                                    f"\n \t Otherwise press the {yellow}enter{end} key: ").lower()
                                if "yes" in show_usernames:
                                    username_list = [i for i in stored_usernames]
                                    print(f"\n \t {pink}{username_list}{end}")
                                continue
                            edited_task = True

                    # Changes the due date of the task.
                    elif modify_task_menu == "2":
                        print(f"\n \t\t\t    {underline}{bold}Extend Deadline{end}")
                        while True:
                            try:
                                new_due_date = datetime.strptime(
                                    input(f"\n \t What date would you like to extend it to? Use the {yellow}yyyy mm dd"
                                          f"{end} format: "), '%Y %m %d')

                                if new_due_date < datetime.now():
                                    print(f"{red}{bold} \t This date has already passed. Please enter a deadline "
                                          f"with an achievable completion date.{end}")
                                    continue

                                convert_date_format = datetime.strftime(new_due_date, "%d %b %Y")
                                print(f"\n \t {green}{bold}The deadline for Task {task_select_input} has been changed "
                                      f"from {yellow}{task_to_edit[4]}{end}{green} to {yellow}{convert_date_format}"
                                      f"{end}. \n"
                                      f" \t Return to the main menu to update the system.")
                                task_to_edit.pop(4)
                                task_to_edit.insert(4, convert_date_format)

                            except (ValueError, TypeError):
                                print(f"{red}{bold} \t Please enter the new due date in the correct format. "
                                      f"For example, today's date is {yellow}{datetime.now().strftime('%Y %m %d')}"
                                      f"{end}.")
                                continue
                            break
                        edited_task = True

            break

        else:
            print(f"\n{pink}{bold} \t Your entry does not represent one of your tasks, please select a valid task "
                  f"number"
                  f" from the display: {end}")
            continue

    # A check which updates the "tasks.txt" file if a task was edited.
    if edited_task:
        if string_to_edit in index_and_all_tasks:
            original_index = index_and_all_tasks.get(string_to_edit)    # Finds index position for the edited task.
        edited_string = ", ".join(task_to_edit)

        # Removes the unedited task from "stored_tasks" then updates the list and "tasks.txt" with the modified version.
        stored_tasks.pop(original_index), stored_tasks.insert(original_index, edited_string)
        post_edit_tasks = "".join(stored_tasks)

        rewrite_tasks = open("tasks.txt", "w", encoding="utf-8")
        rewrite_tasks.write(f"{post_edit_tasks}")
        rewrite_tasks.close()


def statistics():
    """ Reads from the "user_overview.txt" and "task_overview.txt" files and outputs the statistics in a table format.
    """
    dividing_line(red)
    print(f"\n \t\t\t   {bold}{underline}Statistics Menu{end}")

    # dividing_line(yellow)
    generate_reports()
    dividing_line(red)

    task_report = open("task_overview.txt", "r", encoding="UTF-8")
    print(f"\n{task_report.read()}\n\n\n")

    dividing_line(red)

    user_report = open("user_overview.txt", "r", encoding="UTF-8")
    print(f"\n{user_report.read()}\n\n\n")


def percentage_calculator(variant, total_of_tasks):
    """ Calculates the percentage of a number when given two values.
    :param variant: (int) The value of what percentage is needed.
    :param total_of_tasks: (int) Full amount of what is being divided.
    :return: (str) A string which will show 0.00% in the text.
    :return: (int) What percentage the "variant" is of the "total_of_tasks".
    """
    # This check is to avoid a Zero Division Error.
    if variant == 0:
        return "0.00"
    return round((int(variant) / int(total_of_tasks)) * 100, 2)


def generate_reports():
    """ Displays and creates the "task_overview", totals and "user_overview" reports."""
    stored_tasks = read_external_task_file()

    # Data for the task total and user total report.
    report1 = []
    user_title = "\nUser Overview\n\n" \
                 "These reports output all information from the system regarding each user and the tasks assigned to " \
                 "them.\n\n"
    header1 = ["Users registered", "Tasks registered"]
    user_count = len(stored_usernames)
    task_count = len(stored_tasks)
    totals = [user_count, task_count]
    report1.append(header1)
    report1.append(totals)

    # "user_overview" lists, ready to be nested.
    user_overview = []
    header2 = ["Username", "Tasks", "Tasks assigned", "Completed tasks", "Incomplete tasks", "Overdue tasks"]
    user_overview.append(header2)

    # "task_overview" text body, headers and variables.
    report3 = []
    task_overview = []
    task_title = "\nTask Overview\n\n" \
                 "This report reviews all information within the system and displays the data.\n\n"
    header3 = ["Tasks", "Completed tasks", "Incomplete tasks", "Overdue tasks", "Incomplete tasks (%)",
               "Overdue tasks (%)"]
    all_users_complete = 0
    all_users_incomplete = 0
    all_users_overdue = 0
    report3.append(header3)

    # "user_overview" and "task_overview" calculations.
    for user in stored_usernames:
        tasks_per_user = 0
        complete_tasks = 0
        incomplete_tasks = 0
        incomplete_overdue = 0
        report2 = []

        for each in stored_tasks:
            item = each.split(", ")

            if user == item[0]:
                tasks_per_user += 1

                if "Yes" in item[5]:
                    complete_tasks += 1
                    all_users_complete += 1

                elif "No" in item[5]:
                    incomplete_tasks += 1
                    all_users_incomplete += 1

                    # Converts the tasks deadline into a comparable format to determine whether it is overdue.
                    overdue_check = datetime.strptime(item[4], "%d %b %Y")
                    if datetime.now() > overdue_check:
                        incomplete_overdue += 1
                        all_users_overdue += 1

        # User overview percentage calculations.
        perc_tasks_assigned = percentage_calculator(tasks_per_user, task_count)
        perc_tasks_completed = percentage_calculator(complete_tasks, tasks_per_user)
        perc_tasks_incomplete = percentage_calculator(incomplete_tasks, tasks_per_user)
        perc_incomplete_overdue = percentage_calculator(incomplete_overdue, tasks_per_user)

        # Creating a multidimensional array of the "user_overview" so that it is ready to write onto the file.
        report2.append(str(user))
        report2.append(str(tasks_per_user))
        report2.append(str(perc_tasks_assigned) + "%")
        report2.append(str(perc_tasks_completed) + "%")
        report2.append(str(perc_tasks_incomplete) + "%")
        report2.append(str(perc_incomplete_overdue) + "%")

        user_overview.append(report2)

    # Task_overview percentage calculations.
    perc_tasks_incomplete = percentage_calculator(all_users_incomplete, task_count)
    perc_incomplete_overdue = percentage_calculator(all_users_overdue, task_count)

    # Creating a multidimensional array of the "task_overview" so that it is ready to write onto the file.
    task_overview.append(str(task_count))
    task_overview.append(str(all_users_complete))
    task_overview.append(str(all_users_incomplete))
    task_overview.append(str(all_users_overdue))
    task_overview.append(str(perc_tasks_incomplete) + "%")
    task_overview.append(str(perc_incomplete_overdue) + "%")

    report3.append(list(task_overview))

    # Writes the task overview report to the "task_overview.txt" file.
    overview_of_tasks = open("task_overview.txt", "w+", encoding="utf-8")
    overview_of_tasks.write(task_title + tabulate(report3, headers="firstrow", tablefmt="fancy_grid"))
    overview_of_tasks.close()

    # Writes the task total, user total and user overview report to the "user_overview.txt" file.
    overview_of_tasks = open("user_overview.txt", "w+", encoding="utf-8")
    overview_of_tasks.write(user_title + tabulate(report1, headers="firstrow", tablefmt="fancy_grid")
                            + "\n" + tabulate(user_overview, headers="firstrow", tablefmt="fancy_grid"))
    overview_of_tasks.close()

    print(f"\n{green}{bold} \t Generating report..."
          f"\n \t All reports have been generated.{end}")


# Global variables of the login details for each user are stored in two separate lists.
stored_usernames, stored_passwords = read_external_user_file()

# A dictionary is created with the usernames (keys) and passwords (values).
login_dictionary = dict(list(zip(stored_usernames, stored_passwords)))

# Login process which uses the dictionary to check the username and password match.
while True:
    username = input("\n\n            Enter your username:    ")

    if username not in stored_usernames:
        print(f"{red}{bold} \t I'm sorry, this username is incorrect. Please Try again.{end}\n")
        continue

    password = input("            Enter your password:    ")

    if username in login_dictionary and login_dictionary.get(username) == password:
        print(f"\n{green}{bold} \t Login successful. Welcome back {username}.{end}")
        break

    print(f"{red}{bold} \t I'm sorry, the password is incorrect. Please try again.{end}\n")
    continue

# The main menu with extra options displayed if the user is "admin".
while True:
    dividing_line()
    print(f"\n                  {underline}{bold}Main Menu{end}\n")

    if username == "admin":
        print(f"             gr  - {yellow}Generate Report{end}"
              f"\n             st  - {yellow}Statistics{end}")

    print(f"             r   - {yellow}Register New User{end}"
          f"\n             a   - {yellow}Assign A Task{end}"
          f"\n             va  - {yellow}View All Tasks{end}"
          f"\n             vm  - {yellow}View My Tasks{end}"
          f"\n             e   - {yellow}Exit{end}\n")
    dividing_line()
    menu = input(": ").lower()

    # The "register_user" function is called if "r" is entered.
    if menu == 'r':
        register_user()

    # The "assign_task" function is called if "a" is entered.
    elif menu == 'a':
        assign_task()

    # Display all tasks for each user and prints it in a clean, readable display.
    elif menu == 'va':
        view_all_tasks()

    # Displays tasks specific to the user.
    elif menu == 'vm':
        view_mine()

    # Menu selection enabling access to generating reports for the "admin".
    elif menu == "gr" and username == "admin":
        generate_reports()

    # Special menu selection for "admin" where they can view the total number of users and tasks on the system.
    elif menu == "st" and username == "admin":
        statistics()

    # Exits the system.
    elif menu == 'e':
        print(f'\n{pink}{bold} \t Thank you for using the program. All of your data has been saved.{end}')
        exit()

    else:
        print(f"\n{red}{bold} \t That is an incorrect menu option, please choose again.{end}")
