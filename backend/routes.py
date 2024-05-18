from app import app,db

from flask import request , jsonify
from models import Friend

# Get all Friends

@app.route("/api/friends",methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result)


# Create a friend
@app.route('/api/friends',methods=['POST'])
def create_friend():
    try:
        data = request.json

        required_field = ["name","role","description","gender"]

        for fields in required_field:
            if fields not in data:
                return jsonify({
                        "message":f"{fields} is required",
                        "status": 400
                    },)

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")

        # fetch avatar image based on gender

        if gender == 'male':
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == 'female':
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None
        
        new_friend = Friend(name=name,role=role,description=description,gender=gender,img_url=img_url)

        db.session.add(new_friend)
        db.session.commit()

        return jsonify({
            "message": "Friend created successfully",},200)
    
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"message": "Something went wrong", "error": str(e)},
            500
        )
    
# update friend
@app.route('/api/friends/<int:id>',methods=["Patch"])
def update_friend(id):
    try:
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"message":"Friend Not found"},404)
        
        data = request.json

        friend.name = data.get("name",friend.name)
        friend.role = data.get('role',friend.role)
        friend.description = data.get('description',friend.description)
        friend.gender = data.get('gender',friend.gender)
        
        db.session.commit()
    
        return jsonify({"message":"Friend update Succesfully","friend":friend.to_json()},200)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":"Something went wrong"},400)


# delete a friend
@app.route('/api/friends/<int:id>',methods=['DELETE'])
def delete_friend(id):
   try:
       friend = Friend.query.get(id)
       if friend is None:
           return jsonify({
               "message": "Friend not found",
               "status": 404
           })
       
       db.session.delete(friend)
       db.session.commit()

       return jsonify({
           "message": "Friend deleted successfully",
           "status": 200
       })
   except Exception as e:
       db.session.rollback()
       return jsonify(
           {"message": "Something went wrong", "error": str(e)},
           500
       )