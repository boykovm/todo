from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return str(self.task) + ':' + str(self.deadline)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
global session, is_exit
session = Session()

is_exit = False


def today_tasks():
    print('Today ' + str(datetime.today().day) + ' ' + str(datetime.today().strftime('%b')) + ':')
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    c = 1
    empty = True
    for task in rows:
        empty = False
        print(str(c) + ') ' + str(task)[:str(task).index(':')])
        c += 1
    if empty:
        print('Nothing to do!')
    print()
    starting_menu()


def tasks_for_week():
    # print('Today ' + str(datetime.today().day) + ' ' + str(datetime.today().strftime('%b')) + ':')
    for i in range(7):
        print()
        rows = session.query(Table).filter(Table.deadline == (datetime.today() + timedelta(days=i)).date()).all()
        print((datetime.today() + timedelta(days=i)).strftime('%A %d %b:'))
        c = 1
        empty = True
        for task in rows:
            empty = False
            print(str(c) + ') ' + str(task)[:str(task).index(':')])
            c += 1
        if empty:
            print('Nothing to do!')
    print()
    starting_menu()


def all_tasks():
    print('\nAll tasks:')
    c = 1
    tasks = session.query(Table).order_by(Table.deadline).all()
    for task in tasks:
        task_name = str(task)[:str(task).index(":")]
        task_deadline = str(task)[str(task).index(":")+1:]
        year = int(task_deadline[:4])
        month = int(task_deadline[5:7])
        day = int(task_deadline[8:10])
        # task_deadline = datetime(year=year, month=month, day=day)
        # task_deadline = task_deadline.strftime('%d %b')
        if str(day)[-1] == 0:
            day = day[-2]
        if str(month)[-1] == 0:
            month = month[-2]
        monthes = ('Jan',
                   'Feb',
                   'Mar',
                   'Apr',
                   'May',
                   'Jun',
                   'Jul',
                   'Aug',
                   'Sep',
                   'Oct',
                   'Nov',
                   'Dec')
        month = monthes[month-1]
        print(str(c) + '. ' + str(task_name) + '. ' + str(day) + ' ' + str(month))
        c += 1
    print()
    starting_menu()


def missed_tasks():
    print('\nMissed tasks:')
    empty = True
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    c = 1
    for task in rows:
        empty = False
        task_name = str(task)[:str(task).index(":")]
        task_deadline = str(task)[str(task).index(":") + 1:]
        year = int(task_deadline[:4])
        month = int(task_deadline[5:7])
        day = int(task_deadline[8:10])
        # task_deadline = datetime(year=year, month=month, day=day)
        # task_deadline = task_deadline.strftime('%d %b')
        if str(day)[-1] == 0:
            day = day[-2]
        if str(month)[-1] == 0:
            month = month[-2]
        monthes = ('Jan',
                   'Feb',
                   'Mar',
                   'Apr',
                   'May',
                   'Jun',
                   'Jul',
                   'Aug',
                   'Sep',
                   'Oct',
                   'Nov',
                   'Dec')
        month = monthes[month - 1]
        print(str(c) + '. ' + str(task_name) + '. ' + str(day) + ' ' + str(month))
        c += 1
    if empty:
        print('Nothing is missed!')
    print()
    starting_menu()


def add_task():
    print('\nEnter task')
    task = input()
    print('Enter deadline')
    deadline = input()
    deadline = datetime.strptime(deadline,"%Y-%m-%d")
    new_row = Table(
        task = task,
        deadline = deadline
    )
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')
    starting_menu()


def delete_task():
    print('\nChoose the number of the task you want to delete:')
    tasks = session.query(Table).order_by(Table.deadline).all()
    c = 1
    for task in tasks:
        task_name = str(task)[:str(task).index(":")]
        task_deadline = str(task)[str(task).index(":") + 1:]
        year = int(task_deadline[:4])
        month = int(task_deadline[5:7])
        day = int(task_deadline[8:10])
        # task_deadline = datetime(year=year, month=month, day=day)
        # task_deadline = task_deadline.strftime('%d %b')
        if str(day)[-1] == 0:
            day = day[-2]
        if str(month)[-1] == 0:
            month = month[-2]
        monthes = ('Jan',
                   'Feb',
                   'Mar',
                   'Apr',
                   'May',
                   'Jun',
                   'Jul',
                   'Aug',
                   'Sep',
                   'Oct',
                   'Nov',
                   'Dec')
        month = monthes[month - 1]
        print(str(c) + '. ' + str(task_name) + '. ' + str(day) + ' ' + str(month))
        c += 1
    c = int(input())
    special_row = tasks[c-1]
    session.delete(special_row)
    session.commit()
    print('The task has been deleted!\n')
    starting_menu()



def go_exit():
    global is_exit
    is_exit = True
    print('\nBye!')


def menu_choice():
    choice = int(input())

    if choice == 1:
        today_tasks()
    elif choice == 2:
        tasks_for_week()
    elif choice == 3:
        all_tasks()
    elif choice == 4:
        missed_tasks()
    elif choice == 5:
        add_task()
    elif choice == 6:
        delete_task()
    elif choice == 0:
        go_exit()


def starting_menu():
    print('1) Today\'s tasks')
    print('2) Week\'s tasks')
    print('3) All tasks')
    print('4) Missed tasks')
    print('5) Add task')
    print('6) Delete task')
    print('0) Exit')

    menu_choice()

if is_exit == False:
    starting_menu()