"""Seed script for populating the database with test data."""
import uuid
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.genre import Genre
from app.models.movie import Movie, MovieGenre
from app.core.security import get_password_hash


def create_genres(db: Session):
    """Create genres."""
    genres = [
        "Драма",
        "Комедия",
        "Боевик",
        "Триллер",
        "Ужасы",
        "Фантастика",
        "Мелодрама",
        "Приключения",
        "Детектив",
        "Фэнтези",
    ]
    
    genre_objects = []
    for genre_name in genres:
        existing = db.query(Genre).filter(Genre.name == genre_name).first()
        if not existing:
            genre_obj = Genre(name=genre_name)
            db.add(genre_obj)
            genre_objects.append(genre_obj)
        else:
            genre_objects.append(existing)
    
    db.commit()
    return genre_objects


def create_movies(db: Session, genres: list):
    """Create sample movies."""
    movies_data = [
        {
            "name": "Побег из Шоушенка",
            "poster": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg",
            "year": 1994,
            "country": "США",
            "time": 142,
            "tagline": "Страх - это кандалы. Надежда - это свобода",
            "description": "История банкира Энди Дюфрейна, обвиненного в убийстве своей жены и ее любовника.",
            "director": "Фрэнк Дарабонт",
            "budget": 25000000,
            "fees": 73300000,
            "age_limit": 16,
            "genre_names": ["Драма"],
        },
        {
            "name": "Зеленая миля",
            "poster": "https://m.media-amazon.com/images/M/MV5BMTUxMzQyNjA5MF5BMl5BanBnXkFtZTYwOTU2NTY3._V1_.jpg",
            "year": 1999,
            "country": "США",
            "time": 189,
            "tagline": "Чудеса случаются в самых неожиданных местах",
            "description": "Пол Эджкомб - начальник блока смертников в тюрьме «Холодная гора».",
            "director": "Фрэнк Дарабонт",
            "budget": 60000000,
            "fees": 286801374,
            "age_limit": 16,
            "genre_names": ["Драма", "Фантастика"],
        },
        {
            "name": "Форрест Гамп",
            "poster": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
            "year": 1994,
            "country": "США",
            "time": 142,
            "tagline": "Мир уже никогда не будет прежним",
            "description": "История жизни Форреста Гампа, простого человека с IQ 75.",
            "director": "Роберт Земекис",
            "budget": 55000000,
            "fees": 678226465,
            "age_limit": 12,
            "genre_names": ["Драма", "Мелодрама"],
        },
        {
            "name": "Начало",
            "poster": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
            "year": 2010,
            "country": "США",
            "time": 148,
            "tagline": "Твой разум - место преступления",
            "description": "Кобб - талантливый вор, лучший из лучших в опасном искусстве извлечения.",
            "director": "Кристофер Нолан",
            "budget": 160000000,
            "fees": 836836967,
            "age_limit": 12,
            "genre_names": ["Фантастика", "Боевик", "Триллер"],
        },
        {
            "name": "Интерстеллар",
            "poster": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
            "year": 2014,
            "country": "США",
            "time": 169,
            "tagline": "Следующий шаг человечества будет величайшим",
            "description": "Когда засуха приводит человечество к продовольственному кризису, команда исследователей отправляется через червоточину в поисках нового дома.",
            "director": "Кристофер Нолан",
            "budget": 165000000,
            "fees": 701729206,
            "age_limit": 12,
            "genre_names": ["Фантастика", "Драма", "Приключения"],
        },
        {
            "name": "Матрица",
            "poster": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",
            "year": 1999,
            "country": "США",
            "time": 136,
            "tagline": "Добро пожаловать в реальный мир",
            "description": "Хакер Нео узнает, что мир, в котором он живет - это иллюзия, созданная машинами.",
            "director": "Вачовски",
            "budget": 63000000,
            "fees": 466364845,
            "age_limit": 16,
            "genre_names": ["Фантастика", "Боевик"],
        },
        {
            "name": "Бойцовский клуб",
            "poster": "https://m.media-amazon.com/images/M/MV5BNDIzNDU0YzEtYzE5Ni00ZjlkLTk5ZjgtNjM3NWE4YzA3Nzk3XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_.jpg",
            "year": 1999,
            "country": "США",
            "time": 139,
            "tagline": "Разрушая себя, ты разрушаешь мир",
            "description": "Офисный работник и мыловар создают подпольную организацию.",
            "director": "Дэвид Финчер",
            "budget": 63000000,
            "fees": 101209702,
            "age_limit": 18,
            "genre_names": ["Триллер", "Драма"],
        },
        {
            "name": "Престиж",
            "poster": "https://m.media-amazon.com/images/M/MV5BMjA4NDI0MTIxNF5BMl5BanBnXkFtZTYwNTM0MzY2._V1_.jpg",
            "year": 2006,
            "country": "США",
            "time": 130,
            "tagline": "Ты наблюдаешь или видишь?",
            "description": "Роберт и Альфред - фокусники-соперники. Их конкуренция превращается в навязчивую идею.",
            "director": "Кристофер Нолан",
            "budget": 40000000,
            "fees": 109676311,
            "age_limit": 12,
            "genre_names": ["Триллер", "Драма", "Детектив"],
        },
    ]
    
    # Create genre mapping
    genre_map = {genre.name: genre for genre in genres}
    
    for movie_data in movies_data:
        existing = db.query(Movie).filter(Movie.name == movie_data["name"]).first()
        if existing:
            continue
        
        genre_names = movie_data.pop("genre_names")
        movie = Movie(**movie_data)
        db.add(movie)
        db.flush()  # Get movie ID
        
        # Add genres
        for genre_name in genre_names:
            if genre_name in genre_map:
                movie_genre = MovieGenre(
                    movie_id=movie.id,
                    genre_id=genre_map[genre_name].id
                )
                db.add(movie_genre)
    
    db.commit()
    print("✓ Movies created successfully")


def seed_database():
    """Main seed function."""
    print("Starting database seeding...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Create genres
        print("Creating genres...")
        genres = create_genres(db)
        print(f"✓ Created {len(genres)} genres")
        
        # Create movies
        print("Creating movies...")
        create_movies(db, genres)
        
        print("\n✅ Database seeding completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

