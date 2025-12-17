# База данных. Контроль доступа

Светосила v1.0. Спецификации на разработку

**Последнее изменение:** 13.12.2025, 19:20 МСК

## 1. Назначение документа

Описать структуру базы данных системы контроля доступа.

## 2. Термины и определения

## 3. Основные положения

3.1. Всё, что не разрешено, запрещено.

## 4. Таблицы

### 4.1. AC_USERS

Пользователи.

- ID (INTEGER / PK)
- LOGIN (TEXT) - логин
- PASSWORD (TEXT) - пароль
- LAST_NAME (TEXT) - фамилия
- FIRST_NAME (TEXT) - имя
- MIDDLE_NAME (TEXT) - отчество
- ROLE_ID (INTEGER / FK) - роль пользователя

### 4.2. AC_ROLES

Роли.

- ID (INTEGER / PK)
- NAME (TEXT) - наименование роли

### 4.3. AC_PERMISSIONS

Права.

- ID (INTEGER / PK)
- NAME (TEXT) - наименование права
- CAN_CREATE (BOOLEAN) - разрешение на создание
- CAN_READ (BOOLEAN) - разрешение на чтение
- CAN_UPDATE (BOOLEAN) - разрешение на редактирование
- CAN_DELETE (BOOLEAN) - разрешение на удаление

### 4.4. AC_ROLE_PERMISSIONS

Связь ролей с правами. У роли может быть несколько прав.

- ID (INTEGER / PK)
- ROLE_ID (INTEGER / FK) - роль
- PERMISSION_ID (INTEGER / FK) - право

### 4.5. AC_ROLE_ROLES

Иерархия ролей. Роль может включать другие роли.

- ID (INTEGER / PK)
- PARENT_ROLE_ID (INTEGER / FK) - родительская роль
- CHILD_ROLE_ID (INTEGER / FK) - дочерняя роль (входит в родительскую)

### 4.6. AC_TABLES

Таблицы, к которым применяются права.

- ID (INTEGER / PK)
- NAME (TEXT) - наименование таблицы
- AC_PERMISSION_ID (INTEGER / FK) - право доступа к таблице

### 4.7. AC_FIELDS

Поля таблиц.

- ID (INTEGER / PK)
- NAME (TEXT) - наименование поля
- AC_TABLE_ID (INTEGER / FK) - таблица, к которой относится поле


## 5. Вопросы

## 6. Идеи
