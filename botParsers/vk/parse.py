import requests
from bs4 import BeautifulSoup as bs
from botParsers.vk.data.VKPost import VKPost

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}


def parse_vk_post(url: str) -> VKPost:
    vkPost = VKPost()
    content = requests.get(url=url, headers=headers, timeout=30)
    soup = bs(content.text, "html.parser")

    with open(f'{url.split("/")[-1]}.html', 'w', encoding='windows-1251') as file:
        file.write(content.text)

    post = soup.find('div', {'class': 'mark_top_verified', 'id': 'page_wall_posts'}).find('div', class_='_post_content')

    # _post_content
    header_author_data = post.find('div', class_='post_image_stories')

    vkPost.authorHref = 'https://vk.com' + post.find('a', class_='author').get('href')
    vkPost.authorName = header_author_data.find('img').get('alt')
    vkPost.authorImageUrl = header_author_data.find('img').get('src')

    # поиск текста поста (текст может отсутствовать
    wallPostText = post.find('div', class_='wall_post_text')
    if wallPostText is not None:
        vkPost.text = wallPostText.getText(separator='\n')

    # поиск прикреплённых медиа к посту (фото, гиф, видео)
    vkPost.media = []
    mediaThumbs = post.find('div', class_='page_post_sized_thumbs clear_fix')
    if mediaThumbs is not None:
        content = mediaThumbs.find_all('a')
        for page in content:
            # получение ссылки на изображение (если в посте не изображение
            # - будет получена ссылка на превью)
            url = page.get('style').split()[4]
            url = url[4:-2]
            vkPost.media.append(url)
    return vkPost