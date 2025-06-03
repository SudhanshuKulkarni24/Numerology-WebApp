from flask import Flask, request, render_template_string
from datetime import datetime

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

# Base CSS styles for consistent theming across pages
BASE_STYLES = """
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
            --card-hover: rgba(76, 175, 80, 0.1);
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
            --card-hover: rgba(102, 187, 106, 0.1);
        }

        * {
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        }

        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
        }

        .theme-toggle {
            position: fixed;
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
            z-index: 1000;
        }

        .theme-toggle:hover {
            transform: scale(1.1);
            border-color: var(--accent-color);
        }

        .nav-header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background-color: var(--container-bg);
            border-radius: 10px;
            box-shadow: 0 2px 10px var(--shadow);
        }

        .nav-header h1 {
            color: var(--accent-color);
            margin: 0;
            font-size: 2.5em;
        }

        .nav-header p {
            color: var(--text-secondary);
            margin: 10px 0 0 0;
            font-size: 1.1em;
        }

        .nav-links {
            text-align: center;
            margin: 20px 0;
        }

        .nav-links a {
            color: var(--accent-color);
            text-decoration: none;
            margin: 0 15px;
            font-weight: bold;
        }

        .nav-links a:hover {
            text-decoration: underline;
        }

        .container {
            background-color: var(--container-bg);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px var(--shadow);
            margin-bottom: 20px;
        }
"""

# JavaScript for theme toggle
THEME_SCRIPT = """
    <script>
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
        
        function loadTheme() {
            const savedTheme = localStorage.getItem('theme') || 'light';
            const body = document.body;
            const themeIcon = document.getElementById('theme-icon');
            
            body.setAttribute('data-theme', savedTheme);
            themeIcon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
        }
        
        document.addEventListener('DOMContentLoaded', loadTheme);
    </script>
"""

# Home page template
HOME_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Numerology Tools</title>
    <style>
        {BASE_STYLES}
        
        .tools-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }}

        .tool-card {{
            background-color: var(--container-bg);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 20px var(--shadow);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 2px solid transparent;
        }}

        .tool-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 30px var(--shadow);
            border-color: var(--accent-color);
            background-color: var(--card-hover);
        }}

        .tool-icon {{
            font-size: 4em;
            margin-bottom: 20px;
            display: block;
        }}

        .tool-card h2 {{
            color: var(--accent-color);
            margin-bottom: 15px;
            font-size: 1.5em;
        }}

        .tool-card p {{
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 25px;
        }}

        .tool-button {{
            display: inline-block;
            background-color: var(--accent-color);
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }}

        .tool-button:hover {{
            background-color: var(--accent-hover);
            transform: scale(1.05);
        }}

        .features-list {{
            list-style: none;
            padding: 0;
            margin: 15px 0;
        }}

        .features-list li {{
            color: var(--text-secondary);
            margin: 8px 0;
            padding-left: 20px;
            position: relative;
        }}

        .features-list li:before {{
            content: '✓';
            color: var(--accent-color);
            font-weight: bold;
            position: absolute;
            left: 0;
        }}
    </style>
</head>
<body data-theme="light">
    <button class="theme-toggle" onclick="toggleTheme()" title="Toggle theme">
        <span id="theme-icon">🌙</span>
    </button>
    
    <div class="nav-header">
        <h1>Numerology Tools</h1>
        <p>Discover the hidden meanings in names, words, and birth dates</p>
    </div>
    
    <div class="tools-grid">
        <div class="tool-card">
            <span class="tool-icon">🔤</span>
            <h2>Name Calculator</h2>
            <p>Calculate the numerological values of names and words using both Pythagorean and Chaldean systems.</p>
            <ul class="features-list">
                <li>Pythagorean & Chaldean systems</li>
                <li>Master number recognition</li>
                <li>Instant calculations</li>
                <li>Beautiful results display</li>
            </ul>
            <a href="/name-calculator" class="tool-button">Calculate Names</a>
        </div>
        
        <div class="tool-card">
            <span class="tool-icon">🔢</span>
            <h2>Lo Shu Grid</h2>
            <p>Generate your personal Lo Shu Grid based on your birth date to discover your strengths and missing numbers.</p>
            <ul class="features-list">
                <li>Birth date analysis</li>
                <li>Missing number insights</li>
                <li>Strength identification</li>
                <li>Visual grid display</li>
            </ul>
            <a href="/lo-shu-grid" class="tool-button">Generate Grid</a>
        </div>
    </div>
    
    {THEME_SCRIPT}
</body>
</html>
"""

# Name calculator template
NAME_CALC_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Name Calculator - Numerology Tools</title>
    <style>
        {BASE_STYLES}
        
        h1 {{
            color: var(--text-color);
            text-align: center;
            margin-bottom: 30px;
        }}

        form {{
            margin: 20px 0;
        }}

        label {{
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: var(--text-secondary);
        }}

        input[type="text"] {{
            width: 100%;
            padding: 10px;
            border: 2px solid var(--border-color);
            border-radius: 5px;
            font-size: 16px;
            margin-bottom: 15px;
            background-color: var(--container-bg);
            color: var(--text-color);
            box-sizing: border-box;
        }}

        input[type="text"]:focus {{
            outline: none;
            border-color: var(--accent-color);
        }}

        input[type="submit"] {{
            background-color: var(--accent-color);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}

        input[type="submit"]:hover {{
            background-color: var(--accent-hover);
        }}

        .results {{
            margin-top: 30px;
            padding: 20px;
            background-color: var(--results-bg);
            border-radius: 5px;
            border-left: 4px solid var(--accent-color);
        }}

        .result-item {{
            margin: 10px 0;
            font-size: 18px;
        }}

        .result-label {{
            font-weight: bold;
            color: var(--text-color);
        }}

        .result-value {{
            color: var(--accent-color);
            font-weight: bold;
        }}

        .results h2 {{
            color: var(--text-color);
            margin-top: 0;
        }}

        .results p {{
            color: var(--text-muted);
        }}
    </style>
</head>
<body data-theme="light">
    <button class="theme-toggle" onclick="toggleTheme()" title="Toggle theme">
        <span id="theme-icon">🌙</span>
    </button>
    
    <div class="nav-header">
        <h1>Name Calculator</h1>
        <div class="nav-links">
            <a href="/">← Back to Home</a>
            <a href="/lo-shu-grid">Lo Shu Grid →</a>
        </div>
    </div>
    
    <div class="container">
        <form method="post">
            <label>Enter a name or word:</label>
            <input type="text" name="name" required placeholder="Enter your name here..." value="{{{{ input_name }}}}">
            <input type="submit" value="Calculate Numerology">
        </form>

        {{% if result %}}
            <div class="results">
                <h2>Your Numerology Results:</h2>
                <div class="result-item">
                    <span class="result-label">Pythagorean Numerology:</span> 
                    <span class="result-value">{{{{ result.pythagorean }}}}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Chaldean Numerology:</span> 
                    <span class="result-value">{{{{ result.chaldean }}}}</span>
                </div>
                <p style="margin-top: 15px; font-size: 14px; color: var(--text-muted);">
                    <strong>Input:</strong> "{{{{ input_name }}}}"
                </p>
            </div>
        {{% endif %}}
    </div>
    
    {THEME_SCRIPT}
</body>
</html>
"""

# Lo Shu Grid template
LO_SHU_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Lo Shu Grid Generator - Numerology Tools</title>
    <style>
        {BASE_STYLES}
        
        h1 {{
            color: var(--text-color);
            text-align: center;
            margin-bottom: 30px;
        }}

        .date-form {{
            margin: 20px 0;
        }}

        .date-inputs {{
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}

        .date-input {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .date-input label {{
            margin-bottom: 5px;
            font-weight: bold;
            color: var(--text-secondary);
        }}

        .date-input input {{
            padding: 8px 12px;
            border: 2px solid var(--border-color);
            border-radius: 5px;
            font-size: 16px;
            background-color: var(--container-bg);
            color: var(--text-color);
            text-align: center;
            width: 80px;
        }}

        .date-input input:focus {{
            outline: none;
            border-color: var(--accent-color);
        }}

        .submit-btn {{
            text-align: center;
            margin: 20px 0;
        }}

        .submit-btn input {{
            background-color: var(--accent-color);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }}

        .submit-btn input:hover {{
            background-color: var(--accent-hover);
        }}

        .grid-container {{
            display: flex;
            justify-content: center;
            margin: 30px 0;
        }}

        .lo-shu-grid {{
            display: grid;
            grid-template-columns: repeat(3, 80px);
            grid-template-rows: repeat(3, 80px);
            gap: 2px;
            background-color: var(--accent-color);
            border-radius: 10px;
            padding: 10px;
        }}

        .grid-cell {{
            background-color: var(--container-bg);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            color: var(--text-color);
            border-radius: 5px;
        }}

        .grid-numbers {{
            color: var(--accent-color);
        }}

        .analysis {{
            margin-top: 30px;
            padding: 20px;
            background-color: var(--results-bg);
            border-radius: 10px;
            border-left: 4px solid var(--accent-color);
        }}

        .analysis h3 {{
            color: var(--text-color);
            margin-top: 0;
        }}

        .analysis-section {{
            margin: 15px 0;
        }}

        .analysis-section h4 {{
            color: var(--accent-color);
            margin-bottom: 8px;
        }}

        .analysis-section p {{
            color: var(--text-secondary);
            line-height: 1.6;
        }}

        .number-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 0;
        }}

        .number-tag {{
            background-color: var(--accent-color);
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 14px;
            font-weight: bold;
        }}

        .missing-tag {{
            background-color: #f44336;
        }}
    </style>
</head>
<body data-theme="light">
    <button class="theme-toggle" onclick="toggleTheme()" title="Toggle theme">
        <span id="theme-icon">🌙</span>
    </button>
    
    <div class="nav-header">
        <h1>Lo Shu Grid Generator</h1>
        <div class="nav-links">
            <a href="/">← Back to Home</a>
            <a href="/name-calculator">Name Calculator</a>
        </div>
    </div>
    
    <div class="container">
        <form method="post" class="date-form">
            <div class="date-inputs">
                <div class="date-input">
                    <label>Day:</label>
                    <input type="number" name="day" min="1" max="31" required value="{{{{ day or '' }}}}">
                </div>
                <div class="date-input">
                    <label>Month:</label>
                    <input type="number" name="month" min="1" max="12" required value="{{{{ month or '' }}}}">
                </div>
                <div class="date-input">
                    <label>Year:</label>
                    <input type="number" name="year" min="1900" max="2100" required value="{{{{ year or '' }}}}">
                </div>
            </div>
            <div class="submit-btn">
                <input type="submit" value="Generate Lo Shu Grid">
            </div>
        </form>

        {{% if grid_data %}}
            <div class="grid-container">
                <div class="lo-shu-grid">
                    {{% for cell in grid_data.grid %}}
                        <div class="grid-cell">
                            <span class="grid-numbers">{{{{ cell if cell else '' }}}}</span>
                        </div>
                    {{% endfor %}}
                </div>
            </div>

            <div class="analysis">
                <h3>Your Lo Shu Grid Analysis</h3>
                
                <div class="analysis-section">
                    <h4>Birth Date:</h4>
                    <p>{{{{ grid_data.date_string }}</p>
                </div>

                <div class="analysis-section">
                    <h4>Present Numbers:</h4>
                    <div class="number-list">
                        {{% for num in grid_data.present_numbers %}}
                            <span class="number-tag">{{{{ num }}}}</span>
                        {{% endfor %}}
                    </div>
                    <p>These numbers represent your natural strengths and talents.</p>
                </div>

                <div class="analysis-section">
                    <h4>Missing Numbers:</h4>
                    <div class="number-list">
                        {{% for num in grid_data.missing_numbers %}}
                            <span class="number-tag missing-tag">{{{{ num }}}}</span>
                        {{% endfor %}}
                    </div>
                    <p>These numbers represent areas for growth and development in your life.</p>
                </div>

                <div class="analysis-section">
                    <h4>Total Numbers:</h4>
                    <p><strong>{{{{ grid_data.total_count }}</strong> numbers from your birth date</p>
                </div>
            </div>
        {{% endif %}}
    </div>
    
    {THEME_SCRIPT}
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

def generate_lo_shu_grid(day, month, year):
    """Generate Lo Shu Grid from birth date"""
    # Combine all digits from the birth date
    date_string = f"{day:02d}{month:02d}{year}"
    all_digits = [int(d) for d in date_string if d != '0']  # Remove zeros
    
    # Count occurrences of each number 1-9
    number_counts = {}
    for i in range(1, 10):
        number_counts[i] = all_digits.count(i)
    
    # Create the grid (Lo Shu magic square positions)
    # Traditional Lo Shu square:
    # 4 9 2
    # 3 5 7
    # 8 1 6
    lo_shu_positions = [4, 9, 2, 3, 5, 7, 8, 1, 6]
    
    # Fill grid based on number counts
    grid = []
    for pos in lo_shu_positions:
        count = number_counts[pos]
        if count > 0:
            grid.append(str(pos) * count)  # Repeat number based on count
        else:
            grid.append('')  # Empty if not present
    
    # Analyze the grid
    present_numbers = [i for i in range(1, 10) if number_counts[i] > 0]
    missing_numbers = [i for i in range(1, 10) if number_counts[i] == 0]
    
    return {
        'grid': grid,
        'present_numbers': present_numbers,
        'missing_numbers': missing_numbers,
        'total_count': len(all_digits),
        'date_string': f"{day}/{month}/{year}",
        'number_counts': number_counts
    }

@app.route("/")
def home():
    return HOME_TEMPLATE

@app.route("/name-calculator", methods=["GET", "POST"])
def name_calculator():
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
    
    return render_template_string(NAME_CALC_TEMPLATE, result=result, input_name=input_name)

@app.route("/lo-shu-grid", methods=["GET", "POST"])
def lo_shu_grid():
    grid_data = None
    day = month = year = None
    
    if request.method == "POST":
        try:
            day = int(request.form.get("day", ""))
            month = int(request.form.get("month", ""))
            year = int(request.form.get("year", ""))
            
            # Validate date
            if 1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100:
                grid_data = generate_lo_shu_grid(day, month, year)
            
        except (ValueError, TypeError):
            pass  # Invalid input, show form again
    
    return render_template_string(LO_SHU_TEMPLATE, grid_data=grid_data, day=day, month=month, year=year)

# For Vercel
if __name__ == "__main__":
    app.run(debug=True)
