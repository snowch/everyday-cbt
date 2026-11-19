"""Verify the extracted package using a local server, with internet requests blocked."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.parse import urlsplit
from zipfile import ZipFile
from playwright.sync_api import sync_playwright
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
with TemporaryDirectory(prefix='everyday-cbt-') as directory:
    target=Path(directory)
    with ZipFile(ROOT/'dist/everyday-cbt-offline.zip') as archive:
        assert all((target/name).resolve().is_relative_to(target) for name in archive.namelist())
        archive.extractall(target)
    records=json.loads((target/'audio/manifest.json').read_text())['clips']
    assert len(records)==96
    for record in records:assert hashlib.sha256((target/record['file']).read_bytes()).hexdigest()==record['sha256']
    assert (target/'workbook.pdf').read_bytes().startswith(b'%PDF')
    assert (target/'course.pdf').read_bytes().startswith(b'%PDF')
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=directory))
    Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
        page=browser.new_page();unexpected=[]
        def route(request):
            if urlsplit(request.request.url).hostname=='127.0.0.1':request.continue_()
            else:unexpected.append(request.request.url);request.abort()
        page.route('**/*',route)
        page.goto(base,wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        assert page.evaluate('document.fonts.check(\'400 20px CourseSerif\') && document.fonts.check(\'400 20px CourseSans\')')
        page.get_by_role('link',name='Start the first story').click()
        assert page.locator('.lesson-page:visible').count()==1
        page.locator('#p1 audio').evaluate('(a)=>a.play()')
        page.wait_for_function('document.querySelector("#p1 audio").currentTime > .2')
        page.locator('[data-page-link="1"]').click()
        page.locator('#p2 input[value="0"]').check()
        page.get_by_role('button',name='Check choice').click()
        assert page.locator('.feedback:visible').count()==1
        assert not unexpected,unexpected
        browser.close()
    server.shutdown();server.server_close()
print(json.dumps({'extracted_package':'pass','recordings':96,'pdfs':2,'fonts':'pass','playback':'pass','feedback':'pass','external_requests':0,'method':'Local HTTP server with all non-local requests blocked. Managed Chrome blocks file:// navigation, so direct-file mode was not browser-tested.'},indent=2))
