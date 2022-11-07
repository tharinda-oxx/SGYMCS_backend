import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request
from waitress import serve
from werkzeug.utils import secure_filename

model = tf.keras.models.load_model('models/slimfatmodel1.h5')


def prepare_image(img):
    """this function use for image resize"""
    #file_path = f'Store/{file}'
    #img = Image.open(file_path)
    img = np.array(img)
    img = tf.image.resize(img, (256,256))
    img = np.expand_dims(img/255,0)
    return predict_result(img)


def predict_result(img):
    """this function for turing the threshold value for binary classifier"""
    if model.predict(img)[0][0] > 0.5:
        return jsonify({
            'result': 'pass',
            'predict':'fat',
            'Shedule_(before_workout)':{
                'Fat man shedule','Cardio session,'Treadmill 20 minutes','Cycling 10 minutes','Stretching 5 minutes'},
            'Day_1':{
                'Day 1 (low weight)','D/B pullover  15*3','M Chest press  15*3','D/B flys  12*3','Incline D/B press 15*3','Dicline press 15*3','Triceps extention 12*3','Triceps push down 15*3'},
            'Day_2':{
                'D/B full squat 10*3','Leg extension 10*3','Leg curl  10*3','Calf 10*3','Cable rowing 15*3','One arm dumbell rowing  10*3','Let pull down 15*3','Back pull down  12*3','State arm pull down 12*3','Good morning 10*3'},
            'Day_3':{
                'M Shoulder press  12*3','D/B shoulder press 12*3','Side laters 10*3','Shrugs 10*3','B/B curl 10*3','D/B curl 10*3','Hamer curl  10*3','Wrist curl 12*3'},
            'Abdominal (whole 3 days)':{ 
                'Lain leg raises  10*3','Alternative leg raises  10*3','Situps 15*3','Stick side bend 100*3','D/B side bend 100*3','M twistig 100*3','Stretching'},
            'meal_plan':{
                'Breakfast (8am)':
                    {'Oats 100g'}, 
                '12 noon':
                    {'Watermelon juice'},
                'Lunch (1am)':
                    {'Red rice 100g','Beans 100g','Eggs 2 ( white)'}, 
                '5pm':
                    {'1 Banana'},
                '8pm dinner':
                    {'Vegetables 300g','Eggs 4 (white)','Papaya'},
                'daily':
                    {'Water 4L'}}
            }
        
        ),200
    else:
        return jsonify(
            {
            'result':'pass',
            'predict':'slim',
            'Shedule_(before_workout)':{
                'Cardio_session', 'Cross trainer 15 mins', 'Warmup', 'Jumping jack 20*3', 'Stretching'}, 
            'Day_1':{
                'Full squat 10*3', 'Leg curl 10*3', 'Calf 15*3', 'Front press  10*3', 'D/B front later  10*3', 'D/B side later  10*3', 'B/B shrugs 12*3', 'D/B curl 10*3', 'Z bar curl 10*3', 'Precher curl 10*3', 'Reverse curl  10*3','Wrist curl 15*3'},
            'Day_2':{
                'Bench press 12*3', 'D/B press 10*3', 'Incline press 12*3', 'Dicline press 12*3', 'B/B pullover 10*3', 'Cable rowing 15*3', 'One arm rowing 10*3', 'Back pull down 15*3', 'Cable pull down 12*3', 'Triceps extention 12*3', 'Z bar Triceps extension 10*3','Triceps Lain down extension 12*3'},
            'Abdominal':{
                'Incline Situps 15*3', 'Crunches 15*3', 'Leg raises 15*3', 'Leg up situps 15*3', 'Stick side bend 100*3', 'D/B side bend 100*3', 'M twistig 100*3', 'Warm down Stretching'},
            'meal_plan':{
                'Breakfast (8am)':
                    {'Dhal/ green gram 200g','4 Eggs','1 banana'},
                '11am':
                    {'Peanuts 150g','Yougurt 1'},
                'Lunch (1pm)':
                    {'Chicken breast 200g','Spinach 200g','Red rice 300g','Papaya /Avacado / watermelon juice 600ml'},
                '4.30 pm':
                    {'Dates 50g','Oats100g','Fresh milk 200ml (milk shake)'},
                '6.30pm':
                    {'Sandwich bread','4 Eggs ( white)'},
                'Dinner (8pm)':
                    {'salad ( brocholi 150g', 'carrot 100g', 'beans 100g','Chicken 100g','1 banana','Water 4L (daily)'}}
            }
        ),200      


app = Flask(__name__)

@app.route('/predict', methods=['GET', 'POST'])
def infer_image():
    """Catch the image file from a POST request"""
    file = request.files['file']
    filename= secure_filename(file.filename)
    file_path = f'Store/{filename}'
    file.save(file_path)
    # Read the image via file.stream
    img = Image.open(file_path)
    try:
        if img != None:
            print(type(img))
            print("File found")
            return prepare_image(img)
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
