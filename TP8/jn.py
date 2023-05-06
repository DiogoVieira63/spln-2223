import newspaper
import os


url = "https://www.jn.pt/"

path = os.getcwd()

#if not os.path.exists(f"{path}/newspaper_scraper"):
#    os.symlink(f"{path}/newspaper_scraper", "/tmp/.newspaper_scraper")

jn = newspaper.build(url)

print(jn.size())


text = ""
i = 0
for article in jn.articles:
    print(i, article.url, article.title)
    ar = newspaper.Article(article.url)
    ar.download()
    ar.parse()
    text += f"{ar.title}\n{ar.text}"
    i += 1

with open("text/jn.txt", "w") as f:
    f.write(text)