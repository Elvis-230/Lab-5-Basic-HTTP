# Flask Pub-Sub Server

A simple HTTP-based publish-subscribe system built with Python Flask.

## Setup in GitHub Codespace

1. **Create your project directory:**
   ```bash
   mkdir -p Lab5-PubSub
   cd Lab5-PubSub
   ```

2. **Install dependencies:**
   ```bash
   pip3 install flask
   ```

3. **Create the files:**
   - Save server code as `app.py`
   - Save test code as `test_app.py`
   - Save testing script as `test_pubsub.sh`
   - Make script executable: `chmod +x test_pubsub.sh`

## Running the Server

**Terminal 1 - Start the Flask server:**
```bash
python3 app.py
```

You should see:
```
[BACKEND] Flask Pub-Sub Server starting on http://localhost:5000
 * Running on http://127.0.0.1:5000
```

**Note:** GitHub Codespaces will automatically forward port 5000

## Testing

### Option 1: Run Unit Tests

**Terminal 2 - Run unit tests:**
```bash
python3 -m unittest test_app.py -v
```

This runs all unit tests and shows results for each endpoint.

### Option 2: Use the Test Script

**Terminal 2 - Run automated tests:**
```bash
./test_pubsub.sh
```

This will run through all endpoints automatically and format the output nicely.

### Option 3: Manual Testing with curl

**Terminal 2 - Run curl commands manually:**

#### Add a Subscriber
```bash
curl -X POST http://localhost:5000/subscribe \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "url": "http://localhost:3000"}'

curl -X POST http://localhost:5000/subscribe \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob", "url": "http://localhost:3001"}'
```

#### List All Subscribers
```bash
curl http://localhost:5000/subscribers
```

You should see:
```json
{
  "subscribers": {
    "Alice": "http://localhost:3000",
    "Bob": "http://localhost:3001"
  }
}
```

#### Publish to All Subscribers
```bash
curl -X POST http://localhost:5000/publish \
  -H "Content-Type: application/json" \
  -d '{"subject": "Breaking News: Lab 5 Complete!"}'
```

Watch the backend terminal - you'll see notifications printed for each subscriber.

#### Delete a Subscriber
```bash
curl -X DELETE http://localhost:5000/unsubscribe \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

## Endpoints Summary

| Method | Endpoint | Purpose | Body |
|--------|----------|---------|------|
| POST | `/subscribe` | Add subscriber | `{"name": "...", "url": "..."}` |
| DELETE | `/unsubscribe` | Remove subscriber | `{"name": "..."}` |
| GET | `/subscribers` | List all subscribers | (none) |
| POST | `/publish` | Publish to all | `{"subject": "..."}` |

## Project Structure

```
├── app.py              # Main Flask server
├── test_app.py         # Unit tests
└── README.md           # This file
```

## How It Works

1. **Subscribers** are stored in a dictionary on the backend (name → URL)
2. When you **add** a subscriber, it's stored in memory
3. When you **list** subscribers, all stored subscriptions are returned
4. When you **publish**, a message is sent to all subscribers (printed on backend)
5. When you **delete**, the subscriber is removed from the dictionary

## Notes

- Subscribers are stored in-memory and will be cleared when the server restarts
- Notifications are printed as backend output (console log statements)
- This is a basic implementation suitable for learning HTTP and pub-sub patterns
