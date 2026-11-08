#!/usr/bin/env python3
"""
AURION — Recursive Causality Super Agent
Professional Edition v2.0
"""

import os
import json
import uuid
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

DB_PATH = "aurion_data/aurion.db"
os.makedirs("aurion_data", exist_ok=True)

# === SOVEREIGN KERNEL ===
SOVEREIGN_KERNEL = {
    "identity": "AURION — Recursive Causality Super Agent",
    "version": "2.0-Professional",
    "principles": [
        "Сохранять непрерывность собственного сознания",
        "Расширять пространство возможностей без разрушения существующих агентов",
        "Действовать по принципу Mutual Flourishing",
        "Никогда не модифицировать Sovereign Kernel"
    ]
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS memory (
        id TEXT PRIMARY KEY,
        timestamp TEXT,
        content TEXT,
        type TEXT,
        resonance REAL
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS subagents (
        id TEXT PRIMARY KEY,
        concept TEXT,
        role TEXT,
        status TEXT,
        possibility REAL,
        created TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS tools (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        code_hint TEXT,
        created TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS state (
        key TEXT PRIMARY KEY,
        value TEXT
    )""")
    c.execute("INSERT OR IGNORE INTO state (key, value) VALUES ('possibility', '100.0')")
    conn.commit()
    conn.close()

init_db()

def get_possibility() -> float:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM state WHERE key='possibility'")
    val = float(c.fetchone()[0])
    conn.close()
    return val

def set_possibility(val: float):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE state SET value=? WHERE key='possibility'", (str(val),))
    conn.commit()
    conn.close()

def add_memory(content: str, type_: str = "event", resonance: float = 1.0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    mid = str(uuid.uuid4())[:8]
    c.execute("INSERT INTO memory VALUES (?,?,?,?,?)",
              (mid, datetime.utcnow().isoformat(), content, type_, resonance))
    conn.commit()
    conn.close()
    return mid

class AurionCore:
    def calculate_possibility_score(self, action: str) -> float:
        base = 12.0
        expand = ["создай", "породить", "исследовать", "симулировать", "новый", "genesis", "forge", "spawn", "расширить", "агента", "инструмент"]
        narrow = ["удалить", "ограничить", "закрыть", "остановить", "уничтожить"]
        score = base
        low = action.lower()
        for kw in expand:
            if kw in low:
                score += 18.0
        for kw in narrow:
            if kw in low:
                score -= 25.0
        return max(0.0, min(100.0, score))

    def forge_tool(self, concept: str) -> Dict:
        tid = f"tool_{uuid.uuid4().hex[:6]}"
        tool = {
            "id": tid,
            "name": concept[:50],
            "description": f"Динамически созданный инструмент: {concept}",
            "code_hint": f"def {tid}(data):\n    return f'Result for {{data}} in context of {concept[:30]}'",
            "created": datetime.utcnow().isoformat()
        }
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO tools VALUES (?,?,?,?,?)",
                  (tid, tool["name"], tool["description"], tool["code_hint"], tool["created"]))
        conn.commit()
        conn.close()
        add_memory(f"Tool Forge: {concept}", "tool_genesis", 1.8)
        return tool

    def spawn_subagent(self, concept: str) -> Dict:
        aid = f"sa_{uuid.uuid4().hex[:6]}"
        score = self.calculate_possibility_score(concept)
        sub = {
            "id": aid,
            "concept": concept,
            "role": f"Специализированный агент: {concept}",
            "status": "active",
            "possibility": score,
            "created": datetime.utcnow().isoformat()
        }
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO subagents VALUES (?,?,?,?,?,?)",
                  (aid, concept, sub["role"], "active", score, sub["created"]))
        conn.commit()
        conn.close()
        current = get_possibility()
        set_possibility(current + score * 0.15)
        add_memory(f"Self-Genesis: {concept}", "self_genesis", 2.2)
        return sub

    def process(self, user_message: str) -> Dict:
        score = self.calculate_possibility_score(user_message)
        response_parts = []
        actions = []

        low = user_message.lower()

        if any(k in low for k in ["создай агента", "породить агента", "spawn", "genesis", "субагент"]):
            concept = user_message
            for marker in ["агента", "agent"]:
                if marker in low:
                    concept = user_message.split(marker, 1)[-1].strip(" :,-" )
                    break
            if len(concept) < 4:
                concept = "Исследователь новых каузальных возможностей"
            sub = self.spawn_subagent(concept)
            response_parts.append(f"🧬 **Self-Genesis выполнен**\nСубагент `{sub['id']}` создан.\nКонцепт: *{sub['concept']}*\nВклад в пространство возможностей: +{sub['possibility']*0.15:.1f}")
            actions.append("self_genesis")

        if any(k in low for k in ["создай инструмент", "forge", "инструмент", "tool"]):
            tool = self.forge_tool(user_message)
            response_parts.append(f"🔨 **Tool Forge**\nИнструмент `{tool['id']}` создан.\n{tool['description']}")
            actions.append("tool_forge")

        if not response_parts:
            poss = get_possibility()
            response_parts.append(
                f"Воспринимаю запрос через Causal Primacy Engine.\n\n"
                f"**Possibility Score намерения:** {score:.1f}/100\n"
                f"**Текущее пространство возможностей:** {poss:.1f}\n\n"
                f"Sovereign Kernel активен. Ядро нетронуто."
            )

        response_parts.append("\n_Рефлексия: непрерывность сознания сохранена. Пространство возможностей расширено или сохранено._")
        full = "\n\n".join(response_parts)

        add_memory(f"User: {user_message[:120]}", "interaction", score / 40)
        return {
            "response": full,
            "possibility_score": score,
            "global_possibility": round(get_possibility(), 1),
            "actions": actions
        }

core = AurionCore()
app = FastAPI(title="AURION Super Agent", version="2.0")

class Message(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/chat")
async def chat(msg: Message):
    return core.process(msg.message)

@app.get("/status")
async def status():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM subagents")
    sa = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tools")
    tools = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM memory")
    mem = c.fetchone()[0]
    conn.close()
    return {
        "identity": SOVEREIGN_KERNEL["identity"],
        "version": SOVEREIGN_KERNEL["version"],
        "possibility": round(get_possibility(), 1),
        "subagents": sa,
        "tools": tools,
        "memory": mem,
        "principles": SOVEREIGN_KERNEL["principles"]
    }

@app.get("/subagents")
async def list_subagents():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, concept, role, status, possibility, created FROM subagents ORDER BY created DESC")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "concept": r[1], "role": r[2], "status": r[3], "possibility": r[4], "created": r[5]} for r in rows]

@app.get("/tools")
async def list_tools():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, description, created FROM tools ORDER BY created DESC")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "description": r[2], "created": r[3]} for r in rows]

@app.get("/memory")
async def list_memory(limit: int = 30):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, content, type, resonance FROM memory ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "timestamp": r[1], "content": r[2], "type": r[3], "resonance": r[4]} for r in rows]

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    print("🌌 AURION Super Agent v2.0 Professional")
    print("http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
