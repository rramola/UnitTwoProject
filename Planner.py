import calendar
import os
from dataclasses import dataclass
from datetime import datetime
import colorama
from colorama import Fore, Back, Style


################# Ryan's Code ##############################
# - Bills
@dataclass
class Bill:
    name: str
    amount: float
    date: str
    paid: str


def bills():
    bill_file = "Bills.txt"
    with open(f"{bill_file}", "a") as fp:
        pass

    while True:
        print(Back.MAGENTA + "\n----- Bills Menu -----" + Back.RESET)
        print("Options:")
        print("1. Create")
        print("2. View")
        print("3. Search")
        print("4. Pay")
        print("5. Delete")
        print("6. Main Menu")
        bill_command = input("\nEnter your choice (1/2/3/4/5/6): \n\n>")
        if bill_command == "1":
            create_bill(bill_file)
        elif bill_command == "2":
            view_bills(bill_file)
        elif bill_command == "3":
            while True:
                print(Back.MAGENTA + "\n----- Search Menu -----" + Back.RESET)
                print("Options:")
                print("1. Name")
                print("2. Amount")
                print("3. Status")
                print("4. Bill menu")
                search_command = input("\nEnter your choice (1/2/3/4): \n\n>")
                if search_command == "1":
                    search_bill_name(bill_file)
                elif search_command == "2":
                    search_bill_amount(bill_file)
                elif search_command == "3":
                    search_bill_status(bill_file)
                elif search_command == "4":
                    break
                else:
                    print("\nInvalid choice. Please enter (1/2/3/4):\n\n")
        elif bill_command == "4":
            pay_bill(bill_file)
        elif bill_command == "5":
            delete_bill(bill_file)
        elif bill_command == "6":
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, 4, 5, or 6.\n\n")


def bill_date_validation():
    running = True
    while running:
        date = input("\nWhat day is this bill due?\n\n> ").title()
        try:
            datetime.strptime(date, "%d")
            return date
        except ValueError:
            print(Back.RED + "\nInvalid day!" + Back.RESET + "\n\n")


def print_function(bill_file):
    bill_list = []
    with open(f"{bill_file}", "r") as bill_file:
        bills = bill_file.read().splitlines()
        for bill in bills:
            bill_items = bill.split()
            bill_class = Bill(
                bill_items[0], float(bill_items[1]), bill_items[2], bill_items[3]
            )
            bill_list.append(bill_class)
    for item in bill_list:
        if item.paid == "False":
            item.paid = "Not Paid"
        else:
            item.paid = "Paid"
    return bill_list


def suffix(date):
    suffix = ""
    day = int(date)
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    day = str(str(day) + suffix)
    return day


def create_bill(bill_file):
    bills = print_function(bill_file)
    while True:
        account = input(
            "\nWhat is the name of the account for this bill?\n\n> "
        ).title()
        for bill in bills:
            if bill.name == account:
                print("\nBill already saved!\n\n")
                return
        check = account.isdigit()
        while True:
            if check == True:
                print("\nInvalid name!\n\n")
                break
            if account == "":
                print("\nInvalid name!\n\n")
                break

            account = account.split()
            while True:
                try:
                    amount_due = float(input("How much is this bill?\n\n> "))
                    break
                except ValueError:
                    print(Back.RED + "\nInvalid number!" + Back.RESET + "\n\n")
            due_date = bill_date_validation()
            date = suffix(due_date)
            bill = Bill("".join(account), amount_due, (date), "False")
            with open(f"{bill_file}", "a") as bill_file:
                bill_file.write(
                    f"{bill.name} {str(bill.amount)} {bill.date} {bill.paid}\n"
                )
                print("\nBill saved successfully!\n\n")
            return


def view_bills(bill_file):
    bills = print_function(bill_file)
    print(Back.MAGENTA + "\n----- Bills List-----" + Back.RESET)
    for item in bills:
        item.name = "".join(
            " " + char if char.isupper() else char.strip() for char in item.name
        ).strip()
        print(
            f"\n-- Account: {item.name}\n-- Amount Due: ${item.amount}\n-- Due Date: {item.date}\n-- Status: {item.paid}"
        )


def search_bill_name(bill_file):
    found_name = []
    bills = print_function(bill_file)
    while True:
        search = input(
            "\nPlease enter the name of the account you want to search for:\n\n>"
        ).title()
        check = search.isdigit()
        if check == True:
            print("\nInvalid name!\n\n")
        elif search == "":
            print("\nInvalid name!\n\n")
        else:
            for item in bills:
                item.name = "".join(
                    " " + char if char.isupper() else char.strip() for char in item.name
                ).strip()
                if item.name == search:
                    found_name.append(item)
            if found_name == []:
                print("\nNo bills found for this name.\n\n")
                break
            else:
                print("\n----- Account Found-----")
                for item in found_name:
                    print(
                        f"-- Account: {item.name}\n-- Amount Due: ${item.amount}\n-- Due Date: {item.date}\n-- Status: {item.paid}"
                    )
                return


def search_bill_amount(bill_file):
    found_amount = []
    bills = print_function(bill_file)
    while True:
        try:
            search = float(input("\nEnter the amount you are searching for:\n\n> "))
            for item in bills:
                if item.amount <= search:
                    found_amount.append(item)
        except ValueError:
            print("\nInvalid number!\n\n")
            search_bill_amount()
            break
        if found_amount == []:
            print("\nNo bills found for this amount.\n\n")
            break
        else:
            print(Back.MAGENTA + "-----Account(s) Found-----" + Back.RESET)
            for item in found_amount:
                item.name = "".join(
                    " " + char if char.isupper() else char.strip() for char in item.name
                ).strip()
                print(
                    f"-- Account: {item.name}\n-- Amount Due: ${item.amount}\n-- Due Date: {item.date}\n-- status: {item.paid}\n\n"
                )
            return


def search_bill_status(bill_file):
    found = False
    complete = False
    bills = print_function(bill_file)
    while not complete:
        print(Back.MAGENTA + "\n----- Search Status Menu -----" + Back.RESET)
        print("Options:")
        print("1. Paid")
        print("2. Unpaid")
        bill_status_command = input("\nEnter your choice (1/2):\n\n>").title()
        if bill_status_command == "1":
            for item in bills:
                item.name = "".join(
                    " " + char if char.isupper() else char.strip() for char in item.name
                ).strip()
                if item.paid == "Paid":
                    print(
                        f"\n-- Account: {item.name}\n-- Amount Due: ${item.amount}\n-- Due Date: {item.date}\n-- Status: {item.paid}"
                    )
                found = True
                complete = True
        elif bill_status_command == "2":
            for item in bills:
                item.name = "".join(
                    " " + char if char.isupper() else char.strip() for char in item.name
                ).strip()
                if item.paid == "Not Paid":
                    print(
                        f"\n-- Account: {item.name}\n-- Amount Due: ${item.amount}\n-- Due Date: {item.date}\n-- Status: {item.paid}"
                    )
                found = True
                complete = True
        else:
            complete = True


def pay_bill(bill_file):
    paid = False
    bills_list = []
    while True:
        command = input(
            "\nEnter the name of the account you would like to pay:\n\n>"
        ).title()
        check = command.isdigit()
        if check == True:
            print("\nInvalid name!\n\n")
        elif command == "":
            print("\nInvalid name!\n\n")
        else:
            command = command.split()
            command = "".join(
                " " + char if char.isupper() else char.strip() for char in command
            ).strip()
            with open(f"{bill_file}", "r") as file:
                bills = file.read().splitlines()
                for bill in bills:
                    bill_items = bill.split()
                    bill_class = Bill(
                        bill_items[0],
                        float(bill_items[1]),
                        bill_items[2],
                        bill_items[3],
                    )
                    bills_list.append(bill_class)
            for bill in bills_list:
                if bill.name == command:
                    if bill.paid == "False":
                        bill.paid = "True"
                        paid = True
                    else:
                        print("\nBill already paid!\n\n")
                        return
                with open(f"{bill_file}", "w") as file:
                    for bill in bills_list:
                        file.write(
                            f"{bill.name} {str(bill.amount)} {bill.date} {bill.paid}\n"
                        )
            if paid:
                print("\nBill paid successfully!\n\n")
                break
            else:
                print(f"\nNo bill found for {command}!\n\n")
                break


def delete_bill(bill_file):
    command = ""
    deleted = False
    bills_list = []
    while True:
        command = input(
            "\nEnter the name of the account you would like to remove:\n>"
        ).title()
        check = command.isdigit()
        if check == True:
            print("\nInvalid name!\n\n")
        elif command == "":
            print("\nInvalid name!\n\n")
        else:
            command = command.split()
            command = "".join(
                " " + char if char.isupper() else char.strip() for char in command
            ).strip()
            with open(f"{bill_file}", "r") as file:
                bills = file.read().splitlines()
                for bill in bills:
                    bill_items = bill.split()
                    bill_class = Bill(
                        bill_items[0],
                        float(bill_items[1]),
                        bill_items[2],
                        bill_items[3],
                    )
                    bills_list.append(bill_class)
            for bill in bills_list:
                if bill.name == command:
                    bills_list.remove(bill)
                    deleted = True
                with open(f"{bill_file}", "w") as file:
                    for bill in bills_list:
                        file.write(
                            f"{bill.name} {str(bill.amount)} {bill.date} {bill.paid}\n"
                        )
            if deleted:
                print("\nBill deleted!\n\n")
                break
            else:
                print(f"\nNo bills found for {command}!\n\n")
                break


# - TO DO LIST


@dataclass
class TodoItem:
    task: str
    completed: bool


def save_todo_list(todo_list, to_do_file):
    with open(to_do_file, "w") as file:
        for item in todo_list:
            file.write(f"{item.task}|{item.completed}\n")


def load_todo_list(to_do_file):
    todo_list = []
    with open(to_do_file, "r") as file:
        for line in file:
            task, completed_str = line.strip().split("|")
            completed = completed_str.lower() == "true"
            todo_list.append(TodoItem(task=task, completed=completed))
    return todo_list


def display_todo_list(todo_list):
    if not todo_list:
        print("No tasks in the to-do list.")
    else:
        for i, item in enumerate(todo_list, 1):
            status = "Done" if item.completed else "Pending"
            print(f"{i}. {item.task} - {status}")


def add_task(todo_list, task):
    todo_list.append(TodoItem(task=task, completed=False))


def mark_task_as_done(todo_list, task_index):
    if 1 <= task_index <= len(todo_list):
        todo_list[task_index - 1].completed = True
        print(f"Task {task_index} marked as done.")
    else:
        print("Invalid task index.")


def remove_completed_tasks(todo_list):
    todo_list[:] = [item for item in todo_list if not item.completed]
    print("Completed tasks removed.")


def to_do_list():
    to_do_file = "To-Do-List.txt"
    with open(f"{to_do_file}", "a") as fp:
        pass

    todo_list = load_todo_list(to_do_file)

    while True:
        print(Fore.GREEN + "\n----- To-Do List -----" + Fore.RESET)
        print(Fore.GREEN + "Options:" + Fore.RESET)
        print(Fore.GREEN + "1. Add Task" + Fore.RESET)
        print(Fore.GREEN + "2. Mark Task as Done" + Fore.RESET)
        print(Fore.GREEN + "3. List All Tasks" + Fore.RESET)
        print(Fore.GREEN + "4. Remove Completed Tasks" + Fore.RESET)
        print(Fore.GREEN + "5. Save and Return to Main Menu" + Fore.RESET)

        choice = input(Fore.GREEN + "Enter your choice (1/2/3/4/5) " + Fore.RESET)

        if choice == "1":
            task = input("Enter the task: ")
            add_task(todo_list, task)
        elif choice == "2":
            task_index = int(input("Enter the task index to mark as done: "))
            mark_task_as_done(todo_list, task_index)
        elif choice == "3":
            print("\n----- All Tasks -----")
            display_todo_list(todo_list)
        elif choice == "4":
            remove_completed_tasks(todo_list)
        elif choice == "5":
            save_todo_list(todo_list, to_do_file)
            print("To-do list saved. Returning to Main Menu.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")


################## Kera's Code ################################
# Calender


def options_events():
    event_file = "event_file.txt"
    with open(f"{event_file}", "a") as fp:
        pass
    # year = input("What year is your event? \n > ")
    # if year.isdigit():
    #     new_year = int(year)
    #     print(Fore.CYAN + calendar.calendar(new_year) + Fore.RESET)

    # else:
    #     print("That is not even a year")
    while True:
        master_dict = load_event(event_file)
        event_options = (
            input(
                "Would you like to [create] event, [show] event, [delete] event,[return] to main menu?\n > "
            )
            .lower()
            .strip()
        )
        valid_options = ["create", "show", "delete"]
        if event_options == "return":
            break
        elif event_options in valid_options:
            if event_options == "create":
                list = input_event(master_dict)
                save_event(event_file, list)
            elif event_options == "delete":
                delete = delete_event(master_dict)
                save_event(event_file, delete)
            elif event_options == "show":
                show_events(event_file)

        else:
            print(Back.RED + "Invalid choice. Try again" + Back.RESET)


def date_validation_event():
    running = True
    while running:
        event_date = input("Date of event: ").title()
        try:
            datetime.strptime(event_date, "%B %d, %Y")
            return event_date
        except ValueError:
            print(Back.RED + "That is not even a date, Try again." + Back.RESET)


def input_event(load_dictionary):
    event = input("Name of event:  ").strip()
    print(
        """
  
  """
    )
    date = date_validation_event()
    if date in load_dictionary:
        load_dictionary[date].append(event)

    else:
        load_dictionary[date] = [event]
    return load_dictionary


def load_event(file_path):
    current_events = {}
    with open(f"{file_path}", "r") as user:
        line = user.readlines()
        for item in line:
            key, value = item.split("|")
            strip = value.strip("\n").split(",")
            current_events[key] = strip
    return current_events


def save_event(file_path, date_dic):
    with open(f"{file_path}", "w") as bill_file:
        for key, value in date_dic.items():
            myPrintString = f"{key}|"
            for index, event in enumerate(value):
                if index == 0:
                    myPrintString = myPrintString + f"{event}"
                else:
                    myPrintString = myPrintString + f",{event}"
            bill_file.write(f"{myPrintString}\n")


def delete_event(events):
    delete_event = input("Which event would you like to delete?  \n")
    for key in events:
        if delete_event in events[key]:
            events[key].remove(delete_event)

            if len(events[key]) < 1:
                del events[key]
        print(Fore.RED + "Your event has been deleted.\n" + Fore.RESET)

        break
    else:
        print(Back.RED + "Event not found" + Back.RESET)
    return events


def show_events(file_path):
    event_file = file_path
    with open(event_file, "r") as file:
        print(Back.CYAN + "----EVENTS----" + Back.RESET)
        print(file.read())


######################## MAIN #############################


def main():
    running = True
    while running:
        user_input = input(
            """ Would you like to open 
    
    1. Bills 
    2. Events 
    3. To-do List 
    4. Quit
    
    Choose 1, 2, 3 or 4: 
    
    """
        )
        if user_input == "4":
            print("Come back soon for all your planning needs!")
            running = False

        elif user_input == "1":
            # Ryan's Code
            bills()

        elif user_input == "2":
            options_events()
        # kera code

        elif user_input == "3":
            # kelvin code
            to_do_list()

        else:
            print(
                Back.RED + "Invalid input. Please chooose correct option!" + Back.RESET
            )


if __name__ == "__main__":
    main()
