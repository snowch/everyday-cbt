"""Package a built course. Local links and recorded audio work after extraction."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
output=ROOT/'dist'
assert (output/'index.html').exists(),'Run build.py first'
target=output/'everyday-cbt-offline.zip'
with ZipFile(target,'w',compression=ZIP_DEFLATED,compresslevel=6) as archive:
    archive.writestr('READ-ME-OFFLINE.txt', 'Everyday CBT\n\nExtract this ZIP first, then open index.html in a modern browser. Recorded audio, fonts, and learning interactions are included. Source readings require internet access.\n\nIf your browser restricts local files, run python3 -m http.server 8877 from the extracted folder and open http://localhost:8877. No internet connection is needed to use this local server.\n\nThe course is a draft: practitioner review and a learner pilot have not taken place.\n')
    for path in sorted(output.rglob('*')):
        if path.is_file() and path!=target:archive.write(path,path.relative_to(output))
print(f'Packaged {target.stat().st_size/1024/1024:.1f} MiB: {target}')
