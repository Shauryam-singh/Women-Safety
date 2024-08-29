from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video-analysis')
def video_analysis():
    return render_template('video_analysis.html')

@app.route('/speech-analysis')
def speech_analysis():
    return render_template('speech_analysis.html')

@app.route('/behavior-analysis')
def behavior_analysis():
    return render_template('behavior_analysis.html')

@app.route('/route-finder', methods=['GET', 'POST'])
def route_finder():
    if request.method == 'POST':
        # Handle route finding logic here
        data = request.json
        # Example response
        return jsonify({
            "message": "Route data processed",
            "data": data
        })
    return render_template('route_finder.html')

if __name__ == '__main__':
    app.run(debug=True)
