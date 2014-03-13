from io import BytesIO
from freezegun import freeze_time
import boto
from boto.s3.key import Key
from boto.exception import S3ResponseError
from moto import mock_s3
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.contrib.auth.models import User
from administradora.views import LandingView


class TestPaginaInicio(TestCase):

    def test_landing_template_view(self):
        self.factory = RequestFactory()
        request = self.factory.get('/')
        response = LandingView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_gets_redirected(self):
        response = self.client.get('/home/', follow=False)
        self.assertEqual(response.status_code, 302)

    def test_login_form(self):
        appuser = Client()
        self.username = 'username'
        self.email = 'user@example.com'
        self.password = 'password'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)
        userlogin = appuser.login(username=self.username, password=self.password)
        self.assertEqual(userlogin, True)

    def test_login_returns_correct_template(self):
        client = Client()
        response = client.post('/login/', {'username': 'username', 'password': 'password'})
        self.assertEqual(response.status_code, 200)

    @mock_s3
    def test_s3_returns_configuration_error(self):
        #se detecta cuando S3 regresa error por config
        conn = boto.connect_s3('some_key', 'my_secret')
        conn.get_bucket('somebucket')
        self.assertRaises(S3ResponseError)
        #not implemented?

    @mock_s3
    def test_s3_returns_file_error(self):
        #se detecta cuando S3 regresa error por archivo
        #boto.s3.key.set_contents_from_filename method calculate md5 checksums automatically
        pass

    @mock_s3
    def test_inventory_not_valid(self):
        #se rechazan inventarios que no cumplen el formato de la PNDA
        pass

    @mock_s3
    def test_inventory_upload_to_s3(self):
        #se puede cargar inventario a S3
        conn = boto.connect_s3('some_key', 'my_secret')
        bucket = conn.create_bucket("somebucket")
        multipart = bucket.initiate_multipart_upload("some-key")
        firstpart = '0' * 5242880
        multipart.upload_part_from_file(BytesIO(firstpart), 1)
        lastpart = '1'
        multipart.upload_part_from_file(BytesIO(lastpart), 2)
        multipart.complete_upload()
        uploaded = bucket.get_key("some-key").get_contents_as_string()
        self.assertEqual(firstpart + lastpart, uploaded)

    @mock_s3
    def test_inventory_can_be_read(self):
        #se puede leer el contenido del inventario
        pass

    @mock_s3
    def test_data_admin_can_have_more_than_one_inventory(self):
        #un usuario puede tener mas de un inventario
        pass

    @freeze_time("2014-03-11 12:00:00")
    @mock_s3
    def test_last_inventory_can_be_accessed(self):
        #se puede accesar el ultimo inventario
        conn = boto.connect_s3()
        bucket = conn.create_bucket("somebucket")
        key = Key(bucket)
        key.key = "some-key"
        key.set_contents_from_string("some content")
        rs = bucket.get_all_keys()
        self.assertEqual(rs[0].last_modified, '2014-03-11T12:00:00Z')
        self.assertEqual(bucket.get_key("some-key").last_modified, 'Tue, 11 Mar 2014 12:00:00 GMT')
