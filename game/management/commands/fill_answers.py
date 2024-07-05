import random
import string

from django.core.management import BaseCommand

from game.constants import CODE_LANGUAGES
from game.models import Answer, Task


class Command(BaseCommand):
    """creates random answers"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="also delete all answers",
        )

    def handle(self, *args, **options):
        if options["delete"]:
            Answer.objects.all().delete()

        task_id_list = Task.objects.values_list('id', flat=True)
        usersname_list = [
            'Myxa#228',
            'bee4#178',
            'wakandaforever#mu0',
            'huh?#12j',
            'P0BHblY_AXMED#7771'
        ]


        answer_list = []
        for i in range(100):
            code_len = random.randint(20, 100)
            answer_list.append(
                Answer(
                    task_id=random.choice(task_id_list),
                    code=''.join(random.choices(string.ascii_uppercase + string.digits, k=code_len)),
                    code_result='testcase',
                    code_lang='cpp',
                    code_len=code_len,
                    username=random.choice(usersname_list),
                    is_correct=random.choice((True, False))
                )
            )

        Answer.objects.bulk_create(answer_list)
