from flask import Flask, request, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
import os, json

app = Flask(__name__)

# Authorization token for validation
AUTH_TOKEN = 'cbvcasdghcvsdhcvjhsdgjhasdjhsdadjasjdjkhasjhdgjasd'

# Setup the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///influencers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy database instance
db = SQLAlchemy(app)

# Create the Influencer model (table in SQLite)
class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(255), nullable=False)
    platformname = db.Column(db.String(255), nullable=False)
    followers = db.Column(db.String(255), nullable=False)
    platformcredential = db.Column(db.String(255), nullable=False)

# Create the SQLite database if it doesn't exist, within the app context
with app.app_context():
    if not os.path.exists('influencers.db'):
        db.create_all()

@app.route('/myendpoint', methods=['POST'])
def post_influencer_profiledata():
    # Get data from the request
    data = request.json

    userid = data.get('userid')
    platformname = data.get('platformname')
    followers = data.get('followers')
    platformcredential = data.get('platformcredential')
    
    # Check if the influencer already exists based on userid and platformname
    influencer = Influencer.query.filter_by(userid=userid, platformname=platformname).first()
    
    if influencer:
        # If the influencer exists, update the existing record
        influencer.followers = followers
        influencer.platformcredential = platformcredential
        message = "Influencer data updated."
    else:
        # If the influencer doesn't exist, create a new record
        influencer = Influencer(
            userid=userid,
            platformname=platformname,
            followers=followers,
            platformcredential=platformcredential
        )
        db.session.add(influencer)
        message = "New influencer data added."
    
    # Commit the changes to the database
    db.session.commit()

    response = {
        "status": "success",
        "message": message
    }
    return jsonify(response), 200

# Endpoint to get paginated data via AJAX
@app.route('/get_influencer_data', methods=['GET'])
def get_influencer_data():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)  # Default is 10 per page

    # Query influencer data from the database with pagination
    influencers = Influencer.query.paginate(page=page, per_page=per_page, error_out=False)

    # Prepare data for response
    data = [
        {
            'userid': influencer.userid,
            'platformname': influencer.platformname,
            'followers': influencer.followers,
            'platformcredential': influencer.platformcredential
        }
        for influencer in influencers.items
    ]

    # Return paginated data and pagination metadata
    return jsonify({
        'data': data,
        'total': influencers.total,
        'pages': influencers.pages,
        'current_page': influencers.page
    })

# **NEW** Endpoint to show the data table using AJAX
@app.route('/', methods=['GET'])
def show_data_table():
    # This will render the HTML template containing the table and AJAX functionality
    return render_template('table.html')

@app.route('/get_influencer_profile_links/', methods=['GET'])
def get_influencer_profile_links():
    # Check for Authorization header
    auth_header = request.headers.get('authorization')
    
    if not auth_header or auth_header != AUTH_TOKEN:
        # Abort with 401 Unauthorized if the token is missing or incorrect
        abort(401, description="Unauthorized access: Invalid token.")

    platform = request.args.get('platform')

    if not platform:
        return jsonify({"error": "Platform parameter is required"}), 400

    # Load data from JSON file
    with open('influencer_data.json') as json_file:
        influencer_data = json.load(json_file)

    # Filter data based on platform, handle cases where platform is None
    filtered_data = [
        influencer for influencer in influencer_data
        if influencer[1] is not None and influencer[1].lower() == platform.lower()
    ]

    return jsonify(filtered_data)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)

