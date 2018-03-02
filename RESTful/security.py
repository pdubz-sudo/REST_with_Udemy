# if you had a bunch of users then this list would be long. We do this so we don't have to iterate
# through the list every time. So, if we wanted to find bob in a big list we could
# just do something like
# userid_mapping["bob"] or username_mapping = [1]

#######################################################################################
# PART 2
# you did everything below first and then added this stuff after making the user.py file
# you can now import user file because it's in the same directory file as this one.
# from the user file you imported the User class (look at the user file if you have to)
from werkzeug.security import safe_str_cmp  # compares strings (good older versions like python2.7
                                            # don't handle == comparisons to well
from user import User

users = [
    User(1, "bob", "asdf")
]

# instead of copying and pasting all these new users like you did below you can use a set comprehension
# but instead of assigning values your assigning key value pairs.
# after making the set comprehension the instructor deleted the list below because we now replaced it.
# I kept it so we can understand better what these comprehensions are.
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

#######################################################################################

# PART 1

# user = [
#     {
#         "id": 1,
#         "username": "bob"
#         "password": "asdf"
#     }
# ]

# username_mapping = { "bob": {
#         "id": 1,
#         "username": "bob",
#         "password": "asdf"
#     }
# }
#
# userid_mapping = {1: {
#         "id": 1,
#         "username": "bob",
#         "password": "asdf"
#     }
# }

def authenticate(username, password):
    user = username_mapping.get(username, None) # .get is another way of accessing a dictionary. We put None to return None if
                                                # there is no username key that is written.
    # if user and user.password == password:            # we used this for PART 1
    if user and safe_str_cmp(user.password, password):   # <- changed to this in PART 2 because it's more universal for all systems and versions
        return user

def identity(payload):                # unique to Flask_JWT.
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)