from re import match, sub
from typing import List, Union, Tuple
from meapi.exceptions import MeException
from datetime import datetime, date
from meapi.helpers import valid_phone_number
from meapi.models import deleter, watcher, group, social, user, comment, friendship


class Social:

    def friendship(self, phone_number: Union[int, str]) -> friendship.Friendship:
        """
        Get friendship information between you and another number.
        like count mutual friends, total calls duration, how do you name each other, calls count, your watches, comments, and more.

        :param phone_number: International phone number format.
        :type phone_number: Union[int, str]
        :return: Dict with friendship data.
        :rtype: dict

        Example of friendship::

            {
                "calls_duration": None,
                "he_called": 0,
                "he_named": "He named",
                "he_watched": 3,
                "his_comment": None,
                "i_called": 0,
                "i_named": "You named",
                "i_watched": 2,
                "is_premium": False,
                "mutual_friends_count": 6,
                "my_comment": None,
            }
        """
        return friendship.Friendship.new_from_json_dict(self._make_request('get', '/main/contacts/friendship/?phone_number=' + str(valid_phone_number(phone_number))))

    def report_spam(self, country_code: str, spam_name: str, phone_number: Union[str, int]) -> bool:
        """
        Report spam on another phone number.

        :param country_code: Two letters code, ``IL``, ``IT``, ``US`` etc. // `Country codes <https://countrycode.org/>`_.
        :type country_code: str
        :param spam_name: The spam name that you want to give to the spammer.
        :type spam_name: str
        :param phone_number: spammer phone number in international format.
        :type phone_number: Union[int, str]
        :return: Is report success
        :rtype: bool
        """
        body = {"country_code": country_code.upper(), "is_spam": True, "is_from_v": False,
                "name": str(spam_name), "phone_number": str(valid_phone_number(phone_number))}
        return self._make_request('post', '/main/names/suggestion/report/', body)['success']

    def who_deleted(self) -> List[deleter.Deleter]:
        """
        Get list of contacts dicts who deleted you from their contacts.

        **The** ``who_deleted`` **configuration must be enabled in your settings account in order to see who deleted you. See** :py:func:`change_social_settings`.

        :return: list of dicts
        :rtype: List[dict]

        Example::

            [
                {
                    "created_at": "2021-09-12T15:42:57Z",
                    "user": {
                        "email": "",
                        "profile_picture": None,
                        "first_name": "Test",
                        "last_name": "Test",
                        "gender": None,
                        "uuid": "aa221ae8-XXX-4679-XXX-91307XXX5a9a2",
                        "is_verified": False,
                        "phone_number": 123456789012,
                        "slogan": None,
                        "is_premium": False,
                        "verify_subscription": True,
                    },
                }
            ]
        """
        return [deleter.Deleter.new_from_json_dict(deleter) for deleter in self._make_request('get', '/main/users/profile/who-deleted/')]

    def who_watched(self) -> List[watcher.Watcher]:
        """
         Get list of contacts dicts who watched your profile.

        **The** ``who_watched`` **configuration must be enabled in your settings account in order to see watched. See** :py:func:`change_social_settings`.

        :return: list of dicts
        :rtype: List[dict]

        Example::

            [
                {
                    "last_view": "2022-04-16T17:13:24Z",
                    "user": {
                        "email": "eliezXXXXXXXXX94@gmail.com",
                        "profile_picture": "https://d18zXXXXXXXXXXXXXcb14529ccc7db.jpg",
                        "first_name": "Test",
                        "last_name": None,
                        "gender": None,
                        "uuid": "f8d03XXX97b-ae86-35XXXX9c6e5",
                        "is_verified": False,
                        "phone_number": 97876453245,
                        "slogan": None,
                        "is_premium": True,
                        "verify_subscription": True,
                    },
                    "count": 14,
                    "is_search": None,
                }
            ]
        """
        return sorted([watcher.Watcher.new_from_json_dict(watcher) for watcher in
                       self._make_request('get', '/main/users/profile/who-watched/')], key=lambda x: x.count, reverse=True)

    def get_comments(self, uuid: str = None) -> List[comment.Comment]:
        """
        Get user comments.

        :param uuid: User uuid. See :py:func:`get_uuid`. Default: Your uuid.
        :type uuid: str
        :return: Dict with list of comments.
        :rtype: Dict[list]

        Example::

            {
                "comments": [
                    {
                        "like_count": 2,
                        "status": "approved",
                        "message": "Test comment",
                        "author": {
                            "email": "user@domain.com",
                            "profile_picture": "https://d18zaexen4dp1s.cloudfront.net/593a9XXXXXXd7437XXXX7.jpg",
                            "first_name": "Name test",
                            "last_name": "",
                            "gender": None,
                            "uuid": "8a0XXXXXXXXXXX0a-83XXXXXXb597",
                            "is_verified": True,
                            "phone_number": 123456789098,
                            "slogan": "https://example.com",
                            "is_premium": False,
                            "verify_subscription": True,
                        },
                        "is_liked": False,
                        "id": 662,
                        "comments_blocked": False,
                    },
                    {
                        "like_count": 2,
                        "status": "approved",
                        "message": "hhaha",
                        "author": {
                            "email": "haXXXXiel@gmail.com",
                            "profile_picture": None,
                            "first_name": "Test",
                            "last_name": "Test",
                            "gender": None,
                            "uuid": "59XXXXXXXXXXXX-b6c7-f2XXXXXXXXXX26d267",
                            "is_verified": False,
                            "phone_number": 914354653176,
                            "slogan": None,
                            "is_premium": False,
                            "verify_subscription": True,
                        },
                        "is_liked": True,
                        "id": 661,
                        "comments_blocked": False,
                    },
                ],
                "count": 2,
                "user_comment": None,
            }
        """
        if not uuid or uuid == self.uuid:
            if self.phone_number:
                comments: List[dict] = self._make_request('get', '/main/comments/list/' + self.uuid)['comments']
                for com in comments:
                    com.update({'my_comment': True})
            else:
                raise MeException("In https://meapi.readthedocs.io/en/latest/setup.html#official-method mode you must to provide user uuid.")
        else:
            comments = self._make_request('get', '/main/comments/list/' + uuid)['comments']
        return [comment.Comment.new_from_json_dict(com, _meobj=self) for com in comments]

    def get_comment(self, comment_id: Union[int, str]) -> dict:
        """
        Get comment details, comment text, who and how many liked, create time and more.

        :param comment_id: Comment id from :py:func:`get_comments`
        :type comment_id: Union[int, str]
        :return: Dict with comment details.
        :rtype: dict

        Example::

            {
                "comment_likes": [
                    {
                        "author": {
                            "email": "yonXXXXXX@gmail.com",
                            "first_name": "Jonatan",
                            "gender": "M",
                            "is_premium": False,
                            "is_verified": True,
                            "last_name": "Fa",
                            "phone_number": 97655764547,
                            "profile_picture": "https://d18zaexXXXp1s.cloudfront.net/2eXXefea6dXXXXXXe3.jpg",
                            "slogan": None,
                            "uuid": "807XXXXX2-414a-b7XXXXX92cd679",
                            "verify_subscription": True,
                        },
                        "created_at": "2022-04-17T16:53:49Z",
                        "id": 194404,
                    }
                ],
                "like_count": 1,
                "message": "Test comment",
            }
        """
        com = self._make_request('get', '/main/comments/retrieve/' + str(comment_id))
        com.update({'id': int(comment_id)})
        return comment.Comment.new_from_json_dict(com, _meobj=self)

    def approve_comment(self, comment_id: Union[str, int]) -> bool:
        """
        Approve comment. (You can always delete it with :py:func:`delete_comment`.)

        :param comment_id: Comment id from :py:func:`get_comments`.
        :type comment_id: Union[str, int]
        :return: Is approve success.
        :rtype: bool
        """
        return bool(self._make_request('post', f'/main/comments/approve/{comment_id}/') == 'approved')

    def delete_comment(self, comment_id: Union[str, int]) -> bool:
        """
        Delete (Ignore) comment. (you can always approve it with :py:func:`approve_comment`.)

        :param comment_id: Comment id from :py:func:`get_comments`.
        :type comment_id: Union[int, str]
        :return: Is deleting success.
        :rtype: bool
        """
        return bool(self._make_request('delete', f'/main/comments/approve/{comment_id}/') == 'ignored')

    def like_comment(self, comment_id: Union[int, str]) -> bool:
        """
        Like comment.

        :param comment_id: Comment id from :py:func:`get_comments`.
        :type comment_id: Union[int, str]
        :return: Is like success.
        :rtype: bool
        """
        return self._make_request('post', f'/main/comments/like/{comment_id}/')['success']

    def publish_comment(self, uuid: str, your_comment: str) -> Tuple[comment.Comment, bool]:
        """
        Publish comment for another user.

        :param uuid: uuid of the commented user. See :py:func:`get_uuid`.
        :type uuid: str
        :param your_comment: Your comment
        :type your_comment: str
        :return: comment_id if success, else False.
        :rtype: Union[int, bool]
        """
        body = {"message": str(your_comment)}
        com = comment.Comment.new_from_json_dict(self._make_request('post', f'/main/comments/add/{uuid}/', body))
        return com, bool(com.status == 'waiting')

    def get_groups_names(self) -> List[group.Group]:
        """
        Get groups of names and see how people named you.

        :return: Dict with groups.
        :rtype: dict

        Example::

            {
                "cached": False,
                "groups": [
                    {
                        "name": "This is how they name you",
                        "count": 1,
                        "last_contact_at": "2020-06-09T12:24:51Z",
                        "contacts": [
                            {
                                "id": 2218840161,
                                "created_at": "2020-06-09T12:24:51Z",
                                "modified_at": "2020-06-09T12:24:51Z",
                                "user": {
                                    "profile_picture": "https://XXXXp1s.cloudfront.net/28d5XXX96953feX6.jpg",
                                    "first_name": "joz",
                                    "last_name": "me",
                                    "uuid": "0577XXX-1XXXe-d338XXX74483",
                                    "is_verified": False,
                                    "phone_number": 954353655531,
                                },
                                "in_contact_list": True,
                            }
                        ],
                        "contact_ids": [2213546561],
                    }
                ],
            }
        """
        return sorted([group.Group.new_from_json_dict(group, _meobj=self, status='active') for group in
                       self._make_request('get', '/main/names/groups/')['groups']],
                      key=lambda x: x.count, reverse=True)

    def get_deleted_names(self) -> dict:
        """
        Get group names that you deleted.

        :return: dict with names and contact ids.
        :rtype: dict

        Example::

            {
                "names": [
                    {
                        "contact_id": 40108734246,
                        "created_at": "2022-04-18T06:08:33Z",
                        "hidden_at": "2022-04-23T20:45:19Z",
                        "name": "My delivery guy",
                        "user": {
                            "email": "pnhfdishfois@gmail.com",
                            "profile_picture": None,
                            "first_name": "Joe",
                            "last_name": "",
                            "gender": None,
                            "uuid": "52XXXXX-b952-XXXX-853e-XXXXXX",
                            "is_verified": False,
                            "phone_number": 9890987986,
                            "slogan": None,
                            "is_premium": False,
                            "verify_subscription": True,
                        },
                        "in_contact_list": True,
                    }
                ],
                "count": 1,
                "contact_ids": [409879786],
            }
        """
        return self._make_request('get', '/main/settings/hidden-names/')

    def delete_name(self, contacts_ids: Union[int, str, List[Union[int, str]]]) -> bool:
        """
        Delete group name (You can also ask for rename with :py:func:`ask_group_rename`. and you can restore deleted group with :py:func:`restore_name`).

        :param contacts_ids: Single or list of contact ids from the same group. See :py:func:`get_groups_names`.
        :type contacts_ids: Union[int, str, List[Union[int, str]]]
        :return: Is delete success.
        :rtype: bool
        """
        if not isinstance(contacts_ids, list):
            contacts_ids = [contacts_ids]
        body = {"contact_ids": [int(_id) for _id in contacts_ids]}
        return self._make_request('post', '/main/contacts/hide/', body)['success']

    def restore_name(self, contacts_ids: Union[int, str, List[Union[int, str]]]) -> bool:
        """
        Restore deleted group name from :py:func:`get_deleted_names`.

        :param contacts_ids: Single or list of contact ids from the same deleted group. See :py:func:`get_groups_names`.
        :type contacts_ids: Union[int, str, List[Union[int, str]]]
        :return: Is restoring success.
        :rtype: bool
        """
        if not isinstance(contacts_ids, list):
            contacts_ids = [contacts_ids]
        body = {"contact_ids": [int(_id) for _id in contacts_ids]}
        return self._make_request('post', '/main/settings/hidden-names/', body)['success']

    def ask_group_rename(self, contacts_ids: Union[int, str, List[Union[int, str]]], new_name: Union[str, None] = None) -> bool:
        """
        Suggest new name to group of people and ask them to rename you in their contacts book.

        :param contacts_ids: Single or list of contact ids from the same group. See :py:func:`get_groups_names`.
        :type contacts_ids: Union[int, str, List[Union[int, str]]]
        :param new_name: Suggested name, Default: Your profile name from :py:func:`get_profile_info`.
        :type new_name: Union[str, None]
        :return: Is asking success.
        :rtype: bool
        """
        if not isinstance(contacts_ids, list):
            contacts_ids = [contacts_ids]

        if not new_name:  # suggest your name in your profile
            my_profile = self.get_profile_info()
            new_name += str(my_profile.first_name)
            if my_profile.last_name:
                new_name += (" " + my_profile.last_name)

        body = {"contact_ids": [int(_id) for _id in contacts_ids], "name": new_name}
        return self._make_request('post', '/main/names/suggestion/', body)['success']

    def get_socials(self, uuid: str = None) -> social.Social:
        """
        Get connected social networks to Me account.

        :param uuid: User uuid. See :py:func:`get_uuid`. Default: Your uuid.
        :type uuid: str
        :return: Dict with social networks and posts.
        :rtype: dict

        Example::

            {
                "social": {
                    "facebook": {
                        "posts": [],
                        "profile_id": "https://www.facebook.com/app_scoped_user_id/XXXXXXXXXXX/",
                        "is_active": True,
                        "is_hidden": True,
                    },
                    "fakebook": {
                        "is_active": False,
                        "is_hidden": True,
                        "posts": [],
                        "profile_id": None,
                    },
                    "instagram": {
                        "posts": [
                            {
                                "posted_at": "2021-12-23T22:21:06Z",
                                "photo": "https://d18zaexen4dp1s.cloudfront.net/XXXXXXXXXXXXXX.jpg",
                                "text_first": None,
                                "text_second": "IMAGE",
                                "author": "username",
                                "redirect_id": "CXXXXIz-0",
                                "owner": "username",
                            }
                        ],
                        "profile_id": "username",
                        "is_active": True,
                        "is_hidden": False,
                    },
                    "linkedin": {
                        "is_active": True,
                        "is_hidden": False,
                        "posts": [],
                        "profile_id": "https://www.linkedin.com/in/username",
                    },
                    "pinterest": {
                        "posts": [],
                        "profile_id": "https://pin.it/XXXXXXXX",
                        "is_active": True,
                        "is_hidden": False,
                    },
                    "spotify": {
                        "is_active": True,
                        "is_hidden": False,
                        "posts": [
                            {
                                "author": "Chandler bing",
                                "owner": "4xgXXXXXXXt0pv",
                                "photo": "https://d18zaexen4dp1s.cloudfront.net/9bcXXXfa7dXXXXXXXac.jpg",
                                "posted_at": None,
                                "redirect_id": "4KgES5cs3SnMhuAXuBREW2",
                                "text_first": "My friends playlist songs",
                                "text_second": "157",
                            },
                            {
                                "author": "Chandler Bing",
                                "owner": "4xgoXcoriuXXXXpt0pv",
                                "photo": "https://d18zaexen4dp1s.cloudfront.net/55d3XXXXXXXXXXXXXXXXXX4.jpg",
                                "posted_at": None,
                                "redirect_id": "3FjSXXXCQPB14Xt",
                                "text_first": "My favorite songs!",
                                "text_second": "272",
                            },
                        ],
                        "profile_id": "4xgot8coriuXXXXXpt0pv",
                    },
                    "tiktok": {
                        "is_active": False,
                        "is_hidden": True,
                        "posts": [],
                        "profile_id": None,
                    },
                    "twitter": {
                        "is_active": True,
                        "is_hidden": False,
                        "posts": [
                            {
                                "author": "username",
                                "owner": "username",
                                "photo": "https://pbs.twimg.com/profile_images/13XXXXX76/AvBXXXX_normal.jpg",
                                "posted_at": "2021-08-24T10:02:45Z",
                                "redirect_id": "https://twitter.com/username/status/1XXXXXX423",
                                "text_first": "My tweet #1 https://t.co/PLXXXX2Tw https://t.co/zXXXXkk",
                                "text_second": None,
                            },
                            {
                                "author": "username",
                                "owner": "username",
                                "photo": "https://pbs.twimg.com/profile_images/1318XXXX0976/AvBXXXUk_normal.jpg",
                                "posted_at": "2021-08-12T10:09:23Z",
                                "redirect_id": "https://twitter.com/username/status/142XXXXX86624",
                                "text_first": "My second tweet https://t.co/xtqXXXtAC",
                                "text_second": None,
                            },
                        ],
                        "profile_id": "username",
                    },
                },
            }
        """
        if not uuid:
            return social.Social.new_from_json_dict(self._make_request('post', '/main/social/update/'), _meobj=self, _my_social=True)
        return self.get_profile_info(uuid).social

    def add_social(self,
                   twitter_token: str = None,
                   spotify_token: str = None,
                   instagram_token: str = None,
                   facebook_token: str = None,
                   pinterest_url: str = None,
                   linkedin_url: str = None, ) -> Tuple[bool, List[str]]:
        """
        Add social network to your me account.

        - **if you have at least 2 socials, you get** ``is_verified`` = ``True`` **in your profile (Blue check).**

        :param twitter_token: `Twitter Token <https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-twitter_token-md>`_. Default = ``None``.
        :type twitter_token: str
        :param spotify_token: Log in to `spotify <https://accounts.spotify.com/authorize?client_id=0b1ea72f7dce420583038b49fd04be50&response_type=code&redirect_uri=https://app.mobile.me.app/&scope=user-read-email%20playlist-read-private>`_ and copy the token after the ``https://app.mobile.me.app/?code=``. Default = ``None``.
        :type spotify_token: str
        :param instagram_token: Log in to `instagram <https://api.instagram.com/oauth/authorize/?app_id=195953705182737&redirect_uri=https://app.mobile.me.app/&response_type=code&scope=user_profile,user_media>`_ and copy the token after the ``https://app.mobile.me.app/?code=``. Default = ``None``.
        :type instagram_token: str
        :param facebook_token: `Facebook token <https://facebook.com/v12.0/dialog/oauth?cct_prefetching=0&client_id=799397013456724>`_. Default = ``None``.
        :type facebook_token: str
        :param pinterest_url: Profile url - ``https://www.pinterest.com/username/``. Default = ``None``.
        :type pinterest_url: str
        :param linkedin_url: Profile url - ``https://www.linkedin.com/in/username``. Default = ``None``.
        :type linkedin_url: str
        :return: Tuple of: is_success, list of failed.
        :rtype: Tuple[bool, List[str]]
        """
        args = locals()
        del args['self']
        if sum(bool(i) for i in args.values()) < 1:
            raise MeException("You need to provide at least one social!")
        failed = []
        for social, token_or_url in args.items():
            if token_or_url is not None:
                if 'url' in social:
                    if match(r"^https?:\/\/.*{domain}.*$".format(domain=social.replace('_url', '')), token_or_url):
                        field_name = 'profile_id'
                        endpoint = 'update-url'
                        is_token = False
                    else:
                        raise MeException(f"You must provide a valid link to the {social.replace('_url', '').capitalize()} profile!")
                else:
                    field_name = 'code_first'
                    endpoint = 'save-auth-token'
                    is_token = True
                social_name = sub(r'_(token|url)$', '', social)
                body = {'social_name': social_name, field_name: token_or_url}
                results = self._make_request('post', f'/main/social/{endpoint}/', body)
                if not (bool(results['success']) if is_token else bool(results[social_name]['profile_id'] == token_or_url)):
                    failed.append(social_name)
        return not bool(failed), failed

    def remove_social(self,
                      twitter: bool = False,
                      spotify: bool = False,
                      instagram: bool = False,
                      facebook: bool = False,
                      pinterest: bool = False,
                      linkedin: bool = False,
                      tiktok: bool = False,
                      ) -> bool:
        """
        Remove social networks from your profile. You can also hide social instead of deleting it: :py:func:`switch_social_status`.

        :param twitter: To remove Twitter. Default: ``False``.
        :type twitter: bool
        :param spotify: To remove Spotify. Default: ``False``.
        :type spotify: bool
        :param instagram: To remove Instagram. Default: ``False``.
        :type instagram: bool
        :param facebook: To remove Facebook. Default: ``False``.
        :type facebook: bool
        :param pinterest: To remove Pinterest. Default: ``False``.
        :type pinterest: bool
        :param linkedin: To remove Linkedin. Default: ``False``.
        :type linkedin: bool
        :param tiktok: To remove Tiktok. Default: ``False``.
        :type tiktok: bool
        :return: Is removal success.
        :rtype: bool
        """
        args = locals()
        del args['self']
        true_values = sum(bool(i) for i in args.values())
        if true_values < 1:
            raise MeException("You need to remove at least one social!")
        successes = 0
        for social, value in args.items():
            if value and isinstance(value, bool):
                body = {"social_name": str(social)}
                res = self._make_request('post', '/main/social/delete/', body)
                print(res)
                if res.get('success'):
                    successes += 1
        return bool(true_values == successes)

    def switch_social_status(self,
                             twitter: bool = None,
                             spotify: bool = None,
                             instagram: bool = None,
                             facebook: bool = None,
                             pinterest: bool = None,
                             linkedin: bool = None,
                             ) -> bool:
        """
        Switch social network status: Show (``True``) or Hide (``False``).

        :param twitter: Switch Twitter status. Default: ``None``.
        :type twitter: bool
        :param spotify: Switch Spotify status Default: ``None``.
        :type spotify: bool
        :param instagram: Switch Instagram status Default: ``None``.
        :type instagram: bool
        :param facebook: Switch Facebook status Default: ``None``.
        :type facebook: bool
        :param pinterest: Switch Pinterest status Default: ``None``.
        :type pinterest: bool
        :param linkedin: Switch Linkedin status Default: ``None``.
        :type linkedin: bool
        :return: is switch success (you get ``True`` even if social won't set before).
        :rtype: bool
        """
        args = locals()
        del args['self']
        not_null_values = sum(bool(i) for i in args.values() if i is not None) or sum(not bool(i) for i in args.values() if i is not None)
        if not_null_values < 1:
            raise MeException("You need to switch status to at least one social!")
        successes = 0
        for social, status in args.items():
            if status is not None and isinstance(status, bool):
                body = {"social_name": str(social)}
                current_status = self.get_socials()
                if status == current_status[social]['is_hidden'] and current_status[social]['is_active']:  # exists but status not as the required
                    res = self._make_request('post', '/main/social/hide/', body)
                    print(res)
                    new_status = not bool(res['is_hidden'])
                    if status == new_status:
                        successes += 1

        return bool(not_null_values == successes)

    def numbers_count(self) -> int:
        """
        Get total count of numbers on Me.

        :return: total count.
        :rtype: int
        """
        return self._make_request('get', '/main/contacts/count/')['count']

    def suggest_turn_on_comments(self, uuid: str) -> bool:
        """
        Ask another user to turn on comments in his profile.

        :param uuid: User uuid. See :py:func:`get_uuid`.
        :type uuid: str
        :return: Is request success.
        :rtype: bool
        """
        body = {"uuid": str(uuid)}
        return self._make_request('post', '/main/users/profile/suggest-turn-on-comments/', body)['requested']

    def suggest_turn_on_mutual(self, uuid: str) -> bool:
        """
        Ask another user to turn on mutual contacts on his profile.

        :param uuid: User uuid. See :py:func:`get_uuid`.
        :type uuid: str
        :return: Is request success.
        :rtype: bool
        """
        body = {"uuid": str(uuid)}
        return self._make_request('post', '/main/users/profile/suggest-turn-on-mutual/', body)['requested']

    def suggest_turn_on_location(self, uuid: str) -> bool:
        """
        Ask another user to share his location with you.

        :param uuid: User uuid. See :py:func:`get_uuid`. Default: Your uuid.
        :type uuid: str
        :return: Is request success.
        :rtype: bool
        """
        body = {"uuid": str(uuid)}
        return self._make_request('post', '/main/users/profile/suggest-turn-on-location/', body)['requested']

    def get_age(self, uuid=None) -> float:
        """
        Get user age. calculate from ``date_of_birth``, provided by :py:func:`get_profile_info`.

        :param uuid: User uuid. See :py:func:`get_uuid`. Default: Your uuid.
        :type uuid: str
        :return: User age if date of birth exists. else - 0.0
        :rtype: float
        """
        date_of_birth = self.get_profile_info(uuid)['profile']['date_of_birth']
        if match(r"^\d{4}(\-)([0-2][0-9]|(3)[0-1])(\-)(((0)[0-9])|((1)[0-2]))$", str(date_of_birth)):
            days_in_year = 365.2425
            return round((date.today() - datetime.strptime(date_of_birth, "%Y-%m-%d").date()).days / days_in_year, 1)
        return 0.0

    def is_spammer(self, phone_number: Union[int, str]) -> int:
        """
        Check on phone number if reported as spam.

        :param phone_number: International phone number format.
        :type phone_number: Union[int, str]
        :return: count of spam reports. 0 if None.
        :rtype: int
        """
        results = self.phone_search(phone_number)
        if results:
            return results['contact']['suggested_as_spam']
        return 0

    def update_location(self, lat: float, lon: float) -> bool:
        """
        Update your location. See :py:func:`upload_random_data`.

        :param lat: location latitude coordinates.
        :type lat: float
        :param lon: location longitude coordinates.
        :type lon: float
        :return: Is location update success.
        :rtype: bool
        """
        if not isinstance(lat, float) or not isinstance(lon, float):
            raise Exception("Not a valid coordination!")
        body = {"location_latitude": float(lat), "location_longitude": float(lon)}
        return self._make_request('post', '/main/location/update/', body)['success']

    def share_location(self, uuid: str) -> bool:
        """
        Share your :py:func:`update_location` with another user.

        :param uuid: User uuid. See :py:func:`get_uuid`.
        :type uuid: str
        :return: is sharing success.
        :rtype: bool
        """
        return self._make_request('post', '/main/users/profile/share-location/' + str(uuid) + "/")['success']

    def get_distance(self, uuid: str) -> Union[float, None]:
        """
        Get your distance between you and another user.
         - Only if the user shared his location with you. you can ask his location with :py:func:`suggest_turn_on_location`.

        :param uuid: User uuid. See :py:func:`get_uuid`.
        :type uuid: str
        :return: The distance between you in kilometers. None if the user not shared his location with you.
        :rtype: Union[float, None]
        """
        results = self.get_profile_info(uuid)
        if results['profile'].get('distance'):
            return results['profile']['distance']
        return None

    def stop_sharing_location(self, uuids: Union[str, List[str]]) -> bool:
        """
        Stop sharing your :py:func:`update_location` with users.

        :param uuids: Single or list of uuids that you want to stop them from watching you location. See :py:func:`locations_shared_by_me`.
        :type uuids: Union[str, List[str]]
        :return: is stopping success.
        :rtype: bool
        """
        if not isinstance(uuids, list):
            uuids = [uuids]
        body = {"uuids": uuids}
        return self._make_request('post', '/main/users/profile/share-location/stop-for-me/', body)['success']

    def stop_shared_location(self, uuids: Union[str, List[str]]) -> bool:
        """
        Stop locations that shared with you.

        :param uuids: Single or list of uuids that you want to stop their location. See :py:func:`locations_shared_with_me`.
        :type uuids: Union[str, List[str]]
        :return: is stopping success.
        :rtype: bool
        """
        if not isinstance(uuids, list):
            uuids = [uuids]
        body = {"uuids": uuids}
        return self._make_request('post', '/main/users/profile/share-location/stop/', body)['success']

    def locations_shared_by_me(self) -> List[user.User]:
        """
        Get list of users that you shared your location with them. See also :py:func:`locations_shared_with_me`.

        :return: list of dicts with contacts details.
        :rtype: List[dict]

        Example::

            [
                {
                    "first_name": "Rachel Green",
                    "last_name": "",
                    "phone_number": 1234567890,
                    "profile_picture": "https://d18zaexen4dp1s.cloudfront.net/59XXXXXXXXXfa67.jpg",
                    "uuid": "XXXXX-XXXXX-XXXX-XXXX-XXXXXX"
                }
            ]
        """
        return [user.User.new_from_json_dict(usr, _meobj=self) for usr in self._make_request('get', '/main/users/profile/share-location/')]

    def locations_shared_with_me(self) -> dict:
        """
        Get users who have shared a location with you. See also :py:func:`locations_shared_by_me`.

        :return: dict with list of uuids and list with users.
        :rtype: dict

        Example::

            {
                "shared_location_user_uuids": [
                    "3850XXX-XXX-XXX-XXX-XXXXX"
                ],
                "shared_location_users": [
                    {
                        "author": {
                            "first_name": "Gunther",
                            "last_name": "",
                            "phone_number": 3647632874324,
                            "profile_picture": "https://d18zaexen4dp1s.cloudfront.net/dXXXXXXXXXXXXXXXXXXb.jpg",
                            "uuid": "3850XXX-XXX-XXX-XXX-XXXXX"
                        },
                        "distance": 1.4099551982832228,
                        "i_shared": False
                    }
                ]
            }
        """
        return self._make_request('get', '/main/users/profile/share-location/for-me/')
