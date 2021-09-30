from .Posts import Post, PostType
from .Taxonomies import Category,Tag
class PostInterface(object):

    @staticmethod
    def __get_full_version(model):
        post = Post.convert(model)
        post.set_taxonomies()
        return post

    @staticmethod
    def __get_short_version(model):

        post = Post.convert(model)

        return post

    @staticmethod
    def __get_term_version(model):
        post = Post.convert(model)
        post.set_taxonomies()
        return post


    """
       Methods get by ID
    """
    @staticmethod
    def get_by_id(id: int):
        return PostInterface.__get_full_version(Post.query().by_id(id))

    # @staticmethod
    # def get_by_id_short(id: int, values = ['id','title','slug','type']):
    #     return PostInterface.__get_short_version(Post.query().by_id(id, values))
    #
    # @staticmethod
    # def get_by_id_terms(id: int, values=['id', 'title', 'slug', 'type','terms']):
    #     return PostInterface.__get_term_version(Post.convert(Post.query().by_id(id, values)))

    """
        Methods get by slug
    """

    @staticmethod
    def get_by_slug(slug: str):
        return PostInterface.__get_full_version(Post.query().by_slug(slug))
    #
    # @staticmethod
    # def get_by_slug_short(slug: str, values=['id', 'title', 'slug', 'type']):
    #     return PostInterface.__get_short_version(Post.convert(Post.query().by_slug(slug, values)))
    #
    # @staticmethod
    # def get_by_slug_terms(slug: str, values=['id', 'title', 'slug', 'type', 'terms']):
    #     return PostInterface.__get_term_version(Post.convert(Post.query().by_slug(slug, values)))

    """
        Methods get all posts
    """

    @staticmethod
    def get_all():
        return [PostInterface.__get_full_version(model) for model in Post.query().all()]

    # @staticmethod
    # def get_all_short(values=['id', 'title', 'slug', 'type']):
    #     return [PostInterface.__get_short_version(model) for model in Post.query().all(values)]
    #
    # @staticmethod
    # def get_all_terms(values=['id', 'title', 'slug', 'type', 'terms']):
    #     return [PostInterface.__get_term_version(model) for model in Post.query().all(values)]

    """
        Methods get all posts by post type
    """

    @staticmethod
    def get_all_by_type(postType: str):
        return [PostInterface.__get_full_version(model) for model in Post.query().filter({'type':postType})]
    #
    # @staticmethod
    # def get_all_short_by_type(postType: str, values=['id', 'title', 'slug', 'type']):
    #     return [PostInterface.__get_short_version(model) for model in Post.query().filter({'type':postType},values)]
    #
    # @staticmethod
    # def get_all_terms_by_type(postType: str, values=['id', 'title', 'slug', 'type', 'terms']):
    #     return [PostInterface.__get_term_version(model) for model in Post.query().filter({'type':postType},values)]

class PostTypeInterface(object):

    @staticmethod
    def __get_full_version(model):
        post = PostType.convert(model)
        post.set_posts()
        return post

    @staticmethod
    def __get_short_version(model):
        return PostType.convert(model)


    """
        Methods get by ID
    """

    @staticmethod
    def get_by_id(id):
        return PostTypeInterface.__get_full_version(PostType.query().by_id(id))

    @staticmethod
    def get_by_id_short(id):
        return PostTypeInterface.__get_short_version(PostType.query().by_id(id))

    """
           Methods get by slug
       """

    @staticmethod
    def get_by_slug(slug: str):
        return PostTypeInterface.__get_full_version(PostType.query().by_slug(slug))

    @staticmethod
    def get_by_slug_short(slug: str):
        return PostTypeInterface.__get_short_version(PostType.query().by_slug(slug))

    """
            Methods get all posts
        """
    @staticmethod
    def get_all():
        return [PostTypeInterface.__get_full_version(model) for model in PostType.query().all()]

    @staticmethod
    def get_all_short():
        return [PostTypeInterface.__get_short_version(model) for model in PostType.query().all()]

class CategoryInterface(object):

    @staticmethod
    def __get_full_version(model):
        cat = Category.convert(model)
        if cat is None:
            return None
        cat.set_posts()
        cat.set_parent()
        cat.set_childrens()
        return cat

    @staticmethod
    def __get_short_version(model):
        cat = Category.convert(model)
        if cat is None:
            return None
        cat.set_parent()
        cat.set_childrens()
        return cat


    """
        Methods get by ID
    """

    @staticmethod
    def get_by_id(id):
        return CategoryInterface.__get_full_version(Category.query().filter_first({'id':id,'type':'category'}))

    @staticmethod
    def get_by_id_short(id):
        return CategoryInterface.__get_short_version(Category.query().filter_first({'id':id,'type':'category'}))

    """
           Methods get by slug
       """

    @staticmethod
    def get_by_slug(slug: str):
        return CategoryInterface.__get_full_version(Category.query().filter_first({'slug':slug,'type':'category'}))

    @staticmethod
    def get_by_slug_short(slug: str):
        return CategoryInterface.__get_short_version(Category.query().filter_first({'slug':slug,'type':'category'}))

    """
            Methods get all posts
        """
    @staticmethod
    def get_all():
        return [CategoryInterface.__get_full_version(model) for model in Category.query().filter({'type':'category'})]

    @staticmethod
    def get_all_short():
        return [CategoryInterface.__get_short_version(model) for model in Category.query().filter({'type':'category'})]

    @staticmethod
    def get_tree():
        result = []
        cats = CategoryInterface.get_all()
        for i in range(len(CategoryInterface.get_all())):
           cat = cats[i]
           if cat.parent is None:
               result.append([cat , *[CategoryInterface.__get_short_version(m) for m in cat.get_family()]])

        return result


class TagInterface(object):

    @staticmethod
    def __get_full_version(model):
        cat = Tag.convert(model)
        if cat is None:
            return None
        cat.set_posts()
        return cat

    @staticmethod
    def __get_short_version(model):
        cat = Tag.convert(model)
        return cat


    """
        Methods get by ID
    """

    @staticmethod
    def get_by_id(id):
        return TagInterface.__get_full_version(Tag.query().filter_first({'id':id,'type':'tag'}))

    @staticmethod
    def get_by_id_short(id):
        return TagInterface.__get_short_version(Tag.query().filter_first({'id':id,'type':'tag'}))

    """
           Methods get by slug
       """

    @staticmethod
    def get_by_slug(slug: str):
        return TagInterface.__get_full_version(Tag.query().filter_first({'slug':slug,'type':'tag'}))

    @staticmethod
    def get_by_slug_short(slug: str):
        return TagInterface.__get_short_version(Tag.query().filter_first({'slug':slug,'type':'tag'}))

    """
            Methods get all posts
        """
    @staticmethod
    def get_all():
        return [TagInterface.__get_full_version(model) for model in Tag.query().filter({'type':'tag'})]

    @staticmethod
    def get_all_short():
        return [TagInterface.__get_short_version(model) for model in Tag.query().filter({'type':'tag'})]