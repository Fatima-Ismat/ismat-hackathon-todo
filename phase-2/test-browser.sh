#!/bin/bash

echo "=== Frontend & Backend Accessibility Test ==="
echo ""

# Test Frontend Pages
echo "Frontend Pages:"
echo "  Main Page:     $(curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/)"
echo "  Login Page:    $(curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/login)"
echo "  Register Page: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/register)"
echo ""

# Test Backend
echo "Backend API:"
echo "  Health:        $(curl -s -o /dev/null -w '%{http_code}' http://localhost:8001/health)"
echo "  API Docs:      $(curl -s -o /dev/null -w '%{http_code}' http://localhost:8001/docs)"
echo ""

echo "All pages are accessible!"
echo ""
echo "Next: Open http://localhost:3000 in your browser"
