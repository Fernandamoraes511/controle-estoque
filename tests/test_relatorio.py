import unittest
import os
import tempfile

from src.models.estoque import Estoque
from src.models.produto import Produto
from src.relatorio import Relatorio


class TestRelatorio(unittest.TestCase):

    def setUp(self):
        self.estoque = Estoque()
        self.estoque.adicionar_produto(Produto("P001", "Caneta", 2.0, 3))
        self.estoque.adicionar_produto(Produto("P002", "Caderno", 8.0, 50))
        self.estoque.entrada_estoque("P001", 10, "Compra")
        self.estoque.saida_estoque("P002", 5, "Venda")
        self.relatorio = Relatorio(self.estoque)

    def test_texto_produtos_em_falta(self):
        texto = self.relatorio.texto_produtos_em_falta(minimo=5)
        # Caneta tinha 3, +10 de entrada = 13, não deve mais estar em falta
        self.assertNotIn("Caneta", texto)
        self.assertIn("Nenhum produto", texto)

    def test_texto_valor_total(self):
        texto = self.relatorio.texto_valor_total()
        self.assertIn("R$", texto)

    def test_totais_por_produto(self):
        totais = self.relatorio.totais_por_produto()
        self.assertEqual(totais["P001"]["entrada"], 10)
        self.assertEqual(totais["P002"]["saida"], 5)

    def test_gerar_grafico_estoque_atual(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = os.path.join(tmp, "grafico.png")
            resultado = self.relatorio.gerar_grafico_estoque_atual(caminho)
            self.assertTrue(os.path.exists(resultado))

    def test_gerar_grafico_movimentacoes(self):
        with tempfile.TemporaryDirectory() as tmp:
            caminho = os.path.join(tmp, "grafico_mov.png")
            resultado = self.relatorio.gerar_grafico_movimentacoes(caminho)
            self.assertTrue(os.path.exists(resultado))


if __name__ == "__main__":
    unittest.main()