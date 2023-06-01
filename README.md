# API for yatube project
### About project
##### Описание проекта 
Api_yamdb - собирает отзывы пользователей на произведения.
В базе проекта хранятся данные о произведениях, категориях, жанрах,
а также отзывы на произведения и комментарии пользователей. 
##### Основные возможности:
* Пользователи могут оставлять отзывы на произведения, ставить оценки, писать
комментарии.
* Администраторы могут добавлять названия новых произведений, жанры, категории.
* Администраторы могут назначать модераторов для редактирования и удаления
отзывов и комментариев пользователей.

### Авторы

- [Ильгиз Абдуллин](https://github.com/abdullinilgiz) - тимлид команды, реализовала весь механизм управления пользователями (Auth и Users): систему регистрации и аутентификации, права доступа, работу с токеном и систему подтверждения через e-mail, разработал management-команду для импорта данных из csv файлов.

- [Гия Талахадзе](https://github.com/Region070) - описал категории (Categories), жанры (Genres) и произведения (Titles): модели, представления и эндпойнты для них.

- [Ильгиз Абдуллин](https://github.com/abdullinilgiz) и [Гия Талахадзе](https://github.com/Region070) - совместно описали отзывы (Review) и комментарии (Comments): модели, представления и эндпойнты для них. А также, реализовали систему оценок и рейтинга для произведений.


### Installation
Clone this repository to your working folder:
```
git clone git@github.com:abdullinilgiz/api_final_yatube.git
```
```
cd api_final_yatube
```
Create and activate virtual environment:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Install all dependencies from requirement.txt:
```
pip install -r requirements.txt
```
Make migrations:
```
python3 manage.py migrate
```
Run the code:
```
python3 manage.py runserver
```

#### Все доступные запросы можно посмотреть по адресу:
 http://127.0.0.1/redoc/


### Примеры запросов API:
* Создание нового пользователя (на почту приходит код подтверждения):
  
  - api/v1/auth/signup/
```
    {
        "email": "string",
        "username": "string",
    }

``` 
* Получение токена для аутентификации: 

  - api/v1/auth/token/
```
    {
        "username": "string",
        "confirmation_code": "string"
    }

``` 

* Получить список всех категорий Права доступа: Доступно без токена: 

  - api/v1/categories/
  - Доступные параметры: search
```
    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "name": "string",
          "slug": "string"
        }
      ]
    }

``` 

* Получить список всех жанров. Права доступа: Доступно без токена: 

  - api/v1/genres/
  - Доступные параметры: search
 
```
    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "name": "string",
          "slug": "string"
        }
      ]
    }

``` 

* Получить список всех произведений. Права доступа: Доступно без токена: 

  - api/v1/users/me/
  - Доступные параметры: filter по полям category, genre, year, name
 
```
    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": 0,
          "name": "string",
          "year": 0,
          "rating": 0,
          "description": "string",
          "genre": [
            {
              "name": "string",
              "slug": "string"
            }
          ],
          "category": {
            "name": "string",
            "slug": "string"
          }
        }
      ]
    }

``` 
* Получить список всех отзывов. Права доступа: Доступно без токена: 

  - api/v1/titles/{title_id}/reviews/
 
```
    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": 0,
          "text": "string",
          "author": "string",
          "score": 1,
          "pub_date": "2019-08-24T14:15:22Z"
        }
      ]
    }

``` 
* Добавить новый отзыв. Пользователь может оставить только один отзыв
на произведение. Права доступа: Аутентифицированные пользователи: 

  - api/v1/titles/{title_id}/reviews/
 
```
    {
      "text": "string",
      "score": 1
    }

``` 
* Получить список всех комментариев к отзыву по id. Права доступа: Доступно без токена: 

  - api/v1/titles/{title_id}/reviews/{review_id}/comments/
 
```
    {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": 0,
          "text": "string",
          "author": "string",
          "pub_date": "2019-08-24T14:15:22Z"
        }
      ]
    }

``` 
* Получить данные своей учетной записи: 

  - api/v1/users/me/
 
```
    {
      "username": "string",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }

``` 
