import newspaper
import os


url = "https://www.jn.pt/"

path = os.getcwd()

#if not os.path.exists(f"{path}/newspaper_scraper"):
#    os.symlink(f"{path}/newspaper_scraper", "/tmp/.newspaper_scraper")

jn = newspaper.build(url)

print(jn.size())

for article in jn.articles:
    print(article.url, article.title)
    ar = newspaper.Article(article.url)
    ar.download()
    ar.parse()
    print(f"Title: {ar.title}: {ar.text}...{ar.authors}...{ar.publish_date}")