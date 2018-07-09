/**
 * Created by dx on 2018/6/26.
 */

if (process.argv.length < 3 || process.argv.length > 5) {
    console.log("args error")
} else {
    var address = process.argv[2];
    var output = process.argv[3]
    console.log(address, output);
    const puppeteer = require('puppeteer');
    (async() => {
        const browser = await puppeteer.launch({
            // headless:false,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();
        page.setViewport({
            width: 1920,
            height: 1080
        });
        await page.goto(address, {
            timeout: 3000,
            waitUtil: ['networkidle0', 'domcontentloaded ']
        }).then((response)=> {
            console.log("reponse status :", response.status())
        }, () => {
            console.log("load timeout");
        });
        //等待页面加载完毕
        console.log("waiting for page loading..")
        await page.waitFor(8000)
        await page.screenshot({
            path: output,
            fullPage: true
        });
        console.log("screen shot finished")
        page.close();
        await browser.close();
    })();
}
