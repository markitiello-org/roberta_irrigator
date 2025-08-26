# Roberta Irrigator

⚠️ **UNDER DEVELOPMENT** - This project is currently under active development and is not ready for production use yet.

A comprehensive irrigation system built with Python backend and Node.js frontend, designed to manage and automate watering schedules for multiple irrigation zones.

## Architecture Overview

This project consists of two main components:

### Backend (Python)
- **Main Service**: `backend/start.py` - Core irrigation management with RPyC service
- **Zone Control**: GPIO-based hardware control for Raspberry Pi irrigation valves
- **Database**: SQLite database with DAO pattern for zones, schedules, and logging
- **Safety Features**: Emergency shutoff protection to prevent valve damage

### Frontend (Node.js/Express)
- **Web Interface**: Express server with EJS templating and TailwindCSS styling
- **Real-time Dashboard**: Live zone status monitoring and manual control
- **Responsive Design**: Modern UI optimized for desktop and mobile devices

## Features

- **Automated Scheduling**: Configure irrigation times and days for each zone
- **Manual Override**: Turn zones on/off manually through the web interface
- **Safety Controls**: Automatic shutoff timers and confirmation dialogs
- **Real-time Monitoring**: Live status updates and next scheduled irrigation times
- **Logging**: Complete audit trail of all irrigation activities
- **Multi-zone Support**: Manage multiple irrigation zones independently

## Build System

This project uses **Bazel** with Aspect Workflows for unified build management.

### Quick Start

```bash

# Start the backend service
bazel run //backend:start

# Start the frontend web server
bazel run //frontend:app
```

## Hardware Requirements

- Raspberry Pi (for GPIO control)
- Irrigation valves connected to GPIO pins (default: pins 37, 38, 40)
- Network connectivity for web interface access

## Web Interface

Access the dashboard at `http://localhost:3000` (when frontend is running) to:
- View real-time zone status
- Control zones manually with safety confirmations
- Monitor upcoming irrigation schedules
- Access system configuration

### Testing
```bash
# Test specific components
bazel test //backend/dao/test:all
bazel test //backend/db:TestSqlLite
```

## Safety Features

- Confirmation dialogs for opening irrigation zones
- Automatic emergency shutoff if zones remain open too long
- Hardware GPIO abstraction for safe pin management
- Complete operation logging for troubleshooting

## Roadmap

### Phase 1: Core Enhancements P1 (Q3 2025)
- [ ] Complete web interface functionalities
- [ ] Setup CI enviroment with gitaction
- [ ] Add authentication between frontend and backend

### Phase 2: Core Enhancements P2 (Q4 2025)
- [ ] Improve documentations
- [ ] Add web authentication
- [ ] RESTful API documentation and expansion
- [ ] Improve Bazel integration with Node.js part

### Phase 3: Ecosystem Integration (Q2 2026)
- [ ] Home Assistant integration

### Phase 4: Professional Features (Q4 2026)
- [ ] Machine learning for optimal watering patterns

## Author

Marco Chimenti

## License

ISC