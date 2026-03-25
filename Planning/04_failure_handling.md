# Failure Handling Plan

## Possible Failures and Solutions

### Invalid Login
- Show error message: "Invalid username or password"

### Duplicate Registration
- Prevent duplicate usernames/emails

### Product Out of Stock
- Show "Out of Stock" message

### Cart Issues
- Remove invalid or deleted products automatically

### Checkout Errors
- Validate all required fields before submission

### Password Reset Issues
- Handle expired or invalid tokens

### Database Errors
- Show generic error message
- Prevent app crash

### Unauthorized Access
- Redirect to login page

## Logging
- Use Django logging for debugging errors