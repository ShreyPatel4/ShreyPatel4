#!/usr/bin/env python3
import os
import re
import json
import requests
from datetime import datetime
import calendar

# Config
CONFIG_PATH = '.github/readme-config.json'
README_PATH = 'README.md'
JOURNAL_PATH = None


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def select_repo_of_week(repos):
    # deterministic by ISO week number
    week = datetime.utcnow().isocalendar()[1]
    idx = week % len(repos)
    return repos[idx]


def parse_journal(path):
    if not os.path.exists(path):
        return ''
    text = open(path,'r',encoding='utf-8').read()
    # Find sections starting with '## '
    parts = re.split(r'(^##\s+)', text, flags=re.MULTILINE)
    # parts may interleave headings and content; fallback to whole file
    headers = re.findall(r'^##\s+(.+)$', text, flags=re.MULTILINE)
    if not headers:
        return text.strip()
    # find last header position
    last_header = headers[-1]
    pattern = r'##\s+' + re.escape(last_header) + r"(.*?)(?=\n##\s+|\Z)"
    m = re.search(pattern, text, flags=re.S|re.M)
    if m:
        content = m.group(1).strip()
        return f"### {last_header}\n\n{content}"
    return ''


def get_latest_commit(owner, repo):
    token = os.environ.get('GITHUB_TOKEN')
    headers = {'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    r = requests.get(url, headers=headers, params={'per_page': 1})
    if r.status_code == 200 and r.json():
        c = r.json()[0]
        sha = c.get('sha')
        msg = c.get('commit',{}).get('message','')
        author = c.get('commit',{}).get('author',{}).get('name','')
        html_url = c.get('html_url')
        short = sha[:7]
        return f"[{short}]({html_url}) - {msg.splitlines()[0]} (by {author})"
    return ''


def replace_block(text, start_marker, end_marker, new_content):
    pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), flags=re.S)
    replacement = start_marker + '\n' + new_content.strip() + '\n' + end_marker
    if pattern.search(text):
        return pattern.sub(replacement, text)
    else:
        # append at end
        return text + '\n' + replacement


def main():
    cfg = load_config()
    global JOURNAL_PATH
    JOURNAL_PATH = cfg.get('journal', 'JOURNAL.md')
    repos = cfg.get('repos', [])
    rss = cfg.get('rss', [])
    owner = os.environ.get('REPO_OWNER', cfg.get('owner','ShreyPatel4'))
    repo = os.environ.get('REPO_NAME', cfg.get('repo','ShreyPatel4'))

    repo_of_week = select_repo_of_week(repos) if repos else None
    journal_section = parse_journal(JOURNAL_PATH)
    latest_commit = get_latest_commit(owner, repo)

    readme = open(README_PATH,'r',encoding='utf-8').read()

    # Build repo of week markdown
    if repo_of_week:
        name = repo_of_week
        repo_url = f'https://github.com/{name}' if '/' in name else f'https://github.com/{owner}/{name}'
        repo_md = f"### Repo of the week\n\n- **[{name}]({repo_url})**\n\n"
    else:
        repo_md = '### Repo of the week\n\n_No repo configured._\n\n'

    readme = replace_block(readme, '<!-- REPO_OF_WEEK_START -->', '<!-- REPO_OF_WEEK_END -->', repo_md)
    built_md = journal_section or '_Nothing added to the journal yet._'
    readme = replace_block(readme, '<!-- BUILT_THIS_WEEK_START -->', '<!-- BUILT_THIS_WEEK_END -->', built_md)

    # RSS - skip if none
    if rss:
        # Basic fetch of first items
        items_md = ''
        for feed_url in rss[:3]:
            try:
                import feedparser
                d = feedparser.parse(feed_url)
                for e in d.entries[:2]:
                    items_md += f"- [{e.title}]({e.link})\n"
            except Exception:
                pass
        if not items_md:
            items_md = '_No items fetched from RSS._'
    else:
        items_md = '_RSS not configured._'
    readme = replace_block(readme, '<!-- RSS_START -->', '<!-- RSS_END -->', items_md)

    now_md = latest_commit or '_No recent commits found._'
    readme = replace_block(readme, '<!-- NOW_CODING_START -->', '<!-- NOW_CODING_END -->', now_md)

    open(README_PATH,'w',encoding='utf-8').write(readme)

if __name__ == '__main__':
    main()
