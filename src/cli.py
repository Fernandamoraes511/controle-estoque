"""Interface de linha de comando (CLI) do sistema de controle de estoque."""

from __future__ import annotations
from src.models import Estoque, ProdutoPerecivel, ProdutoNaoPerecivel, Fornecedor
from src.relatorio import Relatorio
from src.exceptions import EstoqueError

CAMINHO_DADOS = "data/estoque.json"

MENU = """
========== CONTROLE DE ESTOQUE ==========
 1  - Cadastrar produto
 2  - Listar produtos
 3  - Registrar entrada de estoque
 4  - Registrar saída de estoque
 5  - Buscar produto
 6  - Remover produto
 7  - Cadastrar fornecedor
 8  - Listar fornecedores
 9  - Relatório: produtos em falta
10  - Relatório: produtos próximos do vencimento
11  - Ver valor total do estoque
12  - Gerar gráfico de estoque atual
13  - Gerar gráfico de entradas x saídas
14  - Listar movimentações
 0  - Salvar e sair
==========================================
"""


def ler_inteiro(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Digite um número válido.")


def cadastrar_produto(estoque: Estoque):
    print("\nTipo de produto: [1] Perecível  [2] Não perecível")
    tipo = input("Escolha: ").strip()

    codigo = input("Código: ").strip()
    nome = input("Nome: ").strip()
    preco = ler_float("Preço: R$ ")
    quantidade = ler_inteiro("Quantidade inicial: ")
    categoria = input("Categoria (opcional): ").strip() or "Geral"

    if tipo == "1":
        validade = input("Data de validade (AAAA-MM-DD): ").strip()
        produto = ProdutoPerecivel(codigo, nome, preco, quantidade, validade, categoria)
    else:
        garantia = ler_inteiro("Garantia em meses (0 se não houver): ")
        produto = ProdutoNaoPerecivel(codigo, nome, preco, quantidade, garantia, categoria)

    estoque.adicionar_produto(produto)
    print(f"Produto '{nome}' cadastrado com sucesso.")


def listar_produtos(estoque: Estoque):
    produtos = estoque.listar_produtos()
    if not produtos:
        print("\nNenhum produto cadastrado.")
        return
    print(f"\n{len(produtos)} produto(s) cadastrado(s):")
    for produto in produtos:
        print(f"  {produto}")


def registrar_entrada(estoque: Estoque):
    codigo = input("Código do produto: ").strip()
    quantidade = ler_inteiro("Quantidade a adicionar: ")
    motivo = input("Motivo (opcional): ").strip() or "Reposição"
    estoque.entrada_estoque(codigo, quantidade, motivo)
    print("Entrada registrada com sucesso.")


def registrar_saida(estoque: Estoque):
    codigo = input("Código do produto: ").strip()
    quantidade = ler_inteiro("Quantidade a retirar: ")
    motivo = input("Motivo (opcional): ").strip() or "Venda"
    estoque.saida_estoque(codigo, quantidade, motivo)
    print("Saída registrada com sucesso.")


def buscar_produto(estoque: Estoque):
    codigo = input("Código do produto: ").strip()
    produto = estoque.buscar_produto(codigo)
    print(f"\nEncontrado: {produto}")


def remover_produto(estoque: Estoque):
    codigo = input("Código do produto a remover: ").strip()
    estoque.remover_produto(codigo)
    print("Produto removido com sucesso.")


def cadastrar_fornecedor(estoque: Estoque):
    codigo = input("Código do fornecedor: ").strip()
    nome = input("Nome: ").strip()
    contato = input("Contato (telefone/e-mail): ").strip()
    estoque.adicionar_fornecedor(Fornecedor(codigo, nome, contato))
    print("Fornecedor cadastrado com sucesso.")


def listar_fornecedores(estoque: Estoque):
    fornecedores = estoque.listar_fornecedores()
    if not fornecedores:
        print("\nNenhum fornecedor cadastrado.")
        return
    print(f"\n{len(fornecedores)} fornecedor(es) cadastrado(s):")
    for fornecedor in fornecedores:
        print(f"  {fornecedor}")


def listar_movimentacoes(estoque: Estoque):
    if not estoque.movimentacoes:
        print("\nNenhuma movimentação registrada.")
        return
    print(f"\n{len(estoque.movimentacoes)} movimentação(ões):")
    for mov in estoque.movimentacoes:
        print(f"  {mov}")


def executar():
    estoque = Estoque.carregar(CAMINHO_DADOS)
    relatorio = Relatorio(estoque)

    acoes = {
        "1": lambda: cadastrar_produto(estoque),
        "2": lambda: listar_produtos(estoque),
        "3": lambda: registrar_entrada(estoque),
        "4": lambda: registrar_saida(estoque),
        "5": lambda: buscar_produto(estoque),
        "6": lambda: remover_produto(estoque),
        "7": lambda: cadastrar_fornecedor(estoque),
        "8": lambda: listar_fornecedores(estoque),
        "9": lambda: print("\n" + relatorio.texto_produtos_em_falta()),
        "10": lambda: print("\n" + relatorio.texto_proximos_vencimento()),
        "11": lambda: print("\n" + relatorio.texto_valor_total()),
        "12": lambda: print(f"\nGráfico salvo em: {relatorio.gerar_grafico_estoque_atual()}"),
        "13": lambda: print(f"\nGráfico salvo em: {relatorio.gerar_grafico_movimentacoes()}"),
        "14": lambda: listar_movimentacoes(estoque),
    }

    while True:
        print(MENU)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            estoque.salvar(CAMINHO_DADOS)
            print("Dados salvos. Até logo!")
            break

        acao = acoes.get(opcao)
        if acao is None:
            print("Opção inválida.")
            continue

        try:
            acao()
        except EstoqueError as erro:
            print(f"\n[ERRO] {erro}")
        except ValueError as erro:
            print(f"\n[ERRO] {erro}")


if __name__ == "__main__":
    executar()