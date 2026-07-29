import sqlite3

DB_NAME = "bot.db"


def init_db():
    """Создаём таблицы при первом запуске."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Таблица уже отправленных новостей (чтобы не дублировать)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sent_news (
            link TEXT PRIMARY KEY,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Таблица подписчиков (кому слать новости)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            chat_id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()


def is_news_sent(link):
    """Проверяем, отправляли ли уже эту новость."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM sent_news WHERE link = ?", (link,))
    result = cur.fetchone()
    conn.close()
    return result is not None


def mark_news_sent(link):
    """Помечаем новость как отправленную."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO sent_news (link) VALUES (?)", (link,))
    conn.commit()
    conn.close()


def add_subscriber(chat_id):
    """Добавляем подписчика."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO subscribers (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()


def remove_subscriber(chat_id):
    """Удаляем подписчика."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM subscribers WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()


def get_all_subscribers():
    """Получаем список всех подписчиков."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM subscribers")
    result = [row[0] for row in cur.fetchall()]
    conn.close()
    return result
