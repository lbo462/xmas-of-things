# API Documentation

Nothing to see here yet


---

### **Custom Downlink Payload Formatter in TTN**

To display the action name, value, and ID in TTN when you send commands, you need to set up a custom downlink payload formatter in TTN.

#### **Custom JavaScript Encoder Function**

In TTN Console:

1. **Navigate to your application and select your device (`testarduino`).**
2. **Click on "Payload Formatters" and select the "Downlink" tab.**
3. **Choose "Custom Javascript formatter" as the formatter type.**

Paste the following JavaScript code into the editor:

```javascript
// Custom Downlink Encoder
`function Encoder(obj, fPort) {
    var bytes = [];

    // Encode action_id
    if ('action_id' in obj) {
        bytes.push(obj.action_id);
    }

    // Encode duration if present
    if ('duration' in obj) {
        var duration = obj.duration;
        bytes.push((duration >> 8) & 0xFF);
        bytes.push(duration & 0xFF);
    }

    // Encode action_name length and characters
    if ('action_name' in obj) {
        var name = obj.action_name;
        bytes.push(name.length); // First, add the length of the name
        for (var i = 0; i < name.length; i++) {
            bytes.push(name.charCodeAt(i));
        }
    }

    return bytes;
}`
