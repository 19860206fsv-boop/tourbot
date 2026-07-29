import feedparser
from config import RSS_SOURCES, KEYWORDS, MAX_NEWS_PER_CHECK


def is_tourism_related(text):
    """Проверяем, есть ли в тексте туристические ключевые слова."""
    text_lower = text.lower()
    for keyword in KEYWORDS:
        if keyword in text_lower:
            return True
    return False


def fetch_news():
    """Читаем все RSS-ленты и возвращаем список туристических новостей."""
    news_list = []

    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source)
            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                link = entry.get("link", "")

                # Пропускаем, если нет ссылки
                if not link:
                    continue

                # Проверяем на туристическую тему
                combined_text = title + " " + summary
                if is_tourism_related(combined_text):
                    news_list.append({
                        "title": title,
                        "summary": summary,
                        "link": link,
                    })
        except Exception as e:
            print(f"Ошибка при чтении {source}: {e}")
            continue

    # Ограничиваем количество новостей за один проход
    return news_list[:MAX_NEWS_PER_CHECK]
