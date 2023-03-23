from flask import Flask, request
from redis import Redis

app = Flask(__name__)
redis = Redis(host='0.0.0.0', port=6379, db=0)


@app.route('/')
def hello():
    redis.incr('hits')
    counter = str(redis.get('hits'),'utf-8')
    return "This webpage has been viewed "+counter+" time(s)"


@app.route('/predict', methods=['POST'])
def prediction_endpoint():
    
    input_as_json = request.json
    
    message_id = input_as_json['msg_id']
    
    if redis.get(message_id):
        
    
    prediction, predicted_proba = predict([input_as_json['input_data']])
    
    return {
       'prediction_class': int(prediction),
       'prediction_proba': float(predicted_proba[0][int(prediction)])
    }



def predict(x_to_predict):
    from joblib import load
    
    model = load('model.joblib')
    prediction = model.predict(x_to_predict)
    proba = model.predict_proba(x_to_predict)
    
    return prediction, proba



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    