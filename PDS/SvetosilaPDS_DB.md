# База данных

Светосила v1.0. Спецификации на разработку

**Последнее изменение:** 14.01.2026, 19:40 МСК

## 1. Назначение документа

Описать структуру базы данных.

## 2. Термины и определения

## 3. Основные положения

## 4. Таблицы

### 4.1. LUMINAIRES

Светильники.

- ID (INTEGER / PK)
- NAME (TEXT) - наименование светильника
- VAL_BRIGHT (INTEGER) - текущая яркость 0..255
- POWER (INTEGER) - мощность в Вт
- LUM_TYPE_ID (INTEGER / FK) - тип светильника
- POINT_ID (INTEGER / FK) - точка местонахождения
- PILLAR_ID (INTEGER / FK) - опора

### 4.2. LUM_TYPES

Типы светильников.

- ID (INTEGER / PK)
- NAME (TEXT) - наименование типа светильника

### 4.3. POINTS

Географические точки.

- ID (INTEGER / PK)
- X (REAL) - широта; как в ЯндексКартах
- Y (REAL) - долгота; как в ЯндексКартах
- Z (REAL) - высота над землей, м

### 4.4. BOARDS

Щиты управления (ШУНО).

- ID (INTEGER / PK)
- NAME (TEXT) - наименование щита
- POINT_ID (INTEGER / FK) - точка местонахождения
- IP (TEXT) - IP контроллера RAPIDA в шкафу

### 4.5. CONNECT_POINTS

Точки подключения: трансформаторные подстанции, распределительные пункты.

- ID (INTEGER / PK)
- NAME (TEXT) - наименование точки
- POINT_ID (INTEGER / FK) - точка местонахождения

### 4.6. POWER_LINES

Линии электропередачи.

- ID (INTEGER / PK)
- NAME (TEXT) - наименование линии
- LENGTH (REAL) - длина, м
- WIRE_TYPE_ID (INTEGER / FK) - тип кабеля
- LINE_RELAY_ID (INTEGER) - ID провайдера канала реле силовой линии светильников
- UNDER_VOLTAGE (BOOLEAN) - запитана ли линия

### 4.7. POWER_LINE_POINTS

Точки линии электропередачи.

- ID (INTEGER / PK)
- POWER_LINE_ID (INTEGER / FK) - линия электропередачи, к которой точка относится
- POS (INTEGER) - порядковый номер в линии
- POINT_ID (INTEGER / FK) - точка местонахождения

### 4.8. WIRE_TYPES

Типы кабелей.

- ID (INTEGER / PK)
- NAME (TEXT) - наименование типа кабеля

### 4.9. PILLARS

Опоры.

- ID (INTEGER / PK)
- NAME (TEXT) - наименование опоры
- POINT_ID (INTEGER / FK) - точка местонахождения


## 5. Вопросы

## 6. Идеи
