from rise_info.baseModels import CommonInfo

class FailuerReport(CommonInfo):
    def save(self, *args, **kwargs):
        super(FailuerReport, self).save(self, *args, **kwargs)
    
    class Meta:
        db_table = 'failuer_reports'