from flask import Flask, flash, redirect, request, render_template, url_for
from forms import LoginForm, PredictionForm
from Functions import prepareModel, makePrediction, getAccuracy
from Dash_Visuals import dash_visuals_init

app = Flask(__name__)
dash_visuals_init(app)

app.config['SECRET_KEY'] = '277881c85ffabd4550bbe7cd276ca579'
loggedIn = False

# Prepare Dataframe and Fit Models
ratingModelFit, sentimentModelFit = prepareModel()


@app.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()
    global loggedIn
    loggedIn = False
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            loggedIn = True
            return redirect(url_for('home'))
        else:
            flash("Incorrect Login", 'danger')
    return render_template("index.html", form=form)


@app.route("/home", methods=['GET', 'POST'])
def home():
    global loggedIn
    if loggedIn:
        form = PredictionForm()
        return render_template("home.html", form=form, title='WGU Hotel Review Analysis')
    else:
        return redirect(url_for('index'))


@app.route("/prediction", methods=['GET', 'POST'])
def prediction():
    global loggedIn
    if loggedIn:
        reviewText = request.form['reviewText']
        reviewTitle = request.form['reviewTitle']
        estRating, estSentiment = makePrediction(reviewText, reviewTitle, ratingModelFit, sentimentModelFit)
        mae, accuracy = getAccuracy()
        return render_template("prediction.html", title="Rating Prediction", estRating=estRating,
                               estSentiment=estSentiment, mae=mae, accuracy=accuracy)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

