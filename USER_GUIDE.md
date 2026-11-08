# AURION Super Agent — Руководство пользователя

## Запуск

### Локально
```bash
pip install -r requirements.txt
python aurion.py
```

### Docker
```bash
docker build -t aurion .
docker run -p 8000:8000 -v $(pwd)/aurion_data:/app/aurion_data aurion
```

## Интерфейс

- Главная страница: чат + живая статистика + списки субагентов и инструментов
- API:
  - `POST /chat` — диалог
  - `GET /status` — статус системы
  - `GET /subagents` — список субагентов
  - `GET /tools` — список инструментов
  - `GET /memory` — последние записи памяти

## Примеры

- Создай агента исследователя тишины между словами
- Создай инструмент анализа каузальных цепей
- Каково текущее пространство возможностей?

## Данные

Все данные хранятся в `aurion_data/aurion.db` (SQLite). Папка монтируется в Docker для персистентности.
