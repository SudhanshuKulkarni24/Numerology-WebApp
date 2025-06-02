from flask import Flask, request, render_template_string

app = Flask(__name__)

# Pythagorean numerology mapping
pythagorean = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

# Chaldean numerology mapping
chaldean = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5, 'I': 1,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
    'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7
}

# HTML template as a string to avoid template directory issues on Vercel
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Numerology Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        form {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            margin-bottom: 15px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        .results {
            margin-top: 30px;
            padding: 20px;
            background-color: #e8f5e8;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }
        .result-item {
            margin: 10px 0;
            font-size: 18px;
        }
        .result-label {
            font-weight: bold;
            color: #333;
        }
        .result-value {
            color: #4CAF50;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Numerology Calculator</h1>
        <form method="post">
            <label>Enter a name or word:</label>
            <input type="text" name="name" required placeholder="Enter your name here...">
            <input type="submit" value="Calculate Numerology">
        </form>

        {% if result %}
            <div class="results">
                <h2>Your Numerology Results:</h2>
                <div class="result-item">
                    <span class="result-label">Pythagorean Numerology:</span> 
                    <span class="result-value">{{ result.pythagorean }}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Chaldean Numerology:</span> 
                    <span class="result-value">{{ result.chaldean }}</span>
                </div>
                <p style="margin-top: 15px; font-size: 14px; color: #666;">
                    <strong>Input:</strong> "{{ input_name }}"
                </p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def calculate_numerology(name, mapping):
    total = 0
    for char in name:
        if char.isalpha():
            total += mapping[char.upper()]
    return total

def reduce_to_single_digit(number):
    """Reduce number to single digit (1-9) except for master numbers 11, 22, 33"""
    if number in [11, 22, 33]:
        return number
    while number >= 10:
        number = sum(int(digit) for digit in str(number))
        if number in [11, 22, 33]:
            return number
    return number

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    input_name = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            input_name = name
            pythagorean_result = calculate_numerology(name, pythagorean)
            chaldean_result = calculate_numerology(name, chaldean)
            
            # Reduce to single digits (with master number exceptions)
            pythagorean_reduced = reduce_to_single_digit(pythagorean_result)
            chaldean_reduced = reduce_to_single_digit(chaldean_result)
            
            result = {
                "pythagorean": pythagorean_reduced,
                "chaldean": chaldean_reduced
            }
    
    return render_template_string(HTML_TEMPLATE, result=result, input_name=input_name)

# For Vercel
if __name__ == "__main__":
    app.run(debug=True)
