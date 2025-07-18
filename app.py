from flask import Flask, render_template, request, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session usage

# Load tourist places from JSON
with open('places.json', 'r', encoding='utf-8') as f:
    places = json.load(f)

# Step 1: Home page with dropdown to select state
@app.route('/')
def index():
    unique_states = sorted(set(p['state'].strip() for p in places))
    return render_template('index.html', states=unique_states)

# Step 2: Save selected state and show loading screen
@app.route('/loading', methods=['POST'])
def loading():
    selected_state = request.form.get('state_select')
    if not selected_state:
        return "No state selected."
    session['selected_state'] = selected_state.strip()
    return render_template('loading.html')

# ✅ Step 3: After loading, fetch filtered places and show results
@app.route('/recommend')
def recommend():
    selected_state = session.get('selected_state')
    if not selected_state:
        return "No state selected."

    # Filter places matching selected state (case-insensitive)
    recommended_places = [
        p for p in places
        if p['state'].strip().lower() == selected_state.strip().lower()
    ]

    return render_template(
        'results.html',
        recommended_places=recommended_places,
        selected_state=selected_state
    )

# Start the app
if __name__ == '__main__':
    app.run(debug=True)
