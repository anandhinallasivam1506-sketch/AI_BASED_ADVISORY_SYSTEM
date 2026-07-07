from flask import Flask, render_template, request
import sqlite3
import google.generativeai as genai

app = Flask(__name__)

# -------------------------------
# Gemini API Configuration
# -------------------------------
genai.configure(api_key="AQ.Ab8RN6IndVKYwBjbAACyUjNpKB4iL-PHCk_uQ5649NREdfZB-g")

model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------
# Create Database
# -------------------------------
def create_database():
    conn = sqlite3.connect("farmers.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT,
            crop_name TEXT,
            location TEXT,
            question TEXT,
            answer TEXT
        )
    """)

    conn.commit()
    conn.close()

create_database()

# -------------------------------
# Home Page
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":

        farmer_name = request.form["farmer_name"]
        crop_name = request.form["crop_name"]
        location = request.form["location"]
        question = request.form["question"]

        prompt = f"""
You are an expert agricultural advisor.

Farmer Name: {farmer_name}
Crop: {crop_name}
Location: {location}

Question:
{question}

Give a clear and practical solution in simple English.
"""

        try:
            response = model.generate_content(prompt)
            answer = response.text

            conn = sqlite3.connect("farmers.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO queries
                (farmer_name, crop_name, location, question, answer)
                VALUES (?, ?, ?, ?, ?)
            """, (
                farmer_name,
                crop_name,
                location,
                question,
                answer
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            answer = f"ERROR: {e}"

    return render_template("index.html", answer=answer)


# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)