from flask_app import app
# IMPORT ALL CONTROLLERS TO AVOID 404
from flask_app.controllers import users, critters
if __name__=="__main__":
    app.run(debug=True)