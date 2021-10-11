from peewee import CharField

from base import BaseModel


class Group(BaseModel):
    name = CharField(unique=True, verbose_name='Название группы')

    class Meta:
        db_table = 'groups'

    @classmethod
    def show_menu(cls):
        while True:
            print('----------------------------------------------ИНФОРМАЦИЯ О ГРУППАХ----------------------------------------------')
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
            group_name = input('Введите группу для дальнейшей работы с ней: ')
            group_id = cls.get(cls.name == group_name)
            group_id.print_info()
            cls.print_line()
            while True:
                number = input('\t\tВведите 0 для выхода в главное меню\n'
                               '\t\tВведите 1 для показа всех студентов в этой группе\n'
                               '\t\tВведите 2 для удаления группы\n'
                               '\t\tВведите 3 для редактирования полей группы\n')
                if number == '0':
                    return
                elif number == '1':
                    group_id.show_students()
                elif number == '2':
                    is_delete = group_id.delete_record()
                    if is_delete:
                        return
                elif number == '3':
                    group_id.edit()
                else:
                    print('Введите правильное число! ')
        except Exception as e:
            print(f'Упс, что-то пошло не так, ошибка - {e.__context__}')

    @classmethod
    def add(cls):
        try:
            cls.create(name=input('Введите название группы: '))
            print(
                'Новая группа успешно создана!')
        except Exception as e:
            print(f'Такая группа уже есть {e.__context__}')

    def delete_record(self):
        try:
            if self.student_ids.count() == 0:
                self.delete_instance()
                print('Группа удалена')
                self.print_line()
                return True
            else:
                print('Невозможно удалить группу, т.к в ней есть студенты ')
                self.print_line()
                return False
        except Exception as e:
            print('Произошла ошибка поиска', e.__context__)

    def edit(self):
        try:
            self.print_line()
            self.print_info()
            self.print_line()
            self.name = input('Новое название группы: ')
            self.save()
            print('Название группы изменено.')
            self.print_line()
        except Exception as e:
            print('Такой группы не существует!, ошибка -', e.__context__)

    def print_info(self):
        print(f'| Название группы - {self.name} |')

    def show_students(self):
        print(f'Студентов в группе:  {self.lesson_ids.count()}')
        self.print_line()
        for student in self.student_ids:
            print(student.full_name)
            self.print_line()
