from data import Config, Database


class Console:

    def __init__(self, config: Config, database: Database):
        self.config = config
        self.database = database
        self.listen()

    def listen(self):
        print("Welcome in the BidulHouse Shell.")
        while True:
            command = input("> ").lower()

            if command == "users list":
                print("Users stored in the database :")

                users_list = []

                for user in self.database.get_users():
                    users_list.append(user[0] + " (" + user[1] + ")")

                print_list(users_list)

            if command == "permissions get":
                user_id = int(input("User : "))
                user = self.database.get_user(user_id)

                if user:
                    print(f"Permissions of user {user_id} ({user[1]}) :")
                    print_list(self.database.get_permissions(user_id))
                else:
                    print(f"User {user_id} doesn't exist.")

            if command == "permissions add":
                user_id = int(input("User : "))
                user = self.database.get_user(user_id)

                if not user:
                    print(f"User {user_id} doesn't exist.")
                else:
                    permission = input("Permission : ")
                    self.database.add_permission(user_id, permission)

                    print(f"Permission {permission} added to {user_id} ({user[1]}).")


def print_list(list):
    print("- " + "\n- ".join(list))