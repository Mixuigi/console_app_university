from peewee import CharField, DateField

from datetime import datetime
from base import BaseModel


class Teacher(BaseModel):
    full_name = CharField(verbose_name='ФИО')
    date_of_birth = DateField(verbose_name='Дата рождения')
    position = CharField(verbose_name='Должность')

    class Meta:
        db_table = 'teachers'

    @classmethod
    def show_menu(cls):
        while True:
            print('------------------------------------------ИНФОРМАЦИЯ О ПРЕПОДАВАТЕЛЯХ-------------------------------------------')
            number = cls.base_menu()
            if number == '1':
                cls.add()
            elif number == '2':
                cls.show_all()
            elif number == '3':
                cls.show_menu_for_editing_and_viewing()
            elif number == '0':
                return
            else:
                print('Введите правильное число!')

    @classmethod
    def show_menu_for_editing_and_viewing(cls):
        try:
            teacher_full_name = input('Введите ФИО преподавателя: ')
            teacher_id = cls.get(cls.full_name == teacher_full_name)
            teacher_id.print_info()
            cls.print_line()
            while True:
                number = input(
                    '\t\tВведите 0 для выхода в предыдущее меню\n'
                    '\t\tВведите 1 чтобы узнать какие предметы ведёт преподаватель\n'
                    '\t\tВведите 2 чтобы узнать в каких группах преподаёт преподаватель\n'
                    '\t\tВведите 3 для удаления преподавателя\n'
                    '\t\tВведите 4 для редактирования данных преподавателя\n'
                )
                if number == '0':
                    return
                elif number == '1':
                    teacher_id.show_discipline()
                elif number == '2':
                    teacher_id.show_groups()
                elif number == '3':
                    is_delete = teacher_id.delete_record()
                    if is_delete:
                        return
                elif number == '4':
                    teacher_id.edit()
                else:
                    print('Введите правильное число!')
        except Exception as e:
            print(f'Упс, что-то пошло не так, ошибка - {e.__context__}')

    @classmethod
    def add(cls):
        try:
            cls.create(full_name=input('Введите ФИО преподавателя: '),
                       date_of_birth=datetime.strptime(input('Введите дату рождения (день.месяц.год): '),
                                                       "%d.%m.%Y"),
                       position=input('Введите должность преподавателя: '))
            print('Новый преподаватель добавлен!')
        except Exception as e:
            print(f'Упс, что-то пошло не так, ошибка - {e.__context__}')

    def delete_record(self):
        if self.lesson_ids.count() > 0:
            number = input('Этот преподаватель ведёт несколько дисциплин, вы уверены что хотите удалить его?\n'
                           '1 - чтобы подтвердить\nИли, введите что угодно для отмены операции:\n')
            if number != '1':
                return False
        self.delete_instance()
        print('Преподаватель удалён.')
        return True

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
                    '\t\tВведите 3 чтобы изменить должность преподавателя\n'
                )
                if number == '0':
                    return
                elif number == '1':
                    self.full_name = input('Введите новое ФИО преподавателя: ')
                    self.save()
                elif number == '2':
                    date = datetime.strptime(input('Введите дату рождения (день.месяц.год): '), "%d.%m.%Y")
                    self.date_of_birth = date
                    self.save()
                elif number == '3':
                    self.position = input('Введите новую должность преподавателя: ')
                    self.save()
                else:
                    print('Введите правильное число! \n\n')
            except Exception as e:
                print(f'Упс, что-то пошло не так, ошибка - {e.__context__}')
                return

    def show_discipline(self):
        if self.lesson_ids.count() == 0:
            self.print_line()
            print('Преподаватель не ведёт никаких дисциплин ')
            self.print_line()
        else:
            for index, lesson in enumerate(self.lesson_ids):
                self.print_line()
                print(f'{index + 1}: Дисциплина - {lesson.discipline.name}')
                self.print_line()

    def show_groups(self):
        if self.lesson_ids.count() == 0:
            self.print_line()
            print('Преподаватель не преподаёт ни у одной из групп')
            self.print_line()
        else:
            for index, group_id in enumerate(self.lesson_ids):
                self.print_endline()
                print(f'{index + 1}: Группа - {group_id.group.name}')
                self.print_endline()

    def print_info(self):
        print(f'| ФИО - {self.full_name} | Дата рождения - {self.date_of_birth} | Должность - {self.position} |')
