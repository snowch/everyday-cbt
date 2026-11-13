"""Export printable companions from a running local build (requires Playwright)."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://127.0.0.1:8877');args=parser.parse_args()
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        for source,target in [('workbook.html','workbook.pdf'),('reading.html','course.pdf')]:
            page=browser.new_page()
            page.goto(args.base_url+'/'+source,wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            page.evaluate('document.querySelectorAll("details").forEach(el=>el.open=true)')
            page.emulate_media(media='print')
            page.pdf(path=str(ROOT/target),format='A4',margin={'top':'16mm','bottom':'18mm','left':'15mm','right':'15mm'},print_background=True,tagged=True,outline=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="font:9px Arial;color:#4B6172;width:100%;text-align:center">Everyday CBT · draft course · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
            page.close();print('Exported',target)
        browser.close()
