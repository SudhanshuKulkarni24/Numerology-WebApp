from flask import Flask, request, render_template_string
import traceback
import logging

app = Flask(__name__)

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Your existing numerology dictionaries
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

# Error handling decorator
def handle_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Error in {f.__name__}: {str(e)}")
            app.logger.error(traceback.format_exc())
            return render_template_string(ERROR_TEMPLATE, error=str(e)), 500
    wrapper.__name__ = f.__name__
    return wrapper

# Error page template
ERROR_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Error - Numerology Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .error-container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 5px solid #ff4444;
        }
        h1 { color: #ff4444; }
        .error-message {
            background-color: #ffebee;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            font-family: monospace;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <h1>🚨 Something went wrong!</h1>
        <p>We encountered an error while processing your request.</p>
        <div class="error-message">
            {{ error }}
        </div>
        <a href="/" class="back-link">← Back to Home</a>
        <p style="margin-top: 30px; font-size: 12px; color: #666;">
            If this error persists, please check the server logs for more details.
        </p>
    </div>
</body>
</html>
"""

# Losho Grid calculation functions
def create_losho_grid(name, birth_date):
    """Create a Losho grid from name and birth date"""
    try:
        # Basic Losho grid logic (you may need to adjust this based on your requirements)
        grid = [[0 for _ in range(3)] for _ in range(3)]
        
        # Calculate numbers from name
        name_numbers = []
        for char in name.upper():
            if char.isalpha():
                name_numbers.append(pythagorean[char])
        
        # Calculate numbers from birth date
        birth_numbers = []
        for char in birth_date:
            if char.isdigit():
                birth_numbers.append(int(char))
        
        # Combine all numbers
        all_numbers = name_numbers + birth_numbers
        
        # Count occurrences of each number (1-9)
        number_counts = {}
        for num in all_numbers:
            if 1 <= num <= 9:
                number_counts[num] = number_counts.get(num, 0) + 1
        
        # Fill the grid (traditional Losho grid positions)
        # Grid positions: 1=bottom-left, 2=bottom-center, 3=bottom-right
        #                4=middle-left, 5=middle-center, 6=middle-right
        #                7=top-left,    8=top-center,    9=top-right
        
        grid_positions = {
            1: (2, 0), 2: (2, 1), 3: (2, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (0, 0), 8: (0, 1), 9: (0, 2)
        }
        
        for num, count in number_counts.items():
            row, col = grid_positions[num]
            grid[row][col] = count
        
        return grid, number_counts
    
    except Exception as e:
        app.logger.error(f"Error creating Losho grid: {str(e)}")
        raise

# Losho Grid HTML Template
LOSHO_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Losho Grid Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
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
        h1 { text-align: center; color: #333; }
        .form-group {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input[type="text"], input[type="date"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        .losho-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2px;
            max-width: 300px;
            margin: 20px auto;
            background-color: #333;
            padding: 2px;
        }
        .grid-cell {
            background-color: white;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #333;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .grid-cell.filled {
            background-color: #e8f5e8;
            color: #4CAF50;
        }
        .results {
            margin-top: 30px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }
        .number-analysis {
            margin: 10px 0;
            padding: 10px;
            background-color: white;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔢 Losho Grid Calculator</h1>
        
        <form method="post">
            <div class="form-group">
                <label>Full Name:</label>
                <input type="text" name="name" required placeholder="Enter your full name" value="{{ input_name }}">
            </div>
            
            <div class="form-group">
                <label>Birth Date:</label>
                <input type="date" name="birth_date" required value="{{ input_birth_date }}">
            </div>
            
            <input type="submit" value="Generate Losho Grid">
        </form>

        {% if result %}
            <div class="results">
                <h2>Your Losho Grid:</h2>
                
                <div class="losho-grid">
                    {% for row in result.grid %}
                        {% for cell in row %}
                            <div class="grid-cell {% if cell > 0 %}filled{% endif %}">
                                {{ cell if cell > 0 else '' }}
                            </div>
                        {% endfor %}
                    {% endfor %}
                </div>
                
                <div class="number-analysis">
                    <h3>Number Analysis:</h3>
                    {% for num, count in result.number_counts.items() %}
                        <div>Number {{ num }}: {{ count }} occurrence(s)</div>
                    {% endfor %}
                </div>
                
                <p style="text-align: center; margin-top: 20px;">
                    <strong>Name:</strong> {{ input_name }}<br>
                    <strong>Birth Date:</strong> {{ input_birth_date }}
                </p>
            </div>
        {% endif %}
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/">← Back to Numerology Calculator</a>
        </div>
    </div>
</body>
</html>
"""

# Your existing functions
def calculate_numerology(name, mapping):
    total = 0
    for char in name:
        if char.isalpha():
            total += mapping[char.upper()]
    return total

def reduce_to_single_digit(number):
    while number > 9:
        number = sum(int(digit) for digit in str(number))
    return number

# Routes
@app.route("/")
@handle_errors
def index():
    # Your existing numerology calculator code
    result = None
    input_name = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            input_name = name
            pythagorean_total = calculate_numerology(name, pythagorean)
            chaldean_total = calculate_numerology(name, chaldean)
            pythagorean_reduced = reduce_to_single_digit(pythagorean_total)
            chaldean_reduced = reduce_to_single_digit(chaldean_total)
            
            result = {
                "pythagorean": pythagorean_reduced,
                "chaldean": chaldean_reduced,
                "pythagorean_total": pythagorean_total,
                "chaldean_total": chaldean_total
            }
    
    return render_template_string(HTML_TEMPLATE, result=result, input_name=input_name)

@app.route("/losho", methods=["GET", "POST"])
@handle_errors
def losho_grid():
    result = None
    input_name = ""
    input_birth_date = ""
    
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        birth_date = request.form.get("birth_date", "").strip()
        
        if name and birth_date:
            input_name = name
            input_birth_date = birth_date
            
            grid, number_counts = create_losho_grid(name, birth_date)
            
            result = {
                "grid": grid,
                "number_counts": number_counts
            }
    
    return render_template_string(LOSHO_TEMPLATE, 
                                result=result, 
                                input_name=input_name,
                                input_birth_date=input_birth_date)

# Global error handler
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal error: {error}")
    return render_template_string(ERROR_TEMPLATE, error="Internal server error occurred"), 500

if __name__ == "__main__":
    app.run(debug=True)
