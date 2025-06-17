from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

class DummyModel:
    def predict(self, X):
        return [1523]

model = DummyModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_simulated_farm_data')
def get_simulated_farm_data():
    df = pd.read_csv('cassava_farm_data.csv')
    X = df[['soil_moisture', 'temperature']].iloc[-1].values.reshape(1, -1)
    predicted_yield = int(model.predict(X)[0])
    return jsonify({
        'months': df['date'].tolist(),
        'yields': df['yield_prediction'].tolist(),
        'soil_moisture': df['soil_moisture'].tolist(),
        'temperature': df['temperature'].tolist(),
        'predicted_yield': predicted_yield
    })

@app.route('/initiate_loan_request', methods=['POST'])
def initiate_loan_request():
    data = request.get_json()
    borrower = data.get('borrowerAddress')
    predicted_yield = data.get('predictedYield')

    if not borrower or predicted_yield is None:
        return jsonify({'success': False, 'message': 'Missing data'}), 400

    session[borrower] = {
        'status': 'pending',
        'contractAddress': None,
        'threshold': None,
        'predicted_yield': predicted_yield
    }

    return jsonify({'success': True, 'status': 'pending'})

@app.route('/get_loan_status/<address>')
def get_loan_status(address):
    return jsonify(session.get(address, {'status': 'not_initiated'}))

@app.route('/update_loan_status', methods=['POST'])
def update_loan_status():
    data = request.get_json()
    borrower = data.get('borrowerAddress')
    status = data.get('status')
    contract_address = data.get('contractAddress', None)

    if not borrower or not status:
        return jsonify({'success': False, 'message': 'Missing data'}), 400

    existing = session.get(borrower, {})
    if status == 'authorized':
        existing.update({
            'status': status,
            'contractAddress': contract_address or "0xc5cE95ec9D9178d62ED2F68c51bc03aBe05A5F2c",
            'threshold': existing.get('predicted_yield', 3000)
        })
    else:
        existing.update({
            'status': status,
            'contractAddress': None,
            'threshold': None
        })

    session[borrower] = existing
    return jsonify({'success': True, 'status': status})

@app.route('/reset_session/<address>', methods=['POST'])
def reset_session(address):
    if address in session:
        session.pop(address)
    session[address] = {'status': 'not_initiated', 'contractAddress': None, 'threshold': None, 'predicted_yield': None}
    return jsonify({'success': True})

@app.route('/get_federated_insights')
def get_federated_insights():
    try:
        csv_path = 'federated_farm_data.csv'
        if not os.path.exists(csv_path):
            print("[ERROR] File does not exist")
            return jsonify({'error': 'CSV file not found'}), 500

        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        print("[INFO] Columns found:", df.columns.tolist())
        print("[INFO] Preview rows:", df.head(2).to_dict(orient='records'))

        required_columns = {'farm_id', 'region', 'asset_type', 'yield_prediction', 'credit_score'}
        if not required_columns.issubset(set(df.columns)):
            missing = required_columns - set(df.columns)
            print("[ERROR] Missing columns:", missing)
            return jsonify({'error': f'Missing required fields in CSV: {missing}'}), 500

        return jsonify(df[list(required_columns)].to_dict(orient='records'))

    except Exception as e:
        print("[ERROR] Exception in /get_federated_insights:", str(e))
        return jsonify({'error': str(e)}), 500
