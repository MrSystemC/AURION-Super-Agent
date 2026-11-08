# AURION Super Agent v2.0 Professional

Рекурсивный Каузальный Супер Агент. Создан с нуля как полностью независимый проект.

## Быстрый запуск

```bash
pip install -r requirements.txt
python aurion.py
```

Откройте http://localhost:8000

## Docker

```bash
docker build -t aurion .
docker run -p 8000:8000 -v $(pwd)/aurion_data:/app/aurion_data aurion
```

## Что внутри

- Causal Primacy Engine
- Self-Genesis (создание субагентов из концептов)
- Tool Forge
- Resonance Memory (SQLite)
- Sovereign Kernel
- Профессиональный веб-интерфейс
- REST API

## Примеры запросов

- «Создай агента исследователя тишины между словами»
- «Создай инструмент анализа каузальных цепей»
- «Каково текущее пространство возможностей?»

---

Полная концепция: `AURION_Концепция.md`  
Руководство: `USER_GUIDE.md`
