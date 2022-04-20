from typing import Tuple, List, Any

from meapi.exceptions import MeException


class Settings:
    def get_settings(self):
        """
        Get settings status
        :return: dict with settings
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-settings-py
        """
        return self.make_request('get', '/main/settings/')

    def change_social_settings(self,
                               mutual_contacts_available: bool = None,
                               who_watched_enabled: bool = None,
                               who_deleted_enabled: bool = None,
                               comments_enabled: bool = None,
                               location_enabled: bool = None,
                               language: str = None) -> Tuple[bool, List[str]]:
        """
        Change social settings
        :param mutual_contacts_available: show common contacts
        :param who_watched_enabled: show watched
        :param who_deleted_enabled: show deleted
        :param comments_enabled: allow comments
        :param location_enabled: allow location
        :param language: lang code, iw, en, etc.
        :return: (is success, list of failed)
        """
        args = locals()
        body = {}
        for setting, value in args.items():
            if value is not None and setting != 'self':
                body[setting] = value
                print(body)
        if not body:
            raise MeException("You need to provide at least one setting!")

        results = self.make_request('patch', '/main/settings/', body)
        failed = []
        for setting in body.keys():
            if results[setting] != body[setting]:
                failed.append(setting)
        return not bool(failed), failed

    def change_notification_settings(self,
                                     who_deleted_notification_enabled: bool = None,
                                     who_watched_notification_enabled: bool = None,
                                     distance_notification_enabled: bool = None,
                                     system_notification_enabled: bool = None,
                                     birthday_notification_enabled: bool = None,
                                     comments_notification_enabled: bool = None,
                                     names_notification_enabled: bool = None,
                                     notifications_enabled: bool = None) -> bool:
        """
        Set new settings for notifications
        :param who_deleted:
        :param who_watched:
        :param distance:
        :param system:
        :param birthday:
        :param comments:
        :param names:
        :param notifications:
        :return: is all changes successes
        """
        args = locals()
        body = {}
        for setting, value in args.items():
            if value is not None and setting != 'self':
                body[setting] = value
        if not body:
            raise MeException("You need to provide at least one setting!")

        results = self.make_request('patch', '/main/settings/', body)
        failed = []
        for setting in body.keys():
            if results[setting] != body[setting]:
                failed.append(setting)
        return True
