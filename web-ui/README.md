# Panini-FS Web UI

Modern web interface for the Panini-FS temporal filesystem with time-travel capabilities.

## 🚀 Features

- **Dashboard**: System overview with statistics and recent activity
- **Timeline Viewer**: Interactive timeline with visual event history  
- **Concepts Browser**: Search and browse all concepts
- **Snapshots Manager**: Create and restore system snapshots
- **Time-Travel Queries**: Navigate through filesystem history

## 🛠️ Tech Stack

- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool
- **TailwindCSS**: Styling
- **Axios**: HTTP client
- **Lucide React**: Icons
- **date-fns**: Date formatting

## 📦 Installation

```bash
cd web-ui
npm install
```

## 🏃 Development

### 1. Start the API Server

First, ensure the Panini-FS API server is running:

```bash
cd /home/stephane/GitHub/Panini-FS
PANINI_STORAGE=/tmp/panini-test cargo run --bin panini-api
```

The API should be running on `http://localhost:3000`

### 2. Start the Web UI

In a new terminal:

```bash
cd web-ui
npm run dev
```

The UI will be available at `http://localhost:5173`

## 🏗️ Build for Production

```bash
npm run build
```

Built files will be in `dist/`

## 📁 Project Structure

```
web-ui/
├── src/
│   ├── api/
│   │   └── client.ts          # API client
│   ├── components/
│   │   ├── Layout.tsx          # Main layout with nav
│   │   └── TimelineViewer.tsx  # Timeline component
│   ├── pages/
│   │   ├── Dashboard.tsx       # Dashboard page
│   │   ├── ConceptsPage.tsx    # Concepts browser
│   │   ├── TimelinePage.tsx    # Full timeline
│   │   └── SnapshotsPage.tsx   # Snapshots manager
│   ├── types/
│   │   └── api.ts              # TypeScript types
│   ├── App.tsx                 # Main app component
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## 🎨 UI Components

### Dashboard

- **System Stats Cards**: Displays totals for concepts, versions, snapshots, atoms
- **Storage Metrics**: Shows storage size and deduplication savings
- **Recent Activity**: Timeline of last 10 events

### Timeline Viewer

- **Visual Timeline**: Events displayed chronologically with icons
- **Event Types**:
  - 🟢 Green: Concept created
  - 🔵 Blue: Concept modified
  - 🟣 Purple: Snapshot created
- **Interactive**: Click events to view details

### Concepts Browser

- **Search**: Filter concepts by name
- **List View**: All concepts with version counts
- **Quick Actions**: View details for each concept

## 🔌 API Integration

The UI connects to the REST API at `/api`:

- `GET /api/health` - Health check
- `GET /api/stats` - System statistics
- `GET /api/concepts` - List concepts
- `GET /api/timeline` - Get timeline events
- `GET /api/snapshots` - List snapshots

All requests go through the `apiClient` which handles:
- Automatic error handling
- Response unwrapping
- TypeScript type safety

## 🎨 Customization

### Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      'panini-blue': '#0ea5e9',    // Primary blue
      'panini-purple': '#8b5cf6',  // Secondary purple
      'panini-dark': '#1e293b',    // Dark background
    },
  },
}
```

### Proxy Configuration

The dev server proxies `/api` requests to `http://localhost:3000`.

Edit `vite.config.ts` to change the API URL:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://your-api-server:port',
      changeOrigin: true,
    },
  },
}
```

## 🚧 Coming Soon

- [ ] **Advanced Timeline**: Zoom, filter, search
- [ ] **Concept Detail View**: Full version history and diffs
- [ ] **Snapshot Creation**: UI for creating named snapshots
- [ ] **Time-Travel UI**: Interactive date/time picker
- [ ] **Version Diff Viewer**: Side-by-side comparison with syntax highlighting
- [ ] **Real-time Updates**: WebSocket for live notifications
- [ ] **Graph Visualization**: D3.js concept relationship graph
- [ ] **Dark/Light Theme**: Toggle theme preference

## 🐛 Troubleshooting

### API Connection Failed

**Error**: `Failed to load dashboard` or `Network Error`

**Solution**: Ensure the API server is running:

```bash
# Check if API is responding
curl http://localhost:3000/api/health

# Should return: {"success":true,"data":"OK","error":null}
```

### TypeScript Errors

**Error**: `Cannot find module 'react'`

**Solution**: Install dependencies:

```bash
npm install
```

### Port 5173 Already in Use

**Solution**: Kill the process or use a different port:

```bash
# Use different port
npm run dev -- --port 3001
```

## 📝 Development Notes

### Adding New Pages

1. Create page component in `src/pages/`
2. Add route in `src/App.tsx`
3. Add navigation item in `src/components/Layout.tsx`

### Adding API Endpoints

1. Add TypeScript types in `src/types/api.ts`
2. Add client method in `src/api/client.ts`
3. Use in components with `apiClient.methodName()`

## 🤝 Contributing

This is part of the Panini-FS project. See main repository for contribution guidelines.

## 📄 License

MIT - See main project LICENSE
