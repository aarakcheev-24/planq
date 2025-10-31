# planq — простой CLI‑планировщик задач

## О проекте
**planq** — консольный менеджер/планировщик задач. Позволяет добавлять задачи с приоритетом и сроком, смотреть список, отмечать выполнение, редактировать и удалять. Хранит данные локально в JSON по пути `~/.planq/tasks.json`. Проект предназначен для быстрой демонстрации CLI‑инструмента без внешних зависимостей.

## Функциональность
- `add` — добавление задачи (`--prio low|med|high`, `--due YYYY-MM-DD`)
- `list` — просмотр списка (фильтры: `--status`, `--prio`, `--overdue`)
- `done` — отметка задачи выполненной по ID
- `edit` — редактирование названия/приоритета/срока
- `remove` — удаление по ID; `clear` — очистка списка (все/только выполненные)

## Требования
- Python **3.10+**
- Внешние библиотеки **не требуются** (проект использует только стандартную библиотеку)

## Установка (клонирование и окружение)
```bash
git clone https://github.com/aarakcheev-24/planq.git
cd planq
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
# .\venv\Scripts\activate # Windows PowerShell
```

## Запуск (демо)
```bash
python -m planq --help
python -m planq add "Сдать лабораторную" --prio high --due 2025-11-10
python -m planq list --status all
python -m planq done 1
python -m planq list --status done
```

## Структура проекта
```
planq/
├─ planq/           # исходный код пакета
│  ├─ __init__.py
│  ├─ __main__.py   # точка входа: python -m planq
│  ├─ cli.py        # парсер аргументов и команды
│  ├─ models.py     # модель Task
│  └─ storage.py    # чтение/запись JSON
├─ README.md
├─ .gitignore
└─ LICENSE
```

## Лицензия/автор
Автор: Аракчеев Александр Андреевич  
Лицензия: MIT
