### Задача:
Участникам хакатона при помощи методов искусственного интеллекта и данных, включающих полные адреса домов и зданий г. Санкт-Петербурга, предстоит построить модель, которая сможет адаптироваться к задачам определения корректного адреса, содержащегося в исходной базе данных.

### Предлагаемое решение:

![](Scheme.png)

### Запуск проекта:
1. В папке ***hacks_ai*** необходимо создать среду через команду: ***python3 -m venv myenv***
2. Переход в окружение: ***source myenv/bin/activate***
2. Необходимо установить зависимости для работы с Django и React:
   1. **Django**: ***pip install -r requirements.txt***
   2. **React**: ***npm install*** (если не сработает, то ***npm install --force***)
4. Проект работает на двух серверах. Для удобства работы подготовлен makefile, поэтому для запуска проекта рекомендуется
открыть два терминала и написать следующие команды: 
   1. ***make run-react***
   2. ***make run-django***