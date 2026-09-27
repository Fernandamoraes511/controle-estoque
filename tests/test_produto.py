import unittest
from datetime import date, timedelta

from src.models.produto import Produto, ProdutoPerecivel, ProdutoNaoPerecivel
from src.exceptions import PrecoInvalidoError, QuantidadeInvalidaError


class TestProduto(unittest.TestCase):

    def test_criacao_produto_valido(self):
        p = Produto("P001", "Caneta", 2.5, 100)
        self.assertEqual(p.codigo, "P001")
        self.assertEqual(p.quantidade, 100)

    def test_preco_negativo_gera_erro(self):
        with self.assertRaises(PrecoInvalidoError):
            Produto("P001", "Caneta", -1, 10)

    def test_quantidade_negativa_gera_erro(self):
        with self.assertRaises(QuantidadeInvalidaError):
            Produto("P001", "Caneta", 2.5, -5)

    def test_valor_total(self):
        p = Produto("P001", "Caneta", 2.0, 10)
        self.assertEqual(p.valor_total(), 20.0)

    def test_produto_em_falta(self):
        p = Produto("P001", "Caneta", 2.0, 3)
        self.assertTrue(p.esta_em_falta(minimo=5))
        self.assertFalse(p.esta_em_falta(minimo=1))

    def test_adicionar_e_remover_quantidade(self):
        p = Produto("P001", "Caneta", 2.0, 10)
        p.adicionar_quantidade(5)
        self.assertEqual(p.quantidade, 15)
        p.remover_quantidade(3)
        self.assertEqual(p.quantidade, 12)

    def test_serializacao_produto(self):
        p = Produto("P001", "Caneta", 2.0, 10, categoria="Papelaria")
        dados = p.to_dict()
        p2 = Produto.from_dict(dados)
        self.assertEqual(p.codigo, p2.codigo)
        self.assertEqual(p.quantidade, p2.quantidade)


class TestProdutoPerecivel(unittest.TestCase):

    def test_dias_para_vencer(self):
        validade = (date.today() + timedelta(days=10)).isoformat()
        p = ProdutoPerecivel("P002", "Leite", 4.5, 20, validade)
        self.assertEqual(p.dias_para_vencer(), 10)

    def test_produto_vencido(self):
        validade = (date.today() - timedelta(days=1)).isoformat()
        p = ProdutoPerecivel("P002", "Leite", 4.5, 20, validade)
        self.assertTrue(p.esta_vencido())

    def test_proximo_vencimento(self):
        validade = (date.today() + timedelta(days=3)).isoformat()
        p = ProdutoPerecivel("P002", "Leite", 4.5, 20, validade)
        self.assertTrue(p.esta_proximo_vencimento(dias=7))
        self.assertFalse(p.esta_proximo_vencimento(dias=1))

    def test_serializacao_perecivel(self):
        validade = (date.today() + timedelta(days=5)).isoformat()
        p = ProdutoPerecivel("P002", "Leite", 4.5, 20, validade)
        dados = p.to_dict()
        p2 = Produto.from_dict(dados)
        self.assertIsInstance(p2, ProdutoPerecivel)
        self.assertEqual(p.data_validade, p2.data_validade)


class TestProdutoNaoPerecivel(unittest.TestCase):

    def test_garantia(self):
        p = ProdutoNaoPerecivel("P003", "Furadeira", 250.0, 5, garantia_meses=12)
        self.assertIn("12", p.info_extra())

    def test_serializacao_nao_perecivel(self):
        p = ProdutoNaoPerecivel("P003", "Furadeira", 250.0, 5, garantia_meses=12)
        dados = p.to_dict()
        p2 = Produto.from_dict(dados)
        self.assertIsInstance(p2, ProdutoNaoPerecivel)
        self.assertEqual(p2.garantia_meses, 12)


if __name__ == "__main__":
    unittest.main()