
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
const {
    formatTime, calPercent,
    removeQueryParam, text_cleaner,
    save_metadata, save_as_csv
} = require("./logics");


const HOME_URL = "https://www.flipkart.com";

// Different Routes with Filters
const apis = {
    "sortOrder": ["MOST_HELPFUL", "MOST_RECENT", "POSITIVE_FIRST", "NEGATIVE_FIRST"],
    "certifiedBuyer": ["false", "true"],
    "aid": ["overall"]
};

// Define the selectors for the elements we need to extract.
const selectors = {
    deadend: "div._1G0WLw.mpIySA", // if not present
    allReviews: "div.col.EPCmJX.Ma1fCG",
    authorName: "p._2NsDsF.AwS1CA",
    reviewTitle: "p.z9E0IG",
    rating: "div.XQDdHH.Ga3i8K",
    reviewText: "div.ZmyHeo div > div",
};

const stats_star = {};
for (const key of apis["sortOrder"]) {
    stats_star[key] = 0;
}

let records_cnt = 0, total_pgs = 0;

const {
    SSN_ID,
    PRODUCT_URL, PRODUCT_NAME, CATEGORY,
    SCRAPE_MODE, BROWSER_VIEW,
    WRITE_SPEED, PAGE_SCRAP_LIMIT, PAGE_LOAD_LIMIT,
    FILE_NAME
} = JSON.parse(process.argv[2]);

const ssnDir = path.join(__dirname, "cache", "fkart");
const ssnFile = path.join(ssnDir, `${SSN_ID}.json`);

// Define the path to the "Database" directory and the file name
const dbDir =
(SCRAPE_MODE === "Deploy")?
path.join(__dirname, "..", "..", "database", "fkart") :
path.join(__dirname, "..", "database", "fkart");

const csvFilePath = path.join(dbDir, `${FILE_NAME}.csv`);
const mdFilePath = path.join(dbDir, `meta_data.csv`); // meta-data



function removeFiltersFromURL(fullURL) {
    let t1 = fullURL;
    t1 = removeQueryParam(t1, "sortOrder");
    t1 = removeQueryParam(t1, "certifiedBuyer");
    t1 = removeQueryParam(t1, "page");
    t1 = removeQueryParam(t1, "aid");
    return t1;
}


if (!fs.existsSync(ssnDir) || !fs.existsSync(ssnFile)) {
    console.error(`Session #${SSN_ID} Cookie NOT FOUND`);
    console.error("Ensure Correct Session ID or Ensure to Login First");
    process.exit(1);
}


async function fetch_fkart_reviews() {

    // Record the start time
    let loginST = performance.now();

    const browser = await puppeteer.launch({
        headless: (BROWSER_VIEW == "true") ? false:true,
    });

    // Re-create that page
    const page = await browser.newPage();
    // Load the session data from the file
    const sessionData = JSON.parse(fs.readFileSync(ssnFile));
    // Now that the session is restored, navigate to the Fkart page
    await page.goto(HOME_URL, { waitUntil: "domcontentloaded" });
    // Set cookies
    await page.setCookie(...sessionData.cookies);
    // Restore localStorage
    await page.evaluate((localStorageData) => {
        const parsedData = JSON.parse(localStorageData);
        for (let key in parsedData) {
            localStorage.setItem(key, parsedData[key]);
        }
    }, sessionData.localStorage);
    // Record the end time
    let loginET = performance.now();
    
    // Record the start time
    let scrapST = performance.now();

    // Scraper Logic
    const reviewsData = [];
    for (let j = 0; j < apis["aid"].length; j++) {
        const f1 = `&aid=${apis["aid"][j]}`;
        for (let k = 0; k < apis["sortOrder"].length; k++) {

            const f2 = `&sortOrder=${apis["sortOrder"][k]}`;
            const filteredURL = `${PRODUCT_BASE_URL}?${f1}${f2}`;

            let reviewsCntPerFilter = 0;
            // Scrape reviews from the pages specified in the arguments
            for (var pageNum = 1; ; pageNum++) {

                const productURL = `${filteredURL}&page=${pageNum}`;
                try {
                    await page.goto(productURL, { waitUntil: "load", timeout: PAGE_LOAD_LIMIT });
                    await page.waitForSelector(selectors.deadend, { timeout: PAGE_SCRAP_LIMIT });
                    await page.waitForSelector(selectors.allReviews, { timeout: PAGE_SCRAP_LIMIT });
        
                    // Collect all Review Cards
                    var reviewCards = await page.$$(selectors.allReviews, { timeout: PAGE_SCRAP_LIMIT });
    
                    for (const reviewCard of reviewCards) {
    
                        try {
                            const author1 = await reviewCard.$eval(selectors.authorName, (el) => {
                                return el?.textContent?.trim() ?? "";
                            }, { timeout: PAGE_SCRAP_LIMIT }); var author = text_cleaner(author1);
        
                            try {
                                const title1 = await reviewCard.$eval(selectors.reviewTitle, (el) => {
                                    return el?.innerHTML?.trim() ?? "";
                                }, { timeout: PAGE_SCRAP_LIMIT }); var title = text_cleaner(title1);
        
                            } catch(error) {
                                // let p1 = `Warn: Reviews Title Selector...`;
                                // let p2 = `@PageNum: ${pageNum} - &sortOrder=${apis["sortOrder"][k]}`;
                                // console.log(`${p1}\t${p2}`);
                                continue; // or maybe do something
                            }
        
                            var rating = await reviewCard.$eval(selectors.rating, (el) => {
                                const str = el?.textContent?.trim() ?? "";
                                // Match numerical rating (e.g., 3.5, 4, etc.)
                                const match = str.match(/^(\d+(\.\d+)?)/);
                                return match ? match[1] : "3.33";  // Default rating if not found
                            }, { timeout: PAGE_SCRAP_LIMIT });
        
                            var content1 = await reviewCard.$eval(selectors.reviewText, (el) => {
                                return el?.innerHTML?.trim() ?? "";
                            }, { timeout: PAGE_SCRAP_LIMIT }); var content = text_cleaner(content1);
    
                        } catch (error) {
                            console.error(`New Error: ...`);
                            console.log(`Error2: ${error.message}`);
                            process.exit(1);// break;
                        }
    
                        // Only push the review if all fields are found
                        if (author && title && rating && content) {
                            reviewsCntPerFilter++;
                            reviewsData.push({PRODUCT_NAME, author, title, rating, content });
                            // Don't Save all, just save them
                            if (reviewsData.length >= WRITE_SPEED) {
                                records_cnt += save_as_csv(dbDir, csvFilePath, reviewsData);
                                reviewsData.length = 0;
                            }
                        }
                        // else {
                        //     let p1 = `Warn: DATA-NOT-COMPLETE`;
                        //     let p2 = `@PageNum: ${pageNum} - &sortOrder=${apis["sortOrder"][k]}`;
                        //     console.log(`${p1}\t${p2}`);
                        //     console.log(`${author}\t${title}`);
                        //     console.log(`${rating}\t${content}`);
                        // }
                    }
                } catch (error) {
                    console.log(`End of Reviews-Page #${apis["sortOrder"][k]} @PageNum: ${pageNum}`);
                    // console.log(`ERROR3: ${error.message}`);
                    break;
                }
                total_pgs++;
            }
            stats_star[apis["sortOrder"][k]] = reviewsCntPerFilter;
        }
    } await browser.close();

    // Record the end time
    let scrapET = performance.now();

    if (reviewsData.length > 0) {
        records_cnt += save_as_csv(dbDir, csvFilePath, reviewsData);
        reviewsData.length = 0;
    } save_metadata(dbDir, mdFilePath, {"Product_Name": PRODUCT_NAME, "Category": CATEGORY})

    let loginTime = loginET-loginST;
    let scrapTime = scrapET-scrapST;
    let totalTime = loginTime+scrapTime;
    console.log(`Total Login-Time: ${formatTime(loginTime)}`);
    console.log(`Total Scrap-Time: ${formatTime(scrapTime)}`);
    console.log(`Total Time: ${formatTime(totalTime)}`);

    // Log a Stat message
    // console.log(`Total Number of Records (Expected): ${Number(TOTAL).toLocaleString()}`);
    console.log(`Total Number of Records (Reality): ${Number(records_cnt).toLocaleString()}`);
    // console.log(`Scraping Rate: ${calPercent(records_cnt, TOTAL)}%`);
    console.log(`Total Pages-Covered: ${total_pgs}`);
    // Loop through the key-value pairs of stats_star
    for (const [key, value] of Object.entries(stats_star)) {
        console.log(`${key}: ${Number(value).toLocaleString()} reviews`);
    }
    console.log(`CSV File saved as: ${csvFilePath}`);

}


const PRODUCT_BASE_URL = removeFiltersFromURL(PRODUCT_URL);
console.info(`BASE-URL: ${PRODUCT_BASE_URL}`);
console.info(`Product_Name: ${PRODUCT_NAME}, Category: ${CATEGORY}`);
fetch_fkart_reviews();
