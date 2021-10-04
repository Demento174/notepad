from .EntityAbstract import EntityAbstract
from django.db import models
from wordpress.models import Entities,Terms, Types
from .Protocolos import ProtocolPost
from .Taxonomies import Category
from .Query import QueryEntity, QueryRelationships
from .Errors import *
from functions import convert_dict_to_model


class Post(ProtocolPost,EntityAbstract):

    _terms = None
    _content = None

    _fields = None

    _categories = None
    _tags = None

    _created_at = None
    _updated_at = None
    def __init__(self, model: Entities):

        super().__init__(model)
        self._content = self._set_content(self._model)
        self._fields = self._set_fields()
        self._created_at = self._set_created_at(self._model)
        self._updated_at = self._set_updated_at(self._model)

    # -----------------------[ setters ]-----------------------------------------------
    def _set_fields(self):
        return []

    def _set_content(self,model):
        if isinstance(model, dict):
            return model['content']
        elif isinstance(model, Entities):
            return model.content

    def set_taxonomies(self):
        model = convert_dict_to_model(self._model,Entities)

        self.__set_terms(model)
        self.__set_categories(model)
        self.__set_tags(model)

    def __set_terms(self,model):
        self._terms = model.terms.all()

    def __set_categories(self,model):

        self._categories = []

        for term in model.terms.all():
            if term.type == Terms.TaxonomiesTypes[0][0]:
                self._categories.append(Category(term))

        return self._categories

    def __set_tags(self,model):
        from .Taxonomies import Tag
        self._tags = []
        for term in model.terms.all():
            if term.type == Terms.TaxonomiesTypes[1][0]:
                self._tags.append(Tag(term))



    def _set_created_at(self,model):
        return model.created_at

    def _set_updated_at(self,model):
        return model.updated_at

    # -----------------------[ Getters ]-----------------------------------------------
    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_slug(self):
        return self._slug

    def get_field(self, selector):
        pass

    def get_content(self):
        return self._content

    def get_link(self):
        return self._link

    def get_categories(self):
        return self._categories

    def get_tags(self):

        return self._tags

    def get_created_at(self):
        return self._created_at

    def get_updated_at(self):
        return self._updated_at

    @staticmethod
    def get_link_add(model=Entities,**kwargs):
        return EntityAbstract.get_link_add(model=Entities,**kwargs)





class PostType(EntityAbstract):
    _model = None
    _id = None
    _title = None
    _slug = None
    _link = None
    _content = None
    _posts = None
    _count = None


    def __init__(self,model:Types):

        self._model = self._set_model(model)

        self._id = self._model.id
        self._title = self._set_title(self._model)
        self._slug = self._set_slug(self._model)
        self._link = self._set_link(self._model)
        self._link_edit = self._set_link_edit(self._model)

    # -----------------------[ Setters ]-----------------------------------------------
    def _set_model(self,model):
        return convert_dict_to_model(model,Types)

    def _set_link(self,model):

        if isinstance(model, dict):
            raise Exception("Try to get link object in short version ")
        elif isinstance(model,Types):

            return model.get_absolute_url()

    def set_posts(self):
        self._posts =  [Post(post) for post in self._model.entities_type.all()]

    def content(self):
        self._content = self._model.content

    # -----------------------[ Getters ]-----------------------------------------------

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_slug(self):
        return self._slug

    def get_link(self):
        return self._link

    def get_content(self):
        return self._content

    def get_posts(self):
        return self._posts

    def get_count_posts(self):
        if self._posts is None:
             raise Exception(f"posts for {self._model.slug} not defined")
        else:
            return len(self._posts)

    def get_link_add_post(self):
        return EntityAbstract.get_link_add(model=Entities, type= self.slug)

    @staticmethod
    def get_link_add(model=Types,**kwargs):
        return EntityAbstract.get_link_add(model=Types,**kwargs)




    # -----------------------[ Static methods ]-----------------------------------------------

    @staticmethod
    def query(model=Types):
        queryObject = type('queryClass', (QueryEntity, QueryRelationships), dict(_modelClass=None))
        return queryObject(model)




    def __str__(self):
        return self._title