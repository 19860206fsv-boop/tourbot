import os
from groq import Groq

# Ключ берём из "секретов" (настроим позже, в шаге с запуском)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def analyze_news(title, summary):
    """Анализируем новость через нейросеть и делаем вывод для турагента."""
    prompt = f"""Ты — помощник туристического агентства.
Проанализируй новость и дай КОРОТКИЙ вывод (2-3 предложения):
как это влияет на туристов и работу турагентства.
Пиши простым языком, без воды.

Заголовок: {title}
Текст: {summary}

Дай ответ в формате:
📌 Суть: (в одном предложении)
💼 Что это значит для турагента: (1-2 предложения)"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка нейро-анализа: {e}")
        return "⚠️ Не удалось проанализировать новость."
