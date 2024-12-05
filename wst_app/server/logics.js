const fs = require("fs");



function formatTime(milliseconds) {
    // Convert milliseconds to total seconds
    let totalSeconds = Math.floor(milliseconds / 1000);
    // Calculate hours, minutes, and seconds
    let hours = Math.floor(totalSeconds / 3600);
    let minutes = Math.floor((totalSeconds % 3600) / 60);
    let seconds = totalSeconds % 60;
    // Build the formatted string, skipping zero values
    let timeParts = [];
    if (hours > 0)      timeParts.push(`${hours}h`);
    if (minutes > 0)    timeParts.push(`${minutes}m`);
    if (seconds > 0)    timeParts.push(`${seconds}s`);
    // Join the parts with a hyphen and return the result
    return timeParts.join(' ');
}


function calPercent(a, b) {
    try {
        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error(`Both ${a} and ${b} must be numbers for %Calci.`);

        } if (b === 0) {
            throw new Error('Division by zero is not allowed.');
        }

        let percentage = (a / b) * 100;
        return percentage.toFixed(2); // Round to 2 decimals

    } catch (error) {
        return error.message;
    }
}


function removeQueryParam(url, paramName) {
    // Check if the url and paramName are valid strings
    if (typeof url !== 'string' || typeof paramName !== 'string') {
        throw new Error('Both url and paramName must be strings');
    }

    // Ensure the url contains at least one "?" or "&" (to indicate it's a query string)
    if (!url.includes('?') && !url.includes('&')) {
        return url; // No query string present, so return the URL as-is
    }

    // Create a regex pattern to match the parameter in the form of "&paramName=value"
    const regex = new RegExp(`([&?])${paramName}=[^&]*`);

    // Replace the matched parameter with an empty string
    const updatedUrl = url.replace(regex, (match, p1) => {
        // If it's the only parameter or comes after a ?, preserve the "?" without the parameter
        return p1 === '?' ? '?' : '';
    });

    return updatedUrl;
}


function text_cleaner(rawText) {
    let cleanedText = rawText.trim();

    // Step 1: Replace <br> tags with spaces to preserve line breaks
    cleanedText = cleanedText.replace(/<br\s*\/?>/gi, " ");
    // Step 2: Remove all HTML tags (keep only the raw text)
    cleanedText = cleanedText.replace(/<\/?[^>]+(>|$)/g, "");
    // Step 3: Remove non-printable ASCII characters
    cleanedText = cleanedText.replace(/[^\x20-\x7E]/g, "");
    // Step 4: Remove any character that is not a letter, digit, punctuation, or space
    cleanedText = cleanedText.replace(/[^a-zA-Z0-9\s\.,;:!?()'"-_\[\]{}@#&*%$^+=<>|\\/~`_]/g, "");
    // Step 5: Collapse consecutive spaces into a single space
    cleanedText = cleanedText.replace(/\s+/g, " ");

    cleanedText = cleanedText.replace(/\n/g, " ").replace(/"/g, "'")
    // .replace(/"/g, '""')

    return cleanedText;
}


function save_metadata(dir, fname, data) {
    // Check if the "Database" directory exists, if not, create it
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    
    // Create the CSV content.
    let csvHeader = "Product_Name,Category\n";
    const {Product_Name, Category } = data;
    let csvContent = `"${Product_Name}","${Category}"\n`;

    // Check if the file exists // Add Header if for 1st Time
    if (!fs.existsSync(fname)) {
        fs.writeFileSync(fname, csvHeader, "utf8");

    } fs.appendFileSync(fname, csvContent, "utf8");
}


function save_as_csv(dir, fname, data) {
    // Check if the "Database" directory exists, if not, create it
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }

    // Create the CSV content.
    let csvHeader = "Product_Name,Customer_Name,Review_Title,Rating,Review_Text\n";
    let csvContent = "";
    let records_cnt = 0;
    // Iterate over the reviews data and add it to the CSV content.
    for (const row of data) {
        records_cnt++;
        const {PRODUCT_NAME, author, title, rating, content } = row;
        // Escape quotes
        csvContent += `"${PRODUCT_NAME}","${author}","${title}",${rating},"${content}"\n`;
        // csvContent += `"${PRODUCT_NAME}","${author}","${title}",${rating},"${content.replace(/\n/g, " ").replace(/"/g, "'").replace(/"/g, '""')}"\n`;
    }

    // Check if the file exists // Add Header if for 1st Time
    if (!fs.existsSync(fname)) {
        fs.writeFileSync(fname, csvHeader, "utf8");

    } fs.appendFileSync(fname, csvContent, "utf8");

    return records_cnt;
}


function save_session(dir, fname, data) {
    // Check if the directory exists, if not, create it
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    // Save data to a file
    fs.writeFileSync(fname, data);
}



module.exports = {
    formatTime, calPercent,
    removeQueryParam, text_cleaner,
    save_metadata, save_as_csv, save_session
}