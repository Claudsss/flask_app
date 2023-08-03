from website import create_app

app = create_app()

if __name__ == '__main__': #prevents code from running code once it import main.py
    app.run(debug=True) #run flask app, debug=True means auto run web server when code changes, off for submission
