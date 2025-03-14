from pymongo import MongoClient, errors
from bson.objectid import ObjectId

# Connecting to MongoDB with exception handling
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    db = client["cats_db"]
    collection = db["cats"]
    client.server_info()
except errors.ServerSelectionTimeoutError:
    print (("❌ Error: Unable to connect to MongoDB. Check if the server is running."))
    exit(1)
except errors.ConnectionError:
    print("❌ Error: An error occurred connecting to MongoDB.")
    exit(1)

# Function for adding new cat
def add_cat(name, age, features):
    try:
        cat = {"name": name, "age": age, "features": features}
        result = collection.insert_one(cat)
        print(f"✅ Cat added with _id: {result.inserted_id}")
    except errors.PyMongoError as e:
        print(f"❌ Error adding cat: {e}")

# Function for output all records
def get_all_cats():
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except errors.PyMongoError as e:
        print(f"❌ Error getting cats: {e}")

#Function for finding cat by name
def find_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("❌ No cat with that name found.")
    except errors.PyMongoError as e:
        print(f"❌ Error while searching for a cat: {e}")

# Function for updating cat's age
def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count:
            print(f"✅ Cat age {name} update to {new_age} years.")
        else:
            print("❌ Cat not found or age not changed.")
    except errors.PyMongoError as e:
        print(f"❌ Error when updating age: {e}")

# Function for adding cat characteristics
def add_feature(name, new_feature):
    try:
        result = collection.update_one({"name": name}, {"$push": {"feature": new_feature}})
        if result.modified_count:
            print(f"✅ New characteristic is added '{new_feature}' for cat {name}.")
        else:
            print("❌ Cat not found or characteristic not added.")
    except errors.PyMongoError as e:
        print(f"❌ Error when adding characteristic: {e}")

# Function to delete a cat by name
def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"✅ Cat {name} has been deleted.")
        else:
            print(f"❌ Cat not found.")
    except errors.PyMongoError as e:
        print(f"❌ Error deleting cat: {e} ")

# Function to delete all entries
def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"✅ Deleted {result.deleted_count} cats.")
    except errors.PyMongoError as e:
        print(f"❌ Error deleted all cats: {e}")

# The main menu
def main():
    while True:
        print("\n🔹 MongoDB CRUD menu:")
        print("1.Add cat")
        print("2. Show all cats")
        print("3. Find cat by name")
        print("4. Update cat's age")
        print("5. Add cat's characteristics")
        print("6. Delete cat by name")
        print("7. Delete all cats")
        print("0. Exit")
        choice = input("👉 Enter action namber:")

        if choice == "1":
            name = input("Cat name: ")
            try:
                age = int(input("Cat age: "))
                features = input("Enter characteristics seperated by commas: ")
                add_cat(name, age, features)
            except ValueError:
                print("❌ Error: Cat age must to be integer.")
        elif choice == "2":
            get_all_cats()
        elif choice == "3":
            name = input("Cat name to search for: ")
            find_cat_by_name(name)
        elif choice == "4":
            name = input("Cat name: ")
            try:
                new_age = int(input("New age: "))
                update_cat_age(name, new_age)
            except ValueError:
                print("❌ Error: Cat age must to be integer.")
        elif choice == "5":
            name = input("Cat name: ")
            new_feature = input("New characteristic: ")
            add_feature(name, new_feature)
        elif choice == "6":
            name = input("Delete cat by name: ")
            delete_cat_by_name(name)
        elif choice == "7":
            delete_all_cats()
        elif choice == "0":
            print("👋 Exit...")
            break
        else:
            print("❌ Incorect choice, try again.")

if __name__ == "__main__":
    main()













