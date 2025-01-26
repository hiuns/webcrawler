import asyncio
from collections import deque

import aiohttp
from bs4 import BeautifulSoup


async def async_fetch_page(session, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


def extract_links(html_content: str, base_url: str) -> list[str]:
    """Extract all links from HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    links = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        # Optionally normalize or filter URLs here
        # e.g., using urllib.parse.urljoin(base_url, href)
        links.append(href)
    return links


async def crawl(start_url: str, limit: int = 10):
    """Crawl pages synchronously, starting from `start_url`."""
    visited = set()
    queue = deque([start_url])
    pages_crawled = 0

    async with aiohttp.ClientSession() as session:
        while queue and pages_crawled < limit:
            tasks = []
            for _ in range(min(5, len(queue))):
                url = queue.popleft()
                if url not in visited:
                    tasks.append(
                        asyncio.create_task(async_fetch_page(session, url))
                    )
                    visited.add(url)

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for url, html_or_error in zip(tasks, results):
                if isinstance(html_or_error, Exception):
                    print("fail")
                else:
                    pages_crawled += 1
                    new_links = extract_links(
                        html_or_error, url.get_coro().cr_frame.f_locals["url"]
                    )
                    for link in new_links:
                        if link not in visited:
                            queue.append(link)

        return visited


async def main():
    start_url = ""
    visited_urls = await crawl(start_url, limit=10)
    for v in visited_urls:
        print(v)


if __name__ == "__main__":
    asyncio.run(main())
