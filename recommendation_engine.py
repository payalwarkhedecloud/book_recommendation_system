import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name("books.csv")
WEIGHTS = {"genre": 3, "theme": 2, "reading_level": 2, "length": 1, "mood": 2}

def load_books(path=DATA_FILE):
    required = {"book_id","title","author","genres","themes","reading_level","length_category","language","mood","description"}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("Book CSV is missing required columns.")
        rows = list(reader)
    if not rows:
        raise ValueError("Book knowledge base is empty.")
    if any(not r.get("title") or not r.get("author") for r in rows):
        raise ValueError("Every book must have a title and author.")
    return rows

def split_tags(value):
    return {x.strip().casefold() for x in (value or "").split(";") if x.strip()}

def recommend_books(books, preferences, top_n=5):
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")
    keys = ("genres","themes","reading_level","length","mood")
    if not preferences or not any(preferences.get(k) for k in keys):
        return []
    applicable_max = (WEIGHTS["genre"] if preferences.get("genres") else 0) + (WEIGHTS["theme"] if preferences.get("themes") else 0) + (WEIGHTS["reading_level"] if preferences.get("reading_level") else 0) + (WEIGHTS["length"] if preferences.get("length") else 0) + (WEIGHTS["mood"] if preferences.get("mood") else 0)
    ranked=[]
    for book in books:
        score=0; reasons=[]
        checks=[
            ("genres","genres","genre","Genre", "multi"),
            ("themes","themes","theme","Theme", "multi"),
            ("reading_level","reading_level","reading_level","Reading level","single"),
            ("length","length_category","length","Length","single"),
            ("mood","mood","mood","Mood/purpose","single"),
        ]
        for pref_key, field, weight_key, label, kind in checks:
            selected=preferences.get(pref_key)
            if not selected: continue
            if kind=="multi":
                selected_set=set()
                for val in selected: selected_set |= split_tags(val)
                matched=bool(selected_set & split_tags(book.get(field,"")))
            else:
                matched=str(selected).casefold() in split_tags(book.get(field,""))
            if matched:
                score += WEIGHTS[weight_key]
                reasons.append(f"{label} matched (+{WEIGHTS[weight_key]})")
        if score:
            ranked.append({**book,"score":score,"max_score":applicable_max,
                           "match_percentage":round(score/applicable_max*100,1),
                           "reasons":reasons})
    ranked.sort(key=lambda x:(-x["score"],x["title"].casefold()))
    return ranked[:top_n]

if __name__ == "__main__":
    sample={"genres":["Science Fiction"],"themes":["science"],"reading_level":"Beginner"}
    for i,b in enumerate(recommend_books(load_books(),sample),1):
        print(f"{i}. {b['title']} — {b['score']}/{b['max_score']} ({b['match_percentage']}%)")
        print("   "+"; ".join(b["reasons"]))
