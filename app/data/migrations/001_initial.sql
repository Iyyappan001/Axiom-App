PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    priority TEXT NOT NULL CHECK (priority IN ('High', 'Medium', 'Low')),
    difficulty INTEGER NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
    importance INTEGER NOT NULL CHECK (importance BETWEEN 1 AND 5),
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    created_at TEXT NOT NULL,
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS task_completions (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL REFERENCES tasks(id),
    completed_at TEXT NOT NULL,
    xp_awarded INTEGER NOT NULL CHECK (xp_awarded >= 0),
    UNIQUE (task_id)
);

CREATE TABLE IF NOT EXISTS xp_ledger (
    id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL,
    source_id TEXT NOT NULL,
    xp_delta INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
