from ..models import Listing, Owner, Tenant, Collection, PropertyType, Image, Feature, CustomUser, CustomUserManager, TenantManager,OwnerManager
from django.test import TestCase
from django.contrib.auth.models import Group

class TestModels(TestCase):
    '''Test For Models'''

    def setUp(self):
        '''Creates object for each model'''
        self.Owner_group, self.Owner_created = Group.objects.get_or_create(name='Owner')
        self.Tenant_group, self.Tenant_created = Group.objects.get_or_create(name='Tenant')

        self.owner_test = Owner.objects.create_user(email='owner_test@email.com', username='owner_test', phone_number='+12345678900', password='password')
        self.tenant_test = Tenant.objects.create_user(email='tenant_test@email.com', username='tenant_test', phone_number='+12345678911', password='password')
        self.propertyType_test = PropertyType.objects.create(name='farm')
        self.feature_test = Feature.objects.create(name='wifi')
        self.listing = Listing.objects.create(title='Cow Farm', description='test test', location='country test', area=787, price_per_month=455, bedrooms=5, bathroom=2, owner=self.owner_test)
        self.collection = Collection.objects.create(name='likes', user=self.tenant_test)
        self.collection.listing.add(self.listing)


    def test_create_owner_gp(self):
        '''Test creation of Owner group'''
        self.assertEqual(self.Owner_group.name, 'Owner')
        self.assertTrue(isinstance(self.Owner_group, Group))

    def test_create_Tenant_gp(self):
        '''Test creation of Tenant group'''
        self.assertEqual(self.Tenant_group.name, 'Tenant')
        self.assertTrue(isinstance(self.Tenant_group, Group))

    def test_create_owner(self):
        '''Test creation of Owner user'''
        self.assertEqual(self.owner_test.email, 'owner_test@email.com')
        self.assertTrue(isinstance(self.owner_test, Owner))

    def test_create_tenant(self):
        '''Test creation of Tenant user'''
        self.assertEqual(self.tenant_test.email, 'tenant_test@email.com')
        self.assertTrue(isinstance(self.tenant_test, Tenant))

    def test_owner_in_owner_gp(self):
        '''Test owner user in Owner group'''
        self.assertTrue(self.owner_test.groups.filter(name=self.Owner_group))
        self.assertFalse(self.owner_test.groups.filter(name=self.Tenant_group))

    def test_owner_in_tenant_gp(self):
        '''Test tenant user in Tenant group'''
        self.assertTrue(self.tenant_test.groups.filter(name=self.Tenant_group))
        self.assertFalse(self.tenant_test.groups.filter(name=self.Owner_group))

    def test_create_listing(self):
        '''Test creation of listing'''
        self.assertEqual(self.listing.title, 'Cow Farm')
        self.assertTrue(isinstance(self.listing, Listing))

    def test_owner_listing(self):
        '''Test owner of listing'''
        self.assertEqual(self.listing.owner, self.owner_test)

    def test_create_collection(self):
        '''Test creation of collection'''
        self.assertEqual(self.collection.name, 'likes')

    def test_tenant_collection(self):
        '''Test tenant of collection'''
        self.assertEqual(self.collection.user, self.tenant_test)

    def test_listing_in_collection(self):
        '''Test if listing in collection'''
        collection_from_db = Collection.objects.get(pk=self.collection.pk)
        self.assertIn(self.listing, collection_from_db.listing.all())

    def test_model_property_type(self):
        '''Test creation of property type'''
        self.assertEqual(self.propertyType_test.name, 'farm')


    def test_model_feature(self):
        '''Test creation of property type'''
        self.assertEqual(self.feature_test.name, 'wifi')

    def test_add_property_type_to_listing(self):
        '''Checks property type of a listing'''

        # Add property type to the listing
        self.listing.property_type.add(self.propertyType_test)
        self.assertIn(self.propertyType_test, self.listing.property_type.all())

    def test_add_feature_to_listing(self):
        '''Checks feature of a listing'''

        # Add feature to the listing
        self.listing.feature.add(self.feature_test)
        self.assertIn(self.feature_test, self.listing.feature.all())
    

class TestCustomModels(TestCase):
    '''Test cases for custom and manager models'''
    def setUp(self) -> None:
        '''Creates object for each model'''
        self.Owner_group, self.Owner_created = Group.objects.get_or_create(name='Owner')
        self.Tenant_group, self.Tenant_created = Group.objects.get_or_create(name='Tenant')

        self.owner_test = Owner.objects.create_user(email='owner_test@email.com', username='owner_test', phone_number='+12345678900', password='password')
        self.tenant_test = Tenant.objects.create_user(email='tenant_test@email.com', username='tenant_test', phone_number='+12345678911', password='password')

        self.custom_user_manager = CustomUserManager()
        self.owner_manager = OwnerManager()
        self.tenant_manager =  TenantManager()


    def test_create_custom_user(self):
        '''Test creation of custom user'''

        with self.assertRaises(ValueError):
            self.custom_user_manager.create_user(email='', username='test', password='password')

        # TODO:Fix
        # def test_create_custom_superuser(self):
        #   with self.assertRaises(ValueError):
        #     self.custom_user_manager.create_superuser(email='admin@email.com', password='password', is_superuse=True, is_staff=True)
        
    def test_create_superuser_with_invalid_is_staff(self):
        ''' Test create_superuser method with invalid is_staff value '''
        with self.assertRaises(ValueError):
            self.custom_user_manager.create_superuser(email='admin@example.com', password='password', is_staff=False, is_superuser=True)

    def test_create_superuser_with_invalid_is_superuser(self):
        '''Test create_superuser method with invalid is_superuser value'''
        with self.assertRaises(ValueError):
            self.custom_user_manager.create_superuser(email='admin@example.com', password='password', is_staff=True, is_superuser=False)

    def test_owner_manager(self):
        '''Test owner manager is working properly'''
        queryset = Owner.objects.get_queryset()

        # Check if the test tenant is present in the queryset
        self.assertIn(self.owner_test, queryset)

        # check each user in the queryset belongs to the Tenant group
        for user in queryset:
            self.assertTrue(user.groups.filter(name=self.Owner_group.name).exists())

    def test_tenant_manager(self):
        '''Test tenant manager is working properly'''
        queryset = Tenant.objects.get_queryset()

        # Check if the test tenant is present in the queryset
        self.assertIn(self.tenant_test, queryset)
        
        # check each user in the queryset belongs to the Tenant group
        for user in queryset:
            self.assertTrue(user.groups.filter(name=self.Tenant_group.name).exists())