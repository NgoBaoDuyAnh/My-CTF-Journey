import re
import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import setuptools
import ctypes

# Flask application setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database configuration
DATABASE_HOST = os.getenv('MYSQL_HOST', 'localhost')
DATABASE_USER = os.getenv('MYSQL_USER', 'root')
DATABASE_PASSWORD = os.getenv('MYSQL_PASSWORD', 'rootpassword')
DATABASE_NAME = os.getenv('MYSQL_DB', 'prepared_db')


# Custom Exceptions
class MaliciousCharError(Exception):
    """Malicious characters are detected."""
    pass


class NonPrintableCharError(Exception):
    """Non-printable characters are detected."""
    pass


# Input Validation Classes
class InputValidator:
    """Validates and sanitizes user input strings."""
    
    FORBIDDEN_CHARACTERS = ['"', "(", ")", " ", "," , "'", "\\", "/", "*", "+" "%", "-", ";", "#"]

    def __init__(self, input_value, field_name):
        self.input_value = input_value
        self.field_name = field_name

    def __repr__(self):
        return self.get_validated_value()

    def validate_printable_characters(self):
        """Check if all characters are printable ASCII."""
        if not all(32 <= ord(char) <= 126 for char in self.input_value):
            raise NonPrintableCharError(
                f"Non-printable ASCII character found in '{self.field_name}'."
            )

    def validate_forbidden_characters(self):
        """Check for malicious characters in the input."""
        for char in self.input_value:
            if char in self.FORBIDDEN_CHARACTERS:
                raise MaliciousCharError(
                    f"Malicious character '{char}' found in '{self.field_name}'"
                )

    def get_validated_value(self):
        """Return the validated input value."""
        self.validate_printable_characters()
        self.validate_forbidden_characters()
        return self.input_value


class SQLQueryBuilder:
    """Builds SQL queries with placeholder replacement."""
    
    def __init__(self, template, input_validators):
        self.template = template
        self.validators = {validator.field_name: validator for validator in input_validators}
        self.placeholders = self.extract_placeholders(self.template)

    def extract_placeholders(self, query_string):
        """Extract placeholder names from query template."""
        placeholder_pattern = re.compile(r'\{(\w+)\}')
        return placeholder_pattern.findall(query_string)

    def build_query(self):
        """Build the final SQL query by replacing placeholders."""
        query = self.template
        self.placeholders = self.extract_placeholders(query)
        
        while self.placeholders:
            current_key = self.placeholders[0]
            replacement_map = dict.fromkeys(
                self.placeholders, 
                lambda _, key: f"{{{key}}}"
            )
            
            for placeholder_key in self.placeholders:
                if placeholder_key in self.validators:
                    if current_key == placeholder_key:
                        replacement_map[placeholder_key] = self.validators[placeholder_key].get_validated_value()
                else:
                    replacement_map[placeholder_key] = InputValidator
                    
            query = query.format_map(
                type('FormatDict', (), {
                    '__getitem__': lambda _, key: (
                        replacement_map[key] if isinstance(replacement_map[key], str) 
                        else replacement_map[key]("", key)
                    )
                })()
            )
            
            self.placeholders = self.extract_placeholders(query)
            
        return query


# Database Functions
def create_database_connection():
    """Establish connection to MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Database connection error: {error}")
        return None


def authenticate_user(username, password):
    """Authenticate user credentials against database."""
    try:
        username_validator = InputValidator(username, 'username')
        password_validator = InputValidator(password, 'password')

        query_builder = SQLQueryBuilder(
            "SELECT * FROM users WHERE username = '{username}' AND password = '{password}'",
            [username_validator, password_validator]
        )
        query = query_builder.build_query()
        print(f"Executing query: {query}", flush=True)
        
        return query
    except (MaliciousCharError, NonPrintableCharError) as validation_error:
        raise validation_error


def execute_user_query(query):
    """Execute authentication query and return user record."""
    connection = create_database_connection()
    if not connection:
        return None
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        user_record = cursor.fetchone()
        return user_record
    except mysql.connector.Error as database_error:
        raise database_error
    finally:
        cursor.close()
        connection.close()


# Route Handlers
@app.route('/', methods=['GET', 'POST'])
def login_page():
    """Handle user login requests."""
    if request.method == 'POST':
        form_data = request.form
        username = form_data.get('username', '')
        password = form_data.get('password', '')

        # Validate input presence
        if not username or not password:
            flash("Username and password are required.", 'error')
            return redirect(url_for('login_page'))

        # Authenticate user
        try:
            query = authenticate_user(username, password)
        except (MaliciousCharError, NonPrintableCharError) as validation_error:
            flash(str(validation_error), 'error')
            return redirect(url_for('login_page'))
        except Exception:
            flash("Invalid credentials.", 'error')
            return redirect(url_for('login_page'))

        # Execute query
        try:
            user_record = execute_user_query(query)
            
            if user_record:
                flash("Login successful!", 'success')
                return render_template('404.html')
            else:
                flash("Invalid credentials.", 'error')
        except mysql.connector.Error as database_error:
            flash(f"Database query failed: {database_error}", 'error')
        except Exception:
            flash("Database connection failed.", 'error')

    return render_template('login.html')


@app.route('/404')
def not_found_page():
    """Display 404 page."""
    return render_template('404.html')


# Application Entry Point
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=False)
