import shortuuid
from django.db import models



class CustomPKFields(models.CharField):
    def __init__(self, *args, primary_key=True, **kwargs):

        if 'max_length' not in kwargs:
            kwargs['max_length'] = 20
        kwargs['primary_key']=primary_key
        kwargs['unique']=True
        kwargs['editable']=False
        super().__init__(*args, **kwargs)

    def generate_pk(self):
        return shortuuid.uuid()[:self.max_length]

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            pk = self.generate_pk()
            setattr(model_instance, self.attname, pk)
            return pk
        return super().pre_save(model_instance, add)



