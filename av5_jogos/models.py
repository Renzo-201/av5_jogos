from typing import List
from sqlalchemy import String, Text, Float, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    descricao: Mapped[str] = mapped_column(Text)
    publico_alvo: Mapped[str] = mapped_column(String(50))

    jogos: Mapped[List["Jogo"]] = relationship(
        back_populates="categoria",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Categoria {self.nome}>"

class Jogo(Base):
    __tablename__ = "jogos"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150))
    desenvolvedora: Mapped[str] = mapped_column(String(100))
    ano_lancamento: Mapped[int] = mapped_column(Integer)
    preco: Mapped[float] = mapped_column(Float)

    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    categoria: Mapped["Categoria"] = relationship(back_populates="jogos")

    def __repr__(self):
        return f"<Jogo {self.titulo}>"
