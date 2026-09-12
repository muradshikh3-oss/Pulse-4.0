BEGIN;

-- 2 пользователя
INSERT INTO users (username) VALUES
    ('alice'),
    ('bob');

-- 6 заметок
INSERT INTO notes (user_id, text, tags) VALUES
    (1, 'Купить молоко', 'быт'),
    (1, 'Подготовить отчёт', 'работа'),
    (1, 'Изучить PostgreSQL', 'учёба'),
    (2, 'Убрать квартиру', 'быт'),
    (2, 'Написать тесты', 'работа'),
    (2, 'Старый черновик', 'draft');

-- 3 напоминания
INSERT INTO reminders (user_id, text, due_date) VALUES
    (1, 'Сдать отчёт', CURRENT_TIMESTAMP + INTERVAL '1 day'),
    (1, 'Повторить SQL', CURRENT_TIMESTAMP + INTERVAL '2 days'),
    (2, 'Позвонить другу', CURRENT_TIMESTAMP + INTERVAL '3 days');

-- 4 расхода
INSERT INTO expenses (user_id, amount, category) VALUES
    (1, 850.00, 'продукты'),
    (1, 350.00, 'транспорт'),
    (2, 1200.00, 'продукты'),
    (2, 2500.00, 'обучение');

COMMIT;