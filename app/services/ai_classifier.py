import openai
from app.settings import Settings

settings= Settings()
openai.api_key = settings.OPENAI_API_KEY

async def classify_expense(description: str):
    categories = ["Alimentação", "Transporte", "Lazer", "Educação", "Saúde", "Moradia", "Outros"]
    prompt = (
        f"Classifique a seguinte descrição de despesa em uma das categorias: {categories}.\n"
        f"Descrição: \"{description}\"\n"
        "Retorne apenas o nome da categoria, sem explicações adicionais."
    )

    response = await openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um classificador de despesas financeiras."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    category = response.choices[0].message.content.strip()
    return category
