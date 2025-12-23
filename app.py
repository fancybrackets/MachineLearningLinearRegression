from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the NEW trained model (the one that includes carpet_area)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Get 6 inputs from the form (including carpet_area)
        features = [
            float(request.form['carpet_area']),
            float(request.form['bed_room']),
            float(request.form['kitchen']),
            float(request.form['living_room']),
            float(request.form['dining_room']),
            float(request.form['toilet'])
        ]

        # 2. Convert to numpy array
        final_features = [np.array(features)]
        
        # 3. Predict the price
        prediction = model.predict(final_features)
        raw_price = prediction[0]

        # 4. UI Logic: Handle negative results professionally
        if raw_price < 0:
            output_text = "Price estimation unavailable for these small values (Model Limit)"
        else:
            # Format the positive price with commas for the user
            formatted_price = "{:,.2f}".format(raw_price)
            output_text = f"Predicted Flat Price: ₹{formatted_price}"

        return render_template('index.html', prediction_text=output_text)

    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

if __name__ == "__main__":
    app.run(debug=True)