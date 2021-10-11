import sqlite3

from peewee import SqliteDatabase

from group import Group
from discipline import Discipline
from teacher import Teacher
from student import Student
from lesson import Lesson
from base import BaseModel

database = sqlite3.connect('University.db', check_same_thread=False)  # create db

db = SqliteDatabase('University.db')

with db:
    db.create_tables([Teacher, Discipline, Student, Group, Lesson])


def menu():
    print('\n\n\n\n-------------------------------Система учёта Студентов и Преподавателей-------------------------------\n')
    while True:
        try:
            BaseModel.console_clear()
            number = int(input(
                '\t\tВведите 1 для получения информации о студентах: \n'
                '\t\tВведите 2 для получения информации о группах: \n'
                '\t\tВведите 3 для получения информации о преподавателях: \n'
                '\t\tВведите 4 для получения информации о дисциплинах: \n'
                '\t\tВведите 5 для получения информации о занятиях: \n'
                '\t\tВведите 0 для выхода\n'
            ))
            menus = [
                exit,
                Student.show_menu,
                Group.show_menu,
                Teacher.show_menu,
                Discipline.show_menu,
                Lesson.show_menu,
            ]
            if number in range(len(menus)):
                menus[number]()
            else:
                print('Введите правильное число!')
        except Exception as e:
            print('Упс, что-то пошло не так', e.__context__)


if __name__ == "__main__":
    menu()
