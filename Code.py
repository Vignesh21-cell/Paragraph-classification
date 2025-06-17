import re
import sys
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from difflib import get_close_matches
from collections import Counter

# Load dictionary from the text file
def load_dictionary(file_path):
    dictionary = set()
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                words = re.findall(r'\b[a-zA-Z]+\b', line.lower())  # Extract words
                dictionary.update(words)
        print(f"Dictionary Loaded: {len(dictionary)} words.")
    except FileNotFoundError:
        print("Error: Dictionary file not found.")
        sys.exit(1)
    return dictionary

# Suggest words for a misspelled word
def suggest_words(word, dictionary):
    suggestions = get_close_matches(word.lower(), dictionary, n=3, cutoff=0.7)  # Top 3 suggestions
    return suggestions if suggestions else ["No suggestions found"]

# Auto-correct a word using the closest match from the dictionary
def auto_correct_word(word, dictionary):
    if word.lower() in dictionary or any(char.isdigit() for char in word):
        return word  # Keep numbers and correctly spelled words unchanged

    suggestions = get_close_matches(word.lower(), dictionary, n=1, cutoff=0.8)  # Best match
    corrected_word = suggestions[0] if suggestions else word

    if corrected_word != word:
        correction_text.insert(tk.END, f"Misspelled Word: {word} → Auto-corrected to: {corrected_word}\n")
        correction_text.insert(tk.END, f"Suggestions: {', '.join(suggest_words(word, dictionary))}\n\n")

    return corrected_word

# Paragraph Categorization based on keywords
def categorize_paragraph(paragraph):
    categories = {
        "finance": {"money", "economy", "investment", "market", "bank", "stock", "financial"},
        "technology": {"computer", "software", "hardware", "AI", "technology", "internet", "cyber"},
        "sports": {"football", "cricket", "basketball", "tennis", "athlete", "olympics"},
        "history": {"war", "revolution", "historical", "empire", "ancient", "battle"},
        "science": {"physics", "chemistry", "biology", "science", "research", "experiment"},
        "politics": {"government", "election", "policy", "law", "democracy", "political"},
    }

    words = set(paragraph.lower().split())  # Convert paragraph to a set of words
    category_counts = {category: len(words & keywords) for category, keywords in categories.items()}

    best_category = max(category_counts, key=category_counts.get)
    return best_category if category_counts[best_category] > 0 else "Uncategorized"

# Process the paragraph to correct spelling mistakes and suggest words
def process_paragraph():
    paragraph = input_text.get("1.0", tk.END).strip()
    
    if not paragraph:
        messagebox.showerror("Error", "Please enter a paragraph!")
        return

    corrected_paragraph = []
    correction_text.delete("1.0", tk.END)  # Clear previous results
    
    # Split paragraph into words while preserving punctuation
    words = re.findall(r"[\w']+|[.,!?;:\"()]", paragraph)
    
    for word in words:
        clean_word = re.sub(r"[^\w]", "", word)  # Remove punctuation for checking
        corrected_word = auto_correct_word(clean_word, dictionary)
        corrected_paragraph.append(word.replace(clean_word, corrected_word))  # Maintain punctuation

    corrected_text = " ".join(corrected_paragraph)
    category = categorize_paragraph(corrected_text)  # Categorize the corrected paragraph

    corrected_paragraph_text.delete("1.0", tk.END)
    corrected_paragraph_text.insert(tk.END, corrected_text)

    category_label.config(text=f"Paragraph Category: {category}")

# GUI Setup
root = tk.Tk()
root.title("Spell Checker & Paragraph Categorizer")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Load dictionary
dictionary_path = "E:\\code blocks\\c codes\\DSA\\paragraphs.txt"  # Using the uploaded file
dictionary = load_dictionary(dictionary_path)

# Input Text
tk.Label(root, text="Enter Paragraph:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)
input_text = scrolledtext.ScrolledText(root, height=5, wrap=tk.WORD, font=("Arial", 12))
input_text.pack(fill="both", padx=10, pady=5)

# Process Button
process_button = tk.Button(root, text="Check & Categorize", font=("Arial", 12, "bold"), command=process_paragraph, bg="#4CAF50", fg="white", padx=10, pady=5)
process_button.pack(pady=10)

# Correction Output
tk.Label(root, text="Spelling Corrections & Suggestions:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)
correction_text = scrolledtext.ScrolledText(root, height=6, wrap=tk.WORD, font=("Arial", 12))
correction_text.pack(fill="both", padx=10, pady=5)

# Corrected Paragraph Output
tk.Label(root, text="Corrected Paragraph:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)
corrected_paragraph_text = scrolledtext.ScrolledText(root, height=5, wrap=tk.WORD, font=("Arial", 12))
corrected_paragraph_text.pack(fill="both", padx=10, pady=5)

# Category Label
category_label = tk.Label(root, text="Paragraph Category: ", font=("Arial", 14, "bold"), fg="#333", bg="#f0f0f0")
category_label.pack(pady=10)

# Run GUI
root.mainloop()
