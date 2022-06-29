from datetime import datetime
from typing import Union
from meapi.utils.exceptions import MeException
from meapi.utils.helpers import parse_date
from meapi.models.me_model import MeModel
from meapi.models.user import User


class Comment(MeModel):
    """
    Represents a comment.

    Parameters:
        message (``str``):
            The message of the comment.
        id (``int``):
            The id of the comment.
        status (``str``):
            The status of the comment: ``approved``, ``ignored``, ``waiting``.
        author (:py:obj:`~meapi.models.user.User`):
            The creator of the comment.
        like_count (``int``):
            The number of likes of the comment.
        comment_likes (``list`` of :py:obj:`~meapi.models.user.User`):
            The list of users who liked the comment.
        created_at (``str``):
            The date of the comment creation.
        is_liked (``bool``):
            Whether the creator liked his comment.
        comments_blocked (``bool``):
            Whether the user blocked the comments of the comment.

    Methods:

    .. automethod:: approve
    .. automethod:: delete
    .. automethod:: edit
    .. automethod:: like
    .. automethod:: unlike
    """
    def __init__(self,
                 _meobj,
                 like_count: Union[int, None] = None,
                 status: Union[str, None] = None,
                 message: Union[str, None] = None,
                 author: Union[dict, None] = None,
                 is_liked: Union[bool, None] = None,
                 id: Union[int, None] = None,
                 comments_blocked: Union[bool, None] = None,
                 created_at: Union[str, None] = None,
                 comment_likes: Union[dict, None] = None,
                 profile_uuid: Union[str, None] = None,
                 _my_comment: bool = False
                 ):
        self.like_count = like_count
        self.status = status
        self.message = message
        self.author = User.new_from_json_dict(author)
        self.is_liked = is_liked
        self.id = id
        self.profile_uuid = profile_uuid
        self.comments_blocked = comments_blocked
        self.created_at: Union[datetime, None] = parse_date(created_at)
        self.comment_likes = [User.new_from_json_dict(user['author']) for user in
                              comment_likes] if comment_likes else None
        self.__meobj = _meobj
        self.__my_comment = _my_comment
        self.__init_done = True

    def approve(self) -> bool:
        """
        Approve the comment.
            - You can only approve comments that posted by others on your own profile.
            - The same as :py:func:`~meapi.Me.approve_comment`.

        Returns:
            ``bool``: Is approve success.
        """
        if not self.__my_comment:
            raise MeException("You can only approve others comments!")
        if self.status == 'approved':
            return True
        if self.id:
            if self.__meobj.approve_comment(self.id):
                self.status = 'approved'
                return True
        return False

    def edit(self, new_msg: str) -> bool:
        """
        Edit the comment.
            - You can only edit comments that posted by you.
            - The same as :py:func:`~meapi.Me.publish_comment`.

        Parameters:
            new_msg (``str``):
                The new message of the comment.

        Returns:
            ``bool``: Is edit success.
        """
        if self.author.uuid == self.__meobj.uuid:
            if self.__meobj.publish_comment(self.profile_uuid, new_msg):
                self.message = new_msg
                self.status = 'waiting'
                return True
            return False
        else:
            raise MeException("You can't edit others comments!")

    def delete(self) -> bool:
        """
        Ignore and hide the comment.
            - You can only ignore and hide comments that posted by others on your own profile.
            - The same as :py:func:`~meapi.Me.delete_comment`.

        Returns:
            ``bool``: Is delete success.
        """
        if not self.__my_comment:
            raise MeException("You can delete others comments!")
        if self.status == 'ignored':
            return True
        if self.id:
            if self.__meobj.delete_comment(self.id):
                self.status = 'ignored'
                return True
        return False

    def like(self) -> bool:
        """
        Like the comment.
            - The same as :py:func:`~meapi.Me.like_comment`.

        Returns:
            ``bool``: Is like success.
        """
        if self.status != 'approved':
            raise MeException("You can only like approved comments!")
        if self.__meobj.like_comment(self.id):
            self.like_count += 1
            return True
        return False

    def unlike(self) -> bool:
        """
        Unlike the comment.
            - The same as :py:func:`~meapi.Me.unlike_comment`.

        Returns:
            ``bool``: Is unlike success.
        """
        if self.status != 'approved':
            raise MeException("You can only unlike approved comments!")
        if self.__meobj.unlike_comment(self.id):
            self.like_count -= 1
            return True
        return False

    def __setattr__(self, key, value):
        if getattr(self, '_Comment__init_done', None):
            if key not in ['message', 'status', 'like_count', 'comment_likes']:
                raise MeException("You can't change this attr!")
        return super().__setattr__(key, value)

    def __repr__(self):
        return f"<Comment id={self.id} status={self.status} msg={self.message}>"

    def __str__(self):
        return self.message