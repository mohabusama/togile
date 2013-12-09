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
        """
        User: 'user 1'
        """
        self._login()

        response = self.api_client.get(self.list_url)
        self.assertHttpOK(response)
        self.assertValidJSONResponse(response)

        todo_list = self.deserialize(response)
        self.assertEqual(len(todo_list['objects']), 2)

    def test_get_detail(self):
        """
        User: 'user 1'
        List: 1
        """
        self._login()

        response = self.api_client.get(self.detail_url)
        self.assertHttpOK(response)
        self.assertValidJSONResponse(response)

        todo_list = self.deserialize(response)
        self.assertEqual(todo_list['resource_uri'], self.detail_url)

    ###########################################################################
    # POST
    ###########################################################################
    def test_post_list_unauthorized(self):
        response = self.api_client.post(self.list_url)
        self.assertHttpUnauthorized(response)

    def test_post_list_other_user_unauthorized(self):
        self._login(username='user_2', password='user_2')

        data = {
            'title': 'New Todo List'
        }

        response = self.api_client.post(self.list_url, data=data)
        self.assertHttpUnauthorized(response)

    def test_post_list(self):
        """
        User: 'user 1'
        """
        self._login()

        data = {
            'title': 'New Todo List'
        }

        response = self.api_client.post(self.list_url, data=data)
        self.assertHttpCreated(response)

        todo_list = self.deserialize(response)
        self.assertEqual(todo_list['title'], data['title'])
        self.assertEqual(todo_list['parent_id'], None)

        self.assertIn('resource_uri', todo_list)

        # Now get the list using the reource_uri
        response = self.api_client.get(todo_list['resource_uri'])
        self.assertHttpOK(response)

    def test_post_list_with_parent(self):
        """
        User: 'user 1'
        """
        self._login()

        data = {
            'title': 'New Todo List',
            'parent_id': 1
        }

        response = self.api_client.post(self.list_url, data=data)
        self.assertHttpCreated(response)

        todo_list = self.deserialize(response)
        self.assertEqual(todo_list['title'], data['title'])
        self.assertEqual(todo_list['parent_id'], data['parent_id'])

        self.assertIn('resource_uri', todo_list)

        # Now get the list using the reource_uri
        response = self.api_client.get(todo_list['resource_uri'])
        self.assertHttpOK(response)

    ###########################################################################
    # PUT
    ###########################################################################
    def test_put_detail_unauthorized(self):
        response = self.api_client.put(self.detail_url)
        self.assertHttpUnauthorized(response)

    def test_put_detail_other_user_unauthorized(self):
        self._login(username='user_2', password='user_2')

        data = {
            'title': 'Invalid'
        }

        response = self.api_client.put(self.detail_url, data=data)
        self.assertHttpUnauthorized(response)

    def test_put_detail(self):
        """
        User: 'user 1'
        """
        self._login()

        data = {
            'title': 'Updated Title'
        }

        response = self.api_client.put(self.detail_url, data=data)
        self.assertHttpOK(response)

        todo_list = self.deserialize(response)
        self.assertEqual(todo_list['title'], data['title'])

        self.assertIn('resource_uri', todo_list)

        # Now get the list using the reource_uri
        response = self.api_client.get(todo_list['resource_uri'])
        self.assertHttpOK(response)
        todo_list = self.deserialize(response)
        self.assertEqual(todo_list['title'], data['title'])

    ###########################################################################
    # DELETE
    ###########################################################################
    def test_delete_detail_unauthorized(self):
        response = self.api_client.delete(self.detail_url)
        self.assertHttpUnauthorized(response)

    def test_delete_detail_other_user_unauthorized(self):
        self._login(username='user_2', password='user_2')

        response = self.api_client.delete(self.detail_url)
        self.assertHttpUnauthorized(response)

    def test_delete_detail(self):
        """
        User: 'user 1'
        """
        self._login()

        response = self.api_client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)


class TodoItemResourceTest(ResourceTestCase):

    fixtures = [
        'todo_users.json',
        'todo_lists_items.json'
    ]

    DEFAULT_USER_ID = 1
    DEFAULT_USER = 'user_1'
    DEFAULT_PASSWORD = 'user_1'

    LIST_URL = '/api/v1/users/%s/lists/%s/todos/'
    DETAIL_URL = '/api/v1/users/%s/lists/%s/todos/%s/'

    @property
    def list_url(self):
        return self.LIST_URL % (self.user_id, self.list_id)

    @property
    def detail_url(self):
        return self.DETAIL_URL % (self.user_id, self.list_id, self.todo_id)

    def _login(self, username=DEFAULT_USER, password=DEFAULT_PASSWORD):
        self.api_client.client.login(username=username, password=password)

    def setUp(self):
        super(TodoItemResourceTest, self).setUp()
        self.user_id = self.DEFAULT_USER_ID
        self.list_id = 1
        self.todo_id = 1

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
        """
        User: 'user 1'
        """
        self._login()

        response = self.api_client.get(self.list_url)
        self.assertHttpOK(response)
        self.assertValidJSONResponse(response)

        todo_items = self.deserialize(response)
        self.assertEqual(len(todo_items['objects']), 2)

    def test_get_detail(self):
        """
        User: 'user 1'
        List: 1
        Item: 1
        """
        self._login()

        response = self.api_client.get(self.detail_url)
        self.assertHttpOK(response)
        self.assertValidJSONResponse(response)

        todo_item = self.deserialize(response)
        self.assertEqual(todo_item['resource_uri'], self.detail_url)

    ###########################################################################
    # POST
    ###########################################################################
    def test_post_list_unauthorized(self):
        response = self.api_client.post(self.list_url)
        self.assertHttpUnauthorized(response)

    def test_post_list_other_user_unauthorized(self):
        self._login(username='user_2', password='user_2')

        data = {
            'value': 'New Todo Item!'
        }

        response = self.api_client.post(self.list_url, data=data)
        self.assertHttpUnauthorized(response)

    def test_post_list(self):
        """
        User: 'user 1'
        """
        self._login()

        data = {
            'value': 'New Todo Item!'
        }

        response = self.api_client.post(self.list_url, data=data)
        self.assertHttpCreated(response)

        todo_item = self.deserialize(response)
        self.assertEqual(todo_item['value'], data['value'])

        self.assertIn('resource_uri', todo_item)

        # Now get the item using the reource_uri
        response = self.api_client.get(todo_item['resource_uri'])
        self.assertHttpOK(response)

    def test_post_list_with_status(self):
        """
        User: 'user 1'
        """
        self._login()

        data = {
            'value': 'New Todo Item!',
            'status': True
        }

        response = self.api_client.post(self.list_url, data=data)
        self.assertHttpCreated(response)

        todo_item = self.deserialize(response)
        self.assertEqual(todo_item['value'], data['value'])
        self.assertEqual(todo_item['status'], data['status'])

        self.assertIn('resource_uri', todo_item)

        # Now get the item using the reource_uri
        response = self.api_client.get(todo_item['resource_uri'])
        self.assertHttpOK(response)

    ###########################################################################
    # PUT
    ###########################################################################
    def test_put_detail_unauthorized(self):
        response = self.api_client.put(self.detail_url)
        self.assertHttpUnauthorized(response)

    def test_put_detail_other_user_unauthorized(self):
        self._login(username='user_2', password='user_2')

        data = {
            'value': 'Invalid'
        }

        response = self.api_client.put(self.detail_url, data=data)
        self.assertHttpUnauthorized(response)

    def test_put_detail(self):
        """
        User: 'user 1'
        """
        self._login()

        data = {
            'status': True
        }

        response = self.api_client.put(self.detail_url, data=data)
        self.assertHttpOK(response)

        todo_item = self.deserialize(response)
        self.assertEqual(todo_item['status'], data['status'])

        self.assertIn('resource_uri', todo_item)

        # Now get the item using the reource_uri
        response = self.api_client.get(todo_item['resource_uri'])
        self.assertHttpOK(response)
        todo_item = self.deserialize(response)
        self.assertEqual(todo_item['status'], data['status'])

    ###########################################################################
    # DELETE
    ###########################################################################
    def test_delete_detail_unauthorized(self):
        response = self.api_client.delete(self.detail_url)
        self.assertHttpUnauthorized(response)

    def test_delete_detail_other_user_unauthorized(self):
        self._login(username='user_2', password='user_2')

        response = self.api_client.delete(self.detail_url)
        self.assertHttpUnauthorized(response)

    def test_delete_detail(self):
        """
        User: 'user 1'
        """
        self._login()

        response = self.api_client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
