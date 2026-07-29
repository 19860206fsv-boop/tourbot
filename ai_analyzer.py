import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def analyze_news(title, summary):
    """Анализируем новость и выдаём 3 блока для турагента."""
    prompt = f"""Ты — опытный помощник туристического агентства.
Проанализируй новость и дай ответ строго в ТРЁХ блоках.
Пиши простым языком, конкретно, без воды.

Заголовок: {title}
Текст: {summary}

Ответ дай СТРОГО в таком формате:

📰 <b>СУТЬ НОВОСТИ</b>
(1-2 предложения: что произошло)

👨‍💼 <b>ЧТО ДЕЛАТЬ АГЕНТУ</b>
(конкретные действия прямо сейчас, можно списком через дефис)

💬 <b>СКРИПТ ДЛЯ КЛИЕНТА</b>
(готовый текст, который агент может скопировать и отправить клиенту, если тот летит в ближайшие дни. Если новость не требует связи с клиентом — напиши: "Связь с клиентом не требуется")"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка нейро-анализа: {e}")
        return "⚠️ Не удалось проанализировать новость."
