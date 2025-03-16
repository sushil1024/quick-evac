from utils.helpers import create_app

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0')