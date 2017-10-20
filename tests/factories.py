from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from labsys.extensions import db
from labsys.inventory.models import Product


class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class ProductFactory(BaseFactory):

    class Meta:
        model = Product
        abstract = False

    '''
    These are keywords args passed to class' __init__ method
    Any of these can be overriden
    product = ProductFactory(name='myname')
    '''
    #id = Sequence(lambda n: n)
    name = Sequence(lambda n: 'product-{}'.format(n))
    manufacturer = 'manufacturer'#Sequence(lambda n: 'manufacturer-{}'.format(n))
    catalog = Sequence(lambda n: 'catalog-{}'.format(n))
    stock_unit = 1
    min_stock = 2
    parent_id = None
    subproduct = None
    '''
    For more complex situations:
    @factory.sequence
    def username(n):
        return 'user%d' % n
    '''

    '''
    For functions that do not depend on the object being built, 
    use LazyFunction
    
    timestamp = factory.LazyFunction(datetime.now)
    this function can also be overriden
    There is also @lazy_attribute() decorator available
    '''



'''
Params example (non-model fields)

class RentalFactory(factory.Factory):
    class Meta:
        model = Rental

    begin = factory.fuzzy.FuzzyDate(start_date=datetime.date(2000, 1, 1))
    end = factory.LazyAttribute(lambda o: o.begin + o.duration)

    class Params:
        duration = 12
        
Traits: used to update fields
class OrderFactory(factory.Factory):
    status = 'pending'
    shipped_by = None
    shipped_on = None

    class Meta:
        model = Order

    class Params:
        shipped = factory.Trait(
            status='shipped',
            shipped_by=factory.SubFactory(EmployeeFactory),
            shipped_on=factory.LazyFunction(datetime.date.today),
        )
'''

''' 
Create x Build
Create: saves object to database
Build: provides a local object (unsaved)
MyFactory() == MyFactory.create()
'''

