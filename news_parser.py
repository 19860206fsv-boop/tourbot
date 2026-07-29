import feedparser
from config import RSS_SOURCES, KEYWORDS, MAX_NEWS_PER_CHECK

# 🚫 СТОП-СЛОВА — если есть в тексте, новость ВЫБРАСЫВАЕМ (даже если она "туристическая")
STOP_WORDS = [
    "всу", "сбу", "гур", "украин", "укро", "одесс", "киев", "киів",
    "харьков", "херсон", "запорож", "донецк", "луганск", "мариуполь",
    "мобилизац", "фронт", "обстрел", "военн", "боевик", "карател",
    "теракт", "подорв", "убит", "погиб", "ракет", "дрон", "бпла",
    "снаряд", "минобороны", "спецоперац", " сво ", "зеленск",
    "всушник", "нацбат", "азов", "контрнаступ", "ракетн", "удар по"
]


def has_stop_word(text):
    """Проверяем, есть ли в тексте стоп-слова (не туризм)."""
    text_lower = text.lower()
    for stop in STOP_WORDS:
        if stop in text_lower:
            return True
    return False


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

                combined_text = title + " " + summary

                # 🚫 1. Сначала выбрасываем новости со стоп-словами
                if has_stop_word(combined_text):
                    continue

                # ✅ 2. Потом оставляем только туристические
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
