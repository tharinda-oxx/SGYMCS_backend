import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request
from waitress import serve
from werkzeug.utils import secure_filename

model = tf.keras.models.load_model('models/slimfatmodel1.h5')


def prepare_image(file):
    """this function use for image resize"""
    data =request.files['file']
    filename= secure_filename(skinimagefile.filename)
    file_path = f'Store/Bulk/{filename}'
    skinimagefile.save(file_path)
    img = Image.open(file_path)
    img = np.array(img)
    img = tf.image.resize(img, (256,256))
    img = np.expand_dims(img/255,0)
    return predict_result(img)


def predict_result(img):
    """this function for turing the threshold value for binary classifier"""
    if model.predict(img)[0][0] > 0.5:
        return jsonify({
            'result': 'pass',
            'predict':'fat'}),200

# Cardio session(before workout) 
# Treadmill 20 minutes 
# Cycling 10 minutes
# Stretching 5 minutes

# Day 1 (low weight) 
# D/B pullover  15*3
# M Chest press  15*3
# D/B flys  12*3
# Incline D/B press 15*3
# Dicline press 15*3
# Triceps extention 12*3
# Triceps push down 15*3

# Day  2
# D/B full squat 10*3
# Leg extension 10*3
# Leg curl  10*3
# Calf 10*3
# Cable rowing 15*3
# One arm dumbell rowing  10*3
# Let pull down 15*3
# Back pull down  12*3
# State arm pull down 12*3
# Good morning 10*3

# Day 3
# M Shoulder press  12*3
# D/B shoulder press 12*3
# Side laters 10*3
# Shrugs 10*3
# B/B curl 10*3
# D/B curl 10*3
# Hamer curl  10*3
# Wrist curl 12*3

# Abdominal (whole 3 days) 
# Lain leg raises  10*3
# Alternative leg raises  10*3
# Situps 15*3
# Stick side bend 100*3
# D/B side bend 100*3
# M twistig 100*3
#         },200)
    else:
        return jsonify({
            'result':'pass',
            'predict':'slim',
            'Shedule 1':
            'Cardio session' '(before workout), Cross trainer 15 mins, Warmup (before workouts), Jumping jack 20*3, Stretching', 
            'Day 1':
            'Full squat 10*3, Leg curl 10*3, Calf 15*3, Front press  10*3, D/B front later  10*3, D/B side later  10*3, B/B shrugs 12*3, D/B curl 10*3, Z bar curl 10*3, Precher curl 10*3, Reverse curl  10*3,Wrist curl 15*3',
            'Day 2':
            'Bench press 12*3, D/B press 10*3, Incline press 12*3, Dicline press 12*3, B/B pullover 10*3, Cable rowing 15*3, One arm rowing 10*3, Back pull down 15*3, Cable pull down 12*3, Triceps extention 12*3, Z bar Triceps extension 10*3,Triceps Lain down extension 12*3',
            'Abdominal':
            'Incline Situps 15*3, Crunches 15*3, Leg raises 15*3, Leg up situps 15*3, Stick side bend 100*3, D/B side bend 100*3, M twistig 100*3, Warm down Stretching'
            }),200      


app = Flask(__name__)

@app.route('/predict', methods=['GET', 'POST'])
def infer_image():
    """Catch the image file from a POST request"""
    file = request.files['file']
    # Read the image via file.stream
    try:
        if file != None:
            print(type(file))
            print("File found")
            return prepare_image(file)
        else:
            print("File not found")
            return jsonify({'result': 'Failed'}), 404
    except Exception as e:
        print(e)
        return jsonify({'result': 'Failed'}),   404

@app.route('/', methods=['GET'])
def index():
    return 'Deep CNN Body Type classifier'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=5000)
    #serve(app, host='0.0.0.0',port=5000)
