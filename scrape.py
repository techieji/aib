import bs4
import httpx
from collections import deque
import asyncio
from urllib.parse import urljoin
import json
from bloom_filter2 import BloomFilter

def process_text(st):
    s = bs4.BeautifulSoup(st, 'lxml')
    # Metadata
    l = [x.text for x in s.find_all('td')]
    md = dict(zip(l[::2], l[1::2]))
    # Question, Markscheme, and ER
    spec = [x.get_text().strip() for x in s.select('.specification')]
    l = [x.get_text().strip() for x in s.select('.question')]
    n = len(l) // 3
    qu, ms, er = l[:n], l[n:2*n], l[2*n:]
    # Syllabus
    syl = s.select('.syllabus_section div')[0].text.strip().split('\u00bb')
    return {'md': md, 'specs': spec, 'questions': qu, 'markscheme': ms, 'report': er, 'syllabus': syl}

filename = 'visited.bin'
visited = BloomFilter(max_elements=10**8, error_rate=0.01, filename=(filename, -1))
q = deque()
i = 0

async def visit(client, f):
    try:
        url = q.popleft()
        if url in visited: return
        visited.add(url)
        resp = (await client.get(url))
        if 'questions' in url:
            json.dump(process_text(resp.text), f)
            f.write('\n')
            print(f"[DEBUG] question scraped ({url.split('/')[-1].split('.')[0]})")
        else:
            soup = bs4.BeautifulSoup(resp.text, 'lxml')
            for elem in soup.find_all('a'):
                u = urljoin(url, elem.get('href'))
                if u not in visited and 'dp-mathematics-hl' in u:
                    q.append(u)
            # print(f"[DEBUG] found links from {url[74:]}")
            print(f"[DEBUG] found links from {url}")
    except Exception as e:
        print(f"[ERROR] ({e}) {url}")

async def main():
    q.append("https://ibquestionbank.netlify.app/questionbank.ibo.org/en/teachers/00000/questionbanks/7-dp-mathematics-hl/syllabus_sections.html")
    with open('data.jsonl', 'w') as f:
        async with httpx.AsyncClient() as client:
            while q:
                await visit(client, f)
                await asyncio.sleep(0.01)
                i += 1

try:
    asyncio.run(main())
    print('DONE!')
except Exception as e:
    with open('progress.bin', 'wb') as f:
        pickle.dump([q, i])