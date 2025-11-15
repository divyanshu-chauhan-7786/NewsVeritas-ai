from flask import Flask, render_template, request, session, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'truthlens_secret_key_2024'


model_path = "divyanshu-chauhan-7786/fake-news-roberta"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# pipeline with CPU
detector = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1  
)
# Feedback file path
FEEDBACK_FILE = 'feedback.json'

def get_history():
    """Initialize or get history from session"""
    if 'history' not in session:
        session['history'] = []
    return session['history']

def load_feedback():
    """Load feedback from JSON file"""
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_feedback(feedback_data):
    """Save feedback to JSON file"""
    try:
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(feedback_data, f, indent=2)
        return True
    except:
        return False

def get_confidence_level(confidence, prediction):
    """
    Categorize confidence into different levels
    """
    if prediction == 'FAKE':
        if confidence >= 90:
            return {
                'label': 'Highly Likely Fake',
                'description': 'Strong indicators of misinformation',
                'color': '#ff4444',
                'risk': 'Very High',
                'suggestion': 'Verify with multiple trusted sources before sharing'
            }
        elif confidence >= 75:
            return {
                'label': 'Likely Fake',
                'description': 'Multiple signs of unreliable content',
                'color': '#ff7675',
                'risk': 'High',
                'suggestion': 'Exercise caution and verify facts'
            }
        elif confidence >= 60:
            return {
                'label': 'Possibly Fake',
                'description': 'Some questionable elements detected',
                'color': '#fdcb6e',
                'risk': 'Medium',
                'suggestion': 'Investigate further before believing'
            }
        else:
            return {
                'label': 'Uncertain - Leaning Fake',
                'description': 'Minor indicators of misinformation',
                'color': '#ffeaa7',
                'risk': 'Low',
                'suggestion': 'Consider additional verification'
            }
    else:  # REAL prediction
        if confidence >= 90:
            return {
                'label': 'Highly Authentic',
                'description': 'Strong indicators of reliable content',
                'color': '#00b894',
                'reliability': 'Very High',
                'suggestion': 'Content appears highly trustworthy'
            }
        elif confidence >= 75:
            return {
                'label': 'Likely Authentic',
                'description': 'Good indicators of reliable content',
                'color': '#55efc4',
                'reliability': 'High',
                'suggestion': 'Content appears reliable'
            }
        elif confidence >= 60:
            return {
                'label': 'Possibly Authentic',
                'description': 'Some positive indicators found',
                'color': '#81ecec',
                'reliability': 'Medium',
                'suggestion': 'Content seems plausible'
            }
        else:
            return {
                'label': 'Uncertain - Leaning Authentic',
                'description': 'Limited but positive indicators',
                'color': '#74b9ff',
                'reliability': 'Low',
                'suggestion': 'Consider additional verification'
            }

@app.route("/")
@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    prediction, confidence, headline = None, None, None
    error = None
    confidence_level = None
    current_analysis_id = None
    
    if request.method == "POST":
        headline = request.form.get("headline", "").strip()
        text = request.form.get("news_text", "").strip()
        
        if not text:
            error = "Please enter some text to analyze."
        elif len(text) < 10:
            error = "Please enter at least 10 characters for accurate analysis."
        else:
            try:
                result = detector(text, truncation=True, max_length=512)
                label = "FAKE" if result[0]["label"] == "LABEL_1" else "REAL"
                confidence = round(result[0]["score"] * 100, 2)
                prediction = label
                
                # Get confidence level categorization
                confidence_level = get_confidence_level(confidence, prediction)
                
                history = get_history()
                analysis_entry = {
                    'id': len(history) + 1,
                    'headline': headline or "Untitled",
                    'text': text[:150] + '...' if len(text) > 150 else text,
                    'full_text': text,  # Store full text for feedback
                    'prediction': prediction,
                    'confidence': confidence,
                    'confidence_level': confidence_level,
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                history.append(analysis_entry)
                session['history'] = history
                current_analysis_id = len(history)  # Set current analysis ID
                
            except Exception as e:
                error = f"Analysis failed: {str(e)}"
    
    return render_template("analyze.html", 
                         prediction=prediction, 
                         confidence=confidence,
                         confidence_level=confidence_level,
                         headline=headline,
                         error=error,
                         analysis_id=current_analysis_id,
                         active="analyze")

@app.route("/history")
def history():
    history_data = get_history()
    return render_template("history.html", 
                         history=history_data, 
                         active="history")

@app.route("/dashboard")
def dashboard():
    history_data = get_history()
    total_analyses = len(history_data)
    
    # Calculate basic statistics
    fake_count = len([h for h in history_data if h['prediction'] == 'FAKE'])
    real_count = len([h for h in history_data if h['prediction'] == 'REAL'])
    
    if total_analyses > 0:
        avg_confidence = round(sum([h['confidence'] for h in history_data]) / total_analyses, 2)
    else:
        avg_confidence = 0
    
    fake_percentage = round((fake_count / total_analyses * 100), 1) if total_analyses > 0 else 0
    real_percentage = round((real_count / total_analyses * 100), 1) if total_analyses > 0 else 0
    
    return render_template("dashboard.html", 
                         total_analyses=total_analyses,
                         fake_count=fake_count,
                         real_count=real_count,
                         avg_confidence=avg_confidence,
                         fake_percentage=fake_percentage,
                         real_percentage=real_percentage,
                         active="dashboard")

@app.route("/about")
def about():
    return render_template("about.html", active="about")

@app.route("/clear_history")
def clear_history():
    session['history'] = []
    return render_template("history.html", 
                         history=[], 
                         active="history",
                         message="History cleared successfully!")

@app.route("/provide_feedback", methods=["POST"])
def provide_feedback():
    """Store user feedback in JSON file with complete article data"""
    try:
        analysis_id = request.form.get('analysis_id')
        user_correction = request.form.get('user_correction')
        comment = request.form.get('comment', '')
        
        # Get current analysis from session history
        history_data = get_history()
        analysis_data = None
        
        if analysis_id and history_data:
            try:
                analysis_idx = int(analysis_id) - 1
                if 0 <= analysis_idx < len(history_data):
                    analysis_data = history_data[analysis_idx]
            except:
                pass
        
        # Create comprehensive feedback entry with full article data
        feedback_entry = {
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_correction': user_correction,
            'comment': comment,
            'original_analysis': {
                'headline': analysis_data.get('headline', '') if analysis_data else '',
                'full_text': analysis_data.get('full_text', '') if analysis_data else '',
                'prediction': analysis_data.get('prediction', '') if analysis_data else '',
                'confidence': analysis_data.get('confidence', 0) if analysis_data else 0,
                'confidence_level': analysis_data.get('confidence_level', {}) if analysis_data else {},
                'timestamp': analysis_data.get('timestamp', '') if analysis_data else ''
            }
        }
        
        # Load existing feedback and add new entry
        feedback_data = load_feedback()
        feedback_data.append(feedback_entry)
        
        # Save to JSON file
        if save_feedback(feedback_data):
            return jsonify({
                'status': 'success',
                'message': 'Thank you for your feedback!',
                'feedback_count': len(feedback_data)
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to save feedback'
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })

@app.route("/get_feedback_stats")
def get_feedback_stats():
    """Get feedback statistics"""
    feedback_data = load_feedback()
    return jsonify({
        'total_feedback': len(feedback_data),
        'feedback_samples': feedback_data
    })

@app.route("/view_feedback")
def view_feedback():
    """View all stored feedback (for testing)"""
    feedback_data = load_feedback()
    return jsonify(feedback_data)

if __name__ == "__main__":
    app.run(debug=True)