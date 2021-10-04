from abc import ABCMeta,abstractmethod, ABC
from .Errors import *

class ProtocolEntity(ABC):
    _mode = None
    _id = None
    _title = None
    _slug = None
    _link = None
    _link_edit = None

    # -----------------------[ Setters ]-----------------------------------------------
    @abstractmethod
    def _set_model(self,model):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def _set_title(self,model):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def _set_slug(self,model):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def _set_link(self,model):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def _set_link_edit(self, model):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    # -----------------------[ Getters ]-----------------------------------------------
    @abstractmethod
    def get_id(self):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def get_title(self):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def get_slug(self):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def get_link(self):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def get_link_edit(self):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))



class ProtocolPost(ABC):
    _content = None
    _created_at = None
    _updated_at = None


    @abstractmethod
    def _set_content(self,*args,**kwargs):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def _set_created_at(self,*args,**kwargs):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def _set_updated_at(self,*args,**kwargs):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))


    @abstractmethod
    def get_content(self,*args,**kwargs):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def get_created_at(self,model):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def get_updated_at(self,model):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))



class ProtocolFields(ABC):


    @abstractmethod
    def __set_fields(cls):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))

    @abstractmethod
    def get_field(cls,selector):
        raise NotImplementedError(errors_handler(ERRORS['NotImplemented']))


class ProtocolQuery(ABC):

    @abstractmethod
    def set_modelClass(cls,model):
        return None

