// Register the device for notifications (returns its device token)
var api_key = 'ae43f92633d46f240a9b32ee727d629dee8877ba4ff00767668005ef3fe71ed2';
var url_base = 'https://api.pushy.me';

// Sample code to send "token" to your backend server via an HTTP request:
new URL("https://api.example.com/register/device?token=" + token).openConnection();