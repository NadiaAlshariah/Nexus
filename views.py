from flask import render_template, request, flash, jsonify
from app import app, db, get_top_interests_and_update
from flask_login import login_required, current_user
from models import Post
import joblib
import numpy as np
import pickle
from keras.preprocessing.sequence import pad_sequences
from models import User, Post, LikedPost
from static.model.text_cleaner import TextCleaner


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home", methods=["POST", "GET"])
@login_required
def home():
    get_top_interests_and_update(current_user.id)
    if request.method == "POST":
        post = request.form.get("post")

        if len(post) < 1:
            flash("Post is too short")
        else:
            if len(post.split()) >= 45:
                model1 = joblib.load("static/model/MODEL1_S&NS.pkl")

                file_path = r"static\model\tokenizer1.pickle"
                with open(file_path, "rb") as handle1:
                    loaded_tokenizer = pickle.load(handle1)

                model2 = joblib.load("static/model/MODEL2_E&F.pkl")

                file_path = r"static\model\tokenizer2.pickle"
                with open(file_path, "rb") as handle2:
                    loaded_tokenizer2 = pickle.load(handle2)

                model3 = joblib.load("static/model/MODEL3_EA&EF.pkl")

                file_path = r"static\model\tokenizer3.pickle"
                with open(file_path, "rb") as handle3:
                    loaded_tokenizer3 = pickle.load(handle3)

                model4 = joblib.load("static/model/MODEL4_FA&FF.pkl")

                file_path = r"static\model\tokenizer4.pickle"
                with open(file_path, "rb") as handle4:
                    loaded_tokenizer4 = pickle.load(handle4)

                txt = post

                # image that you want to convert it into text
                mytext = txt
                cleaner = TextCleaner(mytext)
                cleaned_text = cleaner.clean_text()
                pos_tagged_text = cleaner.lemmatize_text(cleaned_text)
                lemmatized_text = cleaner.lemmatize_with_wordnet(pos_tagged_text)
                print("\n", "clean text:", lemmatized_text, "\n")

                sequences = loaded_tokenizer.texts_to_sequences([lemmatized_text])
                max_sequence_length = 20
                padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)

                predictions = model1.predict(padded_sequences)

                # keywords = ["space", "model", "system","quantum","learn","satellite","function"]
                # if any(keyword in txt for keyword in keywords):
                #    predictions[:, 1]=predictions[:, 1]+0.07

                predictedind1 = np.argmax(
                    predictions[0]
                )  # index of the highest probability

                if predictedind1 == 0:
                    predictedind1 = "not science"
                elif predictedind1 == 1:
                    predictedind1 = "science"

                text_type = str(predictedind1)

                if predictedind1 == "science":
                    # Model2
                    sequences = loaded_tokenizer2.texts_to_sequences([lemmatized_text])
                    max_sequence_length = 20
                    padded_sequences = pad_sequences(
                        sequences, maxlen=max_sequence_length
                    )

                    predictions = model2.predict(padded_sequences)
                    predictedind2 = np.argmax(
                        predictions[0]
                    )  # index of the highest probability

                    if predictedind2 == 0:
                        predictedind2 = "Emprical"
                    elif predictedind2 == 1:
                        predictedind2 = "Formal"

                    text_type += " " + str(predictedind2)

                    # model3

                    if predictedind2 == "Emprical":
                        sequences = loaded_tokenizer3.texts_to_sequences(
                            [lemmatized_text]
                        )
                        max_sequence_length = 20
                        padded_sequences = pad_sequences(
                            sequences, maxlen=max_sequence_length
                        )

                        predictions = model3.predict(padded_sequences)
                        predictedind3 = np.argmax(
                            predictions[0]
                        )  # index of the highest probability

                        if predictedind3 == 0:
                            predictedind3 = "Application"
                        elif predictedind3 == 1:
                            predictedind3 = "Foundation"

                        text_type += " " + str(predictedind3)

                    # model4

                    elif predictedind2 == "Formal":
                        sequences = loaded_tokenizer4.texts_to_sequences(
                            [lemmatized_text]
                        )
                        max_sequence_length = 20
                        padded_sequences = pad_sequences(
                            sequences, maxlen=max_sequence_length
                        )

                        predictions = model4.predict(padded_sequences)
                        predictedind4 = np.argmax(
                            predictions[0]
                        )  # index of the highest probability

                        if predictedind4 == 0:
                            predictedind4 = "Application"
                        elif predictedind4 == 1:
                            predictedind4 = "Foundation"

                        text_type += " " + str(predictedind4)
            else:
                text_type = "not science"

            new_post = Post(text=post, user_id=current_user.id, topic=text_type)
            db.session.add(new_post)
            db.session.commit()
            flash("Post added")

    friend_ids = [friend.id for friend in current_user.friends]
    friend_ids.append(current_user.id)

    posts = (
        Post.query.filter(Post.user_id.in_(friend_ids)).order_by(Post.date.desc()).all()
    )

    return render_template("home.html", user=current_user, posts=posts)
