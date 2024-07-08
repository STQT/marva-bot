from flask import Flask, render_template, request, make_response, redirect
from telebot import TeleBot

app = Flask(__name__)
bot = TeleBot('TOKEN')

FEEDBACK_FILE = 'feedback.txt'

def save_feedback(star):
    with open(FEEDBACK_FILE, 'a') as f:
        f.write(f"{star}\n")


def calculate_average_rating():
    try:
        with open(FEEDBACK_FILE, 'r') as f:
            ratings = [int(line.strip()) for line in f.readlines() if line.strip().isdigit()]
        if ratings:
            average_rating = sum(ratings) / len(ratings)
            return round(average_rating, 2)
        else:
            return None
    except FileNotFoundError:
        return Р

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    star = request.form['star']
    feedback = request.form['feedback']

    # Save the star rating to the file
    save_feedback(star)

    # Send feedback message to Telegram
    average = calculate_average_rating()
    text = f"<b>У вас новый отзыв: \nЗвезды: {star}⭐️\nОтзыв: <i>{feedback}</i>\nРейтинг: {average}/5⭐️</b>"
    bot.send_message(-1002158533403, text, parse_mode='html')

    # Set a cookie to prevent multiple submissions
    response = make_response(render_template('thank_you.html'))

    return response 


app.run(host='0.0.0.0')