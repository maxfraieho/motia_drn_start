const express = require('express');
const puppeteer = require('puppeteer');
const winston = require('winston');
const path = require('path');

// Configure logger
const logger = winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console({
            format: winston.format.combine(
                winston.format.colorize(),
                winston.format.simple()
            )
        })
    ]
});

// Express app setup
const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

const PORT = process.env.PORT || 3000;

// Browser instance pool (simple implementation for POC)
let browserInstance = null;

async function getBrowser() {
    if (!browserInstance) {
        logger.info('Launching new browser instance...');
        browserInstance = await puppeteer.launch({
            headless: 'new',
            executablePath: '/usr/bin/chromium-browser',
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        });
        logger.info('Browser instance launched successfully');
    }
    return browserInstance;
}

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'drakon-generator' });
});

// Main diagram generation endpoint
app.post('/generate', async (req, res) => {
    const startTime = Date.now();
    logger.info('Received diagram generation request');

    try {
        const { commands } = req.body;

        if (!commands || !Array.isArray(commands)) {
            return res.status(400).json({
                success: false,
                error: 'Invalid request: commands array required'
            });
        }

        // Get browser instance
        const browser = await getBrowser();
        const page = await browser.newPage();

        // Navigate to host page
        const hostUrl = `http://localhost:${PORT}/host.html`;
        logger.info(`Navigating to ${hostUrl}`);
        await page.goto(hostUrl, { waitUntil: 'networkidle0' });

        // Wait for drakonWidget to load
        await page.waitForFunction('typeof window.DrakonTestAPI !== "undefined"', {
            timeout: 10000
        });

        logger.info('DrakonWidget loaded, executing commands...');

        // Execute commands in the page context
        const diagram = await page.evaluate((cmds) => {
            // Execute each command
            for (const cmd of cmds) {
                switch (cmd.type) {
                    case 'createDiagram':
                        window.DrakonTestAPI.createDiagram(cmd.name);
                        break;
                    case 'addNode':
                        window.DrakonTestAPI.addNode(cmd.nodeType);
                        break;
                    case 'setContent':
                        window.DrakonTestAPI.setNodeContent(cmd.nodeId, cmd.content);
                        break;
                    case 'connect':
                        window.DrakonTestAPI.connectNodes(cmd.from, cmd.to);
                        break;
                }
            }

            // Get the resulting diagram
            return window.DrakonTestAPI.getDiagram();
        }, commands);

        await page.close();

        const generationTime = Date.now() - startTime;
        logger.info(`Diagram generated successfully in ${generationTime}ms`);

        res.json({
            success: true,
            diagram: diagram,
            generationTime: generationTime
        });

    } catch (error) {
        logger.error('Diagram generation failed:', error);
        res.status(500).json({
            success: false,
            error: error.message,
            details: error.stack
        });
    }
});

// Graceful shutdown
process.on('SIGTERM', async () => {
    logger.info('SIGTERM received, closing browser...');
    if (browserInstance) {
        await browserInstance.close();
    }
    process.exit(0);
});

// Start server
app.listen(PORT, () => {
    logger.info(`Drakon Generator Service listening on port ${PORT}`);
    logger.info(`Health check: http://localhost:${PORT}/health`);
    logger.info(`Host page: http://localhost:${PORT}/host.html`);
});
