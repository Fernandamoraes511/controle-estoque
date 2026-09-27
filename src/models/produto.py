"""
Modelagem de produtos do estoque.

Este módulo demonstra herança e polimorfismo: `Produto` é a classe
base e `ProdutoPerecivel` / `ProdutoNaoPerecivel` especializam o
comportamento (por exemplo, o alerta de vencimento só faz sentido
para produtos perecíveis).
"""

from __future__ import annotations
from datetime import date, datetime

from src.exceptions import QuantidadeInvalidaError, PrecoInvalidoError


class Produto:
    """Representa um produto genérico do estoque."""

    def __init__(self, codigo: str, nome: str, preco: float,
                 quantidade: int, categoria: str = "Geral"):
        self._validar_preco(preco)
        self._validar_quantidade(quantidade, permitir_zero=True)

        self.codigo = codigo
        self.nome = nome
        self._preco = float(preco)
        self._quantidade = int(quantidade)
        self.categoria = categoria

    # --- Encapsulamento: acesso controlado a preço e quantidade ---
    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, novo_preco: float):
        self._validar_preco(novo_preco)
        self._preco = float(novo_preco)

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @staticmethod
    def _validar_preco(preco: float):
        if preco is None or preco < 0:
            raise PrecoInvalidoError(preco)

    @staticmethod
    def _validar_quantidade(quantidade: int, permitir_zero: bool = False):
        limite = 0 if permitir_zero else 1
        if quantidade is None or quantidade < limite:
            raise QuantidadeInvalidaError(quantidade)

    def adicionar_quantidade(self, quantidade: int):
        self._validar_quantidade(quantidade)
        self._quantidade += quantidade

    def remover_quantidade(self, quantidade: int):
        self._validar_quantidade(quantidade)
        self._quantidade -= quantidade

    def valor_total(self) -> float:
        """Valor total imobilizado nesse produto (preço * quantidade)."""
        return self._preco * self._quantidade

    def esta_em_falta(self, minimo: int = 5) -> bool:
        return self._quantidade <= minimo

    # --- Polimorfismo: cada subtipo pode sobrescrever esse método ---
    def info_extra(self) -> str:
        """Informação adicional específica do tipo de produto."""
        return "-"

    def to_dict(self) -> dict:
        return {
            "tipo": self.__class__.__name__,
            "codigo": self.codigo,
            "nome": self.nome,
            "preco": self._preco,
            "quantidade": self._quantidade,
            "categoria": self.categoria,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Produto":
        tipo = dados.get("tipo", "Produto")
        if tipo == "ProdutoPerecivel":
            return ProdutoPerecivel.from_dict(dados)
        if tipo == "ProdutoNaoPerecivel":
            return ProdutoNaoPerecivel.from_dict(dados)
        return Produto(
            codigo=dados["codigo"], nome=dados["nome"],
            preco=dados["preco"], quantidade=dados["quantidade"],
            categoria=dados.get("categoria", "Geral"),
        )

    def __str__(self):
        return (f"[{self.codigo}] {self.nome} | Qtd: {self._quantidade} | "
                f"R$ {self._preco:.2f} | {self.categoria} | {self.info_extra()}")


class ProdutoPerecivel(Produto):
    """Produto com data de validade (ex: alimentos, remédios)."""

    def __init__(self, codigo: str, nome: str, preco: float, quantidade: int,
                 data_validade: str, categoria: str = "Perecível"):
        super().__init__(codigo, nome, preco, quantidade, categoria)
        # formato esperado: "AAAA-MM-DD"
        self.data_validade = datetime.strptime(data_validade, "%Y-%m-%d").date()

    def dias_para_vencer(self) -> int:
        return (self.data_validade - date.today()).days

    def esta_vencido(self) -> bool:
        return self.dias_para_vencer() < 0

    def esta_proximo_vencimento(self, dias: int = 7) -> bool:
        return 0 <= self.dias_para_vencer() <= dias

    def info_extra(self) -> str:
        dias = self.dias_para_vencer()
        if dias < 0:
            return f"VENCIDO há {abs(dias)} dia(s)"
        return f"vence em {dias} dia(s)"

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["data_validade"] = self.data_validade.isoformat()
        return dados

    @classmethod
    def from_dict(cls, dados: dict) -> "ProdutoPerecivel":
        return cls(
            codigo=dados["codigo"], nome=dados["nome"], preco=dados["preco"],
            quantidade=dados["quantidade"], data_validade=dados["data_validade"],
            categoria=dados.get("categoria", "Perecível"),
        )


class ProdutoNaoPerecivel(Produto):
    """Produto sem validade próxima (ex: eletrônicos, utensílios)."""

    def __init__(self, codigo: str, nome: str, preco: float, quantidade: int,
                 garantia_meses: int = 0, categoria: str = "Não perecível"):
        super().__init__(codigo, nome, preco, quantidade, categoria)
        self.garantia_meses = garantia_meses

    def info_extra(self) -> str:
        if self.garantia_meses > 0:
            return f"garantia de {self.garantia_meses} mês(es)"
        return "sem garantia"

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["garantia_meses"] = self.garantia_meses
        return dados

    @classmethod
    def from_dict(cls, dados: dict) -> "ProdutoNaoPerecivel":
        return cls(
            codigo=dados["codigo"], nome=dados["nome"], preco=dados["preco"],
            quantidade=dados["quantidade"],
            garantia_meses=dados.get("garantia_meses", 0),
            categoria=dados.get("categoria", "Não perecível"),
        )