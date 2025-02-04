# Developing and Running a Safari Extension in Xcode

This guide provides concise instructions to create, configure, and test a Safari Web Extension directly using Xcode on macOS. It covers installing required tools, setting up your Xcode project, customizing your extension files, building and running the extension in Safari, and troubleshooting common issues.

---

## Step 1: Install Required Tools

Safari Web Extensions require Xcode to build and sign the extension. Ensure that the Xcode CLI tool `xcrun` is available.

### 1.1 Install Xcode

- Open Terminal and verify the Xcode CLI tools:
  ```sh
  xcode-select --version
  ```
- If not installed, run:
  ```sh
  xcode-select --install
  ```

### 1.2 Verify `xcrun` is Available

- Check its version:
  ```sh
  xcrun --version
  ```
- If missing, reinstall Xcode CLI tools:
  ```sh
  sudo rm -rf /Library/Developer/CommandLineTools
  xcode-select --install
  ```

---

## Step 2: Create a New Safari Web Extension Project in Xcode

### 2.1 Launch Xcode and Create a New Project

- Open Xcode.
- Select **File > New > Project...**
- In the template chooser, under the **App** category, select **Safari Web Extension App**.
- Click **Next**.

### 2.2 Configure Your Project

- Enter your project name (for example, "TextareaContentViewer").
- Choose your preferred language (Swift or Objective-C) for the container app.
- Xcode automatically creates two targets:
  - **App**: A minimal host application for your extension.
  - **Safari Web Extension**: Contains the extension files.
- Select a location to save the project and click **Create**.

---

## Step 3: Understand the Project Structure

The new project includes:

- **Safari Web Extension** target:
  - `manifest.json`: The extension manifest.
  - HTML, JavaScript, and CSS files for the extension (for example, `popup.html`, `popup.js`, and `content-script.js`).
- **App** target:
  - A minimal container app that manages extension installation.

---

## Step 4: Customize Your Safari Extension

### 4.1 Modify `manifest.json`

Open `manifest.json` in the Safari Web Extension folder and adjust as needed. For example:

```json
{
  "manifest_version": 2,
  "name": "Textarea Content Viewer",
  "version": "1.0",
  "description": "Gets the content of a textarea on the page and displays it in a popup.",
  "permissions": [
    "activeTab"
  ],
  "browser_action": {
    "default_popup": "popup.html",
    "default_icon": "icons/icon48.png"
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content-script.js"],
      "run_at": "document_end"
    }
  ]
}
```

> Note: Remove any unused sections such as `background` and associated files if they exist.

### 4.2 Edit Extension Files

Customize your extension files within Xcode. Below are sample contents for key files.

#### popup.html

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Textarea Content</title>
  <style>
    body {
      width: 300px;
      padding: 10px;
      font-family: sans-serif;
    }
    pre {
      white-space: pre-wrap;
      word-wrap: break-word;
    }
  </style>
</head>
<body>
  <h1>Textarea Content</h1>
  <pre id="textareaContent">Loading...</pre>

  <script src="popup.js"></script>
</body>
</html>
```

#### popup.js

```js
document.addEventListener('DOMContentLoaded', () => {

  browser.tabs.query({ active: true, currentWindow: true }).then((tabs) => {

    let activeTab = tabs[0];
    return browser.tabs.sendMessage(activeTab.id, { action: "getTextareaContent" });

  }).then((response) => {

    document.getElementById('textareaContent').textContent =
      response.content || "No textarea found.";

  }).catch((error) => {

    document.getElementById('textareaContent').textContent = "Error: " + error;

  });

});
```

#### content-script.js

```js
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {

  if (message.action === "getTextareaContent") {

    let textarea = document.querySelector('textarea');
    let content = textarea ? textarea.value : "";
    sendResponse({ content });

  }

});
```

---

## Step 5: Build and Run the Extension in Xcode

### 5.1 Set Up Signing and Capabilities

- Select the **Safari Web Extension** target.
- Navigate to **Signing & Capabilities**.
- Choose your Apple Developer account.
- If necessary, set up a development team and adjust the bundle identifier.

### 5.2 Build and Run

- Select the appropriate scheme (usually the container app).
- Click **Run** (or press Command+R) to build the project.
- Safari will launch automatically with your extension installed.

---

## Step 6: Enable the Extension in Safari

1. Open Safari.
2. Navigate to **Safari > Settings (Preferences) > Extensions**.
3. Locate **"Textarea Content Viewer"** and enable it.
4. Allow any required permissions, such as **"Always Allow on All Websites"**, if prompted.

---

## Step 7: Test and Debug the Extension

### 7.1 Testing

1. Open a webpage that contains a `<textarea>`.
2. Click the extension icon in the Safari toolbar.
3. A popup should appear, displaying the content of the first `<textarea>` found.

### 7.2 Debugging

- Use Xcode to set breakpoints in your extension code.
- To inspect the extension popup:
  1. Open Safari.
  2. Enable Developer Mode in **Safari > Settings > Advanced > Show Develop menu**.
  3. Right-click the extension popup and select **Inspect Element**.

---

## Step 8: Package the Extension (Optional)

To distribute the extension, package it using Xcode:

1. In Xcode, select **Product > Archive**.
2. When the archive completes, use the **Organizer** window to distribute your extension.
3. Follow Apple guidelines for distributing Safari extensions.

---

## Icon Requirements

Safari expects specific icon sizes:

- **16x16** (small toolbar icon)
- **48x48** (medium)
- **128x128** (large)

If your icons do not match these sizes, rename or create new icons. For example, if you have icons with different names:

```sh
mv icons/text-box-30.png icons/icon16.png
mv icons/text-box-60.png icons/icon48.png
mv icons/text-box-90.png icons/icon128.png
```

---

You now have a concise guide to create, customize, and test a Safari Web Extension directly in Xcode. Use Xcode to edit and build your extension, and then test it in Safari with the provided development tools.
