# Задание 7. REST. FastAPI. Swagger

В ходе работы был создан сервер, предоставляющий пользователю REST API для взаимодействия со списком терминов моей выпускной квалификационной работы. 
В качестве хранилища терминов использется sqlite , Для валидации входных данных используется pydantic. 

Полученный сервис обеспечивает следующие возможности:
+ Получение списка всех терминов.
+ Получение информации о конкретном термине по ключевому слову.
+ Добавление нового термина с описанием.
+ Обновление существующего термина.
+ Удаление термина из глоссария.

С полным перечнем API можно ознакомиться перейдя по адресу docs в развернутом приложении
![image](https://github.com/user-attachments/assets/495713a9-3c5f-4d71-adb8-458119bece56)

Использумая схема для валидации данных
![image](https://github.com/user-attachments/assets/6708739c-7e18-42b0-8879-56cf6d0a83b2)


Для развертывания необходимо склонировать репозиторий командой 
```
git clone https://github.com/murzin66/pyweb_task_7.git
```

Далее необходимо перейти в директорию с Dockerfile и собрать образ командой 
```
docker build .
```
![image](https://github.com/user-attachments/assets/515a42e5-ee75-46c7-9576-24e2877b1b1f)

После того, как выполнена сборка образа, необходимо запустить контейнер с помощью команды
```
docker compose up
```
![image](https://github.com/user-attachments/assets/2c14f9c6-889b-4057-afa6-2b1208055b48)

После выполнения команды полученное приложение развернуто на порту 8000, можем проверить его работоспособность:

+ При переходе по маршруту /terms получаем полный список терминов

![image](https://github.com/user-attachments/assets/3c7599c3-ca28-4b59-a082-7865f794a3ff)

+ Получение информации о конкретном термине по ключевому слову (в данном случае ключём является id)
![image](https://github.com/user-attachments/assets/e2bea921-2b58-4819-8689-fe69800b5513)

+ Добавление нового термина с описанием
![image](https://github.com/user-attachments/assets/ba18d250-75ae-4c36-bb2a-592ee48a9a4f)

![image](https://github.com/user-attachments/assets/4edba429-e26e-45cc-b702-bab64b2092b5)

+ Модификация термина
![image](https://github.com/user-attachments/assets/c22075a9-dc00-4e50-a721-eaa4cd2691a4)

![image](https://github.com/user-attachments/assets/70ee812b-81ec-4059-81bf-92fba64558ad)

+ Удаление термина из глоссария

![image](https://github.com/user-attachments/assets/030ee92d-1e1b-42e1-ad88-05e064c4f491)

После удаления термина как и ожидалось удалился термин с id = 17
![image](https://github.com/user-attachments/assets/379519b3-27ca-40cd-b61c-2a0a594f165f)

Таким образом, было развернуто веб-приложение, предоставляющее API для взаимодействия с глоссарием терминов, функциональность API была успешно протестирована



