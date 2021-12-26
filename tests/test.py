from phaedo.core import DomainModel, Field, ListField

from enum import Enum, auto


class Status(Enum):
    ACTIVE = auto()
    INACTIVE = auto()


class Test(DomainModel):
    status = Field(field_type=Status, name='Status', default=Status.INACTIVE, load=False)
    sns: ListField['SNS'] = ListField(field_type='SNS', name='SNS')


class SNS(DomainModel):
    sns_id = Field(field_type=str, name='SNS ID')


sns1 = SNS()
sns1.sns_id = 'testtest1'
sns2 = SNS()
sns2.sns_id = 'testtest2'

test1 = Test()
test1.sns = [sns1]
test1.sns.append(sns2)

print(test1.dumps())
