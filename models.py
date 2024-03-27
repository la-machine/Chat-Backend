import psycopg2, os
from dotenv import load_dotenv

load_dotenv()
con = psycopg2.connect( database = os.environ.get('db_name'),
                        user = os.environ.get('db_user'),
                        host = os.environ.get('db_host'),
                        password = os.environ.get('db_password'),
                        port = os.environ.get('port'))

cur = con.cursor()

class User:
    """User Model"""
    def __init__(self):
        return


    def create(self, name="", email="", password="", role=""):
        """Create a new user"""
        query = sql.SQL("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s) RETURNING id;")
        self.cur.execute(query, (name, email, password, role))
        self.conn.commit()
        new_user_id = self.cur.fetchone()[0]
        return self.get_by_id(new_user_id)

    def get_all(self):
        """Get all users"""
        query = sql.SQL("SELECT * FROM users WHERE active = true;")
        self.cur.execute(query)
        users = self.cur.fetchall()
        return [{**user, "id": user["id"]} for user in users]

    def get_by_id(self, user_id):
        """Get a user by id"""
        query = sql.SQL("SELECT * FROM users WHERE id = %s AND active = true;")
        self.cur.execute(query, (user_id,))
        user = self.cur.fetchone()
        if not user:
            return
        return {**user, "id": user["id"]}

    def get_by_email(self, email):
        """Get a user by email"""
        query = sql.SQL("SELECT * FROM users WHERE email = %s AND active = true;")
        self.cur.execute(query, (email,))
        user = self.cur.fetchone()
        if not user:
            return
        return {**user, "id": user["id"]}

    def update(self, user_id, name=""):
        """Update a user"""
        data = {}
        if name:
            data["name"] = name
        query = sql.SQL("UPDATE users SET name = %s WHERE id = %s RETURNING id;")
        self.cur.execute(query, (name, user_id))
        self.conn.commit()
        return self.get_by_id(user_id)

    def delete(self, user_id):
        """Delete a user"""
        query = sql.SQL("UPDATE users SET active = false WHERE id = %s RETURNING id;")
        self.cur.execute(query, (user_id,))
        self.conn.commit()
        return self.get_by_id(user_id)

    def disable_account(self, user_id):
        """Disable a user account"""
        query = sql.SQL("UPDATE users SET active = false WHERE id = %s RETURNING id;")
        self.cur.execute(query, (user_id,))
        self.conn.commit()
        return self.get_by_id(user_id)

    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)

    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        if not user or not check_password_hash(user["password"], password):
            return
        return user

    def __del__(self):
        """Destructor to close the database connection"""
        self.cur.close()
        self.conn.close()