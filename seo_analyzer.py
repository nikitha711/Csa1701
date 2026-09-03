import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def analyze_website(url):

    result = {
        "url": url,
        "title": "",
        "meta_description": "",
        "h1_count": 0,
        "h2_count": 0,
        "word_count": 0,
        "link_count": 0,
        "image_count": 0,
        "images_without_alt": 0,
        "keywords": [],
        "keyword_relevance": 0,
        "seo_score": 0,
        "recommendations": [],
        "error": None
    }

    try:

        # --------------------------------
        # URL
        # --------------------------------

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        result["url"] = url

        # --------------------------------
        # FETCH WEBSITE
        # --------------------------------

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        # --------------------------------
        # PARSE HTML
        # --------------------------------

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary elements

        for element in soup(
            ["script", "style", "noscript"]
        ):
            element.decompose()

        # --------------------------------
        # TITLE
        # --------------------------------

        title = soup.title

        if title:
            result["title"] = title.get_text(
                strip=True
            )

        # --------------------------------
        # META DESCRIPTION
        # --------------------------------

        meta = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta:
            result["meta_description"] = meta.get(
                "content",
                ""
            ).strip()

        # --------------------------------
        # HEADINGS
        # --------------------------------

        result["h1_count"] = len(
            soup.find_all("h1")
        )

        result["h2_count"] = len(
            soup.find_all("h2")
        )

        # --------------------------------
        # CONTENT
        # --------------------------------

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        words = text.split()

        result["word_count"] = len(words)

        # --------------------------------
        # LINKS
        # --------------------------------

        result["link_count"] = len(
            soup.find_all("a")
        )

        # --------------------------------
        # IMAGES
        # --------------------------------

        images = soup.find_all("img")

        result["image_count"] = len(images)

        result["images_without_alt"] = sum(
            1
            for image in images
            if not image.get("alt")
        )

        # --------------------------------
        # AI / NLP KEYWORD ANALYSIS
        # --------------------------------

        if len(words) >= 5:

            try:

                vectorizer = TfidfVectorizer(
                    stop_words="english",
                    max_features=15
                )

                content_matrix = vectorizer.fit_transform(
                    [text]
                )

                scores = content_matrix.toarray()[0]

                terms = vectorizer.get_feature_names_out()

                keyword_scores = list(
                    zip(terms, scores)
                )

                keyword_scores.sort(
                    key=lambda item: item[1],
                    reverse=True
                )

                result["keywords"] = [
                    keyword
                    for keyword, score
                    in keyword_scores[:10]
                ]

                # --------------------------------
                # COSINE SIMILARITY
                # --------------------------------

                if result["title"]:

                    title_matrix = vectorizer.transform(
                        [result["title"]]
                    )

                    similarity = cosine_similarity(
                        content_matrix,
                        title_matrix
                    )[0][0]

                    result["keyword_relevance"] = round(
                        similarity * 100,
                        2
                    )

            except Exception:

                result["keywords"] = []

        # --------------------------------
        # SEO SCORE
        # --------------------------------

        score = 0

        # Title

        if result["title"]:
            score += 20

        # Meta description

        if result["meta_description"]:
            score += 20

        # H1

        if result["h1_count"] == 1:
            score += 20

        elif result["h1_count"] > 1:
            score += 10

        # Content

        if result["word_count"] >= 300:
            score += 20

        elif result["word_count"] >= 150:
            score += 10

        # Images

        if result["image_count"] == 0:
            score += 10

        elif result["images_without_alt"] == 0:
            score += 10

        # Links

        if result["link_count"] > 0:
            score += 10

        result["seo_score"] = min(
            score,
            100
        )

        # --------------------------------
        # RECOMMENDATIONS
        # --------------------------------

        recommendations = []

        if not result["title"]:

            recommendations.append(
                "Add a descriptive title tag."
            )

        elif len(result["title"]) < 30:

            recommendations.append(
                "Improve the title by making it more descriptive."
            )

        elif len(result["title"]) > 60:

            recommendations.append(
                "Consider shortening the title tag."
            )

        if not result["meta_description"]:

            recommendations.append(
                "Add a meta description."
            )

        elif len(result["meta_description"]) < 120:

            recommendations.append(
                "Improve the meta description."
            )

        elif len(result["meta_description"]) > 160:

            recommendations.append(
                "Consider shortening the meta description."
            )

        if result["h1_count"] == 0:

            recommendations.append(
                "Add an H1 heading."
            )

        elif result["h1_count"] > 1:

            recommendations.append(
                "Use a single primary H1 heading."
            )

        if result["word_count"] < 300:

            recommendations.append(
                "Increase useful and relevant website content."
            )

        if result["images_without_alt"] > 0:

            recommendations.append(
                "Add ALT text to images."
            )

        if result["link_count"] == 0:

            recommendations.append(
                "Add relevant internal links."
            )

        if result["keyword_relevance"] < 20:

            recommendations.append(
                "Improve keyword relevance between the page title and content."
            )

        if not recommendations:

            recommendations.append(
                "The website has a good basic SEO structure."
            )

        result["recommendations"] = recommendations

    except requests.exceptions.RequestException:

        result["error"] = (
            "Unable to access the website. "
            "Please check the URL and try again."
        )

    except Exception as error:

        result["error"] = str(error)

    return result