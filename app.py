from flask import Flask, jsonify, request
from datetime import datetime
import pytz

app = Flask(__name__)
API_TOKEN = "supersecrettoken123"

CITY_TIMEZONES = {
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Washington": "America/New_York",
    "Boston": "America/New_York",
    "Paris": "Europe/Paris"
}


def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

@app.route('/api/time', methods=['GET'])
@token_required
def get_time():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Missing city parameter!"}), 400
    
    timezone_name = CITY_TIMEZONES.get(city)

    if not timezone_name:
        return jsonify({"error": f"{city} not found in database"}), 404
    
    tz = pytz.timezone(timezone_name)
    current = datetime.now(tz)
    utc_offset = current.strftime('%z')
    utc_offset_formatted = f"UTC{'+' if int(utc_offset) >= 0 else ''}{int(utc_offset)//100}"

    return jsonify({
        "city": city, 
        "local_time": current.strftime('%Y-%m-%d %H:%M:%S'),
        "utc_offset": utc_offset_formatted
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

