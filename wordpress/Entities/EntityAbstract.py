from abc import ABCMeta, abstractmethod, abstractproperty
from .Protocolos import ProtocolEntity,ProtocolFields,ProtocolPost
from wordpress.models import Types,Terms,Entities
from django.db import models
from .Query import *
from django.core.exceptions import ObjectDoesNotExist
from .Errors import *
from functions import convert_model_to_dict,convert_dict_to_model
from django.urls import reverse

def get_types():
    """
    Добавление терминов таксономии к типа сущностей
    """
    types = {}
    for i in Terms.TaxonomiesTypes:
        types[i[0]] = i[1]

    """
    Добавление типов записей к типа сущностей
    """

    for i in Types.objects.all():
        types[i.slug] = i.title

    return types

class EntityAbstract(ProtocolEntity):

    _TYPES = get_types()

    _TYPE = None
    _model = None

    _image = None

    _created_at = None
    _updated_at = None

    def __init__(self, model:models):

        self._model = self._set_model(model)
        self.__set_type(model)
        self._id = self._model['id'] if isinstance(self._model,dict)else self._model.id
        self._title = self._set_title(self._model)
        self._slug = self._set_slug(self._model)
        self._link = self._set_link(self._model)
        self._link_edit = self._set_link_edit(self._model)



    # -----------------------[ Setters ]-----------------------------------------------

    def _set_model(self,model):
        return convert_dict_to_model(model,Entities)

    def __set_type(self, model):

        if isinstance(model,dict) and ("type" in model or "type_id" in model):
            query = QueryEntity(Types)
            type_id = model['type'] if "type" in model else model["type_id"]
            type = query.by_id(type_id,['slug'])['slug']
        else:
            type = model.type

        if str(type) not in self._TYPES:
            raise KeyError(errors_handler(ERRORS['TypeNotExist'],type))

        self._TYPE = self._TYPES[str(type)]

    def _set_title(self,model):
        if isinstance(model,dict):
            return model['title']
        elif isinstance(model,models.Model):
            return model.title

    def _set_slug(self,model):
        if isinstance(self._model, dict):
            return  model['slug']
        elif isinstance(self._model, models.Model):
            return  model.slug

    def _set_link(self,model):

        if isinstance(model, dict):
            raise Exception("Try to get link object in short version ")
        elif isinstance(model, models.Model):
            return model.get_absolute_url()

    def _set_link_edit(self,model):

        if isinstance(model, dict):
            raise Exception("Try to get link object in short version ")
        elif isinstance(model, models.Model):
            return model.get_absolute_url_edit()

    def set_image(self):
        if hasattr(self._model, 'image'):
            self._image = self._model.image
        else:
            self._image = None
    # -----------------------[ Getters ]-----------------------------------------------


    def get_id(self):
        return self._id


    def get_title(self):
        return self._title


    def get_slug(self):
        return self._slug


    def get_link(self):
        return self._link

    def get_type(self):
        return self._TYPE

    def get_image(self):
        return {
            'url': self._image.get_display_url() if self._image is not None else '',
            'alt': self._image.title if self._image is not None else '',
            'id': self._image.id if self._image is not None else '',
        }

    def get_thumbnail(self):
        return {
            'url': self._model.image.get_thumbnail_url(),
            'alt': self._model.image.title
        }

    def get_link_edit(self):
        return self._link_edit


    # -----------------------[ other methods ]-----------------------------------------------
    @classmethod
    def convert(cls, result):
        if result is None:
            return None
        elif isinstance(result, list):
            return [cls(post) for post in result]
        else:
            return cls(result)


    # -----------------------[ static methods ]-----------------------------------------------
    @staticmethod
    def query(model=Entities):
        queryObject = type('queryClass', (QueryEntity, QueryRelationships), dict(_modelClass=None))

        return queryObject(model)

    @staticmethod
    def get_link_add(model=Entities,**kwargs):
        return model.get_absolute_url_create(**kwargs)
    # -----------------------[ Magic methods ]-----------------------------------------------

    def __getattr__(self, key):
        if f"get_{key}" not in dir(self):
            raise AttributeError(key)

        return object.__getattribute__(self, f"get_{key}")()

    def __str__(self):
        return self._title

    def __int__(self):
        return self._id

