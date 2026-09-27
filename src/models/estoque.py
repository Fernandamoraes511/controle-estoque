"""
Classe central do sistema: Estoque.

Ela compõe produtos, fornecedores e movimentações, concentra as
regras de negócio (entrada/saída, validações) e é responsável por
salvar/carregar o estado completo em um arquivo JSON.
"""

from __future__ import annotations
import json
import os

from src.models.produto import Produto
from src.models.fornecedor import Fornecedor
from src.models.movimentacao import MovimentacaoEstoque, TipoMovimentacao
from src.exceptions import (
    ProdutoNaoEncontradoError,
    ProdutoJaExisteError,
    EstoqueInsuficienteError,
    FornecedorNaoEncontradoError,
    QuantidadeInvalidaError,
)


class Estoque:
    """Agrega produtos, fornecedores e o histórico de movimentações."""

    def __init__(self):
        self.produtos: dict[str, Produto] = {}
        self.fornecedores: dict[str, Fornecedor] = {}
        self.movimentacoes: list[MovimentacaoEstoque] = []

    # ---------------- Produtos ----------------
    def adicionar_produto(self, produto: Produto):
        if produto.codigo in self.produtos:
            raise ProdutoJaExisteError(produto.codigo)
        self.produtos[produto.codigo] = produto

    def buscar_produto(self, codigo: str) -> Produto:
        produto = self.produtos.get(codigo)
        if produto is None:
            raise ProdutoNaoEncontradoError(codigo)
        return produto

    def remover_produto(self, codigo: str):
        self.buscar_produto(codigo)  # valida existência
        del self.produtos[codigo]

    def listar_produtos(self) -> list[Produto]:
        return sorted(self.produtos.values(), key=lambda p: p.nome)

    # ---------------- Movimentações ----------------
    def entrada_estoque(self, codigo: str, quantidade: int, motivo: str = "Reposição"):
        produto = self.buscar_produto(codigo)
        produto.adicionar_quantidade(quantidade)
        mov = MovimentacaoEstoque(codigo, TipoMovimentacao.ENTRADA, quantidade, motivo)
        self.movimentacoes.append(mov)
        return mov

    def saida_estoque(self, codigo: str, quantidade: int, motivo: str = "Venda"):
        produto = self.buscar_produto(codigo)
        if quantidade <= 0:
            raise QuantidadeInvalidaError(quantidade)
        if produto.quantidade < quantidade:
            raise EstoqueInsuficienteError(codigo, produto.quantidade, quantidade)
        produto.remover_quantidade(quantidade)
        mov = MovimentacaoEstoque(codigo, TipoMovimentacao.SAIDA, quantidade, motivo)
        self.movimentacoes.append(mov)
        return mov

    # ---------------- Fornecedores ----------------
    def adicionar_fornecedor(self, fornecedor: Fornecedor):
        self.fornecedores[fornecedor.codigo] = fornecedor

    def buscar_fornecedor(self, codigo: str) -> Fornecedor:
        fornecedor = self.fornecedores.get(codigo)
        if fornecedor is None:
            raise FornecedorNaoEncontradoError(codigo)
        return fornecedor

    def listar_fornecedores(self) -> list[Fornecedor]:
        return sorted(self.fornecedores.values(), key=lambda f: f.nome)

    # ---------------- Consultas / regras de negócio ----------------
    def valor_total_estoque(self) -> float:
        return sum(p.valor_total() for p in self.produtos.values())

    def produtos_em_falta(self, minimo: int = 5) -> list[Produto]:
        return [p for p in self.produtos.values() if p.esta_em_falta(minimo)]

    def produtos_proximos_vencimento(self, dias: int = 7) -> list[Produto]:
        from src.models.produto import ProdutoPerecivel
        return [
            p for p in self.produtos.values()
            if isinstance(p, ProdutoPerecivel) and p.esta_proximo_vencimento(dias)
        ]

    # ---------------- Persistência (JSON) ----------------
    def to_dict(self) -> dict:
        return {
            "produtos": [p.to_dict() for p in self.produtos.values()],
            "fornecedores": [f.to_dict() for f in self.fornecedores.values()],
            "movimentacoes": [m.to_dict() for m in self.movimentacoes],
        }

    def salvar(self, caminho: str):
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(self.to_dict(), arquivo, ensure_ascii=False, indent=2)

    @classmethod
    def carregar(cls, caminho: str) -> "Estoque":
        estoque = cls()
        if not os.path.exists(caminho):
            return estoque  # começa vazio se ainda não existir arquivo

        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        for dados_produto in dados.get("produtos", []):
            produto = Produto.from_dict(dados_produto)
            estoque.produtos[produto.codigo] = produto

        for dados_fornecedor in dados.get("fornecedores", []):
            fornecedor = Fornecedor.from_dict(dados_fornecedor)
            estoque.fornecedores[fornecedor.codigo] = fornecedor

        for dados_mov in dados.get("movimentacoes", []):
            estoque.movimentacoes.append(MovimentacaoEstoque.from_dict(dados_mov))

        return estoque