from tortoise import Model, fields
from tortoise.fields import ReverseRelation


class Task(Model):
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    start_date = fields.DatetimeField()
    end_date = fields.DatetimeField()
    status = fields.IntField()

    task_elements: ReverseRelation['TaskElement']

    class Meta:
        table = 'task'


class TaskElement(Model):
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    value = fields.TextField()

    task = fields.ForeignKeyField('models.Task',
                                  related_name='task_elements')

    class Meta:
        table = 'task_element'
