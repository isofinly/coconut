const express = require("express");
const { chromium } = require("playwright");
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

const app = express();
const port = 3050;

const userAgentStrings = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
];

app.use(express.json());

puppeteer.use(StealthPlugin());

app.post("/extract-data", async (req, res) => {
  const { urls } = req.body;

  if (!urls || !Array.isArray(urls)) {
    return res
      .status(400)
      .json({ error: "Missing or invalid URLs in the request body" });
  }

  const results = [];

  try {
    const browser = await chromium.launch({
      headless: false,
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-blink-features=AutomationControlled",
      ],
      slowMo: 100,
    });
    const context = await browser.newContext({
      userAgent:
        userAgentStrings[Math.floor(Math.random() * userAgentStrings.length)],
      permissions: ["clipboard-read", "clipboard-write"],
      viewport: {
        width: 1388,
        height: 768,
      },
    });
  
    for (const url of urls) {
      const page = await context.newPage();
      
      const response = await page.goto(url, {
        waitUntil: 'domcontentloaded', // Wait for DOMContentLoaded event
      }).catch(() => {
        return null;
      });
      
      // Wait for an additional 1.5 seconds (1500 milliseconds) to ensure JavaScript has loaded
      await page.waitForTimeout(1500).catch
        (() => {
          return null;
        });
      
  
      if (response && response.status() === 200) {
        const title = await page.title();
        const description = await page
          .$eval('meta[name="description"]', (meta) => meta.content)
          .catch(() => {
            return "error";
          });
  
        let keywords;
        try {
          keywords = await page.$eval(
            'meta[name="keywords"]',
            (meta) => meta.content
          );
        } catch (error) {
          keywords = "error";
        }
  
        const pTags = await page
          .$$eval("p", (pElements) => pElements.map((p) => p.textContent))
          .catch(() => {
            return ["error"];
          });
        const aTags = await page
          .$$eval("a", (aElements) => aElements.map((a) => a.href))
          .catch(() => {
            return ["error"];
          });
  
        // Extract OG meta data
        const ogTags = await page.$$eval(
          'meta[property^="og:"]',
          (metaElements) => {
            const ogData = {};
            metaElements.forEach((meta) => {
              const property = meta.getAttribute("property");
              const content = meta.getAttribute("content");
              if (property && content) {
                ogData[property] = content;
              }
            });
            return ogData;
          }
        );
  
        const result = {
          title,
          description,
          keywords,
          //   pTags,
          //   aTags,
          ogTags,
        };
        // console.log(result);
        results.push(result);
      }
  
      // Close the page after processing
      await page.close();
    }
  
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
