from abc import ABCMeta, abstractmethod
from django.db import models
from .Errors import *
from .Protocolos import ProtocolQuery


class AbstractQuery(ProtocolQuery):
    _modelClass = None

    def __init__(self,modelClass):

        self._modelClass = self.set_modelClass(modelClass)

    def set_modelClass(cls,model):
        return model

class QueryEntity(AbstractQuery):


    def by_id(self, id: int,values: list=[]):
        return self._modelClass.objects.values(*values).get(pk=id) if values else self._modelClass.objects.get(pk=id)

    def by_slug(self, slug: str,values: list=None ):
        return self._modelClass.objects.values(*values).filter(slug=slug).first() if values else self._modelClass.objects.filter(slug=slug).first()



    def all(self,values: list=None):
        return [entity for entity in (self._modelClass.objects.values(*values).all() if values else self._modelClass.objects.all())]



    def by_identifiers(self,identifiers : list,values: list=None):
        return self._modelClass.objects.values(*values).filter(pk__in=identifiers) if values else self._modelClass.objects.filter(pk__in=identifiers)


    def filter_first(self,kwargs,values=None):
        return self._modelClass.objects.values(*values).filter(**kwargs).first() if values else self._modelClass.objects.filter(**kwargs).first()

    def filter(self,kwargs,values=None):
        return self._modelClass.objects.values(*values).filter(**kwargs) if values else self._modelClass.objects.filter(**kwargs)


class QueryRelationships(AbstractQuery):

    def all_non_empty(self,  titleField:str,values: list = None):
        return [post for post in self._modelClass.objects.values(*values).annotate(cnt=models.Count(titleField)).filter(cnt__gt=0)]


    def all_empty(self, titleField:str,values: list = None):
        return [post for post in
                    self._modelClass.objects.values(*values).annotate(cnt=models.Count(titleField)).filter(cnt=0)]


