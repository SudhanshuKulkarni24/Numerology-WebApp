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
        :root {
            --bg-color: #f5f5f5;
            --container-bg: white;
            --text-color: #333;
            --text-secondary: #555;
            --text-muted: #666;
            --border-color: #ddd;
            --shadow: rgba(0,0,0,0.1);
            --accent-color: #4CAF50;
            --accent-hover: #45a049;
            --results-bg: #e8f5e8;
        }

        [data-theme="dark"] {
            --bg-color: #1a1a1a;
            --container-bg: #2d2d2d;
            --text-color: #e0e0e0;
            --text-secondary: #b0b0b0;
            --text-muted: #888;
            --border-color: #444;
            --shadow: rgba(0,0,0,0.3);
            --accent-color: #66BB6A;
            --accent-hover: #5CB860;
            --results-bg: #1e3a1e;
        }

        * {
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        }

        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: var(--bg-color);
            color: var(--text-color);
        }

        .theme-toggle {
            position: absolute;
            top: 20px;
            right: 20px;
            background: none;
            border: 2px solid var(--border-color);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            font-size: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: var(--container-bg);
            color: var(--text-color);
        }

        .theme-toggle:hover {
            transform: scale(1.1);
            border-color: var(--accent-color);
        }

        .container {
            background-color: var(--container-bg);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px var(--shadow);
            position: relative;
        }

        h1 {
            color: var(--text-color);
            text-align: center;
            margin-bottom: 30px;
        }

        form {
            margin: 20px 0;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: var(--text-secondary);
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 2px solid var(--border-color);
            border-radius: 5px;
            font-size: 16px;
            margin-bottom: 15px;
            background-color: var(--container-bg);
            color: var(--text-color);
            box-sizing: border-box;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: var(--accent-color);
        }

        input[type="submit"] {
            background-color: var(--accent-color);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }

        input[type="submit"]:hover {
            background-color: var(--accent-hover);
        }

        .results {
            margin-top: 30px;
            padding: 20px;
            background-color: var(--results-bg);
            border-radius: 5px;
            border-left: 4px solid var(--accent-color);
        }

        .result-item {
            margin: 10px 0;
            font-size: 18px;
        }

        .result-label {
            font-weight: bold;
            color: var(--text-color);
        }

        .result-value {
            color: var(--accent-color);
            font-weight: bold;
        }

        .results h2 {
            color: var(--text-color);
            margin-top: 0;
        }

        .results p {
            color: var(--text-muted);
        }
    </style>
</head>
<body data-theme="light">
    <button class="theme-toggle" onclick="toggleTheme()" title="Toggle theme">
        <span id="theme-icon">🌙</span>
    </button>
    
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
    
    <script>
        // Theme toggle functionality
        function toggleTheme() {
            const body = document.body;
            const themeIcon = document.getElementById('theme-icon');
            const currentTheme = body.getAttribute('data-theme');
            
            if (currentTheme === 'light') {
                body.setAttribute('data-theme', 'dark');
                themeIcon.textContent = '☀️';
                localStorage.setItem('theme', 'dark');
            } else {
                body.setAttribute('data-theme', 'light');
                themeIcon.textContent = '🌙';
                localStorage.setItem('theme', 'light');
            }
        }
        
        // Load saved theme preference
        function loadTheme() {
            const savedTheme = localStorage.getItem('theme') || 'light';
            const body = document.body;
            const themeIcon = document.getElementById('theme-icon');
            
            body.setAttribute('data-theme', savedTheme);
            themeIcon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
        }
        
        // Initialize theme on page load
        document.addEventListener('DOMContentLoaded', loadTheme);
    </script>
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
