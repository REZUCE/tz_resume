### Исправить + инфаструктура
- [] Исправить вложенность pydantic схемы и добавить json_schema_extra example pydantic v2. Пример:
![image](https://github.com/user-attachments/assets/b4cad465-9f9f-413e-ac85-194e45a47d66)
- [] Query, Path, Body параметры и написать к ним description/title?
![image](https://github.com/user-attachments/assets/f01cc67d-dd86-4a0f-9420-e616b58046f3)
- [] Сделать норм main.py с конструкцией if __name__ == __main__ для удобства, также можно еще из pydantic-settings брать опеределнный ENVIRONMENT. Пример:
![image](https://github.com/user-attachments/assets/c2b35734-42d5-42ae-b05c-477358bf5c40)
Также можно закрыть docs, при определенном ENVIRONMENT:
![image](https://github.com/user-attachments/assets/0ecc4a1f-d8c5-4d8b-99d4-e67d8e6c1f84)
- [] Проверить status_code и response_model(схема pydantic).
- [] Добавит Makefile (вкусовщина)
- [] Добавить стандартный линтер и форматер
