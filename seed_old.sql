-- Пользователи
INSERT INTO users (username, email) VALUES
  ('alice', 'alice@example.com'),
  ('bob', 'bob@example.com');

-- Заметки Alice (user_id = 1)
INSERT INTO notes (user_id, title, body, tag, done) VALUES
  (1, 'Купить молоко', 'В магазине у дома', 'быт', true),
  (1, 'Важно: отчёт', 'Сдать до пятницы', 'работа', false),
  (1, 'Позвонить маме', 'Спросить про дачу', 'быт', false),
  (1, 'Код-ревью PR #42', 'Проверить тесты', 'работа', false),
  (1, 'Прочитать книгу', 'Глава 5-7', 'учёба', true);

-- Заметки Bob (user_id = 2)
INSERT INTO notes (user_id, title, body, tag, done) VALUES
  (2, 'Сделать домашку', 'Математика', 'учёба', false),
  (2, 'Важно: презентация', 'Подготовить слайды', 'работа', false),
  (2, 'Убрать квартиру', 'Пропылесосить', 'быт', true),
  (2, 'Написать тесты', 'pytest для models.py', 'работа', false),
  (2, 'Купить подарок', 'День рождения друга', 'быт', false);

-- 1. Невыполненные заметки Alice
SELECT * FROM notes WHERE user_id = 1 AND done = false;

-- 2. Заметки с тегом 'работа' (оба пользователя)
SELECT * FROM notes WHERE tag = 'работа' ORDER BY title;

-- 3. Заметки с 'важно' в названии (без учёта регистра)
SELECT * FROM notes WHERE title ILIKE '%важно%';

BEGIN;

UPDATE notes
SET done = TRUE
WHERE id = 1
RETURNING id, title, done;

DELETE FROM notes
WHERE tag = 'draft'
AND created_at < CURRENT_TIMESTAMP - INTERVAL '10 days'
RETURNING id, title, tag, created_at;
COMMIT;

CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    remind_at TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);