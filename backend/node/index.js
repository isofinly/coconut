"use strict";
const express = require("express");
const { chromium } = require("playwright-extra");

const stealth = require('puppeteer-extra-plugin-stealth')()

chromium.use(stealth)

chromium.plugins.setDependencyDefaults("stealth/evasions/webgl.vendor", {
  vendor: "Bob",
  renderer: "Alice",
});

const app = express();
const port = 3050;

const userAgentStrings = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
];

app.use(express.json());

/**
 * Handles a POST request to extract metadata from a list of URLs.
 *
 * @param req - The incoming HTTP request object containing the list of URLs in the request body.
 * @param res - The HTTP response object to send the extracted metadata as a JSON response.
 * @returns - JSON response containing metadata extracted from the provided URLs.
 */
app.post("/extract_metadata", async (req, res) => {
  const { urls } = req.body;

  if (!urls || !Array.isArray(urls)) {
    return res
      .status(400)
      .json({ error: "Missing or invalid URLs in the request body" });
  }

  const results = [];

  try {
    const browser = await chromium.launch({
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-blink-features=AutomationControlled",
      ],
      headless: true,
      ignoreHTTPSErrors: true,
    });

    const context = await browser.newContext({
      userAgent:
        userAgentStrings[Math.floor(Math.random() * userAgentStrings.length)],
      viewport: {
        width: 1388,
        height: 768,
      },
    });

    const pagePromises = urls.map(async (url) => {
      const page = await context.newPage();

      const response = await page
        .goto(url, {
          waitUntil: "domcontentloaded",
        })
        .catch(() => null);

      await page.waitForTimeout(1500).catch(() => null);

      if (response && response.status() < 500 && response.status() !== 404) {
        const title = await page.title().catch(() => "None");

        const description = await page
          .$eval('meta[name="description"]', (meta) => meta.content)
          .catch(() => "None");

        let keywords;

        try {
          keywords = await page.$eval(
            'meta[name="keywords"]',
            (meta) => meta.content
          );
        } catch (error) {
          keywords = "None";
        }

        const ogTags = await page
          .$$eval('meta[property^="og:"]', (metaElements) => {
            const ogData = {};
            metaElements.forEach((meta) => {
              const property = meta.getAttribute("property");
              const content = meta.getAttribute("content");
              if (property && content) {
                ogData[property] = content;
              }
            });
            return ogData;
          })
          .catch(() => {
            return {
              "og:url": "None",
              "og:type": "website",
              "og:title": "None",
              "og:image": "None",
              "og:description": "None",
            };
          });

        const result = {
          title,
          description,
          keywords,
          ogTags,
        };
        results.push(result);
      }
      await page.close();
    });

    await Promise.all(pagePromises);

    await browser.close();

    res.json(results);
  } catch (error) {
    console.error(error);
    res
      .status(500)
      .json({ error: "An error occurred while processing the request" });
  }
});


/**
 * Handles a POST request to extract href attributes from &lt;a&gt; tags in a list of URLs.
 *
 * @param req - The incoming HTTP request object containing the list of URLs in the request body.
 * @param res - The HTTP response object to send the extracted href attributes as a JSON response.
 * @returns - JSON response containing href attributes extracted from &lt;a&gt; tags in the provided URLs.
 */
app.post("/extract_a", async (req, res) => {
  const { urls } = req.body;

  if (!urls || !Array.isArray(urls)) {
    return res
      .status(400)
      .json({ error: "Missing or invalid URLs in the request body" });
  }

  const results = [];

  try {
    const browser = await chromium.launch({
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-blink-features=AutomationControlled",
      ],
      headless: true,
      ignoreHTTPSErrors: true,
    });

    const context = await browser.newContext({
      userAgent:
        userAgentStrings[Math.floor(Math.random() * userAgentStrings.length)],
      viewport: {
        width: 1388,
        height: 768,
      },
    });

    const pagePromises = urls.map(async (url) => {
      const page = await context.newPage();

      const response = await page
        .goto(url, {
          waitUntil: "domcontentloaded",
        })
        .catch(() => null);

      await page.waitForTimeout(1500).catch(() => null);

      if (response && response.status() < 500 && response.status() !== 404) {
        const aTags = await page
          .$$eval("a", (aElements) => aElements.map((a) => a.href))
          .catch(() => ["None"]);

        const result = {
          aTags,
        };
        results.push(result);
      }
      await page.close();
    });

    await Promise.all(pagePromises);

    await browser.close();

    res.json(results);
  } catch (error) {
    console.error(error);
    res
      .status(500)
      .json({ error: "An error occurred while processing the request" });
  }
});

/**
 * Handles a POST request to extract text content from &lt;p&gt; tags in a list of URLs.
 *
 * @param req - The incoming HTTP request object containing the list of URLs in the request body.
 * @param res - The HTTP response object to send the extracted text content as a JSON response.
 * @returns - JSON response containing text content extracted from &lt;p&gt; tags in the provided URLs.
 */
app.post("/extract_p", async (req, res) => {
  const { urls } = req.body;

  if (!urls || !Array.isArray(urls)) {
    return res
      .status(400)
      .json({ error: "Missing or invalid URLs in the request body" });
  }

  const results = [];

  try {
    const browser = await chromium.launch({
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-blink-features=AutomationControlled",
      ],
      headless: true,
      ignoreHTTPSErrors: true,
    });

    const context = await browser.newContext({
      userAgent:
        userAgentStrings[Math.floor(Math.random() * userAgentStrings.length)],
      viewport: {
        width: 1388,
        height: 768,
      },
    });

    const pagePromises = urls.map(async (url) => {
      const page = await context.newPage();

      const response = await page
        .goto(url, {
          waitUntil: "domcontentloaded",
        })
        .catch(() => null);

      await page.waitForTimeout(1500).catch(() => null);

      if (response && response.status() < 500 && response.status() !== 404) {
        const pTags = await page
          .$$eval("p", (pElements) => pElements.map((p) => p.textContent))
          .catch(() => ["None"]);

        const result = {
          pTags,
        };
        results.push(result);
      }
      await page.close();
    });

    await Promise.all(pagePromises);

    await browser.close();

    res.json(results);
  } catch (error) {
    console.error(error);
    res
      .status(500)
      .json({ error: "An error occurred while processing the request" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
