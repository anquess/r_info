from rise_info.baseModels import CommonInfo

class Info(CommonInfo):
    def save(self, *args, **kwargs):
        super(Info, self).save(self, *args, **kwargs)
    
    class Meta:
        db_table = 'infos'