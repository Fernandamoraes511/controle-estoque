import unittest
import os
import tempfile

from src.models.estoque import Estoque
from src.models.produto import Produto, ProdutoPerecivel
from src.models.fornecedor import Fornecedor
from src.exceptions import (
    ProdutoNaoEncontradoError,
    ProdutoJaExisteError,
    EstoqueInsuficienteError,
)


class TestEstoque(unittest.TestCase):

    def setUp(self):
        self.estoque = Estoque()
        self.estoque.adicionar_produto(Produto("P001", "Caneta", 2.0, 10))

    def test_adicionar_produto_duplicado_gera_erro(self):
        with self.assertRaises(ProdutoJaExisteError):
            self.estoque.adicionar_produto(Produto("P001", "Caneta 2", 3.0, 5))

    def test_buscar_produto_inexistente_gera_erro(self):
        with self.assertRaises(ProdutoNaoEncontradoError):
            self.estoque.buscar_produto("INEXISTENTE")

    def test_entrada_estoque(self):
        self.estoque.entrada_estoque("P001", 5, "Compra")
        produto = self.estoque.buscar_produto("P001")
        self.assertEqual(produto.quantidade, 15)
        self.assertEqual(len(self.estoque.movimentacoes), 1)

    def test_saida_estoque(self):
        self.estoque.saida_estoque("P001", 4, "Venda")
        produto = self.estoque.buscar_produto("P001")
        self.assertEqual(produto.quantidade, 6)

    def test_saida_maior_que_estoque_gera_erro(self):
        with self.assertRaises(EstoqueInsuficienteError):
            self.estoque.saida_estoque("P001", 999, "Venda")

    def test_valor_total_estoque(self):
        self.estoque.adicionar_produto(Produto("P002", "Lápis", 1.0, 20))
        # P001: 2.0 * 10 = 20 | P002: 1.0 * 20 = 20 -> total 40
        self.assertEqual(self.estoque.valor_total_estoque(), 40.0)

    def test_produtos_em_falta(self):
        self.estoque.adicionar_produto(Produto("P002", "Lápis", 1.0, 2))
        em_falta = self.estoque.produtos_em_falta(minimo=5)
        codigos = [p.codigo for p in em_falta]
        self.assertIn("P002", codigos)
        self.assertNotIn("P001", codigos)

    def test_fornecedores(self):
        self.estoque.adicionar_fornecedor(Fornecedor("F001", "Distribuidora XYZ"))
        fornecedor = self.estoque.buscar_fornecedor("F001")
        self.assertEqual(fornecedor.nome, "Distribuidora XYZ")

    def test_persistencia_salvar_e_carregar(self):
        self.estoque.adicionar_produto(
            ProdutoPerecivel("P003", "Iogurte", 3.5, 8, "2030-01-01")
        )
        self.estoque.adicionar_fornecedor(Fornecedor("F001", "Distribuidora XYZ"))
        self.estoque.entrada_estoque("P001", 5, "Reposição")

        with tempfile.TemporaryDirectory() as tmp:
            caminho = os.path.join(tmp, "estoque_teste.json")
            self.estoque.salvar(caminho)

            estoque_carregado = Estoque.carregar(caminho)

            self.assertEqual(len(estoque_carregado.produtos), 2)
            self.assertEqual(len(estoque_carregado.fornecedores), 1)
            self.assertEqual(len(estoque_carregado.movimentacoes), 1)

            produto = estoque_carregado.buscar_produto("P001")
            self.assertEqual(produto.quantidade, 15)  # 10 + 5 de entrada


if __name__ == "__main__":
    unittest.main()