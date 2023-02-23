from mongoengine import Document, EmbeddedDocument, fields


class GeneratedQuestion(EmbeddedDocument):
    user_score = fields.FloatField(default=0)
    max_score = fields.FloatField(default=1)
    question_id = fields.LongField()
    answers = fields.ListField()
    given_answer = fields.ListField()

    class Meta:
        db_alias = 'gen_connect'


class GeneratedTest(Document):
    user_id = fields.LongField(db_index=True)
    test_id = fields.LongField(db_index=True)
    questions = fields.EmbeddedDocumentListField(GeneratedQuestion)
    result = fields.IntField()
    start_time = fields.DateTimeField()
    end_time = fields.DateTimeField()

    class Meta:
        db_alias = 'gen_connect'