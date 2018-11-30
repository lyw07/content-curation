#!/usr/bin/env python
import os
import json
from random import choice
from locust import HttpLocust, TaskSet, task
try:
    import urllib.request as urlrequest
except ImportError:
    import urllib as urlrequest

USERNAME = os.getenv("LOCUST_USERNAME") or "a@a.com"
PASSWORD = os.getenv("LOCUST_PASSWORD") or "a"
TOKEN = "84c1431fa34b69472cfeba24a218b270cd9cdf57"


class BaseTaskSet(TaskSet):

    def _login(self):
        """
        Helper function to log in the user to the current session.
        """
        resp = self.client.get("/accounts/login/")
        csrf = resp.cookies.get("csrftoken")

        formdata = {
            "username": USERNAME,
            "password": PASSWORD,
            "csrfmiddlewaretoken": csrf,
        }
        response = self.client.post(
            "/accounts/login/",
            data=formdata,
            headers={
                "content-type": "application/x-www-form-urlencoded",
                "referer": "https://develop.studio.learningequality.org/accounts/login/"
            }
        )

    def i18n_requests(self):
        self.client.get("/jsi18n/")
        self.client.get("/jsreverse/")


class ChannelListPage(BaseTaskSet):
    """
    Task to explore different channels lists
    """
    def on_start(self):
        self._login()

    def channel_list_api_calls(self):
        self.client.get("/get_user_pending_channels/")
        self.client.get("/get_user_edit_channels/")
        self.client.get("/get_user_bookmarked_channels/")
        self.client.get("/get_user_public_channels/")
        self.client.get("/get_user_view_channels/")

    @task
    def channel_list(self):
        """
        Load the channel page and the important endpoints.
        """
        self.client.get("/channels/")
        self.channel_list_api_calls()


class ChannelPage(BaseTaskSet):
    """
    Task to open and view a channel, including its topics and nodes
    """
    def on_start(self):
        self._login()

    def get_first_public_channel_id(self):
        """
        Returns the id of the first available public channel
        :returns: id of the first available public channel or None if there are not public channels
        """
        resp = self.client.get("/get_user_public_channels/").json()
        try:
            channel_id = resp[0]['id']
        except IndexError:
            channel_id = None
        return channel_id

    def get_random_topic_id(self, channel_id):
        """
        Returns the id of a randomly selected topic for the provided channel_id
        :param: channel_id: id of the channel where the topic must be found
        :returns: id of the selected topic
        """
        topic_id = None
        channel_resp = self.client.get('/api/channel/{}'.format(channel_id)).json()
        try:
            children = channel_resp['main_tree']['children']
            topic_id = choice(children)
            return topic_id
        except KeyError as e:
            print (channel_resp)
            print (channel_id)
            raise e

    def get_node_children(self, node_id):
        nodes_resp = self.client.get('/api/get_nodes_by_ids/{}'.format(node_id)).json()
        children = nodes_resp[0]['children']
        children_nodes = []
        if children:
            children_nodes = self.client.get('/api/get_nodes_by_ids/{}'.format(','.join(children))).json()
        return children_nodes

    def get_random_resource_id(self, topic_id):
        """
        Returns the id of a randoly selected resource for the provided topic_id
        :param: topic_id: id of the topic where the resource must be found
        :returns: id of the selected resource
        """
        nodes_resp = self.client.get('/api/get_nodes_by_ids/{}'.format(topic_id)).json()
        try:
            while nodes_resp[0]['kind'] == 'topic':
                nodes = nodes_resp[0]['children']
                nodes_resp = self.client.get('/api/get_nodes_by_ids/{}'.format(','.join(nodes))).json()
            return choice(nodes_resp)['id']
        except IndexError:
            return None

    # @task
    # def open_channel(self, channel_id=None):
    #     """
    #     Open to edit a channel, if channel_id is None it opens the first public channel
    #     """
    #     if not channel_id:
    #         channel_id = self.get_first_public_channel_id()
    #     if channel_id:
    #         self.client.get('/channels/{}'.format(channel_id))

    # @task
    # def open_subtopic(self, channel_id=None, topic_id=None):
    #     """
    #     Open  a topic, if channel_id is None it opens the first public channel
    #     """
    #     if not channel_id:
    #         channel_id = self.get_first_public_channel_id()
    #     if channel_id and not topic_id:
    #         topic_id = self.get_random_topic_id(channel_id)
    #     if topic_id:
    #         self.get_random_resource_id(topic_id)

    # @task
    # def preview_random_content_item(self, content_id=None):
    #     """
    #     Do request on all the files for a content item.
    #     If content_id is not provided it will fetch a random content
    #     """
    #     if not content_id:
    #         channel_id = self.get_first_public_channel_id()
    #         topic_id = self.get_random_topic_id(channel_id)
    #         content_id = self.get_random_resource_id(topic_id)
    #         if content_id:
    #             resp = self.client.get('/api/get_nodes_by_ids_complete/{}'.format(content_id)).json()
    #             if 'files' in resp[0]:
    #                 for resource in resp[0]['files']:
    #                     storage_url = resource['storage_url']
    #                     print("Requesting resource {}".format(storage_url))
    #                     urlrequest.urlopen(storage_url).read()

    @task
    def add_random_content_items(self):
        """
        Do request on all the files for a content item.
        If content_id is not provided it will fetch a random content
        """
        # Problem of this approach is that in function `convert_data_to_nodes` of internal.py,
        # the node_is is in the existing node ids, so the for loop will not actually run, which is not something we want to test on
        # overall, we need to find a way to create a contentnode and then send the info to add_nodes endpoint.
        channel_id = self.get_first_public_channel_id()
        topic_id = self.get_random_topic_id(channel_id)
        node_children = self.get_node_children(topic_id)
        if node_children:
            payload = {
                "content_data": node_children,
                "root_id": topic_id,
            }
            # payload = {
            #     "root_id": "a6cc68d8eb084252b5a0b9eac1634d46",
            #     "content_data": [
            #         {
            #             "title": "test",
            #             "language": "en",
            #             "description": "",
            #             "node_id": "a6548c340deb53e18ffdb28a9cca940f",
            #             "content_id": "b7be4fbcbc475970b7164aaa755cf210",
            #             "source_domain": "ddd99da3f88f593c855c4812bf739616",
            #             "source_id": "testing",
            #             "author": ["A"],
            #             "files": [],
            #             "kind": "document",
            #             "license": "CC BY",
            #             "license_description": None,
            #             "copyright_holder": "Noktta",
            #             "questions": [],
            #             "extra_fields": "{}",
            #             "role": "learner"
            #         }
            #     ]
            # }

            resp = self.client.post('/api/internal/add_nodes', data=json.dumps(payload), headers={'Content-Type': 'application/json', 'Authorization': 'Token '+TOKEN})
            print ("response text is {}.".format(resp.text))
            print ("adding nodes result is {}".format(resp.content))


class ChannelClone(BaseTaskSet):
    def on_start(self):
        self._login()


class AdminChannelListPage(BaseTaskSet):

    def on_start(self):
        self._login()

    @task
    def channel_list_api_call(self):
        self.client.get("/api/get_all_channels")


class LoginPage(BaseTaskSet):
    # tasks = [ChannelListPage, AdminChannelListPage, ChannelPage]
    tasks = [ChannelPage]
    # tasks = [ChannelListPage, AdminChannelListPage, ChannelPage, ChannelClone]

    @task
    def loginpage(self):
        """
        Visit the login page and the i18n endpoints without logging in.
        """
        self.client.get("/accounts/login/")
        self.i18n_requests()


class StudioDesktopBrowserUser(HttpLocust):
    task_set = LoginPage
    min_wait = 5000
    max_wait = 20000
