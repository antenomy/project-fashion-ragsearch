import asyncio
import re
from crawl4ai import *

def link_creator(base_link: str, count : int):
    return_list = [base_link]

    return_list.extend(f"{base_link}?page={iter+2}" for iter in range(count-1))

    return return_list

async def crawl_category_page(base_category_url: str) -> list:
    
    # print(f"Discovering products from category: {base_category_url}")
    
    async with AsyncWebCrawler() as crawler:
        category_result = await crawler.arun(url=base_category_url)

        if category_result.markdown:
            product_urls = re.findall(r'productpage\.\d+\.html', category_result.markdown)
            #product_urls = re.findall(r'https://www2\.hm\.com/[^/]+/productpage\.\d+\.html', category_result.markdown)
        else:
            print("No HTML found.")

        if product_urls:
            # print(base_category_url, "\n")
            # print(product_urls, "\n")

            if len(product_urls) > 0:
                return list(map(lambda url: url.removeprefix("productpage.").removesuffix(".html"), product_urls))
            else:
                print("No product URLs found.")
        else:
            print("No product URLs found.")


async def main():
    link_dict = {
        "https://www2.hm.com/sv_se/herr/sport/visa-alla.html" : 6,
        "https://www2.hm.com/sv_se/herr/produkter/merch-graphics.html" : 3,
        "https://www2.hm.com/sv_se/herr/produkter/strumpor.html" : 5,
        "https://www2.hm.com/sv_se/herr/produkter/underklader.html" : 5,
        "https://www2.hm.com/sv_se/herr/produkter/sovplagg-loungewear.html" : 3,
        "https://www2.hm.com/sv_se/herr/produkter/badklader.html" : 2,
        "https://www2.hm.com/sv_se/herr/accessoarer/visa-alla.html" : 11,
        "https://www2.hm.com/sv_se/herr/last-chance/visa-alla.html" : 10,
        "https://www2.hm.com/sv_se/herr/skor/visa-alla.html" : 4
    }

    scrape_list = [link_creator(key, link_dict[key]) for key in link_dict]

    # print(scrape_list)
    for sublist in scrape_list:
        file_name = sublist[0].removeprefix("https://www2.hm.com/sv_se/herr/").replace('.', '').replace('/', '')

        write_string = ""

        result_lists = [await crawl_category_page(url) for url in sublist]

        distilled_set = set()
        page_number = 1

        for result_sublist in result_lists:
            

            if result_sublist:
                distilled_set.update(set(result_sublist))
            else:
                print(f"Not writing to {file_name}\nPage number:{page_number}")
                continue

            page_number += 1

        flat_unique_list = list(distilled_set)

        for element in flat_unique_list: 
            write_string += f"{element},\n"

        write_string = write_string.removesuffix(",\n")

        # print(f"Writing to {file_name}\n")
        # print(write_string)

        with open(file_name, mode='w') as file:
            file.write(write_string)

if __name__ == "__main__":
    asyncio.run(main())