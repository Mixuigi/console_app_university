from peewee import CharField, ForeignKeyField

from group import Group
from discipline import Discipline
from teacher import Teacher
from base import BaseModel


class Lesson(BaseModel):
    name = CharField(unique=True, verbose_name='Уникальное название занятия')
    group = ForeignKeyField(Group, verbose_name='Группа', backref='lesson_ids')
    discipline = ForeignKeyField(Discipline, verbose_name='Дисциплина', backref='lesson_ids')
    teacher = ForeignKeyField(Teacher, verbose_name='Преподаватель', backref='lesson_ids')

    class Meta:
        db_table = 'lessons'

    @classmethod
    def show_menu(cls):
        while True:
            print('----------------------------------------------ИНФОРМАЦИЯ О ЗАНЯТИЯХ---------------------------------------------')
            number = input(
                '\t\tВведите 0 для выхода в главное меню\n'
                '\t\tВведите 1 для добавления занятия\n'
                '\t\tВведите 2 для удаления занятия\n'
                '\t\tВведите 3 для просмотра всех занятий\n'
            )
            if number == '0':
                return
            elif number == '1':
                cls.add()
            elif number == '2':
                cls.delete_lesson()
            elif number == '3':
                cls.show_all()
            else:
                print('Введите правильное число!')

    @classmethod
    def add(cls):
        try:
            cls.create(
                name=input('Введите введите уникальное название урока: '),
                group=Group.get(Group.name == input('Введите группу: ')),
                discipline=Discipline.get(Discipline.name == input('Введите дисциплину: ')),
                teacher=Teacher.get(Teacher.full_name == input('Введите ФИО преподавателя: '))
            )
            print('Новое занятие добавлено!!')
        except Exception as e:
            print('Упс, что-то пошло не так, возможно вы ввели некорректные данные, ошибка - ', e.__context__)

    @classmethod
    def delete_lesson(cls):
        try:
            lesson_id = cls.get(cls.name == input('Введите уникальное название занятия для его удаления: '))
            lesson_id.delete_instance()
            print('Занятие удалено! ')
        except Exception as e:
            print(f'Произошла ошибка поиска, ошибка - {e.__context__}')

    def print_info(self):
        print(f'|Уникальное название - {self.name}|Группа - {self.group.name}|Дисциплина - {self.discipline.name}|'
              f'Преподаватель - {self.teacher.full_name}|')

