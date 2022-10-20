
class VKPost:
    # ссылка на сообщество
    authorHref: str = None
    # название сообщества
    authorName: str = None
    # ссылка на аватар сообщества
    authorImageUrl: str = None
    # текст поста
    text: str = None
    # список ссылок на медиа (изображения)
    media: list = []

    def __str__(self):
        return '\n'.join('{0}:   {1}'.format(field, self.__dict__[field]) for field in self.__dict__.keys())
