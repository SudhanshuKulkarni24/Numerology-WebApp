from flask import Flask, request, render_template

app = Flask(__name__, template_folder="../templates")

# Numerology Mappings
pythagorean = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}
chaldean = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5, 'I': 1,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
    'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7
}

def calculate_numerology(name, mapping):
    total = 0
    for char in name:
        if char.isalpha():
            total += mapping[char.upper()]
    return total

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        pythagorean_result = calculate_numerology(name, pythagorean)
        chaldean_result = calculate_numerology(name, chaldean)
        return render_template("index.html", result=True, name=name,
                               pythagorean=pythagorean_result,
                               chaldean=chaldean_result)
    return render_template("index.html", result=False)

# Required by Vercel
handler = app
