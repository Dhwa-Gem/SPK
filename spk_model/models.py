from sqlalchemy import Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Kamera(Base):
    __tablename__ = 'kamera'
    id_kamera: Mapped[str] = mapped_column(primary_key=True)
    harga: Mapped[int] = mapped_column()
    resolusi_sensor: Mapped[int] = mapped_column()
    rentang_iso: Mapped[int] = mapped_column()
    kecepatan_rana: Mapped[int] = mapped_column()
    jumlah_fStop: Mapped[float] = mapped_column(type_=Float)  
    
    def __repr__(self) -> str:
        return f"Kamera(id_kamera={self.id_kamera!r}, harga={self.harga!r})"