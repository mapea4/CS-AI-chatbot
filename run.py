from app import create_app

# This creates the Flask application instance using the factory in app/__init__.py
app = create_app()

if __name__ == "__main__":
    # This runs the development server
    app.run(debug=True)
