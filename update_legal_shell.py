"""Apply the shared visual shell to the existing legal copy without editing its terms."""
from pathlib import Path
import re

ROOT = Path(__file__).parent
HEADER = '''<header class="site-header"><a class="brand" href="../" aria-label="LaughMyWay home"><span class="brand__burst" aria-hidden="true">✳</span><span>LAUGH<span>MY</span>WAY</span><b aria-hidden="true">®</b></a><nav class="main-nav" aria-label="Main navigation"><a href="../#films">The films</a><a href="../#shorts">Shorts</a><a href="../#about">Our world</a></nav><a class="header-cta" href="https://www.youtube.com/channel/UCHXKAN03_utA3CvBsZUZpcg?sub_confirmation=1" target="_blank" rel="noopener noreferrer">Subscribe <span aria-hidden="true">↗</span></a></header>'''
FOOTER = '''<footer class="footer"><div class="footer__main"><a class="footer__brand" href="../">LAUGH<span>MY</span>WAY<span class="footer__red">.</span></a><div><p>Original illustrated comedy for the wonderfully ridiculous world we live in.</p><a href="https://www.youtube.com/channel/UCHXKAN03_utA3CvBsZUZpcg" target="_blank" rel="noopener noreferrer">YouTube ↗</a></div></div><div class="footer__bottom"><span>© 2026 LAUGHMYWAY</span><nav aria-label="Legal and contact"><a href="../privacy/">Privacy</a><a href="../terms/">Terms</a><a href="../publisher/">Publisher</a><a href="mailto:laughmyway.com@gmail.com">Contact</a></nav><span>MADE FOR THE LAUGH</span></div></footer>'''
for name in ("privacy", "terms"):
    path = ROOT / name / "index.html"
    content = path.read_text(encoding="utf-8")
    content = re.sub(r'<link rel="stylesheet" href="\.\./assets/style\.css">', '<link rel="stylesheet" href="../assets/site.css">\n  <link rel="stylesheet" href="../assets/legal.css">', content)
    content = re.sub(r'  <header class="site-header">.*?</header>', '  ' + HEADER, content, count=1, flags=re.S)
    content = re.sub(r'  <footer class="site-footer">.*?</footer>', '  ' + FOOTER, content, count=1, flags=re.S)
    content = content.replace('<meta name="theme-color" content="#092e32">', '<meta name="theme-color" content="#080808">')
    path.write_text(content, encoding="utf-8")
    print(f"Updated visual shell: {path}")
