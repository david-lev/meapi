from typing import Union, List


def phone_search_raw(meobj, phone_number: Union[str, int]) -> dict:
    """
    Get information on any phone number.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :param phone_number: International phone number format.
    :type phone_number: Union[str, int])
    :rtype: dict

    Example for existed user::

        {
            "contact": {
                "name": "Chandler bing",
                "picture": None,
                "user": {
                    "email": "user@domain.com",
                    "profile_picture": "https://d18zaexXXp1s.cloudfront.net/5XXX971XXXXXXXXXfa67.jpg",
                    "first_name": "Chandler",
                    "last_name": "Bing",
                    "gender": 'M',
                    "uuid": "XXXXX-XXXX-XXXX-XXXX-XXXX",
                    "is_verified": True,
                    "phone_number": 7434872457,
                    "slogan": "User bio",
                    "is_premium": False,
                    "verify_subscription": True,
                    "id": 42453345,
                    "comment_count": 0,
                    "location_enabled": False,
                    "distance": None,
                },
                "suggested_as_spam": 0,
                "is_permanent": False,
                "is_pending_name_change": False,
                "user_type": "BLUE",
                "phone_number": 7434872457,
                "cached": True,
                "is_my_contact": False,
                "is_shared_location": False,
            }
        }

    Example for non user::

        {
            "contact": {
                "name": "Chandler bing",
                "picture": None,
                "user": None,
                "suggested_as_spam": 0,
                "is_permanent": False,
                "is_pending_name_change": False,
                "user_type": "GREEN",
                "phone_number": 123456789,
                "cached": False,
                "is_my_contact": False,
                "is_shared_location": False,
            }
        }
    """
    return meobj._make_request(req_type='get', endpoint=f'/main/contacts/search/?phone_number={phone_number}')


def get_profile_raw(meobj, uuid: Union[str, None]) -> dict:
    """
    Get other users profile.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :param uuid: uuid of the Me user..
    :type uuid: str
    :raises MeApiException: msg: ``api_profile_view_passed_limit`` if you passed the limit (About 500 per day in the unofficial auth method).
    :return: Dict with profile details
    :rtype: dict

    Example::

        {
            "comments_blocked": False,
            "is_he_blocked_me": False,
            "is_permanent": False,
            "is_shared_location": False,
            "last_comment": None,
            "mutual_contacts_available": True,
            "mutual_contacts": [
                {
                    "phone_number": 1234567890,
                    "name": "Ross geller",
                    "referenced_user": {
                        "email": "rossgeller@friends.com",
                        "profile_picture": "https://d18zaexen4dp1s.cloudfront.net/59XXXXXXXXXXXXXXXX67.jpg",
                        "first_name": "Ross",
                        "last_name": "",
                        "gender": 'M',
                        "uuid": "XXXX-XXX-XXX-83c1-XXXX",
                        "is_verified": True,
                        "phone_number": 3432434546546,
                        "slogan": "Pivot!",
                        "is_premium": False,
                        "verify_subscription": True,
                    },
                    "date_of_birth": '1980-03-13',
                }
            ],
            "profile": {
                "carrier": "XXX mobile",
                "comments_enabled": False,
                "country_code": "XX",
                "date_of_birth": '2222-05-20',
                "device_type": "android",
                "distance": None,
                "email": "user@domain.com",
                "facebook_url": "133268763438473",
                "first_name": "Chandler",
                "gdpr_consent": True,
                "gender": 'M',
                "google_url": None,
                "is_premium": False,
                "is_verified": True,
                "last_name": "Bing",
                "location_enabled": False,
                "location_name": "XXXX",
                "login_type": "email",
                "me_in_contacts": True,
                "phone_number": 123456789012,
                "phone_prefix": "123",
                "profile_picture": "https://d18zaexen4dp1s.cloudfront.net/5XXX712a0676XXXXXXXfa67.jpg",
                "slogan": "I will always be there for you",
                "user_type": "BLUE",
                "uuid": "XXXXXXXXXXXXXXXXXXX3c1-6932bc9eb597",
                "verify_subscription": True,
                "who_deleted_enabled": True,
                "who_watched_enabled": True,
            },
            "share_location": False,
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
    return meobj._make_request('get', f'/main/users/profile/{uuid}')


def get_my_profile_raw(meobj) -> dict:
    """
    Get your profile.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :rtype: dict

    Example::

        {
            'first_name': 'Ross geller',
            'last_name': '',
            'facebook_url': '123456789',
            'google_url': None,
            'email': 'ross@friends.tv',
            'profile_picture': 'https://d18zaexen4dp1s.cloudfront.net/dXXXXXXXXXXXXX26b.jpg',
            'date_of_birth': '9999-12-12',
            'gender': None,
            'location_latitude': -37.57539,
            'location_longitude': 31.30874,
            'location_name': 'Argentina',
            'phone_number': 387648734435,
            'is_premium': False,
            'is_verified': False,
            'uuid': '3XXXb-3f7e-XXXX-XXXXX-XXXXX',
            'slogan': 'Pivot!',
            'device_type': 'ios',
            'carrier': 'BlaMobile',
            'country_code': 'AR',
            'phone_prefix': '387',
            'gdpr_consent': True,
            'login_type': 'apple',
            'verify_subscription': True
        }
    """
    return meobj._make_request('get', '/main/users/profile/me/')


def delete_account_raw(meobj) -> dict:
    """
    Delete your account.
    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :rtype: dict
    """
    # todo add json exmaple
    return meobj._make_request('delete', '/main/settings/remove-user/')


def suspend_account_raw(meobj) -> dict:
    """
    Suspend your account.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :rtype: dict
    """
    # todo add json example
    return meobj._make_request('put', '/main/settings/suspend-user/')


def _contact_handler(meobj, to_add: bool, contacts: List[dict]) -> dict:
    body = {"add": contacts if to_add else [], "is_first": False, "remove": contacts if not to_add else []}
    return meobj._make_request('post', '/main/contacts/sync/', body)


def add_contacts_raw(meobj, contacts: List[dict]) -> dict:
    """
    Upload new contacts to your Me account.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :rtype: dict

    Example of list of contacts to add::

        [
            {
                "country_code": "XX",
                "date_of_birth": None,
                "name": "Chandler",
                "phone_number": 512145887,
            }
        ]

    Example of results::

        {
            'total': 1,
            'added': 1,
            'updated': 0,
            'removed': 0,
            'failed': 0,
            'same': 0,
            'result':
                [{
                    'phone_number': 512145887,
                    'name': 'Chandler',
                    'email': None,
                    'referenced_user': None,
                    'created_at': '2022-06-25T22:28:41:955339Z',
                    'modified_at': '2022-06-25T22:28:41Z',
                    'country_code': 'XX',
                    'date_of_birth': None
                }],
            'failed_contacts': []
        }
    """
    return _contact_handler(meobj, to_add=True, contacts=contacts)


def remove_contacts_raw(meobj, contacts: List[dict]) -> dict:
    """
    Remove contacts from your Me account.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :rtype: dict

    Example of list of contacts to remove::

        [
            {
                "country_code": "XX",
                "date_of_birth": None,
                "name": "Chandler",
                "phone_number": 512145887,
            }
        ]

    Example of results::

        {
            'total': 1,
            'added': 0,
            'updated': 0,
            'removed': 1,
            'failed': 0,
            'same': 0,
            'result': [],
            'failed_contacts': []
        }
    """
    return _contact_handler(meobj, to_add=False, contacts=contacts)


def block_profile_raw(meobj, phone_number: int, block_contact: bool, me_full_block: bool) -> dict:
    """
    Block user profile.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :param phone_number: User phone number in international format.
    :type phone_number: Union[str, int]
    :param block_contact: To block for calls.
    :type block_contact: bool
    :param me_full_block: To block for social.
    :type me_full_block: bool
    :return: Dict of results.
    :rtype: dict

    Example of results::

        {
            'success': True,
            'message': 'Successfully block  updated'
        }
    """
    body = {"block_contact": block_contact, "me_full_block": me_full_block, "phone_number": phone_number}
    return meobj._make_request('post', '/main/users/profile/block/', body)


def unblock_profile_raw(meobj, phone_number: int, unblock_contact=True, me_full_unblock=True) -> dict:
    """
    Unlock user profile.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :param phone_number: User phone number in international format.
    :type phone_number: int
    :param unblock_contact: To unblock for calls.
    :type unblock_contact: bool
    :param me_full_unblock: To unblock for social.
    :type me_full_unblock: bool
    :return: Dict of results.
    :rtype: dict

    Example of results::

        {
            'success': True,
            'message': 'Successfully block  updated'
        }
    """
    body = {"block_contact": not unblock_contact, "me_full_block": not me_full_unblock, "phone_number": phone_number}
    return meobj._make_request('post', '/main/users/profile/block/', body)


def block_numbers_raw(meobj, numbers: List[int]) -> dict:
    """
    Block numbers.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :param numbers: Single or list of phone numbers in international format.
    :type numbers: List[int]
    :return: list of dicts with the blocked numbers.
    :rtype: List[dict]

    Example::

        [
            {
                "block_contact": True,
                "me_full_block": False,
                "phone_number": 1234567890
            }
        ]
    """
    return meobj._make_request('post', '/main/users/profile/bulk-block/', {"phone_numbers": numbers})


def unblock_numbers_raw(meobj, numbers: List[int]) -> dict:
    """
    Unblock phone numbers.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :param numbers: Single or list of phone numbers in international format.
    :type numbers: List[int]
    :return: dict with unblock success details.
    :rtype: dict

    Example::

        {
            'success': True,
            'message': 'Phone numbers successfully unblocked'
        }
    """
    return meobj._make_request('post', '/main/users/profile/bulk-unblock/', {"phone_numbers": numbers})


def get_blocked_numbers_raw(meobj) -> List[dict]:
    """
    Get your blocked numbers.

    :param meobj: :py:obj:`~meapi.Me` client object.
    :type meobj: :py:obj:`~meapi.Me`
    :return: list of dicts.
    :rtype: List[dict]

    Example::

        [
            {
                "block_contact": True,
                "me_full_block": False,
                "phone_number": 1234567890
            }
        ]
    """
    return meobj._make_request('get', '/main/settings/blocked-phone-numbers/')
