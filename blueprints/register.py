from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from db_orm import User, SessionLocal

register_bp=Blueprint("auth", __name__, url_prefix="/auth")

@register_bp.route("/register", methods=["POST"])
def register():
    session=SessionLocal()

    data=request.get_json()

    username=data.get("username")
    email=data.get("email")
    password=data.get("password")

    if not username or not password or not email:
        return jsonify({
            "message": "please fill all the required fields"
        }), 400
    
    try:
        existing_user=session.query(User).filter((User.username==username) | (User.email==email)).first()
        if existing_user:
            return jsonify({
                "message": "user already exists"
            })
        
        hashed_password=generate_password_hash(password=password)

        new_user=User(username=username, email=email, password=hashed_password)
        session.add(new_user)
        session.commit()

        return jsonify({
            "message": "user registered successfully"
        }), 201
    
    except Exception as e:
        session.rollback()
        print(str(e))
        return jsonify({
            "message": "internal server error"
        }), 500

    finally:
        session.close()
