from model import Model

user_model = Model("User", ["name", "email", "age"])
user_model.create({"name": "Alice", "email": "alice@gmail.com", "age": 30})
user_model.create({"name": "Bob", "email": "bob@gmail.com", "age": 40})
user_model.create({"name": "Juan", "email": "juan@gmail.com", "age": 40})

user_model.read()

# bob, *_ = user_model.read({"age": 40})
# user_model.read({"id": bob["id"]})

user_model.update({"age": 20}, {"email": "alice@gmail.com", 'age':40})
user_model.read()

# user_model.delete({"name": "Bob"})
# user_model.read()
