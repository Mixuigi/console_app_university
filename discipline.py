from peewee import CharField

from base import BaseModel


class Discipline(BaseModel):
    name = CharField(verbose_name='Название дисциплины')

    class Meta:
        db_table = 'disciplines'

    @classmethod
    def show_menu(cls):
        while True:
            print('--------------------------------------------ИНФОРМАЦИЯ О ДИСЦИПЛИНАХ--------------------------------------------')
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
            discipline_name = input('Введите дисциплину для дальнейшей работы с ней: ')
            discipline_id = cls.get(cls.name == discipline_name)
            discipline_id.print_info()
            cls.print_line()
            while True:
                number = input('\t\tВведите 0 для выхода в главное меню\n'
                               '\t\tВведите 1 для удаления дисциплины\n'
                               '\t\tВведите 2 для редактирования полей дисциплины\n')
                if number == '0':
                    return
                elif number == '1':
                    is_delete = discipline_id.delete_record()
                    if is_delete:
                        return
                elif number == '2':
                    cls.edit(discipline_id)
                else:
                    print('Введите правильное число! ')
        except Exception as e:
            print(f'Упс, что-то пошло не так, ошибка - {e.__context__}')
            return

    @classmethod
    def add(cls):
        try:
            cls.create(name=input('Введите название дисциплины '))
            print('Новая дисциплина успешно создана!')
        except Exception as e:
            print(f'Такая дисциплина уже есть, ошибка - {e.__context__}')

    def delete_record(self):
        if self.lesson_ids.count() > 0:
            number = input('Эту дисциплину ещё ведут преподаватели, '
                           'вы действительно хотите её удалить? \n1 - да, удалить дисциплину '
                           '\nили введите что угодно чтобы отменить операцию: ')
            self.print_line()
            if number != 1:
                return False
        self.delete_instance()
        print('Дисциплина удалена')
        self.print_line()
        return True

    def edit(self):
        self.print_line()
        self.print_info()
        self.print_line()
        try:
            self.name = input('Новое название дисциплины: ')
            self.save()
            self.print_line()
        except Exception as e:
            print('Такой дисциплины не существует!, ошибка- ', e.__context__)

    def print_info(self):
        print(f'| Название дисциплины - {self.name} |')
