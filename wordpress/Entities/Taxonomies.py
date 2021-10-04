from .EntityAbstract import EntityAbstract,ERRORS,errors_handler
from .Query import QueryEntity,QueryRelationships
from django.db import models
from wordpress.models import Terms



class TaxonomiesAbstract(EntityAbstract):
    _posts = None
    _fields = None
    _description = None
    def __init__(self, model: Terms):

        self.check_type(model.type)

        super().__init__(model)

    # -----------------------[ Setters ]-----------------------------------------------

    def set_fields(self):
        self._fields = []

    def set_posts(self):
        result = []
        for post in self._model.entities_terms.all():
            result.append(post.pk)
        self._posts = result

    def set_description(self):
        self._description = self._model.description


    # -----------------------[ Getters ]-----------------------------------------------


    def get_field(self, selector):
        pass

    def get_content(self):
        return self._content


    def get_posts(self):
        return self._posts

    def get_count_post(self):
        return len(self._posts)

    def get_description(self):
        return self._description

    def get_created_at(self):
        return self._created_at

    def get_updated_at(self):
        return self._updated_at



    # -----------------------[ Other Function ]-----------------------------------------------
    @classmethod
    def check_type(self,type):


        if str(type) != str(self._TYPE):
            return False
            # raise Exception(errors_handler(ERRORS['TermIsNotValidType'],self._TYPE,str(type)))
        return True

    def check_posts(self):
        if self.get_count_post() > 0:
            return True
        else:
            return False

    # -----------------------[ static methods ]-----------------------------------------------
    @staticmethod
    def query(model=Terms):
        queryObject = type('queryClass', (QueryEntity, QueryRelationships), dict(_modelClass=None))
        return queryObject(model)

class Category(TaxonomiesAbstract):

    _TYPE = Terms.TaxonomiesTypes[0][0]
    _parent = None
    _childrens = None

    def __init__(self, model:Terms):

        super().__init__(model)

    # -----------------------[ Setters ]-----------------------------------------------
    def set_parent(self):

        self._parent =  self._model.parent_id

    def set_childrens(self):
        result = []

        for children in self._model.get_children():
            result.append(children.pk)
        self._childrens = result

    # -----------------------[ Getters ]-----------------------------------------------
    def get_parent(self):
        if self._parent is not None:
            return Category(Category.query().by_id(self._parent))
        else:
            return None

    def get_childrens(self):
        result = []

        for children in self._childrens:
            result.append(Category(Category.query().by_id(children)))
        return result

    def get_family(self):
        return self._model.get_descendants()

    @staticmethod
    def get_link_add(model=Terms, **kwargs):
        return EntityAbstract.get_link_add(model=Terms, type='category')


class Tag(TaxonomiesAbstract):
    _TYPE = Terms.TaxonomiesTypes[1][0]

    def __int__(self, model: Terms):
        super().__int__(model)

    @staticmethod
    def get_link_add(model=Terms, **kwargs):
        return EntityAbstract.get_link_add(model=Terms, type='tag')


