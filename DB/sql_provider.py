import os
from string import Template   # Чтобы использовать символ $ как переменную


class SQL_Provider:
    def __init__(self, file_path: str) -> None:
        self._scripts = {}   # Контейнер

        for file in os.listdir(file_path):
            self._scripts[file] = Template(open(f'{file_path}/{file}', 'r').read())

    def get(self, _name: str, **kwargs):
        return self._scripts[_name].substitute(**kwargs)

