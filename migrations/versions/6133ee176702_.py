"""empty message

Revision ID: 6133ee176702
Revises: 
Create Date: 2018-06-26 00:31:11.372946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6133ee176702'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('book_logs',
    sa.Column('log_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('action', sa.String(length=30), nullable=False),
    sa.Column('success', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('log_id')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_code', sa.BIGINT(), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=True),
    sa.Column('ddc_code', sa.String(length=30), nullable=True),
    sa.Column('author', sa.String(length=50), nullable=True),
    sa.Column('synopsis', sa.Text(), nullable=True),
    sa.Column('genre', sa.Enum('Fiction', 'Non_fiction', name='genre'), nullable=True),
    sa.Column('sub_genre', sa.String(length=70), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('book_code')
    )
    op.create_table('user_logs',
    sa.Column('log_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('action', sa.String(length=30), nullable=False),
    sa.Column('success', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('log_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('acc_status', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('borrowed_books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('borrow_date', sa.DateTime(), nullable=False),
    sa.Column('return_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=40), nullable=True),
    sa.Column('fee_owed', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrowed_books')
    op.drop_table('users')
    op.drop_table('user_logs')
    op.drop_table('books')
    op.drop_table('book_logs')
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###
