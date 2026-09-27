"""Modelagem de fornecedores."""

from __future__ import annotations


class Fornecedor:
    """Representa um fornecedor de produtos para o estoque."""

    def __init__(self, codigo: str, nome: str, contato: str = ""):
        self.codigo = codigo
        self.nome = nome
        self.contato = contato
        self.produtos_fornecidos: list[str] = []  # códigos de produtos

    def vincular_produto(self, codigo_produto: str):
        if codigo_produto not in self.produtos_fornecidos:
            self.produtos_fornecidos.append(codigo_produto)

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "contato": self.contato,
            "produtos_fornecidos": self.produtos_fornecidos,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Fornecedor":
        f = cls(dados["codigo"], dados["nome"], dados.get("contato", ""))
        f.produtos_fornecidos = dados.get("produtos_fornecidos", [])
        return f

    def __str__(self):
        return f"[{self.codigo}] {self.nome} | Contato: {self.contato} | Produtos: {len(self.produtos_fornecidos)}"