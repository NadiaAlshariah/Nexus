from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from app import db
from models import User, Post, LikedPost, Friendship, Comment
from flask_login import login_required, current_user

user_bp = Blueprint("user", __name__, template_folder="templates")



@user_bp.route("/", methods=["POST", "GET"])
def user_profile(username):
    if username.lower() == "home":
        return redirect(url_for("home"))
    if username.lower() == "interests":
        return redirect(url_for("interests"))
    user = User.query.filter_by(username=username).first()
    if user:
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.date.desc()).all()
        isFriend = user in current_user.friends

        return render_template(
            "user.html",
            user=user,
            posts=posts,
            current_user=current_user,
            isFriend=isFriend,
        )
    else:
        return "no user has this username"


@user_bp.route("/follow")
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()

    if user_to_follow is None:
        flash("User not found", "error")
        return redirect(url_for("user.user_profile", username=username))

    if current_user == user_to_follow:
        flash("You cannot follow yourself", "error")
    elif Friendship.query.filter_by(
        user_id=current_user.id, friend_id=user_to_follow.id
    ).first():
        flash("You are already following this user", "info")
    else:
        # Create a new Friendship record indicating that current_user is following user_to_follow
        friendship = Friendship(user_id=current_user.id, friend_id=user_to_follow.id)
        db.session.add(friendship)
        db.session.commit()
        flash(f"You are now following {user_to_follow.username}", "success")

    return redirect(url_for("user.user_profile", username=username))


@user_bp.route("/unfollow")
@login_required
def unfollow(username):
    user_to_unfollow = User.query.filter_by(username=username).first()

    if user_to_unfollow is None:
        flash("User not found", "error")
        return redirect(url_for("user.user_profile", username=username))

    if current_user == user_to_unfollow:
        flash("You cannot unfollow yourself", "error")
    elif not Friendship.query.filter_by(
        user_id=current_user.id, friend_id=user_to_unfollow.id
    ).first():
        flash("You are not following this user", "info")
    else:
        # Remove the Friendship record indicating that current_user is following user_to_unfollow
        friendship = Friendship.query.filter_by(
            user_id=current_user.id, friend_id=user_to_unfollow.id
        ).first()
        db.session.delete(friendship)
        db.session.commit()
        flash(f"You have unfollowed {user_to_unfollow.username}", category="success")

    return redirect(url_for("user.user_profile", username=username))


@user_bp.route("/create_comment/<post_id>", methods=["POST"])
@login_required
def create_comment(username, post_id):
    text = request.form.get("text")
    if not text:
        flash("Comment cannot be empty", category="error")
    else:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            comment = Comment(text=text, user_id=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("post doesnt exist", category="error")

    return redirect(request.referrer)


@user_bp.route("/<post_id>", methods=["POST", "GET"])
def post_view(username, post_id):
    user = User.query.filter_by(username=username).first()
    post = Post.query.filter_by(id=post_id).first()
    if user:
        if post:
            return render_template(
                "post.html",
                user=user,
                post=post,
                current_user=current_user,
            )
        else:
            return "post doesnt exist"
    else:
        return "no user has this username"


@user_bp.route("/like-post/<post_id>", methods=["POST"])
@login_required
def like_post(username, post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = LikedPost.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if not post:
        return jsonify({"error": "post does not exist"}, 400)
    elif like != None:
        db.session.delete(like)
        db.session.commit()
    else:
        new_like = LikedPost(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()

    return jsonify(
        {
            "likes": len(post.likes),
            "liked": current_user.id in map(lambda x: x.user_id, post.likes),
        }
    )



def get_top_interests_and_update(user_id):
    user = User.query.get(user_id)
    posts = user.posts.order_by(Post.date_created.desc()).limit(20).all()
    likes = user.liked_posts.order_by(Post.date_created.desc()).limit(20).all()
    comments = user.comments.order_by(Post.date_created.desc()).limit(20).all()

    interests = []
    for post in posts:
        interests.append(post.topic)
    for like in likes:
        interests.append(like.topic)
    for comment in comments:
        interests.append(comment.topic)

    print(interests)


