# Webpage Development Plan for Log Manager

## Overview
Transform the current API-only Log Manager into a beautiful web interface using Jinja2 templates with FastAPI.

## Current API Analysis

### Endpoints:
1. **Agent Logs** (`/get_agentlogs`) - Query agent activity by date, MSISDN, IMSI
2. **Command Logs** (`/get_commandlogs`) - Query command execution by date, username, node
3. **SOAP Logs** (`/get_soaplogs`) - Query SOAP services by MSISDN, date, node type

## Development Steps

### Step 1: Setup Jinja2 Integration
- Install dependencies: `jinja2`, `aiofiles`
- Configure Jinja2 template engine in FastAPI
- Set up static file serving
- Create template and static directories

### Step 2: Create Base Template
- Design responsive layout with navigation
- Implement header/footer with branding
- Set up CSS framework (Bootstrap/Tailwind)
- Create consistent design system

### Step 3: Build Dashboard Homepage
- Hero section with system overview
- Quick access cards for each log type
- Statistics and status indicators
- Search shortcuts and recent activity

### Step 4: Agent Logs Interface
- Search form with date pickers and filters
- Results table with sorting/pagination
- Real-time search with AJAX
- Export functionality (CSV/JSON)
- Error status filtering and highlighting

### Step 5: Command Logs Interface
- Search by username and node
- Command execution timeline
- Result status indicators
- Function-based filtering
- User activity tracking

### Step 6: SOAP Logs Interface
- MSISDN and node type search
- Request/response detail views
- Error highlighting and filtering
- Service performance metrics
- SOAP message formatting

### Step 7: Advanced Features
- Data visualization (charts/graphs)
- Advanced filtering and search
- Saved searches and bookmarks
- Bulk operations
- Real-time updates

### Step 8: Web Route Handlers
- Create HTML page routes
- Form handling and validation
- AJAX endpoints for dynamic loading
- Export functionality
- Error handling and user feedback

### Step 9: Responsive Design
- Mobile-friendly interface
- Accessibility compliance
- Cross-browser testing
- Performance optimization

### Step 10: Testing & Optimization
- Performance testing
- User acceptance testing
- Security validation
- Documentation

## Technical Stack

### Frontend
- **CSS**: Bootstrap 5 or Tailwind CSS
- **JavaScript**: Vanilla JS or Alpine.js
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome
- **Date Pickers**: Flatpickr

### Backend
- **Templates**: Jinja2
- **Static Files**: FastAPI StaticFiles
- **Form Handling**: Custom validation
- **Caching**: Redis (optional)

## File Structure

```
templates/
├── base.html
├── index.html
├── agentlogs.html
├── commandlogs.html
├── soaplogs.html
└── components/
    ├── search_form.html
    ├── results_table.html
    └── pagination.html

static/
├── css/
│   ├── main.css
│   └── [log-type].css
├── js/
│   ├── main.js
│   └── [log-type].js
└── images/

web_routes.py (new)
main.py (updated)
```

## Key Features

### User Experience
- Intuitive search and filtering
- Fast response times (< 2s)
- Mobile-responsive design
- Export capabilities

### Functionality
- All API endpoints accessible via web
- Advanced filtering options
- Real-time data updates
- Comprehensive error handling

### Performance
- Efficient pagination
- Optimized database queries
- Caching strategies
- Support for large datasets

## Success Metrics
- Page load < 3 seconds
- Search results < 1 second
- Mobile-friendly design
- WCAG 2.1 accessibility compliance
- All current functionality preserved 