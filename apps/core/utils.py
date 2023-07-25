from django.db.models import When, Value, Case, CharField


def get_choice_display(choices, field):
    options = [
        When(**{field: k, 'then': Value(v)}) for k, v in choices
    ]
    return Case(
        *options, output_field=CharField()
    )


def get_month_display(value: str) -> str:
    months = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Março",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro"
    }

    return months[value]
