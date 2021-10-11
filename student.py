from peewee import CharField, DateField, ForeignKeyField, IntegerField

from group import Group
from datetime import datetime
from base import BaseModel


class Student(BaseModel):
    full_name = CharField(verbose_name='ФИО')
    date_of_birth = DateField(verbose_name='Дата рождения')
    group_id = ForeignKeyField(Group, verbose_name='Группа', backref='student_ids')
    course = IntegerField(verbose_name='курс')
    speciality = CharField(verbose_name='Специальность')

    class Meta:
        db_table = 'students'

    @classmethod
    def show_menu(cls):
        while True:
            print('---------------------------------------------ИНФОРМАЦИЯ О СТУДЕНТАХ---------------------------------------------')
            number = cls.base_menu()
            if number == '0':
                return
            elif number == '1':
                cls.add()
            elif number == '2':
                cls.show_all()
            elif number == '3':
                cls.show_menu_for_editing_and_viewing()
            else:
                print('Введите правильное число!')

    @classmethod
    def show_menu_for_editing_and_viewing(cls):
        try:
            student_full_name = input('Введите ФИО студента: ')
            student_id = cls.get(cls.full_name == student_full_name)
            student_id.print_info()
            cls.print_line()
            while True:
                number = input('\t\tВведите 0 для выхода в предыдущее меню\n'
                               '\t\tВведите 1 для удаления студента\n'
                               '\t\tВведите 2 для редактирования данных студента\n')
                if number == '0':
                    return
                if number == '1':
                    student_id.delete_record()
                    return
                elif number == '2':
                    student_id.edit()
                else:
                    print('Введите правильное число!')
        except Exception as e:
            print(f'Упс, что-то пошло не так... Возможно вы ввели несуществующее имя, ошибка - {e.__context__}')
            return

    @classmethod
    def add(cls):
        try:
            cls.print_line()
            group_name = input('Введите номер группы для студента: ')
            group_id = Group.get(Group.name == group_name)
            input_date = input('Введите дату рождения (день.месяц.год): ')
            date = datetime.strptime(input_date, "%d.%m.%Y")
            cls.create(
                full_name=input('Введите ФИО: '),
                date_of_birth=date,
                group_id=group_id,
                course=input('Введите курс: '),
                speciality=input('Введите специальность: ')
            )
            print('Студент добавлен!')
        except Exception as e:
            print(f'Упс, что-то пошло не так, ошибка - {e.__context__}')

    def edit(self):
        while True:
            try:
                self.print_line()
                self.print_info()
                self.print_line()
                number = input(
                    '\t\tВведите 0 для выхода в предыдущее меню\n'
                    '\t\tВведите 1 чтобы изменить ФИО\n'
                    '\t\tВведите 2 чтобы изменить дату рождения\n'
                    '\t\tВведите 3 чтобы изменить группу студента\n'
                    '\t\tВведите 4 чтобы изменить курс студента\n'
                    '\t\tВведите 5 чтобы изменить специальность студента\n'
                )
                if number == '0':
                    self.print_line()
                    return
                elif number == '1':
                    self.full_name = input('Введите новое ФИО студента: ')
                    self.save()
                    print('ФИО изменено! \n\n')
                elif number == '2':
                    self.add_new_date_of_birth()
                elif number == '3':
                    self.add_new_group()
                elif number == '4':
                    self.course = input('Введите новый курс для студента: ')
                    self.save()
                    print('Курс изменён! \n\n')
                elif number == '5':
                    self.speciality = input('Введите новую специальность: ')
                    self.save()
                    print('Специальность изменена! \n\n')
                else:
                    print('Введите правильное число! \n\n')
            except Exception as e:
                print(f'Упс, что-то пошло не так, ошибка - {e.__context__}')

    def print_info(self):
        print(
            f'| ФИО - {self.full_name} | Дата рождения - {self.date_of_birth} | Группа - {self.group_id.name} |'
            f' Курс - {self.course} | Специальность - {self.speciality} |'
        )

    def add_new_group(self):
        new_group = input('Введите новую группу для студента: ')
        new_group_id = Group.get(Group.name == new_group)
        self.group_id = new_group_id
        self.save()
        print('Группа изменена! \n\n')

    def add_new_date_of_birth(self):
        input_date = input('Введите дату рождения (день.месяц.год): ')
        date = datetime.strptime(input_date, "%d.%m.%Y")
        self.date_of_birth = date
        self.save()
        print('Дата рождения изменена! \n\n')

    def delete_record(self):
        self.delete_instance()
        print('Студент удалён!')