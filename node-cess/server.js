
import express from 'express';
import bodyParser from 'body-parser';
import { InitAPI, Space, Bucket, File, testnetConfig } from 'cess-js-sdk';
import os from 'os';
import fs from 'fs';
import path from 'path';

const app = express();
const port = 3000; // You can choose any port that suits your setup

app.use(bodyParser.json());

const mnemonic = "bottom drive obey lake curtain smoke basket hold race lonely fit walk";
const acctId = "cXgaee2N8E77JJv9gdsGAckv1Qsf3hqWYf7NL4q6ZuQzuAUtB";

const BUCKET_NAME = "test2"; // bucket name

// Initialize CESS SDK
async function initializeCESS() {
    const { api, keyring } = await InitAPI(testnetConfig);
    const space = new Space(api, keyring);
    const common = new Common(api, keyring);
    const bucket = new Bucket(api, keyring);
    const file = new File(api, keyring, testnetConfig.gatewayURL);
  
    console.log("API initialized.");
  
    const [chain, nodeName, nodeVersion] = await Promise.all([
      api.rpc.system.chain(),
      api.rpc.system.name(),
      api.rpc.system.version(),
    ]);
    console.log(`Connected to chain ${chain} using ${nodeName} v${nodeVersion}`);
  
    const balanceEncoded = await api.query.system.account(acctId);
    const { data } = balanceEncoded.toJSON();
    console.log(`User: ${acctId}, balance:`, BigInt(data.free));
    return { api, keyring, file };
}

// Example endpoint for uploading files to CESS
app.post('/upload', async (req, res) => {
    const { api, keyring, file } = await initializeCESS();

    const privateVal = req.body.private;
    const publicVal = req.body.public;

    // Create the file content
    const fileContent = JSON.stringify({ private: privateVal, public: publicVal });

    try {
        // Generate a temporary file path
        const tempDir = os.tmpdir();
        const filePath = path.join(tempDir, `upload_${Date.now()}.json`);

        // Write the content to the temporary file
        await fs.writeFile(filePath, fileContent);

        // Log the file path (optional)
        console.log("Temporary file path:", filePath);

        // Upload the file to CESS using the fileService
        const fileService = new File(api, keyring, testnetConfig.gatewayURL);
        const uploadResponse = await fileService.uploadFile(mnemonic, acctId, filePath, BUCKET_NAME);

        // Respond to the client
        res.json({ message: 'File uploaded successfully', file_hash: uploadResponse.data });
    } catch (error) {
        console.error("Failed to upload file:", error);
        res.status(500).json({ error: 'Failed to upload file' });
    }
});

app.get('/download/:fileHash', async (req, res) => {
    const { fileHash } = req.params;
    const { api, keyring, file } = await initializeCESS();
    // Generate a temporary file path
    const tempDir = os.tmpdir();
    const tempFilePath = path.join(tempDir, `tempFile_${fileHash}.json`);

    try {
        // Download the file to the temporary path
        await file.downloadFile(fileHash, tempFilePath);
        console.log(`File with hash ${fileHash} downloaded successfully to ${tempFilePath}`);

        // Read the file contents
        const fileContents = await fs.readFile(tempFilePath, 'utf8');
        // Parse the JSON content
        const { private: privateVal, public: publicVal } = JSON.parse(fileContents);

        // Send the private and public values back in the response
        res.json({
            message: "File processed successfully.",
            data: {
                private: privateVal,
                public: publicVal,
            },
        });
    } catch (error) {
        console.error("Error processing file:", error);
        res.status(500).send(`Failed to process file with hash ${fileHash}.`);
    } finally {
        // Delete the temporary file
        try {
            await fs.unlink(tempFilePath);
            console.log(`Temporary file ${tempFilePath} deleted successfully.`);
        } catch (error) {
            console.error("Error deleting temporary file:", error);
            // Handle deletion error if necessary, like logging or sending a notification
        }
    }
});

// Delete file endpoint
app.delete('/delete-file/:fileHash', async (req, res) => {
    const { fileHash } = req.params; // Get the fileHash from the URL parameter
    const { api, keyring, file } = await initializeCESS();

    try {
        const deleteResponse = await file.deleteFile(mnemonic, acctId, fileHash);
        console.log("Delete file response:", deleteResponse); // Log or handle the response as needed

        // Respond to the client indicating success
        res.json({ message: "File deleted successfully.", fileHash });
    } catch (error) {
        console.error("Error deleting file:", error);
        res.status(500).json({ error: "Failed to delete file.", details: error.message });
    }
});

app.listen(port, () => {
    console.log(`Node server listening at http://localhost:${port}`);
});
