"""empty message

Revision ID: 5b6605d2daf6
Revises: 
Create Date: 2021-10-26 14:33:02.162394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b6605d2daf6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('establishments',
    sa.Column('id_establishment', sa.Integer(), nullable=False),
    sa.Column('social_reason', sa.String(length=200), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('cnpj', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id_establishment'),
    sa.UniqueConstraint('cnpj')
    )
    op.create_table('flasksqlalchemy-tutorial-users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_flasksqlalchemy-tutorial-users_email'), 'flasksqlalchemy-tutorial-users', ['email'], unique=True)
    op.create_table('parking_spaces',
    sa.Column('id_parking_space', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('floor', sa.String(length=10), nullable=False),
    sa.Column('localization', sa.String(length=200), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('desc', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id_parking_space')
    )
    op.create_table('payment_method',
    sa.Column('id_payment_method', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('desc', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id_payment_method')
    )
    op.create_table('person',
    sa.Column('id_person', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('sexo', sa.String(length=30), nullable=False),
    sa.Column('cpf', sa.String(length=50), nullable=False),
    sa.Column('rg', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id_person'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('rg')
    )
    op.create_table('sensors_types',
    sa.Column('id_sensor_type', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('desc', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id_sensor_type')
    )
    op.create_table('service_category',
    sa.Column('id_service_category', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('desc', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id_service_category')
    )
    op.create_table('states',
    sa.Column('id_state', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('initials', sa.String(length=10), nullable=False),
    sa.Column('desc', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id_state')
    )
    op.create_table('vehicle_category',
    sa.Column('id_vehicle_category', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('desc', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id_vehicle_category'),
    sa.UniqueConstraint('name')
    )
    op.create_table('vehicles_brands',
    sa.Column('id_vehicle_brand', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('desc', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id_vehicle_brand'),
    sa.UniqueConstraint('name')
    )
    op.create_table('cities',
    sa.Column('id_city', sa.Integer(), nullable=False),
    sa.Column('fk_state', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('desc', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['fk_state'], ['states.id_state'], ),
    sa.PrimaryKeyConstraint('id_city')
    )
    op.create_table('sensors',
    sa.Column('id_sensor', sa.Integer(), nullable=False),
    sa.Column('fk_sensor_type', sa.Integer(), nullable=True),
    sa.Column('fk_parking_space', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('modelo', sa.String(length=200), nullable=False),
    sa.Column('observacoes', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['fk_parking_space'], ['parking_spaces.id_parking_space'], ),
    sa.ForeignKeyConstraint(['fk_sensor_type'], ['sensors_types.id_sensor_type'], ),
    sa.PrimaryKeyConstraint('id_sensor')
    )
    op.create_table('services',
    sa.Column('id_service', sa.Integer(), nullable=False),
    sa.Column('fk_service_category', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('desc', sa.String(length=500), nullable=False),
    sa.Column('valor', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['fk_service_category'], ['service_category.id_service_category'], ),
    sa.PrimaryKeyConstraint('id_service')
    )
    op.create_table('telephones',
    sa.Column('id_telephone', sa.Integer(), nullable=False),
    sa.Column('fk_person', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('number', sa.String(length=30), nullable=False),
    sa.Column('desc', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['fk_person'], ['person.id_person'], ),
    sa.PrimaryKeyConstraint('id_telephone'),
    sa.UniqueConstraint('number')
    )
    op.create_table('users',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('fk_person', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('type', sa.String(length=30), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['fk_person'], ['person.id_person'], ),
    sa.PrimaryKeyConstraint('id_user'),
    sa.UniqueConstraint('email')
    )
    op.create_table('vehicle_models',
    sa.Column('id_modelo_vehicle', sa.Integer(), nullable=False),
    sa.Column('fk_vehicle_brand', sa.Integer(), nullable=True),
    sa.Column('fk_vehicle_category', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('desc', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['fk_vehicle_brand'], ['vehicles_brands.id_vehicle_brand'], ),
    sa.ForeignKeyConstraint(['fk_vehicle_category'], ['vehicle_category.id_vehicle_category'], ),
    sa.PrimaryKeyConstraint('id_modelo_vehicle')
    )
    op.create_table('addresses',
    sa.Column('id_address', sa.Integer(), nullable=False),
    sa.Column('fk_person', sa.Integer(), nullable=True),
    sa.Column('fk_city', sa.Integer(), nullable=True),
    sa.Column('public_place', sa.String(length=200), nullable=False),
    sa.Column('district', sa.String(length=100), nullable=False),
    sa.Column('number', sa.String(length=12), nullable=False),
    sa.Column('complement', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['fk_city'], ['cities.id_city'], ),
    sa.ForeignKeyConstraint(['fk_person'], ['person.id_person'], ),
    sa.PrimaryKeyConstraint('id_address')
    )
    op.create_table('owners',
    sa.Column('id_owner', sa.Integer(), nullable=False),
    sa.Column('fk_user', sa.Integer(), nullable=True),
    sa.Column('fk_establishment', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fk_establishment'], ['establishments.id_establishment'], ),
    sa.ForeignKeyConstraint(['fk_user'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_owner')
    )
    op.create_table('vehicles',
    sa.Column('id_vehicle', sa.Integer(), nullable=False),
    sa.Column('fk_user', sa.Integer(), nullable=True),
    sa.Column('fk_model', sa.Integer(), nullable=True),
    sa.Column('plate', sa.String(length=40), nullable=False),
    sa.Column('color', sa.String(length=50), nullable=False),
    sa.Column('renavam', sa.String(length=60), nullable=False),
    sa.Column('chassi', sa.String(length=60), nullable=False),
    sa.ForeignKeyConstraint(['fk_model'], ['vehicle_models.id_modelo_vehicle'], ),
    sa.ForeignKeyConstraint(['fk_user'], ['users.id_user'], ),
    sa.PrimaryKeyConstraint('id_vehicle'),
    sa.UniqueConstraint('chassi'),
    sa.UniqueConstraint('renavam')
    )
    op.create_table('rents',
    sa.Column('id_rent', sa.Integer(), nullable=False),
    sa.Column('fk_payment_method', sa.Integer(), nullable=True),
    sa.Column('fk_vehicle', sa.Integer(), nullable=True),
    sa.Column('fk_user', sa.Integer(), nullable=True),
    sa.Column('fk_parking_space', sa.Integer(), nullable=True),
    sa.Column('entry_time', sa.DateTime(), nullable=False),
    sa.Column('exit_time', sa.DateTime(), nullable=False),
    sa.Column('hourly_value', sa.Float(), nullable=False),
    sa.Column('desc', sa.String(length=400), nullable=False),
    sa.ForeignKeyConstraint(['fk_parking_space'], ['parking_spaces.id_parking_space'], ),
    sa.ForeignKeyConstraint(['fk_payment_method'], ['payment_method.id_payment_method'], ),
    sa.ForeignKeyConstraint(['fk_user'], ['users.id_user'], ),
    sa.ForeignKeyConstraint(['fk_vehicle'], ['vehicles.id_vehicle'], ),
    sa.PrimaryKeyConstraint('id_rent')
    )
    op.create_table('services_rental',
    sa.Column('id_service_rent', sa.Integer(), nullable=False),
    sa.Column('fk_rent', sa.Integer(), nullable=True),
    sa.Column('fk_service', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('desc', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['fk_rent'], ['rents.id_rent'], ),
    sa.ForeignKeyConstraint(['fk_service'], ['services.id_service'], ),
    sa.PrimaryKeyConstraint('id_service_rent')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services_rental')
    op.drop_table('rents')
    op.drop_table('vehicles')
    op.drop_table('owners')
    op.drop_table('addresses')
    op.drop_table('vehicle_models')
    op.drop_table('users')
    op.drop_table('telephones')
    op.drop_table('services')
    op.drop_table('sensors')
    op.drop_table('cities')
    op.drop_table('vehicles_brands')
    op.drop_table('vehicle_category')
    op.drop_table('states')
    op.drop_table('service_category')
    op.drop_table('sensors_types')
    op.drop_table('person')
    op.drop_table('payment_method')
    op.drop_table('parking_spaces')
    op.drop_index(op.f('ix_flasksqlalchemy-tutorial-users_email'), table_name='flasksqlalchemy-tutorial-users')
    op.drop_table('flasksqlalchemy-tutorial-users')
    op.drop_table('establishments')
    # ### end Alembic commands ###