const express = require('express');
const bodyParser = require('body-parser');
const { InitAPI, Space, Bucket, File, testnetConfig } = require('cess-js-sdk');

const app = express();
const port = 3000; // You can choose any port that suits your setup

app.use(bodyParser.json());

// Initialize CESS SDK
async function initializeCESS() {
    const { api, keyring } = await InitAPI(testnetConfig);
    return { api, keyring };
}

// Example endpoint for uploading files to CESS
app.post('/upload', async (req, res) => {
    const { api, keyring } = await initializeCESS();
    // Implement file upload logic here using cess-js-sdk
    // e.g., const bucket = new Bucket(api, keyring);
    res.send('File uploaded successfully');
});

// Example endpoint for downloading files from CESS
app.get('/download/:fileHash', async (req, res) => {
    const { fileHash } = req.params;
    const { api, keyring } = await initializeCESS();
    // Implement file download logic here
    res.send(`File with hash ${fileHash} downloaded successfully`);
});

app.listen(port, () => {
    console.log(`Node server listening at http://localhost:${port}`);
});
