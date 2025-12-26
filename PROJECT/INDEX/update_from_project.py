#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обновления index.html из PROJECT/*.md
Обновляет:
- Дневник коротышек из PROJECT/log.md
- Статусы из PROJECT/status.md
"""

import re
import sys
from pathlib import Path

SCHEME_START_MARKER = '<!-- PROJECT_SCHEME_START -->'
SCHEME_END_MARKER = '<!-- PROJECT_SCHEME_END -->'


def _extract_title_from_md(md_text: str) -> str | None:
    """Extract the first Markdown H1 title (line starting with '# ')."""
    for line in md_text.splitlines():
        s = line.strip()
        if s.startswith('# '):
            return s[2:].strip()
    return None


def _extract_mermaid_from_md(md_text: str) -> str | None:
    """
    Extract Mermaid code from a markdown file.
    Expected format:
        ```mermaid
        ...code...
        ```
    Returns the code without fences, or None if not found.
    """
    m = re.search(r'```mermaid\s*(.*?)\s*```', md_text, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    code = m.group(1).strip('\n')
    # Remove leading blank lines inside the code block, keep formatting otherwise
    return code.strip()


def update_project_scheme(repo_root):
    """Insert/update Mermaid diagram from PROJECT/scheme.md into PROJECT/INDEX/index.html under hero block (no heading)."""
    scheme_file = Path(repo_root) / 'PROJECT' / 'scheme.md'
    index_file = Path(repo_root) / 'PROJECT' / 'INDEX' / 'index.html'

    if not index_file.exists():
        print(f"[!] Index file not found: {index_file}")
        return False

    if not scheme_file.exists():
        print(f"[!] Scheme file not found: {scheme_file}")
        return False

    with open(scheme_file, 'r', encoding='utf-8') as f:
        scheme_md = f.read()

    scheme_title = _extract_title_from_md(scheme_md)
    mermaid_code = _extract_mermaid_from_md(scheme_md)
    if not mermaid_code:
        print("[!] No Mermaid code block found in PROJECT/scheme.md")
        return False

    with open(index_file, 'r', encoding='utf-8') as f:
        index_content = f.read()

    # Replace content between markers (there should be exactly one block; if multiple exist, replace the LAST one)
    marker_pattern = re.compile(
        re.escape(SCHEME_START_MARKER) + r'[\s\S]*?' + re.escape(SCHEME_END_MARKER),
        flags=re.DOTALL
    )

    replacement_block = (
        f"{SCHEME_START_MARKER}\n"
        f"        <div class=\"section project-scheme\">\n"
        f"{'            <h2>' + scheme_title + '</h2>\\n' if scheme_title else ''}"
        f"            <div class=\"mermaid\">\n{mermaid_code}\n            </div>\n"
        f"        </div>\n"
        f"        {SCHEME_END_MARKER}"
    )

    if SCHEME_START_MARKER in index_content and SCHEME_END_MARKER in index_content:
        matches = list(marker_pattern.finditer(index_content))
        if len(matches) > 1:
            print(f"[!] Warning: found {len(matches)} PROJECT_SCHEME blocks in index.html; replacing the last one")
        if not matches:
            print("[!] Could not locate PROJECT_SCHEME block in index.html")
            return False
        last = matches[-1]
        new_content = index_content[: last.start()] + replacement_block + index_content[last.end() :]
    else:
        # Fallback: insert after hero-grid block (before the progress script)
        insert_point = index_content.find('</div>\n\n    <script>')
        if insert_point == -1:
            print("[!] Could not find insertion point for project scheme in index.html")
            return False
        new_content = index_content[:insert_point] + '\n\n' + replacement_block + '\n' + index_content[insert_point:]

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("[OK] Updated project Mermaid scheme in index.html")
    return True


def update_log(repo_root):
    """Обновить дневник коротышек из PROJECT/log.md"""
    log_file = Path(repo_root) / 'PROJECT' / 'log.md'
    index_file = Path(repo_root) / 'PROJECT' / 'INDEX' / 'index.html'
    
    if not log_file.exists():
        print(f"[!] Log file not found: {log_file}")
        return False
    
    if not index_file.exists():
        print(f"[!] Index file not found: {index_file}")
        return False
    
    # Read log.md
    with open(log_file, 'r', encoding='utf-8') as f:
        log_content = f.read()
    
    # Parse log entries (format: YYYY-MM-DD HH:MM — text)
    entries = []
    for line in log_content.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        match = re.match(r'^(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2})\s*[—–-]\s*(.+)$', line)
        if match:
            date_time = match.group(1)
            text = match.group(2)
            entries.append((date_time, text))
    
    if not entries:
        print("[!] No log entries found in log.md")
        return False
    
    # Generate HTML
    log_html_parts = []
    for date_time, text in entries:
        # Convert URLs to links with "Жмякай сюды" text
        # Remove trailing punctuation from URLs
        def replace_url(match):
            url = match.group(0)
            # Strip trailing punctuation
            trailing = ''
            while url and url[-1] in '.,;!?':
                trailing = url[-1] + trailing
                url = url[:-1]
            return f'<a href="{url}" target="_blank">Жмякай сюды</a>{trailing}'
        
        text_html = re.sub(r'https?://[^\s<>]+', replace_url, text)
        
        log_html_parts.append(f'''            <div class="log-entry">
                <span class="log-date">{date_time}</span>
                <p class="log-text">{text_html}</p>
            </div>''')
    
    log_html = '\n'.join(log_html_parts)
    
    # Read index.html
    with open(index_file, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Replace log entries
    pattern = r'(<div class="hero-log">\s*<h3>Дневник коротышек</h3>\s*)((?:<div class="log-entry">.*?</div>\s*)+)(\s*</div>)'
    
    def replace_log_fn(match):
        before = match.group(1)
        after = match.group(3)
        return before + '\n' + log_html + '\n        ' + after
    
    new_content, count = re.subn(pattern, replace_log_fn, index_content, flags=re.DOTALL)
    
    if count == 0:
        print("[!] Could not find log section in index.html")
        return False
    
    # Write updated index.html
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[OK] Updated log with {len(entries)} entries")
    return True


def update_status(repo_root):
    """Обновить статусы из PROJECT/status.md"""
    status_file = Path(repo_root) / 'PROJECT' / 'status.md'
    index_file = Path(repo_root) / 'PROJECT' / 'INDEX' / 'index.html'
    
    if not status_file.exists():
        print(f"[!] Status file not found: {status_file}")
        return False
    
    if not index_file.exists():
        print(f"[!] Index file not found: {index_file}")
        return False
    
    # Read status.md
    with open(status_file, 'r', encoding='utf-8') as f:
        status_content = f.read()
    
    # Parse sections
    sections = {
        'postponed': [],
        'doing': [],
        'done': []
    }
    
    current_section = None
    for line in status_content.split('\n'):
        line_stripped = line.strip()
        
        if 'послезавтра' in line_stripped or 'Отложено' in line_stripped:
            current_section = 'postponed'
        elif 'сейчас делаем' in line_stripped or 'Прям сейчас' in line_stripped:
            current_section = 'doing'
        elif 'Готовченко' in line_stripped:
            current_section = 'done'
        elif line_stripped.startswith('- ') and current_section:
            item = line_stripped[2:].strip()
            sections[current_section].append(item)
    
    # Generate HTML for each section
    def generate_section_html(items):
        if not items:
            return '                    <li>—</li>'
        # Convert URLs to links in status items
        html_items = []
        for item in items:
            # Convert URLs to links
            def replace_url(match):
                url = match.group(0)
                # Strip trailing punctuation
                trailing = ''
                while url and url[-1] in '.,;!?':
                    trailing = url[-1] + trailing
                    url = url[:-1]
                return f'<a href="{url}" target="_blank">Жмякай сюды</a>{trailing}'
            
            item_html = re.sub(r'https?://[^\s<>]+', replace_url, item)
            html_items.append(f'                    <li>{item_html}</li>')
        return '\n'.join(html_items)
    
    # Read index.html
    with open(index_file, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Replace postponed section
    pattern_postponed = r'(<div class="status-block">\s*<h3>Отложено на <s>завтра</s> послезавтра</h3>\s*<ul>\s*)((?:<li>.*?</li>\s*)+)(\s*</ul>\s*</div>)'
    new_content = re.sub(
        pattern_postponed,
        lambda m: m.group(1) + '\n' + generate_section_html(sections['postponed']) + '\n' + m.group(3),
        index_content,
        flags=re.DOTALL
    )
    
    # Replace doing section
    pattern_doing = r'(<div class="status-block">\s*<h3>Прям сейчас делаем</h3>\s*<ul>\s*)((?:<li>.*?</li>\s*)+)(\s*</ul>\s*</div>)'
    new_content = re.sub(
        pattern_doing,
        lambda m: m.group(1) + '\n' + generate_section_html(sections['doing']) + '\n' + m.group(3),
        new_content,
        flags=re.DOTALL
    )
    
    # Replace done section
    pattern_done = r'(<div class="status-block">\s*<h3>Готовченко</h3>\s*<ul>\s*)((?:<li>.*?</li>\s*)+)(\s*</ul>\s*</div>)'
    new_content = re.sub(
        pattern_done,
        lambda m: m.group(1) + '\n' + generate_section_html(sections['done']) + '\n' + m.group(3),
        new_content,
        flags=re.DOTALL
    )
    
    # Write updated index.html
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[OK] Updated status sections")
    return True


def main():
    """Main function"""
    print('=' * 60)
    print('Обновление index.html из PROJECT/*.md')
    print('=' * 60)
    
    # Get repo root (parent of PROJECT/INDEX)
    repo_root = Path(__file__).parent.parent.parent
    
    print(f'Repo root: {repo_root}')
    
    success = True
    
    # Update log
    if not update_log(repo_root):
        success = False
    
    # Update status
    if not update_status(repo_root):
        success = False

    # Update project scheme
    if not update_project_scheme(repo_root):
        # Non-fatal: keep pipeline going, but mark overall as failed
        success = False
    
    print('=' * 60)
    if success:
        print('Обновление завершено успешно')
    else:
        print('Обновление завершено с ошибками')
    print('=' * 60)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())

