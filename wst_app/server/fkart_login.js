
const puppeteer = require("puppeteer");
const path = require("path");
const { save_session } = require("./logics");


const FKART_SIGN_IN_URL = "https://www.flipkart.com/account/login"

const login_selectors = {
    emailid: `input[class="r4vIwl BV+Dqf"]`,
    continue: `button[class="QqFHMw twnTnD _7Pd1Fp"]`,
    verify: "button[type=submit]",
    home: `input.Pke_EE`,
};


const dataJson = process.argv[2];
const data = JSON.parse(dataJson);
const { EMAIL_PHONE, SSN_ID } = data;


async function login_fkart() {
    const browser = await puppeteer.launch({
        // Running in non-headless mode to keep the browser visible
        headless: false,
    });

    const page = await browser.newPage();
    // Disable any other timeouts
    page.setDefaultTimeout(0);
    await page.goto(FKART_SIGN_IN_URL);

    await page.waitForSelector(login_selectors.emailid);
    await page.type(login_selectors.emailid, EMAIL_PHONE, { delay: 50 });
    await page.click(login_selectors.continue);

    // Manually Enter the opt
    await page.waitForSelector(login_selectors.verify);
    // then wait for Auto-Redirection
    await page.waitForSelector(login_selectors.home);
    // await page.waitForNavigation({ waitUntil: 'load' });

    // Serialize cookies and localStorage
    const cookies = await page.cookies();
    const localStorageData = await page.evaluate(() => {
        return JSON.stringify(localStorage);
    });
    // Close Broswer
    browser.close();

    // Cache Page-Session
    const cacheDir = path.join(__dirname, "Cache", "Fkart");
    const fname = path.join(cacheDir, `${SSN_ID}.json`);
    const cacheData = JSON.stringify({ cookies, localStorage: localStorageData });
    save_session(cacheDir, fname, cacheData);

    console.log(`Session saved: ${fname}`);
    console.log("Use Session Keys to Scrap Flipkart-Website");

}


login_fkart();
