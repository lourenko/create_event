from datetime import date, datetime, timedelta
from cal_setup import get_calendar_service
import click


@click.command()
@click.option("--sumario", prompt="Sumário") #, help="The title for the calendar event."
@click.option("--descricao", default=" ", prompt="Descrição", help="Enter the event description.")
@click.option("--data", default="today", prompt="Data") # , help="The data of ocurrence em 'dia/mes/ano'"
@click.option("--hora", default="10:00", prompt="Hora", help="The hour of ocurrence em [10,30]")
@click.option("--freq", default=None, help="The frequency of ocurrency.")
@click.option("--local", default=None, help="The location")
@click.option("--corid", default=10, help="A color int from 1 to 11.")
@click.option("--duration", default=1.0, help="The time duration in hours.")
def new_event(sumario, descricao, data, hora, freq, local, corid, duration):
    """
    Cores:
        10:verde, 9:azul, 8:branco, 7:ciano, 6:laranja,
        5:amarelo, 4:goiaba, 3:roxo, 2:cana, 11:vermelho
    """
    service = get_calendar_service()

    if data == "today":
        today = date.today()
        dia = today.day
        mes = today.month
        ano = today.year

    else:
        dataf = [int(i) for i in data.split('/')]

        if len(dataf) < 2:
            raise ValueError("A data está errada!")

        dia = dataf[0]
        mes = dataf[1]

        if len(dataf) > 2:
            ano = dataf[2]
            if len(str(ano)) < 3:
                ano = int('20'+str(ano))
        else:
            ano = 2022

    hora = [int(i) for i in hora.split(':')]

    data = datetime(ano, mes, dia, *hora)
    start = data.isoformat()
    end = (data + timedelta(hours=float(duration))).isoformat()

    if not freq:
        ocorrencia = None
    else:
        Frequencia, Vezes = freq.split(':')
        Times = int(Vezes)
        if Frequencia == 'diária':
            Frequency = "DAILY"
        elif Frequencia == 'semanal':
            Frequency = "WEEKLY"
        elif Frequencia == 'mensal':
            Frequency = "MONTHLY"
        elif Frequencia == 'anual':
            Frequency = "YEARLY"
        else:
            raise ValueError("The frequency type is wrong!")
        ocorrencia = ['RRULE:FREQ={};COUNT={}'.format(Frequency, Times),]

    event_result = service.events().insert(
        calendarId = 'primary',
        body = {
            "summary": sumario,
            "colorId": corid,
            "description": descricao,
            "location": local,
            "start": {"dateTime": start, "timeZone": 'America/Sao_Paulo'},
            "end": {"dateTime": end, "timeZone": 'America/Sao_Paulo'},
            "recurrence":ocorrencia, #
        }
    ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])

if __name__ == '__main__':

    sumario = "Teste para o calendario"
    descricao = """
    Estou fazendo
    um teste!
    """
    data = "16/03"
    hora = [10,25]
    new_event() #sumario, descricao, data, hora, 11)

    # @click.command()
    # @click.option("--count", default=1, help="Number of greetings.")
    # @click.option("--name", default=" ", prompt="Your name", help="The person to greet.")
    # def hello(count, name):
    #     """Simple program that greets NAME for a total of COUNT times."""
    #     for _ in range(count):
    #         click.echo(click.style(f"Hello, {name}!", fg="magenta", bold=True))
    #
    # hello()

