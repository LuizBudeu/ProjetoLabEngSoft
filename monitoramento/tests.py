from django.test import TestCase
from monitoramento.models import Voos, Partidas, Chegadas
from datetime import datetime, timedelta, timezone


class VoosTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        voo = {
            'companhia_aerea': 'Verde',
            'codigo': 'AA0000',
            'origem': 'Sao Paulo',
            'destino': 'Rio de Janeiro',
            'partida_prevista': datetime.now().replace(tzinfo=timezone.utc),
            'chegada_prevista': datetime.now().replace(tzinfo=timezone.utc) + timedelta(hours=1),
        }

        Voos.objects.create(**voo)

    def test_criacao_id(self):
        voo_1 = Voos.objects.get(codigo='AA0000')
        self.assertEqual(voo_1.id, 1)

    def test_update_destino(self):
        voo_1 = Voos.objects.get(destino='Rio de Janeiro')
        voo_1.destino = "Rio de Fevereiro"
        voo_1.save()
        self.assertEqual(voo_1.destino, "Rio de Fevereiro")

    def test_delete(self):
        Voos.objects.filter(id=1).delete()
        self.assertEqual(Voos.objects.count(),0)


class PartidasTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        partida = {
            'status': 'programado',
            'destino': 'Rio de Janeiro',
            'partida_prevista':datetime.now().replace(tzinfo=timezone.utc),
            'partida_real': datetime.now().replace(tzinfo=timezone.utc) + timedelta(hours=1),
        }

        Partidas.objects.create(**partida)

    def test_criacao_id(self):
        partida_1 = Partidas.objects.get(status='programado')
        self.assertEqual(partida_1.id, 1)

    def test_update_status(self):
        partida_1 = Partidas.objects.get(status='programado')
        partida_1.status = "embarcando"
        partida_1.save()
        self.assertEqual(partida_1.status, "embarcando")
    
    def test_delete(self):
        Partidas.objects.filter(id=1).delete()
        self.assertEqual(Partidas.objects.count(),0)


class ChegadasTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        chegada = {
            'origem': 'Sao Paulo',
            'chegada_prevista': datetime.now().replace(tzinfo=timezone.utc),
            'chegada_real': datetime.now().replace(tzinfo=timezone.utc),
        }

        Chegadas.objects.create(**chegada)

    def test_criacao_id(self):
        voo_1 = Chegadas.objects.get(origem='Sao Paulo')
        self.assertEqual(voo_1.id, 1)

    def test_update_chegada_real(self):
        voo_1 = Chegadas.objects.get()
        voo_1.chegada_real = datetime.now().replace(tzinfo=timezone.utc) + timedelta(hours=1)
        voo_1.save()
        self.assertEqual(voo_1.chegada_real, datetime.now().replace(tzinfo=timezone.utc) + timedelta(hours=1))

    def test_delete(self):
        Chegadas.objects.filter(id=1).delete()
        self.assertEqual(Chegadas.objects.count(),0)