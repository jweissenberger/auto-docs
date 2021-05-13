import newspaper


def find_max(values):
    return max(values)


def average(values: list) -> int:

    total = 0
    for i in values:
        total += i

    return total/len(values)


def chunks(l, n):
    d, r = divmod(len(l), n)
    for i in range(n):
        si = (d + 1) * (i if i < r else r) + d * (0 if i < r else i - r)
        yield l[si:si + (d + 1 if i < r else d)]


def pull_articles_from_source(url, source, article_data=[]):
    paper = newspaper.build(url)
    i = 0
    failed = 0
    print(len(paper.articles))
    paper.download_articles()
    paper.parse_articles()  # remove articles that are too small (probably not articles)
    print(len(paper.articles))
    for article in paper.articles:
        i += 1
        if i > 10:
            break
        try:
            # fail if the article is empty or less than 40 words
            if article.text.isspace() or article.text == '' or len(article.text.split(' ')) < 40:
                failed += 1
                continue
            article.nlp()

            authors = article.authors
            temp = []
            for i in authors:
                if len(i.split(' ')) > 5:
                    continue
                temp.append(i)
            authors = temp

            data = {'source': source, 'title': article.title, 'authors': authors, 'text': article.text,
                    'keywords': article.keywords, 'summary': article.summary, 'url': article.url,
                    'date': article.publish_date}
            article_data.append(data)
        except:
            failed += 1

    return article_data


def source_from_url(link):

    if 'www' in link:
        source = link.split('.')[1]
    else:
        if '.com' in link:
            source = link.split('.com')[0]
        else:
            source = link.split('.')[0]
    source = source.replace('https://', '')
    source = source.replace('http://', '')
    return source