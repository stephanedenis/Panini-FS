#!/bin/bash
# Start Panini-FS API and Web UI

set -e

echo "🚀 Starting Panini-FS..."
echo ""

# Check if we're in the right directory
if [ ! -f "Cargo.toml" ]; then
    echo "❌ Error: Must run from Panini-FS root directory"
    exit 1
fi

# Check if API binary exists
if [ ! -f "target/release/panini-api" ]; then
    echo "⚠️  API binary not found. Building release..."
    cargo build --release --bin panini-api
fi

# Start API server in background
echo "📡 Starting API server..."
PANINI_STORAGE=/tmp/panini-demo \
PANINI_HOST=127.0.0.1 \
PANINI_PORT=3000 \
RUST_LOG=info \
./target/release/panini-api > /tmp/panini-api.log 2>&1 &
API_PID=$!

echo "   API PID: $API_PID"
echo "   Logs: /tmp/panini-api.log"

# Wait for API to start
sleep 2

# Check if API is running
if ! curl -s http://localhost:3000/api/health > /dev/null; then
    echo "❌ API failed to start. Check logs:"
    tail -20 /tmp/panini-api.log
    kill $API_PID 2>/dev/null || true
    exit 1
fi

echo "✅ API server running on http://localhost:3000"
echo ""

# Check if node_modules exists
if [ ! -d "web-ui/node_modules" ]; then
    echo "📦 Installing Web UI dependencies..."
    cd web-ui
    npm install
    cd ..
fi

# Start Web UI
echo "🎨 Starting Web UI..."
cd web-ui
npm run dev &
WEB_PID=$!

echo "   Web PID: $WEB_PID"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Panini-FS is running!"
echo ""
echo "   📡 API:    http://localhost:3000"
echo "   🎨 Web UI: http://localhost:5173"
echo ""
echo "   Press Ctrl+C to stop all services"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $API_PID 2>/dev/null || true
    kill $WEB_PID 2>/dev/null || true
    echo "✅ Stopped"
    exit 0
}

trap cleanup INT TERM

# Wait for processes
wait
