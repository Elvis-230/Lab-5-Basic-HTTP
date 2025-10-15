from flask import Flask, request, jsonify

app = Flask(__name__)

# Store subscribers as a dictionary: {name: url}
subscribers = {}
current_subject = ""

# Endpoint 1: Add a subscriber
@app.route('/subscribe', methods=['POST'])
def add_subscriber():
    """Add a new subscriber with a name and URL"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'url' not in data:
        return jsonify({'error': 'Missing name or url'}), 400
    
    name = data['name']
    url = data['url']
    
    subscribers[name] = url
    print(f"[BACKEND] Subscriber added: {name} -> {url}")
    
    return jsonify({'message': f'Subscriber {name} added successfully'}), 201

# Endpoint 2: Delete a subscriber
@app.route('/unsubscribe', methods=['DELETE'])
def delete_subscriber():
    """Delete a subscriber by name"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    
    name = data['name']
    
    if name not in subscribers:
        return jsonify({'error': f'Subscriber {name} not found'}), 404
    
    del subscribers[name]
    print(f"[BACKEND] Subscriber deleted: {name}")
    
    return jsonify({'message': f'Subscriber {name} deleted successfully'}), 200

# Endpoint 3: List all subscribers
@app.route('/subscribers', methods=['GET'])
def list_subscribers():
    """Return all subscribers and their URLs"""
    print(f"[BACKEND] List requested. Current subscribers: {subscribers}")
    return jsonify({'subscribers': subscribers}), 200

# Endpoint 4: Publish subject and notify all subscribers
@app.route('/publish', methods=['POST'])
def publish():
    """Update the published subject and notify all subscribers"""
    global current_subject
    data = request.get_json()
    
    if not data or 'subject' not in data:
        return jsonify({'error': 'Missing subject'}), 400
    
    current_subject = data['subject']
    
    print(f"\n[BACKEND] ===== PUBLISHING =====")
    print(f"[BACKEND] Subject: {current_subject}")
    print(f"[BACKEND] Notifying {len(subscribers)} subscriber(s)...")
    
    # Notify all subscribers
    for name, url in subscribers.items():
        print(f"[BACKEND] -> Notification sent to {name} at {url}")
        print(f"[BACKEND]    Message: {current_subject}")
    
    print(f"[BACKEND] ===== END PUBLISH =====\n")
    
    return jsonify({
        'message': f'Published to {len(subscribers)} subscriber(s)',
        'subject': current_subject
    }), 200

if __name__ == '__main__':
    print("[BACKEND] Flask Pub-Sub Server starting on http://localhost:5000")
    app.run(debug=True, port=5000)