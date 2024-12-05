
const puppeteer = require("puppeteer");
const path = require("path");
const { save_session } = require("./logics");


const AZON_SIGN_IN_URL = "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
const HOME_URL = "https://www.amazon.com";

const login_selectors = {
    emailid: "input[name=email]",
    password: "input[name=password]",
    continue: "input[id=continue]",
    signin: "input[id=signInSubmit]",
    home: "input[type=text]",
};


const dataJson = process.argv[2];
const data = JSON.parse(dataJson);
const { EMAIL_PHONE, PASSWORD, SSN_ID } = data;

// Cache the session data
console.log("Saving session data...");
const cacheDir = path.join(__dirname, "Cache", "Azon");
const fname = path.join(cacheDir, `${SSN_ID}.json`);


async function login_azon() {
    let browser = null;
    try {
        // Launch the browser
        console.log("Launching the browser...");
        browser = await puppeteer.launch({
            headless: false,
            // timeout: 0
        });

        const page = await browser.newPage();
        await page.goto(AZON_SIGN_IN_URL);

        await page.waitForSelector(login_selectors.emailid);
        await page.type(login_selectors.emailid, EMAIL_PHONE, { delay: 100 });
        await page.click(login_selectors.continue);

        await page.waitForSelector(login_selectors.password);
        await page.type(login_selectors.password, PASSWORD, { delay: 100 });
        await page.click(login_selectors.signin);
        // await page.waitForSelector(login_selectors.home);
        // Wait for navigation after login (wait until network is idle)
        // await page.waitForNavigation({ waitUntil: 'networkidle0' });
        // await page.goto(HOME_URL);

        // Step 4: Serialize cookies and localStorage
        console.log("Serializing cookies and localStorage...");

        // // Serialize cookies and localStorage
        // const cookies = await page.cookies();
        // const localStorageData = await page.evaluate(() => {
        //     return JSON.stringify(localStorage);
        // });

        const cookiesPromise = page.cookies();
        const localStoragePromise = page.evaluate(() => JSON.stringify(localStorage));
        // Step 6: Wait for promises to resolve and process data
        const cookies = await cookiesPromise;
        const localStorageData = await localStoragePromise;

        const cacheData = JSON.stringify({ cookies, localStorage: localStorageData });
        save_session(cacheDir, fname, cacheData);
        // // Close Broswer
        // browser.close();

        console.log(`Session saved successfully: ${fname}`);
        console.log("You can now use the session keys to scrape the Amazon website.");

    } catch (error) {
        // Handle different types of errors in each part of the process
        if (error.message.includes('puppeteer')) {
            console.log("Error while launching or interacting with Puppeteer:\n", error.message);
        } else if (error.message.includes('navigation')) {
            console.log("Navigation error - Could not load the page:\n", error.message);
        } else if (error.message.includes('cookies') || error.message.includes('localStorage')) {
            console.log("Error while retrieving cookies or localStorage:\n", error.message);
        } else if (error.message.includes('save_session')) {
            console.log("Error while saving the session data:\n", error.message);
        } else {
            console.log("An unexpected error occurred:\n", error.message);
        }

        // Clean-up if the browser is open, to avoid any hanging processes
        if (browser) {
            try {
                await browser.close();
                console.log("Browser closed.");
            } catch (closeError) {
                console.log("Error closing the browser:\n", closeError.message);
            }
        }
    }
}

login_azon();