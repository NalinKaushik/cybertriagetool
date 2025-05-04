import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from flask import Flask, request, jsonify

# Dummy dataset (in practice, you'll use real data)
data = {
    'alert_type': ['malware', 'phishing', 'ransomware', 'malware', 'phishing', 'ransomware'],
    'severity': [7, 5, 9, 6, 4, 8],  # 1-10 severity scale
    'source_ip': ['192.168.0.1', '192.168.0.2', '192.168.0.3', '192.168.0.4', '192.168.0.5', '192.168.0.6'],
    'is_true_positive': [1, 0, 1, 1, 0, 1]  # 1 = True Positive, 0 = False Positive
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Feature selection
X = df[['severity']]  # Predicting based on severity (simplified feature)
y = df['is_true_positive']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Test model accuracy
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')

# Flask app to serve model
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_alert():
    data = request.json
    severity = data.get('severity')
    prediction = model.predict([[severity]])  # Predict based on severity
    return jsonify({'prediction': 'True Positive' if prediction[0] == 1 else 'False Positive'})

if __name__ == '__main__':
    app.run(debug=True)
