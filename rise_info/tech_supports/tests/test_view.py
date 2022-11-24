#from django.test import TestCase
#from django.urls import resolve, reverse
#
#
#from addresses.views import addresses_new, addresses_edit, addresses_del
#from addresses.models import Addresses
#from addresses.tests.test_form import make_mock_right_param
#from accounts.tests.com_setup import login
#
#
# def addMockAddress(testCase) -> None:
#    testCase.client.force_login(testCase.user)
#    make_mock_right_param(testCase)
#    data = {
#        'name': testCase.params['name'],
#        'position': testCase.params['position'],
#        'mail': testCase.params['mail'],
#    }
#    testCase.response = testCase.client.post(
#        "/addresses/new/", data)
#
#
# class AddressesListTest(TestCase):
#    def setUp(self) -> None:
#        login(self)
#
#    def test_addresse_list_return_200_and_expected_title(self) -> None:
#        response = self.client.get("/addresses/")
#        self.assertContains(response, "配信先一覧", status_code=200)
#
#    def test_addresse_list_uses_expected_template(self) -> None:
#        response = self.client.get("/addresses/")
#        self.assertTemplateUsed(response, "addresses/address_list.html")
#
#
# class CreateAddressTest(TestCase):
#    def setUp(self) -> None:
#        login(self)
#
#    def test_render_creation_form(self):
#        response = self.client.get("/addresses/new/")
#        self.assertContains(response, "配信先の登録", status_code=200)
#
#    def test_create_info(self):
#        login(self)
#        addMockAddress(self)
#        address = Addresses.object.get_or_none(name=self.params['name'])
#        if address:
#            self.assertEqual(self.params['position'], address.position)
#        else:
#            self.assertEqual(Addresses.object.all().count(), 1)
#            self.fail('addressが空')
#
#
# def edit_common_setUp(testCase, isEdit: bool):
#    login(testCase)
#    addMockAddress(testCase)
#    address = Addresses.object.get_or_none(name=testCase.params['name'])
#    if address:
#        if isEdit:
#            testCase.response = testCase.client.get(
#                "/addresses/%s/edit/" % address.id)
#        else:
#            testCase.response = testCase.client.get(
#                "/addresses/%s/" % address.id)
#    else:
#        testCase.fail('あるはずのMockInfoが見つからない')
#
#
# class EditInfoTest(TestCase):
#    def setUp(self) -> None:
#        edit_common_setUp(self, True)
#
#    def test_should_use_expected_template(self):
#        self.assertTemplateUsed(
#            self.response, "addresses/address_edit_new.html")
#
#
# class EditInfoTest(TestCase):
#    def test_should_resolve_addresse_edit(self):
#        found = resolve("/addresses/1/edit/")
#        self.assertEqual(addresses_edit, found.func)
#
#
# class AddresseDelTest(TestCase):
#    def setUp(self) -> None:
#        login(self)
#        addMockAddress(self)
#
#    def test_addresse_del_count(self):
#        try:
#            address = Addresses.object.get_or_none(name=self.params['name'])
#        except:
#            self.fail('あるはずのmockAddressが見つからない')
#        response = self.client.get("/addresses/" + str(address.pk) + "/del/")
#        self.assertRedirects(response, reverse('address_list'), status_code=302,
#                             target_status_code=200, msg_prefix='', fetch_redirect_response=True)
#        try:
#            address = Addresses.object.get_or_none(name=self.params['name'])
#        except:
#            return None
#        if address:
#            self.fail('ないはずのmockAddressが見つかった')
#
