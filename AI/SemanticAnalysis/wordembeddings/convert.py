import json

INPUT_FILE = "glove.6B.50d.txt"
OUTPUT_FILE = "embeddings.json"

MAX_WORDS = 20000

embeddings = {}

count = 0

print("Reading GloVe file...")

with open(INPUT_FILE, "r", encoding="utf-8") as f:

    for line in f:

        parts = line.strip().split()

        if len(parts) < 51:
            continue

        word = parts[0]

        try:
            vector = [round(float(x), 6) for x in parts[1:]]
        except:
            continue

        embeddings[word] = vector

        count += 1

        if count >= MAX_WORDS:
            break

print(f"Loaded {count} words")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(embeddings, f)

print(f"Saved to {OUTPUT_FILE}")