from flask import Flask, request, render_template_string
from datetime import datetime
import logging

app = Flask(__name__)

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

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

# JavaScript for theme toggle - Fixed to work without localStorage
THEME_SCRIPT = """
    <script>
        // Use a simple variable instead of localStorage
        let currentTheme = 'light';
        
        function toggleTheme() {
            const body = document.body;
            const themeIcon = document.getElementById('theme-icon');
            
            if (currentTheme === 'light') {
                body.setAttribute('data-theme', 'dark');
                themeIcon.textContent = '☀️';
                currentTheme = 'dark';
            } else {
                body.setAttribute('data-theme', 'light');
                themeIcon.textContent = '🌙';
                currentTheme = 'light';
            }
        }
        
        function loadTheme() {
            const body = document.body;
            const themeIcon = document.getElementById('theme-icon');
            
            body.setAttribute('data-theme', currentTheme);
            themeIcon.textContent = currentTheme === 'dark' ? '☀️' : '🌙';
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

# Name calculator template - Fixed template syntax
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

# Lo Shu Grid template - Enhanced with better visuals and numerology meanings
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

        .intro-section {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, var(--accent-color), #66BB6A);
            border-radius: 15px;
            color: white;
        }}

        .intro-section h2 {{
            margin: 0 0 10px 0;
            font-size: 1.8em;
        }}

        .intro-section p {{
            margin: 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}

        .date-form {{
            margin: 30px 0;
        }}

        .date-inputs {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 25px;
        }}

        .date-input {{
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: var(--container-bg);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px var(--shadow);
            transition: transform 0.2s ease;
        }}

        .date-input:hover {{
            transform: translateY(-2px);
        }}

        .date-input label {{
            margin-bottom: 8px;
            font-weight: bold;
            color: var(--accent-color);
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .date-input input {{
            padding: 12px;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-size: 18px;
            background-color: var(--container-bg);
            color: var(--text-color);
            text-align: center;
            width: 90px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}

        .date-input input:focus {{
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2);
            transform: scale(1.05);
        }}

        .submit-btn {{
            text-align: center;
            margin: 30px 0;
        }}

        .submit-btn input {{
            background: linear-gradient(135deg, var(--accent-color), #66BB6A);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }}

        .submit-btn input:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }}

        .grid-section {{
            text-align: center;
            margin: 40px 0;
        }}

        .grid-container {{
            display: flex;
            justify-content: center;
            margin: 30px 0;
            position: relative;
        }}

        .lo-shu-grid {{
            display: grid;
            grid-template-columns: repeat(3, 100px);
            grid-template-rows: repeat(3, 100px);
            gap: 3px;
            background: linear-gradient(135deg, var(--accent-color), #66BB6A);
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 8px 30px rgba(76, 175, 80, 0.3);
        }}

        .grid-cell {{
            background-color: var(--container-bg);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
            color: var(--text-color);
            border-radius: 8px;
            position: relative;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .grid-cell:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 15px var(--shadow);
        }}

        .grid-cell.empty {{
            background-color: rgba(244, 67, 54, 0.1);
            border: 2px dashed #f44336;
        }}

        .grid-numbers {{
            color: var(--accent-color);
        }}

        .grid-legend {{
            margin: 20px 0;
            padding: 15px;
            background-color: var(--container-bg);
            border-radius: 10px;
            border: 1px solid var(--border-color);
        }}

        .legend-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid var(--border-color);
        }}

        .legend-row:last-child {{
            border-bottom: none;
        }}

        .legend-position {{
            font-weight: bold;
            color: var(--accent-color);
        }}

        .legend-meaning {{
            color: var(--text-secondary);
            font-size: 14px;
        }}

        .analysis {{
            margin-top: 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}

        .analysis-card {{
            padding: 25px;
            background-color: var(--container-bg);
            border-radius: 15px;
            box-shadow: 0 4px 20px var(--shadow);
            border-left: 4px solid var(--accent-color);
            transition: transform 0.3s ease;
        }}

        .analysis-card:hover {{
            transform: translateY(-5px);
        }}

        .analysis-card h3 {{
            color: var(--accent-color);
            margin-top: 0;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .analysis-card .icon {{
            font-size: 1.5em;
        }}

        .analysis-section {{
            margin: 20px 0;
        }}

        .analysis-section h4 {{
            color: var(--accent-color);
            margin-bottom: 12px;
            font-size: 1.1em;
        }}

        .analysis-section p {{
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 15px;
        }}

        .number-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }}

        .number-tag {{
            background: linear-gradient(135deg, var(--accent-color), #66BB6A);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
            transition: transform 0.2s ease;
        }}

        .number-tag:hover {{
            transform: scale(1.1);
        }}

        .missing-tag {{
            background: linear-gradient(135deg, #f44336, #ef5350);
            box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
        }}

        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .stat-item {{
            text-align: center;
            padding: 15px;
            background-color: var(--results-bg);
            border-radius: 10px;
            border: 1px solid var(--border-color);
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: var(--accent-color);
            display: block;
        }}

        .stat-label {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .meanings-section {{
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(102, 187, 106, 0.1));
            border-radius: 15px;
            border: 1px solid var(--border-color);
        }}

        .meanings-section h4 {{
            color: var(--accent-color);
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.3em;
        }}

        .meaning-item {{
            display: flex;
            align-items: flex-start;
            margin: 15px 0;
            padding: 15px;
            background-color: var(--container-bg);
            border-radius: 10px;
            box-shadow: 0 2px 10px var(--shadow);
        }}

        .meaning-number {{
            background: linear-gradient(135deg, var(--accent-color), #66BB6A);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
            flex-shrink: 0;
        }}

        .meaning-content {{
            flex: 1;
        }}

        .meaning-title {{
            font-weight: bold;
            color: var(--text-color);
            margin-bottom: 5px;
        }}

        .meaning-desc {{
            color: var(--text-secondary);
            font-size: 14px;
            line-height: 1.5;
        }}

        .error-message {{
            background: linear-gradient(135deg, #ffebee, #ffcdd2);
            color: #c62828;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #f44336;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(244, 67, 54, 0.2);
        }}

        @media (max-width: 768px) {{
            .lo-shu-grid {{
                grid-template-columns: repeat(3, 80px);
                grid-template-rows: repeat(3, 80px);
            }}
            
            .analysis {{
                grid-template-columns: 1fr;
            }}
            
            .date-inputs {{
                flex-direction: column;
                align-items: center;
            }}
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
    
    <div class="intro-section">
        <h2>🔮 Discover Your Destiny Numbers</h2>
        <p>The Lo Shu Grid reveals your personality traits, strengths, and areas for growth based on your birth date numerology</p>
    </div>
    
    <div class="container">
        <form method="post" class="date-form">
            <div class="date-inputs">
                <div class="date-input">
                    <label>Day</label>
                    <input type="number" name="day" min="1" max="31" required value="{{{{ day if day else '' }}}}" placeholder="DD">
                </div>
                <div class="date-input">
                    <label>Month</label>
                    <input type="number" name="month" min="1" max="12" required value="{{{{ month if month else '' }}}}" placeholder="MM">
                </div>
                <div class="date-input">
                    <label>Year</label>
                    <input type="number" name="year" min="1900" max="2100" required value="{{{{ year if year else '' }}}}" placeholder="YYYY">
                </div>
            </div>
            <div class="submit-btn">
                <input type="submit" value="✨ Generate My Grid ✨">
            </div>
        </form>

        {{% if error_message %}}
            <div class="error-message">
                <strong>⚠️ Oops!</strong> {{{{ error_message }}}}
            </div>
        {{% endif %}}

        {{% if grid_data %}}
            <div class="grid-section">
                <h3 style="color: var(--accent-color); text-align: center; margin-bottom: 20px;">
                    🌟 Your Personal Lo Shu Grid 🌟
                </h3>
                
                <div class="grid-container">
                    <div class="lo-shu-grid">
                        {{% for i in range(9) %}}
                            <div class="grid-cell {{{{ 'empty' if not grid_data.grid[i] else '' }}}}" 
                                 title="Position {{{{ [4,9,2,3,5,7,8,1,6][i] }}}}: {{{{ ['Planning & Organization', 'Fame & Recognition', 'Knowledge & Wisdom', 'Patience & Hard Work', 'Mental Strength', 'Love & Care', 'Communication', 'Money & Material', 'Health & Harmony'][i] }}}}">
                                <span class="grid-numbers">{{{{ grid_data.grid[i] if grid_data.grid[i] else '○' }}}}</span>
                            </div>
                        {{% endfor %}}
                    </div>
                </div>

                <div class="grid-legend">
                    <h4 style="text-align: center; margin-bottom: 15px; color: var(--accent-color);">Grid Position Meanings</h4>
                    <div class="legend-row">
                        <span class="legend-position">4 - Planning</span>
                        <span class="legend-position">9 - Fame</span>
                        <span class="legend-position">2 - Knowledge</span>
                    </div>
                    <div class="legend-row">
                        <span class="legend-position">3 - Patience</span>
                        <span class="legend-position">5 - Mental Strength</span>
                        <span class="legend-position">7 - Love</span>
                    </div>
                    <div class="legend-row">
                        <span class="legend-position">8 - Money</span>
                        <span class="legend-position">1 - Communication</span>
                        <span class="legend-position">6 - Health</span>
                    </div>
                </div>

                <div class="analysis">
                    <div class="analysis-card">
                        <h3><span class="icon">📊</span> Your Statistics</h3>
                        <div class="stat-grid">
                            <div class="stat-item">
                                <span class="stat-number">{{{{ grid_data.date_string }}}}</span>
                                <span class="stat-label">Birth Date</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">{{{{ grid_data.present_numbers|length }}}}</span>
                                <span class="stat-label">Active Numbers</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">{{{{ grid_data.missing_numbers|length }}}}</span>
                                <span class="stat-label">Growth Areas</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">{{{{ grid_data.total_count }}}}</span>
                                <span class="stat-label">Total Digits</span>
                            </div>
                        </div>
                    </div>

                    <div class="analysis-card">
                        <h3><span class="icon">💪</span> Your Strengths</h3>
                        <div class="analysis-section">
                            <p>These numbers appear in your birth date and represent your natural talents:</p>
                            <div class="number-list">
                                {{% for num in grid_data.present_numbers %}}
                                    <span class="number-tag" title="Number {{{{ num }}}} strength">{{{{ num }}}}</span>
                                {{% endfor %}}
                            </div>
                            {{% if not grid_data.present_numbers %}}
                                <p style="color: var(--text-muted); font-style: italic;">No specific strengths identified from birth date digits.</p>
                            {{% endif %}}
                        </div>
                    </div>

                    <div class="analysis-card">
                        <h3><span class="icon">🎯</span> Growth Opportunities</h3>
                        <div class="analysis-section">
                            <p>These missing numbers represent areas for personal development:</p>
                            <div class="number-list">
                                {{% for num in grid_data.missing_numbers %}}
                                    <span class="number-tag missing-tag" title="Number {{{{ num }}}} - area for growth">{{{{ num }}}}</span>
                                {{% endfor %}}
                            </div>
                            {{% if not grid_data.missing_numbers %}}
                                <p style="color: var(--accent-color); font-weight: bold;">Amazing! All numbers are present in your birth date.</p>
                            {{% endif %}}
                        </div>
                    </div>
                </div>

                <div class="meanings-section">
                    <h4>🔍 Number Meanings & Life Areas</h4>
                    <div class="meaning-item">
                        <div class="meaning-number">1</div>
                        <div class="meaning-content">
                            <div class="meaning-title">Communication & Leadership</div>
                            <div class="meaning-desc">Expression, speaking ability, leadership qualities, and social connections.</div>
                        </div>
                    </div>
                    <div class="meaning-item">
                        <div class="meaning-number">2</div>
                        <div class="meaning-content">
                            <div class="meaning-title">Knowledge & Intuition</div>
                            <div class="meaning-desc">Learning capacity, wisdom, intuitive abilities, and emotional intelligence.</div>
                        </div>
                    </div>
                    <div class="meaning-item">
                        <div class="meaning-number">3</div>
                        <div class="meaning-content">
                            <div class="meaning-title">Patience & Hard Work</div>
                            <div class="meaning-desc">Perseverance, dedication, ability to work through challenges systematically.</div>
                        </div>
                    </div>
                    <div class="meaning-item">
                        <div class="meaning-number">4</div>
                        <div class="meaning-content">
                            <div class="meaning-title">Planning & Organization</div>
                            <div class="meaning-desc">Systematic thinking, organizational skills, and structured approach to life.</div>
                        </div>
                    </div>
                    <div class="meaning-item">
                        <div class="meaning-number">5</div>
                        <div class="meaning-content">
                            <div class="meaning-title">Mental Strength & Focus</div>
                            <div class="meaning-desc">Mental resilience, concentration, ability to handle stress and pressure.</div>
                        </div>
                    </div>
                    <div class="meaning-item">
                        <div class="meaning-number">6</div>
                        <div class="meaning-content">
                            <div class="meaning-title">Health & Family Harmony</div>
                            <div class="meaning-desc">Physical wellbeing, family relationships, nurturing, and caring nature.</div>
                        </div>
                    </div>
                    <div class="meaning-item">
                        <div class="meaning-number">7</div>
                        <div class="meaning-content">
                            <div class="meaning-title">Love & Relationships</div>
                            <div class="meaning-desc">Emotional connections, romantic relationships, empathy, and compassion.</div>
                        </div>
                    </div>
                    <div class="meaning-item">
                        <div class="meaning-number">8</div>
                        <div class="meaning-content">
                            <div class="meaning-title">Money & Material Success</div>
                            <div class="meaning-desc">Financial acumen, business sense, material achievements, and practical skills.</div>
                        </div>
                    </div>
                    <div class="meaning-item">
                        <div class="meaning-number">9</div>
                        <div class="meaning-content">
                            <div class="meaning-title">Fame & Recognition</div>
                            <div class="meaning-desc">Public recognition, reputation, spiritual growth, and humanitarian nature.</div>
                        </div>
                    </div>
                </div>
            </div>
        {{% endif %}}
    </div>
    
    {THEME_SCRIPT}
</body>
</html>
"""

def calculate_numerology(name, mapping):
    """Calculate numerology value for a name using the given mapping"""
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

def is_valid_date(day, month, year):
    """Validate if the given date is valid"""
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        return False

def generate_lo_shu_grid(day, month, year):
    """Generate Lo Shu Grid from birth date"""
    try:
        # Validate the date first
        if not is_valid_date(day, month, year):
            raise ValueError("Invalid date")
        
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
    except Exception as e:
        app.logger.error(f"Error generating Lo Shu grid: {str(e)}")
        raise

@app.route("/")
def home():
    """Home page route"""
    return HOME_TEMPLATE

@app.route("/name-calculator", methods=["GET", "POST"])
def name_calculator():
    """Name calculator route"""
    result = None
    input_name = ""
    
    try:
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
    except Exception as e:
        app.logger.error(f"Error in name calculator: {str(e)}")
        # Continue with empty result to show form
    
    return render_template_string(NAME_CALC_TEMPLATE, result=result, input_name=input_name)

@app.route("/lo-shu-grid", methods=["GET", "POST"])
def lo_shu_grid():
    """Lo Shu Grid generator route"""
    grid_data = None
    day = month = year = None
    error_message = None
    
    try:
        if request.method == "POST":
            try:
                day = int(request.form.get("day", ""))
                month = int(request.form.get("month", ""))
                year = int(request.form.get("year", ""))
                
                # Validate date ranges
                if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100):
                    error_message = "Please enter valid date ranges: Day (1-31), Month (1-12), Year (1900-2100)"
                elif not is_valid_date(day, month, year):
                    error_message = "Please enter a valid date (e.g., February 29th only exists in leap years)"
                else:
                    grid_data = generate_lo_shu_grid(day, month, year)
                    
            except (ValueError, TypeError) as e:
                app.logger.error(f"Invalid input in Lo Shu grid: {str(e)}")
                error_message = "Please enter valid numbers for day, month, and year"
                # Keep the input values for user convenience
                day = request.form.get("day", "")
                month = request.form.get("month", "")  
                year = request.form.get("year", "")
                
    except Exception as e:
        app.logger.error(f"Unexpected error in Lo Shu grid: {str(e)}")
        error_message = "An unexpected error occurred. Please try again."
    
    return render_template_string(
        LO_SHU_TEMPLATE, 
        grid_data=grid_data, 
        day=day, 
        month=month, 
        year=year,
        error_message=error_message
    )

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    app.logger.error(f"Internal server error: {str(error)}")
    return "Internal Server Error. Please check the logs.", 500

# For Vercel deployment
if __name__ == "__main__":
    app.run(debug=True)
