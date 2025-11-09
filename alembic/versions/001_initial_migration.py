"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('birth_date', sa.DateTime(), nullable=True),
        sa.Column('gender', sa.Integer(), nullable=False),
        sa.Column('avatar_link', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create genres table
    op.create_table(
        'genres',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )
    op.create_index('ix_genres_name', 'genres', ['name'], unique=True)

    # Create movies table
    op.create_table(
        'movies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('poster', sa.String(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('time', sa.Integer(), nullable=False),
        sa.Column('tagline', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('director', sa.String(), nullable=True),
        sa.Column('budget', sa.Integer(), nullable=True),
        sa.Column('fees', sa.Integer(), nullable=True),
        sa.Column('age_limit', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Create movie_genres table
    op.create_table(
        'movie_genres',
        sa.Column('movie_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('genre_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint('movie_id', 'genre_id')
    )
    op.create_foreign_key('fk_movie_genres_movie_id', 'movie_genres', 'movies', ['movie_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_movie_genres_genre_id', 'movie_genres', 'genres', ['genre_id'], ['id'], ondelete='CASCADE')

    # Create reviews table
    op.create_table(
        'reviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('movie_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('review_text', sa.Text(), nullable=False),
        sa.Column('is_anonymous', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_foreign_key('fk_reviews_movie_id', 'reviews', 'movies', ['movie_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_reviews_user_id', 'reviews', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # Create favorite_movies table
    op.create_table(
        'favorite_movies',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('movie_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('user_id', 'movie_id')
    )
    op.create_foreign_key('fk_favorite_movies_user_id', 'favorite_movies', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_favorite_movies_movie_id', 'favorite_movies', 'movies', ['movie_id'], ['id'], ondelete='CASCADE')

    # Create refresh_tokens table
    op.create_table(
        'refresh_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_foreign_key('fk_refresh_tokens_user_id', 'refresh_tokens', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_index('ix_refresh_tokens_token', 'refresh_tokens', ['token'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_refresh_tokens_token', table_name='refresh_tokens')
    op.drop_table('refresh_tokens')
    op.drop_table('favorite_movies')
    op.drop_table('reviews')
    op.drop_table('movie_genres')
    op.drop_table('movies')
    op.drop_index('ix_genres_name', table_name='genres')
    op.drop_table('genres')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')

