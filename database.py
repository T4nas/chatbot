from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import bcrypt

# Connect to MongoDB
client = MongoClient("mongodb+srv://editionheritagemohammadien:Ajurrum-AI2025@ajurrumai.zua8i.mongodb.net/?retryWrites=true&w=majority&appName=AjurrumAI")
db = client['ajurrumai']

# Define collections
topics_col = db['topics']
courses_col = db['courses']
lessons_col = db['lessons']
users_col = db['users']
masteries_col = db['masteries']

# Setup collections with validation schemas
def setup_collections():
    # Schema for topics collection
    try:
        db.create_collection("topics", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["name", "description", "courses"],
                "properties": {
                    "name": {
                        "bsonType": "string",
                        "description": "Must be a string and is required"
                    },
                    "description": {
                        "bsonType": "string",
                        "description": "Must be a string and is required"
                    },
                    "courses": {
                        "bsonType": "array",
                        "items": {"bsonType": "objectId"},
                        "description": "Must be an array of ObjectIds and is required"
                    }
                }
            }
        })
    except Exception:
        pass  # Collection already exists

    # Schema for courses collection
    try:
        db.create_collection("courses", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["name", "description", "topic_id", "lessons"],
                "properties": {
                    "name": {
                        "bsonType": "string",
                        "description": "Must be a string and is required"
                    },
                    "description": {
                        "bsonType": "string",
                        "description": "Must be a string and is required"
                    },
                    "topic_id": {
                        "bsonType": "objectId",
                        "description": "Must be an ObjectId and is required"
                    },
                    "lessons": {
                        "bsonType": "array",
                        "items": {"bsonType": "objectId"},
                        "description": "Must be an array of ObjectIds and is required"
                    }
                }
            }
        })
    except Exception:
        pass  # Collection already exists

    # Schema for lessons collection
    try:
        db.create_collection("lessons", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["name", "content", "course_id"],
                "properties": {
                    "name": {
                        "bsonType": "string",
                        "description": "Must be a string and is required"
                    },
                    "content": {
                        "bsonType": "string",
                        "description": "Must be a string and is required"
                    },
                    "course_id": {
                        "bsonType": "objectId",
                        "description": "Must be an ObjectId and is required"
                    }
                }
            }
        })
    except Exception:
        pass  # Collection already exists

    # Schema for users collection
    try:
        db.create_collection("users", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["username", "password", "age"],
                "properties": {
                    "username": {
                        "bsonType": "string",
                        "description": "Must be a string and is required"
                    },
                    "password": {
                        "bsonType": "string",
                        "description": "Must be a string and is required"
                    },
                    "age": {
                        "bsonType": "int",
                        "description": "Must be an integer and is required"
                    }
                }
            }
        })
    except Exception:
        pass  # Collection already exists

    # Schema for masteries collection
    try:
        db.create_collection("masteries", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["user_id", "category", "item_id", "mastered"],
                "properties": {
                    "user_id": {
                        "bsonType": "objectId",
                        "description": "Must be an ObjectId and is required"
                    },
                    "category": {
                        "enum": ["topic", "course", "lesson"],
                        "description": "Must be 'topic', 'course', or 'lesson'"
                    },
                    "item_id": {
                        "bsonType": "objectId",
                        "description": "Must be an ObjectId and is required"
                    },
                    "mastered": {
                        "bsonType": "bool",
                        "description": "Must be a boolean and is required"
                    },
                    "revision_date": {
                        "bsonType": ["date", "null"],
                        "description": "Must be a date or null"
                    },
                    "repetitions": {
                        "bsonType": ["int", "null"],
                        "description": "Must be an integer or null"
                    }
                }
            }
        })
    except Exception:
        pass  # Collection already exists

# Create indexes for masteries collection
def create_indexes():
    masteries_col.create_index(
        [("user_id", ASCENDING), ("category", ASCENDING), ("item_id", ASCENDING)],
        unique=True
    )
    masteries_col.create_index("revision_date")
    masteries_col.create_index("user_id")

# Initialize collections and indexes
setup_collections()
create_indexes()

# CRUD operations for Topics
def add_topic(name, description):
    topic = {
        "name": name,
        "description": description,
        "courses": []
    }
    result = topics_col.insert_one(topic)
    return result.inserted_id

def get_topic(topic_id):
    return topics_col.find_one({"_id": ObjectId(topic_id)})

def update_topic(topic_id, name=None, description=None):
    update_fields = {}
    if name:
        update_fields["name"] = name
    if description:
        update_fields["description"] = description
    if update_fields:
        topics_col.update_one({"_id": ObjectId(topic_id)}, {"$set": update_fields})

def remove_topic(topic_id):
    # Remove all associated courses
    topic = get_topic(topic_id)
    if topic and "courses" in topic:
        courses_col.delete_many({"_id": {"$in": topic["courses"]}})
    # Remove the topic
    topics_col.delete_one({"_id": ObjectId(topic_id)})

# CRUD operations for Courses
def add_course(name, description, topic_id):
    course = {
        "name": name,
        "description": description,
        "topic_id": ObjectId(topic_id),
        "lessons": []
    }
    result = courses_col.insert_one(course)
    # Update the topic with the new course
    topics_col.update_one(
        {"_id": ObjectId(topic_id)},
        {"$push": {"courses": result.inserted_id}}
    )
    return result.inserted_id

def get_course(course_id):
    return courses_col.find_one({"_id": ObjectId(course_id)})

def update_course(course_id, name=None, description=None, topic_id=None):
    update_fields = {}
    if name:
        update_fields["name"] = name
    if description:
        update_fields["description"] = description
    if topic_id:
        update_fields["topic_id"] = ObjectId(topic_id)
    if update_fields:
        courses_col.update_one({"_id": ObjectId(course_id)}, {"$set": update_fields})

def remove_course(course_id):
    # Remove all associated lessons
    course = get_course(course_id)
    if course and "lessons" in course:
        lessons_col.delete_many({"_id": {"$in": course["lessons"]}})
    # Remove the course
    courses_col.delete_one({"_id": ObjectId(course_id)})
    # Remove the course from the topic
    topics_col.update_one(
        {"_id": ObjectId(course["topic_id"])},
        {"$pull": {"courses": ObjectId(course_id)}}
    )

# CRUD operations for Lessons
def add_lesson(name, content, course_id):
    lesson = {
        "name": name,
        "content": content,
        "course_id": ObjectId(course_id)
    }
    result = lessons_col.insert_one(lesson)
    # Update the course with the new lesson
    courses_col.update_one(
        {"_id": ObjectId(course_id)},
        {"$push": {"lessons": result.inserted_id}}
    )
    return result.inserted_id

def get_lesson(lesson_id):
    return lessons_col.find_one({"_id": ObjectId(lesson_id)})

def update_lesson(lesson_id, name=None, content=None, course_id=None):
    update_fields = {}
    if name:
        update_fields["name"] = name
    if content:
        update_fields["content"] = content
    if course_id:
        update_fields["course_id"] = ObjectId(course_id)
    if update_fields:
        lessons_col.update_one({"_id": ObjectId(lesson_id)}, {"$set": update_fields})

def remove_lesson(lesson_id):
    # Remove the lesson
    lesson = get_lesson(lesson_id)
    if lesson:
        lessons_col.delete_one({"_id": ObjectId(lesson_id)})
        # Remove the lesson from the course
        courses_col.update_one(
            {"_id": ObjectId(lesson["course_id"])},
            {"$pull": {"lessons": ObjectId(lesson_id)}}
        )

# CRUD operations for Users
def add_user(username, password, age):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        "username": username,
        "password": hashed_password.decode('utf-8'),
        "age": age
    }
    result = users_col.insert_one(user)
    return result.inserted_id

def get_user_by_username(username):
    return users_col.find_one({"username": username})

def get_user(user_id):
    return users_col.find_one({"_id": ObjectId(user_id)})

def update_user(user_id, username=None, password=None, age=None):
    update_fields = {}
    if username:
        update_fields["username"] = username
    if password:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        update_fields["password"] = hashed_password.decode('utf-8')
    if age is not None:
        update_fields["age"] = age
    if update_fields:
        users_col.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})

def remove_user(user_id):
    # Remove all associated masteries
    masteries_col.delete_many({"user_id": ObjectId(user_id)})
    # Remove the user
    users_col.delete_one({"_id": ObjectId(user_id)})

# Authentication functions
def register(username, password, age):
    if get_user_by_username(username):
        return "USERNAME_TAKEN"
    add_user(username, password, age)
    return "REGISTER_SUCCESS"

def login(username, password):
    user = get_user_by_username(username)
    if not user:
        return "INCORRECT_CREDENTIALS"
    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return "LOGIN_SUCCESS"
    return "INCORRECT_CREDENTIALS"

# CRUD operations for Masteries
def set_mastery(user_id, category, item_id, mastered=True):
    if category not in ["topics", "courses", "lessons"]:
        raise ValueError("Category must be one of 'topics', 'courses', 'lessons'")

    category_singular = category[:-1]  # 'topics' -> 'topic', etc.

    masteries_col.update_one(
        {
            "user_id": ObjectId(user_id),
            "category": category_singular,
            "item_id": ObjectId(item_id)
        },
        {
            "$set": {
                "mastered": mastered
            }
        },
        upsert=True
    )

def get_mastery(user_id, category, item_id):
    if category not in ["topics", "courses", "lessons"]:
        raise ValueError("Category must be one of 'topics', 'courses', 'lessons'")

    category_singular = category[:-1]

    return masteries_col.find_one({
        "user_id": ObjectId(user_id),
        "category": category_singular,
        "item_id": ObjectId(item_id)
    })

def remove_mastery(user_id, category, item_id):
    if category not in ["topics", "courses", "lessons"]:
        raise ValueError("Category must be one of 'topics', 'courses', 'lessons'")

    category_singular = category[:-1]

    masteries_col.delete_one({
        "user_id": ObjectId(user_id),
        "category": category_singular,
        "item_id": ObjectId(item_id)
    })

# Revision functions
def schedule_revision(user_id, lesson_id, interval_days=7):
    revision_date = datetime.utcnow() + timedelta(days=interval_days)
    masteries_col.update_one(
        {
            "user_id": ObjectId(user_id),
            "category": "lesson",
            "item_id": ObjectId(lesson_id)
        },
        {
            "$set": {"revision_date": revision_date}
        },
        upsert=True
    )
    return revision_date

def schedule_revision_spaced(user_id, lesson_id):
    mastery = masteries_col.find_one({
        "user_id": ObjectId(user_id),
        "category": "lesson",
        "item_id": ObjectId(lesson_id)
    })

    if not mastery:
        repetitions = 1
    else:
        repetitions = mastery.get("repetitions", 0) + 1

    if repetitions == 1:
        interval_days = 1
    elif repetitions == 2:
        interval_days = 3
    elif repetitions == 3:
        interval_days = 7
    elif repetitions == 4:
        interval_days = 14
    else:
        interval_days = 30  # Maximum interval

    revision_date = datetime.utcnow() + timedelta(days=interval_days)

    masteries_col.update_one(
        {
            "user_id": ObjectId(user_id),
            "category": "lesson",
            "item_id": ObjectId(lesson_id)
        },
        {
            "$set": {
                "revision_date": revision_date,
                "repetitions": repetitions
            }
        },
        upsert=True
    )
    return revision_date, repetitions

def perform_revision_spaced(user_id, lesson_id):
    mastery = masteries_col.find_one({
        "user_id": ObjectId(user_id),
        "category": "lesson",
        "item_id": ObjectId(lesson_id)
    })

    if not mastery:
        return

    repetitions = mastery.get("repetitions", 0)

    if repetitions < 5:
        schedule_revision_spaced(user_id, lesson_id)
    else:
        masteries_col.update_one(
            {
                "user_id": ObjectId(user_id),
                "category": "lesson",
                "item_id": ObjectId(lesson_id)
            },
            {
                "$unset": {"revision_date": ""}
            }
        )

def complete_lesson(user_id, lesson_id, mastered=True):
    set_mastery(user_id, "lessons", lesson_id, mastered)
    if mastered:
        schedule_revision(user_id, lesson_id)

def get_due_revisions(user_id):
    current_date = datetime.utcnow()
    due_revisions = masteries_col.find({
        "user_id": ObjectId(user_id),
        "category": "lesson",
        "revision_date": {"$lte": current_date}
    })
    return list(due_revisions)

# Utility functions
def get_all_topics():
    return list(topics_col.find())

def get_courses_by_topic(topic_id):
    topic = get_topic(topic_id)
    if topic and "courses" in topic:
        return list(courses_col.find({"_id": {"$in": topic["courses"]}}))
    return []

def get_lessons_by_course(course_id):
    course = get_course(course_id)
    if course and "lessons" in course:
        return list(lessons_col.find({"_id": {"$in": course["lessons"]}}))
    return []

def is_mastered(user_id, category, item_id):
    mastery = get_mastery(user_id, category, item_id)
    return mastery.get("mastered", False) if mastery else False

def get_masteries(user_id, category=None):
    query = {"user_id": ObjectId(user_id)}
    if category:
        query["category"] = category[:-1]
    return list(masteries_col.find(query))
