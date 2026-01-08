# 🔍 LOGOUT BUTTON DEBUGGING GUIDE

## Step 1: Check Console Logs

Open browser console (F12) and look for these logs:

```
[useAuth] Starting checkAuth...
[useAuth] /api/auth/me response status: 200
[useAuth] User data received: {id: "9", email: "noshi@test.com", name: "noshi"}
[useAuth] Auth check complete
[Dashboard] Render - user: {id: "9", email: "noshi@test.com", name: "noshi"}
[Dashboard] Render - logout function exists: true
```

## Step 2: Run DOM Inspection (Paste in Console)

```javascript
// Check if logout button exists in DOM
console.log('=== LOGOUT BUTTON DOM INSPECTION ===')

// Method 1: By test ID
const logoutByTestId = document.querySelector('[data-testid="logout-button"]')
console.log('Found by testid:', logoutByTestId)

// Method 2: By LogOut icon
const logoutIcons = document.querySelectorAll('svg')
const logoutButton = Array.from(logoutIcons).find(svg =>
  svg.innerHTML.includes('M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4')
)?.closest('button')
console.log('Found by LogOut icon:', logoutButton)

// Method 3: Count all buttons
const allButtons = document.querySelectorAll('button')
console.log('Total buttons on page:', allButtons.length)
console.log('All buttons:', Array.from(allButtons).map(btn => ({
  text: btn.textContent,
  classes: btn.className,
  visible: btn.offsetParent !== null
})))

// Check z-index and visibility
if (logoutByTestId) {
  const styles = window.getComputedStyle(logoutByTestId)
  console.log('Logout button styles:', {
    display: styles.display,
    visibility: styles.visibility,
    opacity: styles.opacity,
    zIndex: styles.zIndex,
    position: styles.position
  })
}
```

## Step 3: Check Authentication State

```javascript
// Check localStorage
const authSession = localStorage.getItem('auth-session')
console.log('localStorage auth-session:', authSession ? JSON.parse(authSession) : 'NOT FOUND')

// Check cookies
console.log('Cookies:', document.cookie)

// Test /api/auth/me endpoint
fetch('/api/auth/me')
  .then(r => r.json())
  .then(data => console.log('/api/auth/me response:', data))
  .catch(err => console.error('/api/auth/me error:', err))
```

## Step 4: Force Render Button (Temporary Test)

```javascript
// Create a temporary logout button to test if it's a rendering issue
const testButton = document.createElement('button')
testButton.textContent = 'TEST LOGOUT'
testButton.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; padding: 10px; background: red; color: white; border: none; cursor: pointer;'
testButton.onclick = async () => {
  await fetch('/api/auth/signout', { method: 'POST' })
  localStorage.removeItem('auth-session')
  window.location.href = '/login'
}
document.body.appendChild(testButton)
console.log('Test logout button added to top-right corner (red)')
```

## Expected Results:

### If Authentication is Working:
- ✅ Console shows user object
- ✅ `data-testid="logout-button"` found in DOM
- ✅ Button is visible (offsetParent !== null)
- ✅ Multiple buttons on page (5+ on tasks page)

### If Button is Hidden by CSS:
- ✅ Button exists in DOM
- ❌ visibility: hidden or opacity: 0
- ❌ display: none
- Fix: Check CSS classes and z-index

### If Authentication Failed:
- ❌ /api/auth/me returns 401 or error
- ❌ localStorage.getItem('auth-session') is null
- ❌ User object is null in console
- Fix: Re-login at /login

### If Button Not in DOM:
- ❌ querySelector returns null
- ❌ Console doesn't show "[Dashboard] Render" logs
- Fix: Check if on correct page (/ or /tasks)

## Quick Fixes:

### Fix 1: Hard Refresh
```bash
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)
```

### Fix 2: Clear Everything and Re-login
```javascript
localStorage.clear()
document.cookie.split(";").forEach(c => {
  document.cookie = c.split("=")[0] + "=;expires=" + new Date().toUTCString() + ";path=/"
})
location.href = '/login'
```

### Fix 3: Manual Logout
```javascript
// Paste in console
async function manualLogout() {
  try {
    await fetch('/api/auth/signout', { method: 'POST' })
    console.log('API logout successful')
  } catch (e) {
    console.log('API logout failed:', e)
  }
  localStorage.removeItem('auth-session')
  localStorage.clear()
  window.location.href = '/login'
}
manualLogout()
```

## Report Back:

Please run Step 2 (DOM Inspection) and share:
1. Total buttons found
2. Is logout button in DOM? (logoutByTestId result)
3. What page are you on? (window.location.pathname)
4. Console logs from [useAuth] and [Dashboard/Tasks]
