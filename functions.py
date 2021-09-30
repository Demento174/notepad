from django.db import models
from django.forms.models import model_to_dict

import wordpress.models


def convert_model_to_dict(model):

    if isinstance(model, dict):
        return model
    elif(isinstance(model,models.Model)):
        result = model_to_dict(model)
        if 'get_absolute_url' in model:
            result['get_absolute_url'] = model.get_absolute_url()
        return result
    else:
        raise Exception(f"{model} have undefined type")


def convert_dict_to_model(values,model:models.Model):

    if isinstance(values,models.Model):
        return values
    elif isinstance(values,dict):
        return model.objects.filter(**values).first()
    else:
        raise Exception(f"{values} have undefined type")