import getpass
import sys
import bcrypt
from sqlalchemy import Select, insert

from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role

session = SessionLocal()


def create_admin():
    # is there already an admin?
    is_admin = session.execute(Select(User.id).join(Role, User.role_id == Role.id).where(Role.rank == 30)).fetchone()

    # if there is one, we don't do anything
    if is_admin is not None:
        print("Admin already exists. Exiting.")
        sys.exit()

    print("No admin exists. Creating one now.")

    # first username check
    username = input("Username: ")
    username_taken = session.execute(Select(User.username).where(User.username == username.lower())).scalar()

    # if there is a username...
    # though wouldn't this always be None if i check it in the first place it's the first user
    while username_taken is not None:
        print("Username taken.")
        # get another one and check it again
        username = input("Username: ")
        username_taken = session.execute(Select(User.username).where(User.username.lower() == username.lower())).scalar()
        # either it breaks out or it continues again


    print(f"Your username is {username}.")

    # it's easier to just do it all in a loop this time
    passwords_match = False

    while not passwords_match:
        # get the password, check it against a confirmation
        password = getpass.getpass("Password: ")
        password_confirmation = getpass.getpass("Confirm password: ")

        if password == password_confirmation:
            passwords_match = True
        else:
            print("Passwords do not match.")

    # generate the password hash
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(pw_bytes, salt).decode('utf-8')

    role = session.execute(Select(Role.id).where(Role.name == "admin")).scalar()

    new_user = User(username=username, password_hash=pw_hash, role_id=role)

    session.add(new_user)
    session.commit()

    print("Admin created successfully.")
    

if __name__ == "__main__":
    create_admin()