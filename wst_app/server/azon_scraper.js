
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
const {
    formatTime, calPercent,
    removeQueryParam, text_cleaner,
    save_metadata, save_as_csv
} = require("./logics");


const HOME_URL = "https://www.amazon.com";

// Different Routes with Filters
const apis = {
    "sortBy": ["helpful", "recent"],
    "reviewerType": ["all_reviews", "avp_only_reviews"],
    "filterByStar": ["five_star", "four_star", "three_star", "two_star", "one_star"]//, "positive", "critical"]
};

// Define the selectors for the elements we need to extract.
const selectors = {
    allReviews: '#cm_cr-review_list div.review',
    authorName: 'div[data-hook="genome-widget"] span.a-profile-name',
    reviewTitle: '[data-hook=review-title]>span:not([class])',
    rating: '[data-hook="review-title"] span.a-icon-alt',
    reviewText: 'div[class="a-row a-spacing-small review-data"] span',
    totalReviews: `div[data-hook="cr-filter-info-review-rating-count"]`
};

const stats_star = {};
for (const key of apis["filterByStar"]) {
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

const ssnDir = path.join(__dirname, "cache", "azon");
const ssnFile = path.join(ssnDir, `${SSN_ID}.json`);

// Define the path to the "Database" directory and the file name
const dbDir =
(SCRAPE_MODE === "Deploy")?
path.join(__dirname, "..", "..", "database", "azon") :
path.join(__dirname, "..", "database", "azon");

const csvFilePath = path.join(dbDir, `${FILE_NAME}.csv`);
const mdFilePath = path.join(dbDir, `meta_data.csv`); // meta-data



function removeFiltersFromURL(fullURL) {
    let t1 = fullURL;
    t1 = removeQueryParam(t1, "sortBy");
    t1 = removeQueryParam(t1, "reviewerType");
    t1 = removeQueryParam(t1, "filterByStar");
    t1 = removeQueryParam(t1, "formatType");
    t1 = removeQueryParam(t1, "mediaType");
    t1 = removeQueryParam(t1, "pageNumber");
    return t1;
}


if (!fs.existsSync(ssnDir) || !fs.existsSync(ssnFile)) {
    console.error(`${SSN_ID} COOKIE-NOT-FOUND`);
    console.error("Ensure Correct Session ID or Ensure to Login First");
    process.exit(1);
}


async function fetch_azon_reviews() {

    // Record the start time
    let loginST = performance.now();
    let browser = null;
    let page = null;
    
    try {
        browser = await puppeteer.launch({
            headless: (BROWSER_VIEW == "true") ? false:true,
        });
        // Re-create that page
        page = await browser.newPage();
        // Load the session data from the file
        const sessionData = JSON.parse(fs.readFileSync(ssnFile));
        // Now that the session is restored, navigate to the Amazon page
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
        var loginET = performance.now();
        
        // Record the start time
        var scrapST = performance.now();
        // Increase TIMEOUT Value (in ms)
        await page.goto(PRODUCT_BASE_URL, { waitUntil: "load", timeout: PAGE_LOAD_LIMIT });

        var TOTAL = await page.$eval(selectors.totalReviews, (el) => {
            let text = el?.innerHTML?.trim() ?? "";
            text = text.replace(/,/g, '');
            let match = text.match(/(\d+)\s+with\s+reviews/);
            if (match)
                return parseInt(match[1], 10);
            match = text.match(/(\d+)\s+with\s+review/);
            if (match)
                return parseInt(match[1], 10);
            return 0;
        }, { timeout: PAGE_SCRAP_LIMIT });
    } catch (error) {
        console.error(`SESSION-KEYS ERROR, COULDN'T LOAD LOGGED-IN PAGE`);
        console.error(`${error.message}`);
    }

    const reviewsData = []; // keep a limit to store, then push to file
    for (let k = 0; k < apis["filterByStar"].length; k++) {

        const filter = `&filterByStar=${apis["filterByStar"][k]}`;
        const filteredURL = `${PRODUCT_BASE_URL}?${filter}`;

        let reviewsCntPerStar = 0;
        // Scrape reviews from the pages specified in the arguments
        for (var pageNum = 1; ; pageNum++) {

            const productURL = `${filteredURL}&pageNumber=${pageNum}`;
            try {
                await page.goto(productURL, { waitUntil: "load", timeout: PAGE_LOAD_LIMIT });
                await page.waitForSelector(selectors.allReviews, { timeout: PAGE_SCRAP_LIMIT });

                let total = await page.$eval(selectors.totalReviews, (el) => {
                    let text = el?.innerHTML?.trim() ?? "";
                    text = text.replace(/,/g, '');
                    let match = text.match(/(\d+)\s+with\s+reviews/);
                    if (match)
                        return parseInt(match[1], 10);
                    match = text.match(/(\d+)\s+with\s+review/);
                    if (match)
                        return parseInt(match[1], 10);
                    return 0;
                }, { timeout: PAGE_SCRAP_LIMIT });

                if (total == 0) {
                    console.log(`End of Reviews-Page #${apis["filterByStar"][k]} @PageNum: ${pageNum}`);
                    break;
                }

                // Collect all Review Cards
                var reviewCards = await page.$$(selectors.allReviews, { timeout: PAGE_SCRAP_LIMIT });

                for (const reviewCard of reviewCards) {

                    try {
                        const author1 = await reviewCard.$eval(selectors.authorName, (el) => {
                            return el?.textContent?.trim() ?? "";
                        }, { timeout: PAGE_SCRAP_LIMIT }); var author = text_cleaner(author1);

                        var rating = await reviewCard.$eval(selectors.rating, (el) => {
                            const str = el?.textContent?.trim() ?? "";
                            // Match numerical rating (e.g., 3.5, 4, etc.)
                            const match = str.match(/^(\d+(\.\d+)?)/);
                            return match ? match[1] : "3.33";  // Default rating if not found
                        }, { timeout: PAGE_SCRAP_LIMIT });
                        
                        const content1 = await reviewCard.$eval(selectors.reviewText, (el) => {
                            return el?.innerHTML?.trim() ?? "";
                        }, { timeout: PAGE_SCRAP_LIMIT }); var content = text_cleaner(content1);

                        try {
                            const title1 = await reviewCard.$eval(selectors.reviewTitle, (el) => {
                                return el?.textContent?.trim() ?? "";
                            }, { timeout: PAGE_SCRAP_LIMIT }); var title = text_cleaner(title1);
    
                        } catch(error) {
                            // let p1 = `Warn: Reviews Title Selector...`;
                            // let p2 = `@PageNum: ${pageNum} - &filterByStar=${apis["filterByStar"][k]}`;
                            // console.log(`${p1}\t${p2}`);
                            continue; // or maybe do something
                        }    

                    } catch (error) {
                        // If reviews not from India
                        continue;
                        // console.error(`New Error: ...`);
                        // console.log(`New Error: ${error.message}`);
                        // process.exit(1);// break;
                    }

                    // Only push the review if all fields are found
                    if (author && title && rating && content) {
                        reviewsCntPerStar++;
                        reviewsData.push({PRODUCT_NAME, author, title, rating, content });
                        // Don't Save all, just save them
                        if (reviewsData.length >= WRITE_SPEED) {
                            records_cnt += save_as_csv(dbDir, csvFilePath, reviewsData);
                            reviewsData.length = 0;
                        }
                    }
                    // else {
                    //     let p1 = `Warn: DATA-NOT-COMPLETE`;
                    //     let p2 = `@PageNum: ${pageNum} - &filterByStar=${apis["filterByStar"][k]}`;
                    //     console.log(`${p1}\t${p2}`);
                    //     console.log(`${author}\t${title}`);
                    //     console.log(`${rating}\t${content}`);
                    // }
                }
            } catch (error) {
                console.log(`End of Reviews-Page #${apis["filterByStar"][k]} @PageNum: ${pageNum}`);
                break;
            }
            total_pgs++;
        }
        stats_star[apis["filterByStar"][k]] = reviewsCntPerStar;
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
    console.log(`Total Number of Records (Expected): ${Number(TOTAL).toLocaleString()}`);
    console.log(`Total Number of Records (Reality): ${Number(records_cnt).toLocaleString()}`);
    console.log(`Scraping Rate: ${calPercent(records_cnt, TOTAL)}%`);
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
fetch_azon_reviews();
