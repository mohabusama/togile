from tastypie.test import ResourceTestCase


class TodoListResourceTest(ResourceTestCase):

    fixtures = [
        'todo_users.json',
        'todo_lists_items.json'
    ]

    DEFAULT_USER_ID = 1
    DEFAULT_USER = 'user_1'
    DEFAULT_PASSWORD = 'user_1'

    LIST_URL = '/api/v1/users/%s/lists/'
    DETAIL_URL = '/api/v1/users/%s/lists/%s/'

    @property
    def list_url(self):
        return self.LIST_URL % (self.user_id)

    @property
    def detail_url(self):
        return self.DETAIL_URL % (self.user_id, self.list_id)

    def _login(self, username=DEFAULT_USER, password=DEFAULT_PASSWORD):
        self.api_client.client.login(username=username, password=password)

    def setUp(self):
        super(TodoListResourceTest, self).setUp()
        self.user_id = self.DEFAULT_USER_ID
        self.list_id = 1

    ###########################################################################
    # METHOD NOT ALLOWED
    ###########################################################################
    def test_put_list_not_allowed(self):
        response = self.api_client.put(self.list_url)
        self.assertHttpMethodNotAllowed(response)

    def test_delete_list_not_allowed(self):
        response = self.api_client.delete(self.list_url)
        self.assertHttpMethodNotAllowed(response)

    def test_post_detail_not_allowed(self):
        response = self.api_client.post(self.detail_url)
        self.assertHttpMethodNotAllowed(response)

    ###########################################################################
    # GET
    ###########################################################################
    def test_get_list_unauthorized(self):
        response = self.api_client.get(self.list_url)
        self.assertHttpUnauthorized(response)

    def test_get_list_other_user_unauthorized(self):
        self._login(username='user_2', password='user_2')
        response = self.api_client.get(self.list_url)
        self.assertHttpUnauthorized(response)

    def test_get_detail_other_user_unauthorized(self):
        self._login(username='user_2', password='user_2')
        response = self.api_client.get(self.detail_url)
        self.assertHttpUnauthorized(response)

    def test_get_list(self):
        # User: 'user 1'
        self._login()

        response = self.api_client.get(self.list_url)
        self.assertHttpOK(response)
        self.assertValidJSONResponse(response)

        # todo_list = self.deserialize(response)
        # self.assertEqual(len(todo_list['objects']), 2)

    def test_get_detail(self):
        # User: 'user 1'
        # List: 1
        self._login()

        response = self.api_client.get(self.detail_url)
        self.assertHttpOK(response)
        self.assertValidJSONResponse(response)

        todo_list = self.deserialize(response)
        self.assertEqual(todo_list['id'], 1)


class TodoItemResourceTest(ResourceTestCase):

    DEFAULT_USER = 'user_1'
    DEFAULT_PASSWORD = 'user_1'

    def _login(self, username=DEFAULT_USER, password=DEFAULT_PASSWORD):
        self.api_client.client.login(username=username, password=password)

    def setUp(self):
        pass

    def tearDown(self):
        pass
