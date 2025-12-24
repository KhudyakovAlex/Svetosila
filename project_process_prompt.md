# Порядок обработки репозитория Светосила

Папка с репозиторием должна обрабатываться строго в следующем порядке:
1. Обработка markdown-файлов
2. Синхронизация PROJECT с index.html
3. Обновление дат в MD-файлах
4. Загрузка репозитория на GitHub

---

## 1. Обработка markdown-файлов

### Основная обработка

Перед заливкой исправь орфографические и пунктуационные ошибки во всех markdown-файлах.
Отформатируй их. Не надо ничего переформулировать и добавлять от себя. Не надо расшифровывать аббревиатуры.
Исправь нумерацию всех пунктов и подпунктов во всех документах. Порядок этих пунктов в тексте менять не надо.
Убери лишние пробелы.
Исправь неправильное оформление номеров пунктов: должно быть 1. 1.2. 1.2.3. и т.д.

### Файлы для обработки

#### PRD (Техническое задание)
- `PRD/ТЗ_АСУНО_В21082025_1этап_коментари_Черменского_ПП_ред.docx` — техническое задание (Word)

#### PDS (Спецификация на разработку)
- `PDS/SvetosilaPDS_DB.md` — структура базы данных
- `PDS/SvetosilaPDS_DB_scheme.md` — Mermaid-схема БД
- `PDS/SvetosilaPDS_DB_AC.md` — контроль доступа
- `PDS/SvetosilaPDS_DB_AC_scheme.md` — Mermaid-схема контроля доступа

#### PROJECT (Управление проектом)
- `PROJECT/log.md` — дневник коротышек
- `PROJECT/status.md` — статусы задач
- `PROJECT/README.md` — инструкции по автоматизации

#### DESIGN (Дизайн)
- `DESIGN/Logo/` — логотипы (PNG, SVG, JPG)
- `DESIGN/Style/` — варианты стилей (JPG)

---

## 2. Синхронизация PROJECT с index.html

### Дневник коротышек (PROJECT/log.md)

**Формат записей:**
```
YYYY-MM-DD HH:MM — текст записи
```

**Пример:**
```
2025-12-18 12:00 — Надо уже окончательно определяться с тем, чью карту будем юзать.
```

**ВАЖНО**: КАЖДАЯ запись ДОЛЖНА начинаться с даты и времени.

**URL-ссылки в дневнике и статусе:**
- Все URL (http://, https://) автоматически конвертируются в ссылки
- Текст ссылки: "Жмякай сюды"
- Открываются в новой вкладке
- Сам URL не отображается на странице
- Пример: `https://example.com` → `<a href="https://example.com" target="_blank">Жмякай сюды</a>`

### Статусы (PROJECT/status.md)

**Формат:**
```markdown
# Текущий статус

## Отложено на <s>завтра</s> послезавтра

- Задача 1
- Задача 2

## Прям сейчас делаем

- Задача 3
- Задача 4

## Готовченко

- Готовая задача 1
- Готовая задача 2
```

### Автоматическое обновление

**Скрипт синхронизации:**
```bash
python PROJECT\INDEX\update_from_project.py
```

Скрипт автоматически:
- Читает `PROJECT/log.md` и обновляет раздел "Дневник коротышек" в `index.html`
- Читает `PROJECT/status.md` и обновляет статусные блоки в `index.html`

---

## 3. Обновление дат в MD-файлах

### Автоматическое обновление дат

**Скрипт:**
```bash
python PROJECT\update_dates.py
```

**Работа скрипта:**
1. Находит все изменённые MD-файлы (PDS/, PRD/), добавленные в git индекс
2. Обновляет строку "**Последнее изменение:**" на текущую дату (МСК, UTC+3)
3. Добавляет обновлённые файлы обратно в индекс

**ВАЖНО**: Запускать ПОСЛЕ `git add` и ПЕРЕД `git commit`

**Команды:**
```bash
git add .
python PROJECT\update_dates.py
```

---

## 4. Загрузка репозитория на GitHub

### Структура проекта

```
D:\Git\Svetosila\
├── .gitignore
├── project_process_prompt.md   (этот файл)
├── PRD/                         (техническое задание)
│   └── ТЗ_АСУНО_*.docx
├── PDS/                         (спецификации)
│   ├── SvetosilaPDS_DB.md
│   ├── SvetosilaPDS_DB_scheme.md
│   ├── SvetosilaPDS_DB_AC.md
│   └── SvetosilaPDS_DB_AC_scheme.md
├── DESIGN/                      (дизайн)
│   ├── Logo/
│   └── Style/
├── PROJECT/                     (управление)
│   ├── log.md
│   ├── status.md
│   ├── README.md
│   ├── update_dates.py
│   └── INDEX/                   (веб-версия)
│       ├── index.html
│       ├── update_from_project.py
│       ├── PDS/
│       │   ├── SvetosilaPDS_DB.html
│       │   └── SvetosilaPDS_DB_AC.html
│       ├── DESIGN/
│       │   ├── Logo.html
│       │   └── Style.html
│       └── assets/
│           ├── css/style.css
│           ├── js/main.js
│           └── img/
└── .git/hooks/
    └── pre-commit              (Git hook)
```

### Git Hook (автоматический)

**При каждом `git commit` автоматически:**
1. Обновляются даты в MD-файлах (`update_dates.py`)
2. Синхронизируются `log.md` и `status.md` с `index.html` (`update_from_project.py`)
3. Обновленный `index.html` добавляется в коммит

**Hook установлен в:** `.git/hooks/pre-commit`

**Пропустить hook (не рекомендуется):**
```bash
git commit --no-verify
```

### Процедура обновления при коммитах

**ОБЯЗАТЕЛЬНАЯ последовательность:**

1. **Внести изменения** в MD-файлы (PDS/, PROJECT/log.md, PROJECT/status.md)

2. **Добавить в индекс:**
   ```bash
   git add .
   ```

3. **Закоммитить** (hook сработает автоматически):
   ```bash
   git commit -m "Update documentation: [описание]"
   ```
   
   Hook автоматически:
   - Обновит даты в PDS/*.md
   - Синхронизирует PROJECT/*.md → index.html
   - Добавит index.html в коммит

4. **Отправить на GitHub:**
   ```bash
   git push origin main
   ```

### Ручной запуск (если hook не сработал)

```powershell
cd D:\Git\Svetosila
git add -A
python PROJECT\update_dates.py
python PROJECT\INDEX\update_from_project.py
git add PROJECT\INDEX\index.html
git commit -m "Update documentation"
git push origin main
```

---

## 5. Структура веб-версии (PROJECT/INDEX)

### Главная страница (index.html)

**Структура:**
- **Шапка**: логотип слева, ссылка "GitHub →" справа
- **Hero-блок**: три колонки
  - **Слева**: Дневник коротышек (из `PROJECT/log.md`)
  - **Центр**: Корабль со шкалой готовности (прогресс от 15.12.2025 до 27.02.2026)
  - **Справа**: Статусы (из `PROJECT/status.md`)
- **Разделы документов**:
  - **ТЗ**: ссылка на Word-документ
  - **Дизайн**: ссылки на Logo.html и Style.html
  - **Backend**: ссылки на PDS/SvetosilaPDS_DB.html и PDS/SvetosilaPDS_DB_AC.html

### Страницы документов

**Структура:**
- **Шапка**: логотип, ссылка на GitHub (исходный MD-файл)
- **Заголовок h1**: под шапкой, на всю ширину
- **Боковая панель**: автогенерируемое оглавление (h2, h3)
- **Контент**: основной текст с Mermaid-диаграммами

**Файлы:**
- `PDS/SvetosilaPDS_DB.html` — структура БД (с Mermaid-схемой)
- `PDS/SvetosilaPDS_DB_AC.html` — контроль доступа (с Mermaid-схемой)
- `DESIGN/Logo.html` — галерея логотипов
- `DESIGN/Style.html` — галерея стилей

### Стили (assets/css/style.css)

**Цветовая схема:**
- Основной фон: `#ffffff`
- Вторичный фон: `#f4f4f4`
- Основной текст: `#161616`
- Акцентный цвет: `#2b2b2b`
- Оранжевый акцент: `#ff860e`

**Принципы:**
- Без скруглений (`border-radius: 0 !important`)
- IBM Plex Sans (Google Fonts)
- Адаптивный дизайн (mobile-friendly)

### JavaScript (assets/js/main.js)

**Функциональность:**
- Автогенерация оглавления из h2/h3
- Подсветка активного раздела при скролле
- Плавная прокрутка к якорям

---

## Технические замечания для ИИ-ассистента

### Автоматическая обработка репозитория

**При команде "Обработать репозиторий согласно project_process_prompt.md":**

1. **Обработать MD-файлы** (форматирование, исправление ошибок)
2. **Синхронизировать PROJECT с index.html:**
   ```bash
   python PROJECT\INDEX\update_from_project.py
   ```
3. **Добавить изменения:**
   ```bash
   git add .
   ```
4. **Обновить даты:**
   ```bash
   python PROJECT\update_dates.py
   ```
5. **Закоммитить:**
   ```bash
   git commit -m "Update documentation: [описание изменений]"
   ```
6. **Отправить на GitHub:**
   ```bash
   git push origin main
   ```

**ВАЖНО:**
- Выполнять все шаги ПОСЛЕДОВАТЕЛЬНО без остановок
- НЕ ЖДАТЬ подтверждения пользователя между шагами
- После `git commit` СРАЗУ делать `git push`

### PowerShell в Windows

- **НЕ использовать `&&`** — PowerShell не поддерживает
- Использовать `;` для объединения команд:
  ```powershell
  cd D:\Git\Svetosila; git status
  ```

### Терминал в Cursor

- Если видишь промпт `PS D:\...>` или результат — команда завершена
- СРАЗУ выполнять следующую команду
- НЕ ЖДАТЬ дополнительных сигналов

### Финальный скрипт

**После выполнения всех шагов ОБЯЗАТЕЛЬНО выдать PowerShell-скрипт для ручного запуска:**

```powershell
cd D:\Git\Svetosila; git add -A; python PROJECT\update_dates.py; python PROJECT\INDEX\update_from_project.py; git add PROJECT\INDEX\index.html; git commit -m "Update documentation"; git push origin main
```

Этот скрипт позволяет пользователю полностью воспроизвести процесс вручную.

