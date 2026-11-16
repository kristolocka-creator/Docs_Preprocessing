from pathlib import Path
from text_cleaner import clean_text

input_file = Path("datasets/sample_documents.txt")
output_file = Path("src/data/cleaned_documents.txt")

text = input_file.read_text(encoding="utf-8")
cleaned_text = clean_text(text)

output_file.write_text(cleaned_text, encoding="utf-8")

print("Очистка завершена!")
print(f"Исходный текст: {len(text)} символов")
print(f"Очищенный текст: {len(cleaned_text)} символов")
print(f"Результат сохранён: {output_file}")
