-- Все заметки пользователя
SELECT * FROM users

-- -- 2. Заметки с тегом «работа»
SELECT *
FROM notes
WHERE tags = 'работа';


-- 3. Количество заметок у каждого пользователя,
-- включая пользователей без заметок
SELECT
    users.id,
    users.username,
    COUNT(notes.id) AS notes_count
FROM users
LEFT JOIN notes ON users.id = notes.user_id
GROUP BY users.id, users.username;


-- 4. Сумма расходов по категориям
SELECT
    category,
    SUM(amount) AS total_amount
FROM expenses
GROUP BY category;


-- 5. Заметки вместе с именами их авторов
SELECT
    notes.id,
    notes.text,
    users.username
FROM notes
JOIN users ON notes.user_id = users.id;


-- 6. Последние 5 заметок
SELECT *
FROM notes
ORDER BY created_at DESC, id DESC
LIMIT 5;


-- 7. Категории, в которых сумма расходов больше 1000
SELECT
    category,
    SUM(amount) AS total_amount
FROM expenses
GROUP BY category
HAVING SUM(amount) > 1000;


-- 8. Изменить текст заметки с id = 1
UPDATE notes
SET text = 'Обновлённый текст заметки'
WHERE id = 1
RETURNING *;


-- 9. Удалить заметку с id = 6
DELETE FROM notes
WHERE id = 6
RETURNING *;


-- 10. Найти расходы, превышающие среднюю сумму расхода
SELECT *
FROM expenses
WHERE amount > (
    SELECT AVG(amount)
    FROM expenses
);