from sqlalchemy.orm import Session
from database import engine
from models import Categoria, Jogo

def cadastrar_categoria(session: Session):
    print("\n--- CADASTRO DE CATEGORIA (ABA) ---")
    nome = input("Nome da Categoria/Aba (ex: Ação): ").strip()
    desc = input("Descrição da Categoria: ").strip()
    publico = input("Público-Alvo (ex: Livre, +16): ").strip()

    nova_cat = Categoria(nome=nome, descricao=desc, publico_alvo=publico)
    session.add(nova_cat)
    session.commit()
    print(f"✔️ Categoria '{nome}' cadastrada com sucesso!")

def cadastrar_jogo(session: Session):
    print("\n--- CADASTRO DE JOGO ---")
    categorias = session.query(Categoria).all()
    if not categorias:
        print("❌ Nenhuma categoria cadastrada. Cadastre uma Categoria primeiro!")
        return

    print("\nCategorias/Abas Disponíveis:")
    for c in categorias:
        print(f"  [{c.id}] {c.nome}")

    try:
        cat_id = int(input("\nDigite o ID da Categoria para o jogo: "))
        cat_existe = session.get(Categoria, cat_id)
        if not cat_existe:
            print("❌ ID de Categoria inválido.")
            return

        titulo = input("Título do Jogo: ").strip()
        dev = input("Desenvolvedora: ").strip()
        ano = int(input("Ano de Lançamento: "))
        preco = float(input("Preço (R$): "))

        novo_jogo = Jogo(
            titulo=titulo,
            desenvolvedora=dev,
            ano_lancamento=ano,
            preco=preco,
            categoria_id=cat_id
        )
        session.add(novo_jogo)
        session.commit()
        print(f"✔️ Jogo '{titulo}' cadastrado com sucesso!")
    except ValueError:
        print("❌ Entrada inválida. Digite números para ID, Ano e Preço.")

def listar_tudo(session: Session):
    print("\n==========================================")
    print("   BIBLIOTECA DE JOGOS - LISTAGEM GERAL")
    print("==========================================")
    categorias = session.query(Categoria).all()

    if not categorias:
        print("Nenhum dado cadastrado até o momento.")
        return

    for cat in categorias:
        print(f"\n📂 ABA / CATEGORIA: [{cat.id}] {cat.nome} (Público: {cat.publico_alvo})")
        print(f"   Descrição: {cat.descricao}")
        if not cat.jogos:
            print("   (Nenhum jogo nesta aba)")
        else:
            for j in cat.jogos:
                print(f"   └─ 🎮 [{j.id}] {j.titulo} | Dev: {j.desenvolvedora} ({j.ano_lancamento}) - R$ {j.preco:.2f}")

def excluir_jogo(session: Session):
    print("\n--- EXCLUSÃO DE JOGO ---")
    try:
        jogo_id = int(input("Digite o ID do jogo a ser excluído: "))
        jogo = session.get(Jogo, jogo_id)
        if jogo:
            session.delete(jogo)
            session.commit()
            print(f"✔️ Jogo '{jogo.titulo}' excluído com sucesso!")
        else:
            print("❌ Jogo não encontrado.")
    except ValueError:
        print("❌ Digite um número válido para o ID.")

def excluir_categoria(session: Session):
    print("\n--- EXCLUSÃO DE CATEGORIA (ABA) ---")
    try:
        cat_id = int(input("Digite o ID da categoria a ser excluída: "))
        cat = session.get(Categoria, cat_id)
        if cat:
            session.delete(cat)
            session.commit()
            print(f"✔️ Categoria '{cat.nome}' e seus jogos foram excluídos!")
        else:
            print("❌ Categoria não encontrada.")
    except ValueError:
        print("❌ Digite um número válido para o ID.")

def menu_principal():
    with Session(engine) as session:
        while True:
            print("\n" + "="*40)
            print("      SISTEMA DE BIBLIOTECA DE JOGOS")
            print("="*40)
            print("1 - Cadastrar Categoria (Aba)")
            print("2 - Cadastrar Jogo")
            print("3 - Listar Categorias e Jogos")
            print("4 - Excluir Jogo")
            print("5 - Excluir Categoria")
            print("0 - Sair")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                cadastrar_categoria(session)
            elif opcao == "2":
                cadastrar_jogo(session)
            elif opcao == "3":
                listar_tudo(session)
            elif opcao == "4":
                excluir_jogo(session)
            elif opcao == "5":
                excluir_categoria(session)
            elif opcao == "0":
                print("\nEncerrando o sistema...")
                break
            else:
                print("❌ Opção inválida.")

if __name__ == "__main__":
    menu_principal()

    