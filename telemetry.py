from app import app, db, socketio 
from app.models import BMS, KLS, Runs 

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
