from repo.models import Condition, ConditionType, Measurement, MeasurementSet, MeasurementType, Compound, Source, Reference, Model
from django.contrib import admin

admin.site.register(Model)
admin.site.register(Condition)
admin.site.register(ConditionType)
admin.site.register(Measurement)
admin.site.register(MeasurementSet)
admin.site.register(MeasurementType)
admin.site.register(Compound)
admin.site.register(Source)
admin.site.register(Reference)
