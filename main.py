# encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from bs4 import BeautifulSoup as bs
import urllib.request
import json


from config import CNKI_SEARCH_URL, KEYWORD_LIST


def main():
    """
    Fetch papers from CNKI and filter by keywords
    CNKI provides APIs for search functionality
    """
    keyword_list = KEYWORD_LIST
    keyword_dict = {key: [] for key in keyword_list}
    
    total_paper = 0
    full_report = ''
    
    # For each keyword, search CNKI
    for keyword in keyword_list:
        full_report = full_report + '## Keyword: ' + keyword + '\n'
        papers_found = fetch_cnki_papers(keyword, CNKI_SEARCH_URL)
        
        if len(papers_found) == 0:
            full_report = full_report + 'There is no result \n'
        else:
            keyword_dict[keyword] = papers_found
        
        for paper in papers_found:
            report = '### {}\n - **Authors:** {}\n - **Published:** {}\n - **CNKI link:** {}\n - **Abstract**\n {}' \
                .format(paper['title'], paper['authors'], paper['published'], paper['link'],
                        paper['abstract'])
            full_report = full_report + report + '\n'
        total_paper += len(papers_found)
    
    # Opening the existing HTML file
    Func = open("mail.html", "w", encoding='utf-8')

    # Adding input data to the HTML file
    Func.write(full_report)

    # Saving the data into the HTML file
    Func.close()
    return total_paper


def fetch_cnki_papers(keyword, base_url):
    """
    Fetch papers from CNKI based on keyword
    
    Args:
        keyword: Search keyword
        base_url: CNKI search base URL
    
    Returns:
        List of paper dictionaries
    """
    papers = []
    try:
        # Build search URL for CNKI
        # CNKI search URL format: base_url?keyword=your_keyword&sortfield=pubdate
        search_url = f"{base_url}?keyword={keyword}&sortfield=pubdate"
        
        # Set User-Agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        req = urllib.request.Request(search_url, headers=headers)
        page = urllib.request.urlopen(req, timeout=10)
        soup = bs(page, features="html.parser")
        
        # Parse CNKI search results
        # CNKI results are typically in a table or list structure
        result_items = soup.find_all("tr", {"class": "oddTr"})
        if not result_items:
            result_items = soup.find_all("tr", {"class": "evenTr"})
        
        for item in result_items[:10]:  # Limit to 10 results per keyword
            try:
                paper = parse_cnki_paper(item)
                if paper:
                    papers.append(paper)
            except Exception as e:
                print(f"Error parsing paper: {e}")
                continue
                
    except Exception as e:
        print(f"Error fetching papers for keyword '{keyword}': {e}")
    
    return papers


def parse_cnki_paper(item):
    """
    Parse a single paper entry from CNKI
    
    Args:
        item: BeautifulSoup element containing paper information
    
    Returns:
        Dictionary with paper information or None if parsing fails
    """
    try:
        paper = {}
        
        # Extract title and link
        title_elem = item.find("a", {"target": "_blank"})
        if title_elem:
            paper['title'] = title_elem.text.strip()
            paper['link'] = title_elem.get('href', '')
            if not paper['link'].startswith('http'):
                paper['link'] = 'https://kns.cnki.net' + paper['link']
        else:
            return None
        
        # Extract authors (usually in a specific column)
        tds = item.find_all("td")
        if len(tds) >= 2:
            paper['authors'] = tds[1].text.strip() if len(tds) > 1 else "Unknown"
        else:
            paper['authors'] = "Unknown"
        
        # Extract published date
        if len(tds) >= 3:
            paper['published'] = tds[2].text.strip() if len(tds) > 2 else "Unknown"
        else:
            paper['published'] = "Unknown"
        
        # Extract abstract if available
        # This might require additional requests to get full details
        paper['abstract'] = "Please visit the CNKI link for full abstract"
        
        return paper
        
    except Exception as e:
        print(f"Error in parse_cnki_paper: {e}")
        return None


if __name__ == '__main__':
    main()
