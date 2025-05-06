from openai import OpenAI


client = OpenAI(api_key="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")

ingredientes = input("Ingresa 3 ingredientes separados por coma: ").strip().split(",")
ingredientes = [ing.strip() for ing in ingredientes]

prompt = f"Dame una receta fácil y breve usando estos ingredientes: {', '.join(ingredientes)}."

respuesta = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("\nReceta sugerida por la IA:")
print(respuesta.choices[0].message.content)