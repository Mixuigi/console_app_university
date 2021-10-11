from peewee import PrimaryKeyField, SqliteDatabase, Model

import os

db = SqliteDatabase('University.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True, verbose_name='Уникальный идентефикатор')

    class Meta:
        database = db
        order_by = 'id'

    @classmethod
    def base_menu(cls):
        number = input(
            '\t\tВведите 0 для выхода в главное меню\n'
            '\t\tВведите 1 чтобы добавить\n'
            '\t\tВведите 2 чтобы посмотреть все\n'
            '\t\tВведите 3 для удаления/редактирования/особой фильтрации данных\n'
        )
        return number

    @classmethod
    def console_clear(cls):
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def print_line(cls):
        print('----------------------------------------------------------------------------------------------------------------')

    @classmethod
    def show_all(cls):
        print(f'Всего {cls.select().count()}')
        for record in cls.select():
            cls.print_line()
            record.print_info()
        cls.print_line()
