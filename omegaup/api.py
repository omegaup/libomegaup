"""A Python implementation of an omegaUp API client.

The [omegaUp
API](https://github.com/omegaup/omegaup/blob/master/frontend/server/src/Controllers/README.md)
allows calling it using an API token (see the docs for `User.createAPIToken`)
that does not expire.  This API token can then be provided to the `Client`
constructor, which will then allow accessing the rest of the API functions.

Sample usage:

```python
import pprint

import omegaup.api

client = omegaup.api.Client(api_token='my API token')
session = client.session.currentSession()
pprint.pprint(session)
```
"""
import datetime
import logging
import urllib.parse

from typing import Any, BinaryIO, Dict, Iterable, Mapping, Optional

import requests

_DEFAULT_TIMEOUT = datetime.timedelta(minutes=1)


def _filterKeys(d: Mapping[str, Any], keys: Iterable[str]) -> Dict[str, Any]:
    """Returns a copy of the mapping with certain values redacted.

    Any of values mapped to the keys in the `keys` iterable will be replaced
    with the string '[REDACTED]'.
    """
    result: Dict[str, Any] = dict(d)
    for key in keys:
        if key in result:
            result[key] = '[REDACTED]'
    return result


ApiReturnType = Dict[str, Any]
"""The return type of any of the API requests."""


class Admin:
    r"""
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def platformReportStats(
            self,
            *,
            end_time: Optional[int] = None,
            start_time: Optional[int] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get stats for an overall platform report.

        Args:
            end_time:
            start_time:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if end_time is not None:
            parameters['end_time'] = str(end_time)
        if start_time is not None:
            parameters['start_time'] = str(start_time)
        return self._client.query('/api/admin/platformReportStats/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Authorization:
    r"""AuthorizationController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def problem(
            self,
            *,
            problem_alias: str,
            token: str,
            username: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            problem_alias:
            token:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
            'token': token,
        }
        if username is not None:
            parameters['username'] = str(username)
        return self._client.query('/api/authorization/problem/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Badge:
    r"""BadgesController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def list(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of existing badges

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/badge/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def myList(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of badges owned by current user

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/badge/myList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def userList(
            self,
            *,
            target_username: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of badges owned by a certain user

        Args:
            target_username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if target_username is not None:
            parameters['target_username'] = str(target_username)
        return self._client.query('/api/badge/userList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def myBadgeAssignationTime(
            self,
            *,
            badge_alias: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a the assignation timestamp of a badge
        for current user.

        Args:
            badge_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if badge_alias is not None:
            parameters['badge_alias'] = badge_alias
        return self._client.query('/api/badge/myBadgeAssignationTime/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def badgeDetails(
            self,
            *,
            badge_alias: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns the number of owners and the first
        assignation timestamp for a certain badge

        Args:
            badge_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if badge_alias is not None:
            parameters['badge_alias'] = badge_alias
        return self._client.query('/api/badge/badgeDetails/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Clarification:
    r"""Description of ClarificationController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def create(
            self,
            *,
            message: str,
            problem_alias: str,
            assignment_alias: Optional[str] = None,
            contest_alias: Optional[str] = None,
            course_alias: Optional[str] = None,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Creates a Clarification for a contest or an assignment of a course

        Args:
            message:
            problem_alias:
            assignment_alias:
            contest_alias:
            course_alias:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'message': message,
            'problem_alias': problem_alias,
        }
        if assignment_alias is not None:
            parameters['assignment_alias'] = assignment_alias
        if contest_alias is not None:
            parameters['contest_alias'] = contest_alias
        if course_alias is not None:
            parameters['course_alias'] = course_alias
        if username is not None:
            parameters['username'] = username
        return self._client.query('/api/clarification/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def details(
            self,
            *,
            clarification_id: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""API for getting a clarification

        Args:
            clarification_id:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'clarification_id': str(clarification_id),
        }
        return self._client.query('/api/clarification/details/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def update(
            self,
            *,
            clarification_id: int,
            answer: Optional[str] = None,
            message: Optional[str] = None,
            public: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Update a clarification

        Args:
            clarification_id:
            answer:
            message:
            public:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'clarification_id': str(clarification_id),
        }
        if answer is not None:
            parameters['answer'] = answer
        if message is not None:
            parameters['message'] = message
        if public is not None:
            parameters['public'] = str(public)
        return self._client.query('/api/clarification/update/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Contest:
    r"""ContestController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def list(
            self,
            *,
            page: int,
            page_size: int,
            query: str,
            tab_name: str,
            active: Optional[int] = None,
            admission_mode: Optional[Any] = None,
            participating: Optional[int] = None,
            recommended: Optional[int] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of contests

        Args:
            page:
            page_size:
            query:
            tab_name:
            active:
            admission_mode:
            participating:
            recommended:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'page': str(page),
            'page_size': str(page_size),
            'query': query,
            'tab_name': tab_name,
        }
        if active is not None:
            parameters['active'] = str(active)
        if admission_mode is not None:
            parameters['admission_mode'] = str(admission_mode)
        if participating is not None:
            parameters['participating'] = str(participating)
        if recommended is not None:
            parameters['recommended'] = str(recommended)
        return self._client.query('/api/contest/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def adminList(
            self,
            *,
            page: Optional[int] = None,
            page_size: Optional[int] = None,
            show_archived: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of contests where current user has admin rights (or is
        the director).

        Args:
            page:
            page_size:
            show_archived:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if page is not None:
            parameters['page'] = str(page)
        if page_size is not None:
            parameters['page_size'] = str(page_size)
        if show_archived is not None:
            parameters['show_archived'] = str(show_archived)
        return self._client.query('/api/contest/adminList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def myList(
            self,
            *,
            page: Optional[int] = None,
            page_size: Optional[int] = None,
            query: Optional[str] = None,
            show_archived: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of contests where current user is the director

        Args:
            page:
            page_size:
            query:
            show_archived:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if page is not None:
            parameters['page'] = str(page)
        if page_size is not None:
            parameters['page_size'] = str(page_size)
        if query is not None:
            parameters['query'] = query
        if show_archived is not None:
            parameters['show_archived'] = str(show_archived)
        return self._client.query('/api/contest/myList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def listParticipating(
            self,
            *,
            page: Optional[int] = None,
            page_size: Optional[int] = None,
            query: Optional[str] = None,
            show_archived: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of contests where current user is participating in

        Args:
            page:
            page_size:
            query:
            show_archived:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if page is not None:
            parameters['page'] = str(page)
        if page_size is not None:
            parameters['page_size'] = str(page_size)
        if query is not None:
            parameters['query'] = query
        if show_archived is not None:
            parameters['show_archived'] = str(show_archived)
        return self._client.query('/api/contest/listParticipating/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def publicDetails(
            self,
            *,
            contest_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            contest_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return self._client.query('/api/contest/publicDetails/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def registerForContest(
            self,
            *,
            contest_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            contest_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return self._client.query('/api/contest/registerForContest/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def open(
            self,
            *,
            contest_alias: str,
            privacy_git_object_id: str,
            statement_type: str,
            share_user_information: Optional[bool] = None,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Joins a contest - explicitly adds a identity to a contest.

        Args:
            contest_alias:
            privacy_git_object_id:
            statement_type:
            share_user_information:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'privacy_git_object_id': privacy_git_object_id,
            'statement_type': statement_type,
        }
        if share_user_information is not None:
            parameters['share_user_information'] = str(share_user_information)
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/contest/open/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def details(
            self,
            *,
            contest_alias: str,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns details of a Contest. Requesting the details of a contest will
        not start the current user into that contest. In order to participate
        in the contest, \OmegaUp\Controllers\Contest::apiOpen() must be used.

        Args:
            contest_alias:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/contest/details/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def adminDetails(
            self,
            *,
            contest_alias: str,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns details of a Contest, for administrators. This differs from
        apiDetails in the sense that it does not attempt to calculate the
        remaining time from the contest, or register the opened time.

        Args:
            contest_alias:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/contest/adminDetails/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def activityReport(
            self,
            *,
            contest_alias: str,
            length: Optional[int] = None,
            page: Optional[int] = None,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a report with all user activity for a contest.

        Args:
            contest_alias:
            length:
            page:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if length is not None:
            parameters['length'] = str(length)
        if page is not None:
            parameters['page'] = str(page)
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/contest/activityReport/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def clone(
            self,
            *,
            contest_alias: str,
            description: str,
            start_time: int,
            title: str,
            alias: Optional[str] = None,
            auth_token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Clone a contest

        Args:
            contest_alias:
            description:
            start_time:
            title:
            alias:
            auth_token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'description': description,
            'start_time': str(start_time),
            'title': title,
        }
        if alias is not None:
            parameters['alias'] = alias
        if auth_token is not None:
            parameters['auth_token'] = auth_token
        return self._client.query('/api/contest/clone/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def createVirtual(
            self,
            *,
            alias: str,
            start_time: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            alias:
            start_time:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'start_time': str(start_time),
        }
        return self._client.query('/api/contest/createVirtual/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def create(
            self,
            *,
            admission_mode: Optional[Any] = None,
            alias: Optional[Any] = None,
            contest_for_teams: Optional[bool] = None,
            description: Optional[Any] = None,
            feedback: Optional[Any] = None,
            finish_time: Optional[Any] = None,
            languages: Optional[Any] = None,
            needs_basic_information: Optional[bool] = None,
            partial_score: Optional[bool] = None,
            penalty: Optional[Any] = None,
            penalty_calc_policy: Optional[Any] = None,
            penalty_type: Optional[Any] = None,
            points_decay_factor: Optional[Any] = None,
            problems: Optional[str] = None,
            requests_user_information: Optional[Any] = None,
            scoreboard: Optional[Any] = None,
            show_scoreboard_after: Optional[Any] = None,
            start_time: Optional[Any] = None,
            submissions_gap: Optional[Any] = None,
            teams_group_alias: Optional[str] = None,
            title: Optional[Any] = None,
            window_length: Optional[int] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Creates a new contest

        Args:
            admission_mode:
            alias:
            contest_for_teams:
            description:
            feedback:
            finish_time:
            languages:
            needs_basic_information:
            partial_score:
            penalty:
            penalty_calc_policy:
            penalty_type:
            points_decay_factor:
            problems:
            requests_user_information:
            scoreboard:
            show_scoreboard_after:
            start_time:
            submissions_gap:
            teams_group_alias:
            title:
            window_length:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if admission_mode is not None:
            parameters['admission_mode'] = str(admission_mode)
        if alias is not None:
            parameters['alias'] = str(alias)
        if contest_for_teams is not None:
            parameters['contest_for_teams'] = str(contest_for_teams)
        if description is not None:
            parameters['description'] = str(description)
        if feedback is not None:
            parameters['feedback'] = str(feedback)
        if finish_time is not None:
            parameters['finish_time'] = str(finish_time)
        if languages is not None:
            parameters['languages'] = str(languages)
        if needs_basic_information is not None:
            parameters['needs_basic_information'] = str(
                needs_basic_information)
        if partial_score is not None:
            parameters['partial_score'] = str(partial_score)
        if penalty is not None:
            parameters['penalty'] = str(penalty)
        if penalty_calc_policy is not None:
            parameters['penalty_calc_policy'] = str(penalty_calc_policy)
        if penalty_type is not None:
            parameters['penalty_type'] = str(penalty_type)
        if points_decay_factor is not None:
            parameters['points_decay_factor'] = str(points_decay_factor)
        if problems is not None:
            parameters['problems'] = problems
        if requests_user_information is not None:
            parameters['requests_user_information'] = str(
                requests_user_information)
        if scoreboard is not None:
            parameters['scoreboard'] = str(scoreboard)
        if show_scoreboard_after is not None:
            parameters['show_scoreboard_after'] = str(show_scoreboard_after)
        if start_time is not None:
            parameters['start_time'] = str(start_time)
        if submissions_gap is not None:
            parameters['submissions_gap'] = str(submissions_gap)
        if teams_group_alias is not None:
            parameters['teams_group_alias'] = teams_group_alias
        if title is not None:
            parameters['title'] = str(title)
        if window_length is not None:
            parameters['window_length'] = str(window_length)
        return self._client.query('/api/contest/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def problems(
            self,
            *,
            contest_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets the problems from a contest

        Args:
            contest_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return self._client.query('/api/contest/problems/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addProblem(
            self,
            *,
            contest_alias: str,
            order_in_contest: int,
            points: float,
            problem_alias: str,
            commit: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds a problem to a contest

        Args:
            contest_alias:
            order_in_contest:
            points:
            problem_alias:
            commit:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'order_in_contest': str(order_in_contest),
            'points': str(points),
            'problem_alias': problem_alias,
        }
        if commit is not None:
            parameters['commit'] = commit
        return self._client.query('/api/contest/addProblem/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeProblem(
            self,
            *,
            contest_alias: str,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes a problem from a contest

        Args:
            contest_alias:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/contest/removeProblem/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def runsDiff(
            self,
            *,
            contest_alias: str,
            version: str,
            problem_alias: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Return a report of which runs would change due to a version change.

        Args:
            contest_alias:
            version:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'version': version,
        }
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        return self._client.query('/api/contest/runsDiff/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addUser(
            self,
            *,
            contest_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds a user to a contest.
        By default, any user can view details of public contests.
        Only users added through this API can view private contests

        Args:
            contest_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/contest/addUser/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeUser(
            self,
            *,
            contest_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Remove a user from a private contest

        Args:
            contest_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/contest/removeUser/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def replaceTeamsGroup(
            self,
            *,
            contest_alias: str,
            teams_group_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Replace the teams group assigned to a contest

        Args:
            contest_alias: The alias of the contest
            teams_group_alias: The alias of the teams group

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'teams_group_alias': teams_group_alias,
        }
        return self._client.query('/api/contest/replaceTeamsGroup/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addGroup(
            self,
            *,
            contest_alias: str,
            group: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds a group to a contest

        Args:
            contest_alias:
            group:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group': group,
        }
        return self._client.query('/api/contest/addGroup/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeGroup(
            self,
            *,
            contest_alias: str,
            group: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes a group from a contest

        Args:
            contest_alias:
            group:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group': group,
        }
        return self._client.query('/api/contest/removeGroup/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addAdmin(
            self,
            *,
            contest_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds an admin to a contest

        Args:
            contest_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/contest/addAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeAdmin(
            self,
            *,
            contest_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes an admin from a contest

        Args:
            contest_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/contest/removeAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addGroupAdmin(
            self,
            *,
            contest_alias: str,
            group: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds a group admin to a contest

        Args:
            contest_alias:
            group:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group': group,
        }
        return self._client.query('/api/contest/addGroupAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeGroupAdmin(
            self,
            *,
            contest_alias: str,
            group: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes a group admin from a contest

        Args:
            contest_alias:
            group:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group': group,
        }
        return self._client.query('/api/contest/removeGroupAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def clarifications(
            self,
            *,
            contest_alias: str,
            offset: int,
            rowcount: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get clarifications of a contest

        Args:
            contest_alias:
            offset:
            rowcount:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'offset': str(offset),
            'rowcount': str(rowcount),
        }
        return self._client.query('/api/contest/clarifications/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def problemClarifications(
            self,
            *,
            contest_alias: str,
            offset: int,
            problem_alias: str,
            rowcount: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get clarifications of problem in a contest

        Args:
            contest_alias:
            offset:
            problem_alias:
            rowcount:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'offset': str(offset),
            'problem_alias': problem_alias,
            'rowcount': str(rowcount),
        }
        return self._client.query('/api/contest/problemClarifications/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def scoreboardEvents(
            self,
            *,
            contest_alias: str,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns the Scoreboard events

        Args:
            contest_alias:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/contest/scoreboardEvents/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def scoreboard(
            self,
            *,
            contest_alias: str,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns the Scoreboard

        Args:
            contest_alias:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/contest/scoreboard/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def scoreboardMerge(
            self,
            *,
            contest_aliases: str,
            contest_params: Optional[Any] = None,
            usernames_filter: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets the accomulative scoreboard for an array of contests

        Args:
            contest_aliases:
            contest_params:
            usernames_filter:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_aliases': contest_aliases,
        }
        if contest_params is not None:
            parameters['contest_params'] = str(contest_params)
        if usernames_filter is not None:
            parameters['usernames_filter'] = usernames_filter
        return self._client.query('/api/contest/scoreboardMerge/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def requests(
            self,
            *,
            contest_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            contest_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return self._client.query('/api/contest/requests/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def arbitrateRequest(
            self,
            *,
            contest_alias: str,
            username: str,
            note: Optional[str] = None,
            resolution: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            contest_alias:
            username:
            note:
            resolution:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'username': username,
        }
        if note is not None:
            parameters['note'] = note
        if resolution is not None:
            parameters['resolution'] = str(resolution)
        return self._client.query('/api/contest/arbitrateRequest/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def users(
            self,
            *,
            contest_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns ALL identities participating in a contest

        Args:
            contest_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return self._client.query('/api/contest/users/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def searchUsers(
            self,
            *,
            contest_alias: str,
            query: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Search users in contest

        Args:
            contest_alias:
            query:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if query is not None:
            parameters['query'] = query
        return self._client.query('/api/contest/searchUsers/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def admins(
            self,
            *,
            contest_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns all contest administrators

        Args:
            contest_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return self._client.query('/api/contest/admins/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def update(
            self,
            *,
            contest_alias: str,
            finish_time: int,
            submissions_gap: int,
            window_length: int,
            admission_mode: Optional[str] = None,
            alias: Optional[str] = None,
            contest_for_teams: Optional[bool] = None,
            default_show_all_contestants_in_scoreboard: Optional[bool] = None,
            description: Optional[str] = None,
            feedback: Optional[Any] = None,
            languages: Optional[Any] = None,
            needs_basic_information: Optional[bool] = None,
            partial_score: Optional[bool] = None,
            penalty: Optional[int] = None,
            penalty_calc_policy: Optional[Any] = None,
            penalty_type: Optional[Any] = None,
            points_decay_factor: Optional[float] = None,
            problems: Optional[str] = None,
            requests_user_information: Optional[str] = None,
            scoreboard: Optional[float] = None,
            show_scoreboard_after: Optional[bool] = None,
            start_time: Optional[datetime.datetime] = None,
            teams_group_alias: Optional[str] = None,
            title: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Update a Contest

        Args:
            contest_alias:
            finish_time:
            submissions_gap:
            window_length:
            admission_mode:
            alias:
            contest_for_teams:
            default_show_all_contestants_in_scoreboard:
            description:
            feedback:
            languages:
            needs_basic_information:
            partial_score:
            penalty:
            penalty_calc_policy:
            penalty_type:
            points_decay_factor:
            problems:
            requests_user_information:
            scoreboard:
            show_scoreboard_after:
            start_time:
            teams_group_alias:
            title:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'finish_time': str(finish_time),
            'submissions_gap': str(submissions_gap),
            'window_length': str(window_length),
        }
        if admission_mode is not None:
            parameters['admission_mode'] = admission_mode
        if alias is not None:
            parameters['alias'] = alias
        if contest_for_teams is not None:
            parameters['contest_for_teams'] = str(contest_for_teams)
        if default_show_all_contestants_in_scoreboard is not None:
            parameters['default_show_all_contestants_in_scoreboard'] = str(
                default_show_all_contestants_in_scoreboard)
        if description is not None:
            parameters['description'] = description
        if feedback is not None:
            parameters['feedback'] = str(feedback)
        if languages is not None:
            parameters['languages'] = str(languages)
        if needs_basic_information is not None:
            parameters['needs_basic_information'] = str(
                needs_basic_information)
        if partial_score is not None:
            parameters['partial_score'] = str(partial_score)
        if penalty is not None:
            parameters['penalty'] = str(penalty)
        if penalty_calc_policy is not None:
            parameters['penalty_calc_policy'] = str(penalty_calc_policy)
        if penalty_type is not None:
            parameters['penalty_type'] = str(penalty_type)
        if points_decay_factor is not None:
            parameters['points_decay_factor'] = str(points_decay_factor)
        if problems is not None:
            parameters['problems'] = problems
        if requests_user_information is not None:
            parameters['requests_user_information'] = requests_user_information
        if scoreboard is not None:
            parameters['scoreboard'] = str(scoreboard)
        if show_scoreboard_after is not None:
            parameters['show_scoreboard_after'] = str(show_scoreboard_after)
        if start_time is not None:
            parameters['start_time'] = str(int(start_time.timestamp()))
        if teams_group_alias is not None:
            parameters['teams_group_alias'] = teams_group_alias
        if title is not None:
            parameters['title'] = title
        return self._client.query('/api/contest/update/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def updateEndTimeForIdentity(
            self,
            *,
            contest_alias: str,
            end_time: datetime.datetime,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Update Contest end time for an identity when window_length
        option is turned on

        Args:
            contest_alias:
            end_time:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'end_time': str(int(end_time.timestamp())),
            'username': username,
        }
        return self._client.query('/api/contest/updateEndTimeForIdentity/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def runs(
            self,
            *,
            contest_alias: str,
            problem_alias: str,
            language: Optional[str] = None,
            offset: Optional[int] = None,
            rowcount: Optional[int] = None,
            status: Optional[str] = None,
            username: Optional[str] = None,
            verdict: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns all runs for a contest

        Args:
            contest_alias:
            problem_alias:
            language:
            offset:
            rowcount:
            status:
            username:
            verdict:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'problem_alias': problem_alias,
        }
        if language is not None:
            parameters['language'] = language
        if offset is not None:
            parameters['offset'] = str(offset)
        if rowcount is not None:
            parameters['rowcount'] = str(rowcount)
        if status is not None:
            parameters['status'] = status
        if username is not None:
            parameters['username'] = username
        if verdict is not None:
            parameters['verdict'] = verdict
        return self._client.query('/api/contest/runs/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def stats(
            self,
            *,
            contest_alias: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Stats of a contest

        Args:
            contest_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if contest_alias is not None:
            parameters['contest_alias'] = contest_alias
        return self._client.query('/api/contest/stats/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def report(
            self,
            *,
            contest_alias: str,
            auth_token: Optional[str] = None,
            filterBy: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a detailed report of the contest

        Args:
            contest_alias:
            auth_token:
            filterBy:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if auth_token is not None:
            parameters['auth_token'] = auth_token
        if filterBy is not None:
            parameters['filterBy'] = filterBy
        return self._client.query('/api/contest/report/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def role(
            self,
            *,
            contest_alias: str,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            contest_alias:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/contest/role/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def setRecommended(
            self,
            *,
            contest_alias: str,
            value: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Given a contest_alias, sets the recommended flag on/off.
        Only omegaUp admins can call this API.

        Args:
            contest_alias:
            value:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if value is not None:
            parameters['value'] = str(value)
        return self._client.query('/api/contest/setRecommended/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def contestants(
            self,
            *,
            contest_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Return users who participate in a contest, as long as contest admin
        has chosen to ask for users information and contestants have
        previously agreed to share their information.

        Args:
            contest_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return self._client.query('/api/contest/contestants/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def archive(
            self,
            *,
            contest_alias: str,
            archive: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Archives or Unarchives a contest if user is the creator

        Args:
            contest_alias:
            archive:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if archive is not None:
            parameters['archive'] = str(archive)
        return self._client.query('/api/contest/archive/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Course:
    r"""CourseController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def generateTokenForCloneCourse(
            self,
            *,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/generateTokenForCloneCourse/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def clone(
            self,
            *,
            alias: str,
            course_alias: str,
            name: str,
            start_time: datetime.datetime,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Clone a course

        Args:
            alias:
            course_alias:
            name:
            start_time:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'course_alias': course_alias,
            'name': name,
            'start_time': str(int(start_time.timestamp())),
        }
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/course/clone/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def create(
            self,
            *,
            admission_mode: Optional[Any] = None,
            alias: Optional[Any] = None,
            description: Optional[Any] = None,
            finish_time: Optional[Any] = None,
            languages: Optional[Any] = None,
            level: Optional[str] = None,
            name: Optional[Any] = None,
            needs_basic_information: Optional[Any] = None,
            objective: Optional[str] = None,
            public: Optional[Any] = None,
            requests_user_information: Optional[Any] = None,
            school_id: Optional[Any] = None,
            show_scoreboard: Optional[Any] = None,
            start_time: Optional[Any] = None,
            unlimited_duration: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Create new course API

        Args:
            admission_mode:
            alias:
            description:
            finish_time:
            languages:
            level:
            name:
            needs_basic_information:
            objective:
            public:
            requests_user_information:
            school_id:
            show_scoreboard:
            start_time:
            unlimited_duration:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if admission_mode is not None:
            parameters['admission_mode'] = str(admission_mode)
        if alias is not None:
            parameters['alias'] = str(alias)
        if description is not None:
            parameters['description'] = str(description)
        if finish_time is not None:
            parameters['finish_time'] = str(finish_time)
        if languages is not None:
            parameters['languages'] = str(languages)
        if level is not None:
            parameters['level'] = level
        if name is not None:
            parameters['name'] = str(name)
        if needs_basic_information is not None:
            parameters['needs_basic_information'] = str(
                needs_basic_information)
        if objective is not None:
            parameters['objective'] = objective
        if public is not None:
            parameters['public'] = str(public)
        if requests_user_information is not None:
            parameters['requests_user_information'] = str(
                requests_user_information)
        if school_id is not None:
            parameters['school_id'] = str(school_id)
        if show_scoreboard is not None:
            parameters['show_scoreboard'] = str(show_scoreboard)
        if start_time is not None:
            parameters['start_time'] = str(start_time)
        if unlimited_duration is not None:
            parameters['unlimited_duration'] = str(unlimited_duration)
        return self._client.query('/api/course/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def createAssignment(
            self,
            *,
            course_alias: str,
            alias: Optional[Any] = None,
            assignment_type: Optional[Any] = None,
            description: Optional[Any] = None,
            finish_time: Optional[Any] = None,
            name: Optional[Any] = None,
            order: Optional[int] = None,
            problems: Optional[str] = None,
            publish_time_delay: Optional[Any] = None,
            start_time: Optional[Any] = None,
            unlimited_duration: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""API to Create an assignment

        Args:
            course_alias:
            alias:
            assignment_type:
            description:
            finish_time:
            name:
            order:
            problems:
            publish_time_delay:
            start_time:
            unlimited_duration:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        if alias is not None:
            parameters['alias'] = str(alias)
        if assignment_type is not None:
            parameters['assignment_type'] = str(assignment_type)
        if description is not None:
            parameters['description'] = str(description)
        if finish_time is not None:
            parameters['finish_time'] = str(finish_time)
        if name is not None:
            parameters['name'] = str(name)
        if order is not None:
            parameters['order'] = str(order)
        if problems is not None:
            parameters['problems'] = problems
        if publish_time_delay is not None:
            parameters['publish_time_delay'] = str(publish_time_delay)
        if start_time is not None:
            parameters['start_time'] = str(start_time)
        if unlimited_duration is not None:
            parameters['unlimited_duration'] = str(unlimited_duration)
        return self._client.query('/api/course/createAssignment/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def updateAssignment(
            self,
            *,
            assignment: str,
            course: str,
            finish_time: datetime.datetime,
            start_time: datetime.datetime,
            unlimited_duration: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Update an assignment

        Args:
            assignment:
            course:
            finish_time:
            start_time:
            unlimited_duration:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'course': course,
            'finish_time': str(int(finish_time.timestamp())),
            'start_time': str(int(start_time.timestamp())),
        }
        if unlimited_duration is not None:
            parameters['unlimited_duration'] = str(unlimited_duration)
        return self._client.query('/api/course/updateAssignment/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addProblem(
            self,
            *,
            assignment_alias: str,
            course_alias: str,
            points: float,
            problem_alias: str,
            commit: Optional[str] = None,
            is_extra_problem: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds a problem to an assignment

        Args:
            assignment_alias:
            course_alias:
            points:
            problem_alias:
            commit:
            is_extra_problem:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'points': str(points),
            'problem_alias': problem_alias,
        }
        if commit is not None:
            parameters['commit'] = commit
        if is_extra_problem is not None:
            parameters['is_extra_problem'] = str(is_extra_problem)
        return self._client.query('/api/course/addProblem/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def updateProblemsOrder(
            self,
            *,
            assignment_alias: str,
            course_alias: str,
            problems: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            assignment_alias:
            course_alias:
            problems:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'problems': problems,
        }
        return self._client.query('/api/course/updateProblemsOrder/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def updateAssignmentsOrder(
            self,
            *,
            assignments: str,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            assignments:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignments': assignments,
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/updateAssignmentsOrder/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def getProblemUsers(
            self,
            *,
            course_alias: str,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            course_alias:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/course/getProblemUsers/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeProblem(
            self,
            *,
            assignment_alias: str,
            course_alias: str,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Remove a problem from an assignment

        Args:
            assignment_alias:
            course_alias:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/course/removeProblem/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def listAssignments(
            self,
            *,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""List course assignments

        Args:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/listAssignments/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeAssignment(
            self,
            *,
            assignment_alias: str,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Remove an assignment from a course

        Args:
            assignment_alias:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/removeAssignment/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def requests(
            self,
            *,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns the list of requests made by participants who are interested to
        join the course

        Args:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/requests/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def arbitrateRequest(
            self,
            *,
            course_alias: str,
            resolution: bool,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Stores the resolution given to a certain request made by a contestant
        interested to join the course.

        Args:
            course_alias:
            resolution:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'resolution': str(resolution),
            'username': username,
        }
        return self._client.query('/api/course/arbitrateRequest/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def listStudents(
            self,
            *,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""List students in a course

        Args:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/listStudents/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def studentProgress(
            self,
            *,
            assignment_alias: str,
            course_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            assignment_alias:
            course_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/course/studentProgress/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def myProgress(
            self,
            *,
            alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns details of a given course

        Args:
            alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
        }
        return self._client.query('/api/course/myProgress/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addStudent(
            self,
            *,
            accept_teacher_git_object_id: str,
            course_alias: str,
            privacy_git_object_id: str,
            share_user_information: bool,
            statement_type: str,
            usernameOrEmail: str,
            accept_teacher: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Add Student to Course.

        Args:
            accept_teacher_git_object_id:
            course_alias:
            privacy_git_object_id:
            share_user_information:
            statement_type:
            usernameOrEmail:
            accept_teacher:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'accept_teacher_git_object_id': accept_teacher_git_object_id,
            'course_alias': course_alias,
            'privacy_git_object_id': privacy_git_object_id,
            'share_user_information': str(share_user_information),
            'statement_type': statement_type,
            'usernameOrEmail': usernameOrEmail,
        }
        if accept_teacher is not None:
            parameters['accept_teacher'] = str(accept_teacher)
        return self._client.query('/api/course/addStudent/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeStudent(
            self,
            *,
            course_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Remove Student from Course

        Args:
            course_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/course/removeStudent/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def admins(
            self,
            *,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns all course administrators

        Args:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/admins/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addAdmin(
            self,
            *,
            course_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds an admin to a course

        Args:
            course_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/course/addAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeAdmin(
            self,
            *,
            course_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes an admin from a course

        Args:
            course_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/course/removeAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addGroupAdmin(
            self,
            *,
            course_alias: str,
            group: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds an group admin to a course

        Args:
            course_alias:
            group:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'group': group,
        }
        return self._client.query('/api/course/addGroupAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeGroupAdmin(
            self,
            *,
            course_alias: str,
            group: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes a group admin from a course

        Args:
            course_alias:
            group:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'group': group,
        }
        return self._client.query('/api/course/removeGroupAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def introDetails(
            self,
            *,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Show course intro only on public courses when user is not yet registered

        Args:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/introDetails/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def studentsProgress(
            self,
            *,
            course: str,
            length: int,
            page: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            course:
            length:
            page:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course': course,
            'length': str(length),
            'page': str(page),
        }
        return self._client.query('/api/course/studentsProgress/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def registerForCourse(
            self,
            *,
            course_alias: str,
            accept_teacher: Optional[bool] = None,
            share_user_information: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            course_alias:
            accept_teacher:
            share_user_information:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        if accept_teacher is not None:
            parameters['accept_teacher'] = str(accept_teacher)
        if share_user_information is not None:
            parameters['share_user_information'] = str(share_user_information)
        return self._client.query('/api/course/registerForCourse/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def adminDetails(
            self,
            *,
            alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns all details of a given Course

        Args:
            alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
        }
        return self._client.query('/api/course/adminDetails/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def activityReport(
            self,
            *,
            course_alias: str,
            length: Optional[int] = None,
            page: Optional[int] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a report with all user activity for a course.

        Args:
            course_alias:
            length:
            page:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        if length is not None:
            parameters['length'] = str(length)
        if page is not None:
            parameters['page'] = str(page)
        return self._client.query('/api/course/activityReport/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def archive(
            self,
            *,
            archive: bool,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Archives or un-archives a course

        Args:
            archive:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'archive': str(archive),
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/archive/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def assignmentDetails(
            self,
            *,
            assignment: str,
            course: str,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns details of a given assignment

        Args:
            assignment:
            course:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'course': course,
        }
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/course/assignmentDetails/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def runs(
            self,
            *,
            assignment_alias: str,
            course_alias: str,
            language: Optional[str] = None,
            offset: Optional[int] = None,
            problem_alias: Optional[str] = None,
            rowcount: Optional[int] = None,
            status: Optional[str] = None,
            username: Optional[str] = None,
            verdict: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns all runs for a course

        Args:
            assignment_alias:
            course_alias:
            language:
            offset:
            problem_alias:
            rowcount:
            status:
            username:
            verdict:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
        }
        if language is not None:
            parameters['language'] = language
        if offset is not None:
            parameters['offset'] = str(offset)
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        if rowcount is not None:
            parameters['rowcount'] = str(rowcount)
        if status is not None:
            parameters['status'] = status
        if username is not None:
            parameters['username'] = username
        if verdict is not None:
            parameters['verdict'] = verdict
        return self._client.query('/api/course/runs/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def details(
            self,
            *,
            alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns details of a given course

        Args:
            alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
        }
        return self._client.query('/api/course/details/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def update(
            self,
            *,
            alias: str,
            languages: str,
            school_id: int,
            admission_mode: Optional[str] = None,
            description: Optional[str] = None,
            finish_time: Optional[datetime.datetime] = None,
            level: Optional[str] = None,
            name: Optional[str] = None,
            needs_basic_information: Optional[bool] = None,
            objective: Optional[str] = None,
            requests_user_information: Optional[str] = None,
            show_scoreboard: Optional[bool] = None,
            start_time: Optional[datetime.datetime] = None,
            unlimited_duration: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Edit Course contents

        Args:
            alias:
            languages:
            school_id:
            admission_mode:
            description:
            finish_time:
            level:
            name:
            needs_basic_information:
            objective:
            requests_user_information:
            show_scoreboard:
            start_time:
            unlimited_duration:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'languages': languages,
            'school_id': str(school_id),
        }
        if admission_mode is not None:
            parameters['admission_mode'] = admission_mode
        if description is not None:
            parameters['description'] = description
        if finish_time is not None:
            parameters['finish_time'] = str(int(finish_time.timestamp()))
        if level is not None:
            parameters['level'] = level
        if name is not None:
            parameters['name'] = name
        if needs_basic_information is not None:
            parameters['needs_basic_information'] = str(
                needs_basic_information)
        if objective is not None:
            parameters['objective'] = objective
        if requests_user_information is not None:
            parameters['requests_user_information'] = requests_user_information
        if show_scoreboard is not None:
            parameters['show_scoreboard'] = str(show_scoreboard)
        if start_time is not None:
            parameters['start_time'] = str(int(start_time.timestamp()))
        if unlimited_duration is not None:
            parameters['unlimited_duration'] = str(unlimited_duration)
        return self._client.query('/api/course/update/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def clarifications(
            self,
            *,
            course_alias: str,
            offset: int,
            rowcount: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets the clarifications of all assignments in a course

        Args:
            course_alias:
            offset:
            rowcount:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'offset': str(offset),
            'rowcount': str(rowcount),
        }
        return self._client.query('/api/course/clarifications/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def problemClarifications(
            self,
            *,
            assignment_alias: str,
            course_alias: str,
            offset: int,
            problem_alias: str,
            rowcount: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get clarifications of problem in a contest

        Args:
            assignment_alias:
            course_alias:
            offset:
            problem_alias:
            rowcount:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'offset': str(offset),
            'problem_alias': problem_alias,
            'rowcount': str(rowcount),
        }
        return self._client.query('/api/course/problemClarifications/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def assignmentScoreboard(
            self,
            *,
            assignment: str,
            course: str,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets Scoreboard for an assignment

        Args:
            assignment:
            course:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'course': course,
        }
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/course/assignmentScoreboard/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def assignmentScoreboardEvents(
            self,
            *,
            assignment: str,
            course: str,
            token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns the Scoreboard events

        Args:
            assignment:
            course:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'course': course,
        }
        if token is not None:
            parameters['token'] = token
        return self._client.query('/api/course/assignmentScoreboardEvents/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def listSolvedProblems(
            self,
            *,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get Problems solved by users of a course

        Args:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/listSolvedProblems/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def listUnsolvedProblems(
            self,
            *,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get Problems unsolved by users of a course

        Args:
            course_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return self._client.query('/api/course/listUnsolvedProblems/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Grader:
    r"""Description of GraderController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def status(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Calls to /status grader

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/grader/status/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Group:
    r"""GroupController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def create(
            self,
            *,
            alias: str,
            description: str,
            name: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""New group

        Args:
            alias:
            description:
            name:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'description': description,
            'name': name,
        }
        return self._client.query('/api/group/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def update(
            self,
            *,
            alias: str,
            description: str,
            name: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Update an existing group

        Args:
            alias:
            description:
            name:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'description': description,
            'name': name,
        }
        return self._client.query('/api/group/update/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addUser(
            self,
            *,
            group_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Add identity to group

        Args:
            group_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/group/addUser/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeUser(
            self,
            *,
            group_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Remove user from group

        Args:
            group_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/group/removeUser/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def myList(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of groups by owner

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/group/myList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def list(
            self,
            *,
            query: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of groups that match a partial name. This returns an
        array instead of an object since it is used by typeahead.

        Args:
            query:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if query is not None:
            parameters['query'] = query
        return self._client.query('/api/group/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def details(
            self,
            *,
            group_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Details of a group (scoreboards)

        Args:
            group_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
        }
        return self._client.query('/api/group/details/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def members(
            self,
            *,
            group_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Members of a group (usernames only).

        Args:
            group_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
        }
        return self._client.query('/api/group/members/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def createScoreboard(
            self,
            *,
            group_alias: str,
            name: str,
            alias: Optional[str] = None,
            description: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Create a scoreboard set to a group

        Args:
            group_alias:
            name:
            alias:
            description:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
            'name': name,
        }
        if alias is not None:
            parameters['alias'] = alias
        if description is not None:
            parameters['description'] = description
        return self._client.query('/api/group/createScoreboard/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class GroupScoreboard:
    r"""GroupScoreboardController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def addContest(
            self,
            *,
            contest_alias: str,
            group_alias: str,
            scoreboard_alias: str,
            weight: float,
            only_ac: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Add contest to a group scoreboard

        Args:
            contest_alias:
            group_alias:
            scoreboard_alias:
            weight:
            only_ac:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group_alias': group_alias,
            'scoreboard_alias': scoreboard_alias,
            'weight': str(weight),
        }
        if only_ac is not None:
            parameters['only_ac'] = str(only_ac)
        return self._client.query('/api/groupScoreboard/addContest/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeContest(
            self,
            *,
            contest_alias: str,
            group_alias: str,
            scoreboard_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Add contest to a group scoreboard

        Args:
            contest_alias:
            group_alias:
            scoreboard_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group_alias': group_alias,
            'scoreboard_alias': scoreboard_alias,
        }
        return self._client.query('/api/groupScoreboard/removeContest/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def details(
            self,
            *,
            group_alias: str,
            scoreboard_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Details of a scoreboard. Returns a list with all contests that belong to
        the given scoreboard_alias

        Args:
            group_alias:
            scoreboard_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
            'scoreboard_alias': scoreboard_alias,
        }
        return self._client.query('/api/groupScoreboard/details/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def list(
            self,
            *,
            group_alias: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Details of a scoreboard

        Args:
            group_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if group_alias is not None:
            parameters['group_alias'] = group_alias
        return self._client.query('/api/groupScoreboard/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Identity:
    r"""IdentityController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def create(
            self,
            *,
            gender: str,
            name: str,
            password: str,
            school_name: str,
            username: str,
            country_id: Optional[str] = None,
            group_alias: Optional[str] = None,
            identities: Optional[Any] = None,
            state_id: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for Create an Identity API

        Args:
            gender:
            name:
            password:
            school_name:
            username:
            country_id:
            group_alias:
            identities:
            state_id:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'gender': gender,
            'name': name,
            'password': password,
            'school_name': school_name,
            'username': username,
        }
        if country_id is not None:
            parameters['country_id'] = country_id
        if group_alias is not None:
            parameters['group_alias'] = group_alias
        if identities is not None:
            parameters['identities'] = str(identities)
        if state_id is not None:
            parameters['state_id'] = state_id
        return self._client.query('/api/identity/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def bulkCreate(
            self,
            *,
            identities: str,
            group_alias: Optional[str] = None,
            name: Optional[Any] = None,
            username: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for Create bulk Identities API

        Args:
            identities:
            group_alias:
            name:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'identities': identities,
        }
        if group_alias is not None:
            parameters['group_alias'] = group_alias
        if name is not None:
            parameters['name'] = str(name)
        if username is not None:
            parameters['username'] = str(username)
        return self._client.query('/api/identity/bulkCreate/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def bulkCreateForTeams(
            self,
            *,
            team_group_alias: str,
            team_identities: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for Create bulk Identities for teams API

        Args:
            team_group_alias:
            team_identities:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
            'team_identities': team_identities,
        }
        return self._client.query('/api/identity/bulkCreateForTeams/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def updateIdentityTeam(
            self,
            *,
            gender: str,
            group_alias: str,
            name: str,
            original_username: str,
            school_name: str,
            username: str,
            country_id: Optional[str] = None,
            identities: Optional[Any] = None,
            state_id: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for Update an Identity team API

        Args:
            gender:
            group_alias:
            name:
            original_username:
            school_name:
            username:
            country_id:
            identities:
            state_id:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'gender': gender,
            'group_alias': group_alias,
            'name': name,
            'original_username': original_username,
            'school_name': school_name,
            'username': username,
        }
        if country_id is not None:
            parameters['country_id'] = country_id
        if identities is not None:
            parameters['identities'] = str(identities)
        if state_id is not None:
            parameters['state_id'] = state_id
        return self._client.query('/api/identity/updateIdentityTeam/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def update(
            self,
            *,
            gender: str,
            group_alias: str,
            name: str,
            original_username: str,
            school_name: str,
            username: str,
            country_id: Optional[str] = None,
            identities: Optional[Any] = None,
            state_id: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for Update an Identity API

        Args:
            gender:
            group_alias:
            name:
            original_username:
            school_name:
            username:
            country_id:
            identities:
            state_id:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'gender': gender,
            'group_alias': group_alias,
            'name': name,
            'original_username': original_username,
            'school_name': school_name,
            'username': username,
        }
        if country_id is not None:
            parameters['country_id'] = country_id
        if identities is not None:
            parameters['identities'] = str(identities)
        if state_id is not None:
            parameters['state_id'] = state_id
        return self._client.query('/api/identity/update/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def changePassword(
            self,
            *,
            group_alias: str,
            password: str,
            username: str,
            identities: Optional[Any] = None,
            name: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for change passowrd of an identity

        Args:
            group_alias:
            password:
            username:
            identities:
            name:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
            'password': password,
            'username': username,
        }
        if identities is not None:
            parameters['identities'] = str(identities)
        if name is not None:
            parameters['name'] = str(name)
        return self._client.query('/api/identity/changePassword/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def selectIdentity(
            self,
            *,
            usernameOrEmail: str,
            auth_token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for switching between associated identities for a user

        Args:
            usernameOrEmail:
            auth_token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'usernameOrEmail': usernameOrEmail,
        }
        if auth_token is not None:
            parameters['auth_token'] = auth_token
        return self._client.query('/api/identity/selectIdentity/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Notification:
    r"""BadgesController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def myList(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of unread notifications for user

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/notification/myList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def readNotifications(
            self,
            *,
            notifications: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Updates notifications as read in database

        Args:
            notifications:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if notifications is not None:
            parameters['notifications'] = str(notifications)
        return self._client.query('/api/notification/readNotifications/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Problem:
    r"""ProblemsController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def create(
            self,
            *,
            problem_alias: str,
            visibility: str,
            allow_user_add_tags: Optional[bool] = None,
            email_clarifications: Optional[bool] = None,
            extra_wall_time: Optional[Any] = None,
            group_score_policy: Optional[str] = None,
            input_limit: Optional[Any] = None,
            languages: Optional[Any] = None,
            memory_limit: Optional[Any] = None,
            output_limit: Optional[Any] = None,
            overall_wall_time_limit: Optional[Any] = None,
            problem_level: Optional[str] = None,
            selected_tags: Optional[str] = None,
            show_diff: Optional[str] = None,
            source: Optional[str] = None,
            time_limit: Optional[Any] = None,
            title: Optional[str] = None,
            update_published: Optional[str] = None,
            validator: Optional[str] = None,
            validator_time_limit: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Create a new problem

        Args:
            problem_alias:
            visibility:
            allow_user_add_tags:
            email_clarifications:
            extra_wall_time:
            group_score_policy:
            input_limit:
            languages:
            memory_limit:
            output_limit:
            overall_wall_time_limit:
            problem_level:
            selected_tags:
            show_diff:
            source:
            time_limit:
            title:
            update_published:
            validator:
            validator_time_limit:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
            'visibility': visibility,
        }
        if allow_user_add_tags is not None:
            parameters['allow_user_add_tags'] = str(allow_user_add_tags)
        if email_clarifications is not None:
            parameters['email_clarifications'] = str(email_clarifications)
        if extra_wall_time is not None:
            parameters['extra_wall_time'] = str(extra_wall_time)
        if group_score_policy is not None:
            parameters['group_score_policy'] = group_score_policy
        if input_limit is not None:
            parameters['input_limit'] = str(input_limit)
        if languages is not None:
            parameters['languages'] = str(languages)
        if memory_limit is not None:
            parameters['memory_limit'] = str(memory_limit)
        if output_limit is not None:
            parameters['output_limit'] = str(output_limit)
        if overall_wall_time_limit is not None:
            parameters['overall_wall_time_limit'] = str(
                overall_wall_time_limit)
        if problem_level is not None:
            parameters['problem_level'] = problem_level
        if selected_tags is not None:
            parameters['selected_tags'] = selected_tags
        if show_diff is not None:
            parameters['show_diff'] = show_diff
        if source is not None:
            parameters['source'] = source
        if time_limit is not None:
            parameters['time_limit'] = str(time_limit)
        if title is not None:
            parameters['title'] = title
        if update_published is not None:
            parameters['update_published'] = update_published
        if validator is not None:
            parameters['validator'] = validator
        if validator_time_limit is not None:
            parameters['validator_time_limit'] = str(validator_time_limit)
        return self._client.query('/api/problem/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addAdmin(
            self,
            *,
            problem_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds an admin to a problem

        Args:
            problem_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/problem/addAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addGroupAdmin(
            self,
            *,
            group: str,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds a group admin to a problem

        Args:
            group:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group': group,
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/problem/addGroupAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def updateProblemLevel(
            self,
            *,
            problem_alias: str,
            level_tag: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Updates the problem level of a problem

        Args:
            problem_alias:
            level_tag:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        if level_tag is not None:
            parameters['level_tag'] = level_tag
        return self._client.query('/api/problem/updateProblemLevel/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addTag(
            self,
            *,
            name: str,
            problem_alias: str,
            public: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds a tag to a problem

        Args:
            name:
            problem_alias:
            public:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'name': name,
            'problem_alias': problem_alias,
        }
        if public is not None:
            parameters['public'] = str(public)
        return self._client.query('/api/problem/addTag/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeAdmin(
            self,
            *,
            problem_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes an admin from a problem

        Args:
            problem_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/problem/removeAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeGroupAdmin(
            self,
            *,
            group: str,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes a group admin from a problem

        Args:
            group:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group': group,
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/problem/removeGroupAdmin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeTag(
            self,
            *,
            name: str,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes a tag from a contest

        Args:
            name:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'name': name,
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/problem/removeTag/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def delete(
            self,
            *,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes a problem whether user is the creator

        Args:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/problem/delete/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def admins(
            self,
            *,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns all problem administrators

        Args:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/problem/admins/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def tags(
            self,
            *,
            problem_alias: str,
            include_voted: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns every tag associated to a given problem.

        Args:
            problem_alias:
            include_voted:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        if include_voted is not None:
            parameters['include_voted'] = str(include_voted)
        return self._client.query('/api/problem/tags/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def rejudge(
            self,
            *,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Rejudge problem

        Args:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/problem/rejudge/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def update(
            self,
            *,
            message: str,
            problem_alias: str,
            allow_user_add_tags: Optional[bool] = None,
            email_clarifications: Optional[bool] = None,
            extra_wall_time: Optional[Any] = None,
            group_score_policy: Optional[str] = None,
            input_limit: Optional[Any] = None,
            languages: Optional[Any] = None,
            memory_limit: Optional[Any] = None,
            output_limit: Optional[Any] = None,
            overall_wall_time_limit: Optional[Any] = None,
            problem_level: Optional[str] = None,
            redirect: Optional[Any] = None,
            selected_tags: Optional[str] = None,
            show_diff: Optional[str] = None,
            source: Optional[str] = None,
            time_limit: Optional[Any] = None,
            title: Optional[str] = None,
            update_published: Optional[str] = None,
            validator: Optional[str] = None,
            validator_time_limit: Optional[Any] = None,
            visibility: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Update problem contents

        Args:
            message:
            problem_alias:
            allow_user_add_tags:
            email_clarifications:
            extra_wall_time:
            group_score_policy:
            input_limit:
            languages:
            memory_limit:
            output_limit:
            overall_wall_time_limit:
            problem_level:
            redirect:
            selected_tags:
            show_diff:
            source:
            time_limit:
            title:
            update_published:
            validator:
            validator_time_limit:
            visibility:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'message': message,
            'problem_alias': problem_alias,
        }
        if allow_user_add_tags is not None:
            parameters['allow_user_add_tags'] = str(allow_user_add_tags)
        if email_clarifications is not None:
            parameters['email_clarifications'] = str(email_clarifications)
        if extra_wall_time is not None:
            parameters['extra_wall_time'] = str(extra_wall_time)
        if group_score_policy is not None:
            parameters['group_score_policy'] = group_score_policy
        if input_limit is not None:
            parameters['input_limit'] = str(input_limit)
        if languages is not None:
            parameters['languages'] = str(languages)
        if memory_limit is not None:
            parameters['memory_limit'] = str(memory_limit)
        if output_limit is not None:
            parameters['output_limit'] = str(output_limit)
        if overall_wall_time_limit is not None:
            parameters['overall_wall_time_limit'] = str(
                overall_wall_time_limit)
        if problem_level is not None:
            parameters['problem_level'] = problem_level
        if redirect is not None:
            parameters['redirect'] = str(redirect)
        if selected_tags is not None:
            parameters['selected_tags'] = selected_tags
        if show_diff is not None:
            parameters['show_diff'] = show_diff
        if source is not None:
            parameters['source'] = source
        if time_limit is not None:
            parameters['time_limit'] = str(time_limit)
        if title is not None:
            parameters['title'] = title
        if update_published is not None:
            parameters['update_published'] = update_published
        if validator is not None:
            parameters['validator'] = validator
        if validator_time_limit is not None:
            parameters['validator_time_limit'] = str(validator_time_limit)
        if visibility is not None:
            parameters['visibility'] = visibility
        return self._client.query('/api/problem/update/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def updateStatement(
            self,
            *,
            message: str,
            problem_alias: str,
            statement: str,
            visibility: str,
            allow_user_add_tags: Optional[bool] = None,
            email_clarifications: Optional[bool] = None,
            extra_wall_time: Optional[Any] = None,
            group_score_policy: Optional[str] = None,
            input_limit: Optional[Any] = None,
            lang: Optional[Any] = None,
            languages: Optional[Any] = None,
            memory_limit: Optional[Any] = None,
            output_limit: Optional[Any] = None,
            overall_wall_time_limit: Optional[Any] = None,
            problem_level: Optional[str] = None,
            selected_tags: Optional[str] = None,
            show_diff: Optional[str] = None,
            source: Optional[str] = None,
            time_limit: Optional[Any] = None,
            title: Optional[str] = None,
            update_published: Optional[str] = None,
            validator: Optional[str] = None,
            validator_time_limit: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Updates problem statement only

        Args:
            message:
            problem_alias:
            statement:
            visibility:
            allow_user_add_tags:
            email_clarifications:
            extra_wall_time:
            group_score_policy:
            input_limit:
            lang:
            languages:
            memory_limit:
            output_limit:
            overall_wall_time_limit:
            problem_level:
            selected_tags:
            show_diff:
            source:
            time_limit:
            title:
            update_published:
            validator:
            validator_time_limit:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'message': message,
            'problem_alias': problem_alias,
            'statement': statement,
            'visibility': visibility,
        }
        if allow_user_add_tags is not None:
            parameters['allow_user_add_tags'] = str(allow_user_add_tags)
        if email_clarifications is not None:
            parameters['email_clarifications'] = str(email_clarifications)
        if extra_wall_time is not None:
            parameters['extra_wall_time'] = str(extra_wall_time)
        if group_score_policy is not None:
            parameters['group_score_policy'] = group_score_policy
        if input_limit is not None:
            parameters['input_limit'] = str(input_limit)
        if lang is not None:
            parameters['lang'] = str(lang)
        if languages is not None:
            parameters['languages'] = str(languages)
        if memory_limit is not None:
            parameters['memory_limit'] = str(memory_limit)
        if output_limit is not None:
            parameters['output_limit'] = str(output_limit)
        if overall_wall_time_limit is not None:
            parameters['overall_wall_time_limit'] = str(
                overall_wall_time_limit)
        if problem_level is not None:
            parameters['problem_level'] = problem_level
        if selected_tags is not None:
            parameters['selected_tags'] = selected_tags
        if show_diff is not None:
            parameters['show_diff'] = show_diff
        if source is not None:
            parameters['source'] = source
        if time_limit is not None:
            parameters['time_limit'] = str(time_limit)
        if title is not None:
            parameters['title'] = title
        if update_published is not None:
            parameters['update_published'] = update_published
        if validator is not None:
            parameters['validator'] = validator
        if validator_time_limit is not None:
            parameters['validator_time_limit'] = str(validator_time_limit)
        return self._client.query('/api/problem/updateStatement/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def updateSolution(
            self,
            *,
            message: str,
            problem_alias: str,
            solution: str,
            visibility: str,
            allow_user_add_tags: Optional[bool] = None,
            email_clarifications: Optional[bool] = None,
            extra_wall_time: Optional[Any] = None,
            group_score_policy: Optional[str] = None,
            input_limit: Optional[Any] = None,
            lang: Optional[str] = None,
            languages: Optional[Any] = None,
            memory_limit: Optional[Any] = None,
            output_limit: Optional[Any] = None,
            overall_wall_time_limit: Optional[Any] = None,
            problem_level: Optional[str] = None,
            selected_tags: Optional[str] = None,
            show_diff: Optional[str] = None,
            source: Optional[str] = None,
            time_limit: Optional[Any] = None,
            title: Optional[str] = None,
            update_published: Optional[str] = None,
            validator: Optional[str] = None,
            validator_time_limit: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Updates problem solution only

        Args:
            message:
            problem_alias:
            solution:
            visibility:
            allow_user_add_tags:
            email_clarifications:
            extra_wall_time:
            group_score_policy:
            input_limit:
            lang:
            languages:
            memory_limit:
            output_limit:
            overall_wall_time_limit:
            problem_level:
            selected_tags:
            show_diff:
            source:
            time_limit:
            title:
            update_published:
            validator:
            validator_time_limit:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'message': message,
            'problem_alias': problem_alias,
            'solution': solution,
            'visibility': visibility,
        }
        if allow_user_add_tags is not None:
            parameters['allow_user_add_tags'] = str(allow_user_add_tags)
        if email_clarifications is not None:
            parameters['email_clarifications'] = str(email_clarifications)
        if extra_wall_time is not None:
            parameters['extra_wall_time'] = str(extra_wall_time)
        if group_score_policy is not None:
            parameters['group_score_policy'] = group_score_policy
        if input_limit is not None:
            parameters['input_limit'] = str(input_limit)
        if lang is not None:
            parameters['lang'] = lang
        if languages is not None:
            parameters['languages'] = str(languages)
        if memory_limit is not None:
            parameters['memory_limit'] = str(memory_limit)
        if output_limit is not None:
            parameters['output_limit'] = str(output_limit)
        if overall_wall_time_limit is not None:
            parameters['overall_wall_time_limit'] = str(
                overall_wall_time_limit)
        if problem_level is not None:
            parameters['problem_level'] = problem_level
        if selected_tags is not None:
            parameters['selected_tags'] = selected_tags
        if show_diff is not None:
            parameters['show_diff'] = show_diff
        if source is not None:
            parameters['source'] = source
        if time_limit is not None:
            parameters['time_limit'] = str(time_limit)
        if title is not None:
            parameters['title'] = title
        if update_published is not None:
            parameters['update_published'] = update_published
        if validator is not None:
            parameters['validator'] = validator
        if validator_time_limit is not None:
            parameters['validator_time_limit'] = str(validator_time_limit)
        return self._client.query('/api/problem/updateSolution/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def details(
            self,
            *,
            problem_alias: str,
            contest_alias: Optional[str] = None,
            lang: Optional[str] = None,
            prevent_problemset_open: Optional[bool] = None,
            problemset_id: Optional[int] = None,
            show_solvers: Optional[bool] = None,
            statement_type: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for Problem Details API

        Args:
            problem_alias:
            contest_alias:
            lang:
            prevent_problemset_open:
            problemset_id:
            show_solvers:
            statement_type:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        if contest_alias is not None:
            parameters['contest_alias'] = contest_alias
        if lang is not None:
            parameters['lang'] = lang
        if prevent_problemset_open is not None:
            parameters['prevent_problemset_open'] = str(
                prevent_problemset_open)
        if problemset_id is not None:
            parameters['problemset_id'] = str(problemset_id)
        if show_solvers is not None:
            parameters['show_solvers'] = str(show_solvers)
        if statement_type is not None:
            parameters['statement_type'] = statement_type
        return self._client.query('/api/problem/details/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def solution(
            self,
            *,
            contest_alias: Optional[str] = None,
            forfeit_problem: Optional[bool] = None,
            lang: Optional[str] = None,
            problem_alias: Optional[str] = None,
            problemset_id: Optional[Any] = None,
            statement_type: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns the solution for a problem if conditions are satisfied.

        Args:
            contest_alias:
            forfeit_problem:
            lang:
            problem_alias:
            problemset_id:
            statement_type:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if contest_alias is not None:
            parameters['contest_alias'] = contest_alias
        if forfeit_problem is not None:
            parameters['forfeit_problem'] = str(forfeit_problem)
        if lang is not None:
            parameters['lang'] = lang
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        if problemset_id is not None:
            parameters['problemset_id'] = str(problemset_id)
        if statement_type is not None:
            parameters['statement_type'] = statement_type
        return self._client.query('/api/problem/solution/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def versions(
            self,
            *,
            problem_alias: Optional[str] = None,
            problemset_id: Optional[int] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for Problem Versions API

        Args:
            problem_alias:
            problemset_id:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        if problemset_id is not None:
            parameters['problemset_id'] = str(problemset_id)
        return self._client.query('/api/problem/versions/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def selectVersion(
            self,
            *,
            commit: Optional[str] = None,
            problem_alias: Optional[str] = None,
            update_published: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Change the version of the problem.

        Args:
            commit:
            problem_alias:
            update_published:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if commit is not None:
            parameters['commit'] = commit
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        if update_published is not None:
            parameters['update_published'] = update_published
        return self._client.query('/api/problem/selectVersion/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def runsDiff(
            self,
            *,
            version: str,
            problem_alias: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Return a report of which runs would change due to a version change.

        Args:
            version:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'version': version,
        }
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        return self._client.query('/api/problem/runsDiff/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def runs(
            self,
            *,
            language: Optional[str] = None,
            offset: Optional[int] = None,
            problem_alias: Optional[str] = None,
            rowcount: Optional[int] = None,
            show_all: Optional[bool] = None,
            status: Optional[str] = None,
            username: Optional[str] = None,
            verdict: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for Problem runs API

        Args:
            language:
            offset:
            problem_alias:
            rowcount:
            show_all:
            status:
            username:
            verdict:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if language is not None:
            parameters['language'] = language
        if offset is not None:
            parameters['offset'] = str(offset)
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        if rowcount is not None:
            parameters['rowcount'] = str(rowcount)
        if show_all is not None:
            parameters['show_all'] = str(show_all)
        if status is not None:
            parameters['status'] = status
        if username is not None:
            parameters['username'] = username
        if verdict is not None:
            parameters['verdict'] = verdict
        return self._client.query('/api/problem/runs/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def clarifications(
            self,
            *,
            problem_alias: str,
            offset: Optional[Any] = None,
            rowcount: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for Problem clarifications API

        Args:
            problem_alias:
            offset:
            rowcount:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        if offset is not None:
            parameters['offset'] = str(offset)
        if rowcount is not None:
            parameters['rowcount'] = str(rowcount)
        return self._client.query('/api/problem/clarifications/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def stats(
            self,
            *,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Stats of a problem

        Args:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/problem/stats/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def list(
            self,
            *,
            only_quality_seal: bool,
            difficulty: Optional[str] = None,
            difficulty_range: Optional[str] = None,
            language: Optional[Any] = None,
            level: Optional[str] = None,
            max_difficulty: Optional[int] = None,
            min_difficulty: Optional[int] = None,
            min_visibility: Optional[int] = None,
            offset: Optional[Any] = None,
            only_karel: Optional[Any] = None,
            order_by: Optional[Any] = None,
            page: Optional[Any] = None,
            programming_languages: Optional[str] = None,
            query: Optional[str] = None,
            require_all_tags: Optional[Any] = None,
            rowcount: Optional[Any] = None,
            some_tags: Optional[Any] = None,
            sort_order: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""List of public and user's private problems

        Args:
            only_quality_seal:
            difficulty:
            difficulty_range:
            language:
            level:
            max_difficulty:
            min_difficulty:
            min_visibility:
            offset:
            only_karel:
            order_by:
            page:
            programming_languages:
            query:
            require_all_tags:
            rowcount:
            some_tags:
            sort_order:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'only_quality_seal': str(only_quality_seal),
        }
        if difficulty is not None:
            parameters['difficulty'] = difficulty
        if difficulty_range is not None:
            parameters['difficulty_range'] = difficulty_range
        if language is not None:
            parameters['language'] = str(language)
        if level is not None:
            parameters['level'] = level
        if max_difficulty is not None:
            parameters['max_difficulty'] = str(max_difficulty)
        if min_difficulty is not None:
            parameters['min_difficulty'] = str(min_difficulty)
        if min_visibility is not None:
            parameters['min_visibility'] = str(min_visibility)
        if offset is not None:
            parameters['offset'] = str(offset)
        if only_karel is not None:
            parameters['only_karel'] = str(only_karel)
        if order_by is not None:
            parameters['order_by'] = str(order_by)
        if page is not None:
            parameters['page'] = str(page)
        if programming_languages is not None:
            parameters['programming_languages'] = programming_languages
        if query is not None:
            parameters['query'] = query
        if require_all_tags is not None:
            parameters['require_all_tags'] = str(require_all_tags)
        if rowcount is not None:
            parameters['rowcount'] = str(rowcount)
        if some_tags is not None:
            parameters['some_tags'] = str(some_tags)
        if sort_order is not None:
            parameters['sort_order'] = str(sort_order)
        return self._client.query('/api/problem/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def adminList(
            self,
            *,
            page: int,
            page_size: int,
            query: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of problems where current user has admin rights (or is
        the owner).

        Args:
            page:
            page_size:
            query:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'page': str(page),
            'page_size': str(page_size),
        }
        if query is not None:
            parameters['query'] = query
        return self._client.query('/api/problem/adminList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def myList(
            self,
            *,
            page: int,
            query: Optional[str] = None,
            rowcount: Optional[int] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets a list of problems where current user is the owner

        Args:
            page:
            query:
            rowcount:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'page': str(page),
        }
        if query is not None:
            parameters['query'] = query
        if rowcount is not None:
            parameters['rowcount'] = str(rowcount)
        return self._client.query('/api/problem/myList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def bestScore(
            self,
            *,
            contest_alias: Optional[str] = None,
            problem_alias: Optional[str] = None,
            problemset_id: Optional[Any] = None,
            statement_type: Optional[str] = None,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns the best score for a problem

        Args:
            contest_alias:
            problem_alias:
            problemset_id:
            statement_type:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if contest_alias is not None:
            parameters['contest_alias'] = contest_alias
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        if problemset_id is not None:
            parameters['problemset_id'] = str(problemset_id)
        if statement_type is not None:
            parameters['statement_type'] = statement_type
        if username is not None:
            parameters['username'] = username
        return self._client.query('/api/problem/bestScore/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def randomLanguageProblem(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/problem/randomLanguageProblem/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def randomKarelProblem(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/problem/randomKarelProblem/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class ProblemForfeited:
    r"""ProblemForfeitedController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def getCounts(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns the number of solutions allowed
        and the number of solutions already seen

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/problemForfeited/getCounts/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Problemset:
    r"""
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def details(
            self,
            *,
            assignment: str,
            contest_alias: str,
            course: str,
            problemset_id: int,
            auth_token: Optional[Any] = None,
            token: Optional[str] = None,
            tokens: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            assignment:
            contest_alias:
            course:
            problemset_id:
            auth_token:
            token:
            tokens:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'contest_alias': contest_alias,
            'course': course,
            'problemset_id': str(problemset_id),
        }
        if auth_token is not None:
            parameters['auth_token'] = str(auth_token)
        if token is not None:
            parameters['token'] = token
        if tokens is not None:
            parameters['tokens'] = str(tokens)
        return self._client.query('/api/problemset/details/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def scoreboard(
            self,
            *,
            assignment: str,
            contest_alias: str,
            course: str,
            problemset_id: int,
            auth_token: Optional[Any] = None,
            token: Optional[Any] = None,
            tokens: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            assignment:
            contest_alias:
            course:
            problemset_id:
            auth_token:
            token:
            tokens:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'contest_alias': contest_alias,
            'course': course,
            'problemset_id': str(problemset_id),
        }
        if auth_token is not None:
            parameters['auth_token'] = str(auth_token)
        if token is not None:
            parameters['token'] = str(token)
        if tokens is not None:
            parameters['tokens'] = str(tokens)
        return self._client.query('/api/problemset/scoreboard/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def scoreboardEvents(
            self,
            *,
            assignment: str,
            contest_alias: str,
            course: str,
            problemset_id: int,
            auth_token: Optional[Any] = None,
            token: Optional[Any] = None,
            tokens: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns the Scoreboard events

        Args:
            assignment:
            contest_alias:
            course:
            problemset_id:
            auth_token:
            token:
            tokens:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'contest_alias': contest_alias,
            'course': course,
            'problemset_id': str(problemset_id),
        }
        if auth_token is not None:
            parameters['auth_token'] = str(auth_token)
        if token is not None:
            parameters['token'] = str(token)
        if tokens is not None:
            parameters['tokens'] = str(tokens)
        return self._client.query('/api/problemset/scoreboardEvents/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class QualityNomination:
    r"""QualityNominationController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def create(
            self,
            *,
            contents: str,
            nomination: str,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Creates a new QualityNomination

        There are three ways in which users can interact with this:

        # Suggestion

        A user that has already solved a problem can make suggestions about a
        problem. This expects the `nomination` field to be `suggestion` and the
        `contents` field should be a JSON blob with at least one the following fields:

        * `difficulty`: (Optional) A number in the range [0-4] indicating the
                        difficulty of the problem.
        * `quality`: (Optional) A number in the range [0-4] indicating the quality
                    of the problem.
        * `tags`: (Optional) An array of tag names that will be added to the
                  problem upon promotion.
        * `before_ac`: (Optional) Boolean indicating if the suggestion has been sent
                       before receiving an AC verdict for problem run.

        # Quality tag

        A reviewer could send this type of nomination to make the user marked as
        a quality problem or not. The reviewer could also specify which category
        is the one the problem belongs to. The 'contents' field should have the
        following subfields:

        * tag: The name of the tag corresponding to the category of the problem
        * quality_seal: A boolean that if activated, means that the problem is a
          quality problem

        # Promotion

        A user that has already solved a problem can nominate it to be promoted
        as a Quality Problem. This expects the `nomination` field to be
        `promotion` and the `contents` field should be a JSON blob with the
        following fields:

        * `statements`: A dictionary of languages to objects that contain a
                        `markdown` field, which is the markdown-formatted
                        problem statement for that language.
        * `source`: A URL or string clearly documenting the source or full name
                    of original author of the problem.
        * `tags`: An array of tag names that will be added to the problem upon
                  promotion.

        # Demotion

        A demoted problem is banned, and cannot be un-banned or added to any new
        problemsets. This expects the `nomination` field to be `demotion` and
        the `contents` field should be a JSON blob with the following fields:

        * `rationale`: A small text explaining the rationale for demotion.
        * `reason`: One of `['duplicate', 'no-problem-statement', 'offensive', 'other', 'spam']`.
        * `original`: If the `reason` is `duplicate`, the alias of the original
                      problem.
        # Dismissal
        A user that has already solved a problem can dismiss suggestions. The
        `contents` field is empty.

        Args:
            contents:
            nomination:
            problem_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contents': contents,
            'nomination': nomination,
            'problem_alias': problem_alias,
        }
        return self._client.query('/api/qualityNomination/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def resolve(
            self,
            *,
            problem_alias: str,
            qualitynomination_id: int,
            rationale: str,
            status: str,
            all: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Marks a problem of a nomination (only the demotion type supported for now) as (resolved, banned, warning).

        Args:
            problem_alias:
            qualitynomination_id:
            rationale:
            status:
            all:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
            'qualitynomination_id': str(qualitynomination_id),
            'rationale': rationale,
            'status': status,
        }
        if all is not None:
            parameters['all'] = str(all)
        return self._client.query('/api/qualityNomination/resolve/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def list(
            self,
            *,
            offset: int,
            rowcount: int,
            column: Optional[str] = None,
            query: Optional[str] = None,
            status: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            offset:
            rowcount:
            column:
            query:
            status:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'offset': str(offset),
            'rowcount': str(rowcount),
        }
        if column is not None:
            parameters['column'] = column
        if query is not None:
            parameters['query'] = query
        if status is not None:
            parameters['status'] = str(status)
        return self._client.query('/api/qualityNomination/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def myAssignedList(
            self,
            *,
            page: int,
            page_size: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Displays the nominations that this user has been assigned.

        Args:
            page:
            page_size:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'page': str(page),
            'page_size': str(page_size),
        }
        return self._client.query('/api/qualityNomination/myAssignedList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def myList(
            self,
            *,
            offset: int,
            rowcount: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            offset:
            rowcount:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'offset': str(offset),
            'rowcount': str(rowcount),
        }
        return self._client.query('/api/qualityNomination/myList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def details(
            self,
            *,
            qualitynomination_id: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Displays the details of a nomination. The user needs to be either the
        nominator or a member of the reviewer group.

        Args:
            qualitynomination_id:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'qualitynomination_id': str(qualitynomination_id),
        }
        return self._client.query('/api/qualityNomination/details/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Reset:
    r"""
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def create(
            self,
            *,
            email: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Creates a reset operation, the first of two steps needed to reset a
        password. The first step consist of sending an email to the user with
        instructions to reset he's password, if and only if the email is valid.

        Args:
            email:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'email': email,
        }
        return self._client.query('/api/reset/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def generateToken(
            self,
            *,
            email: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Creates a reset operation, support team members can generate a valid
        token and then they can send it to end user

        Args:
            email:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'email': email,
        }
        return self._client.query('/api/reset/generateToken/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def update(
            self,
            *,
            email: str,
            password: str,
            password_confirmation: str,
            reset_token: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Updates the password of a given user, this is the second and last step
        in order to reset the password. This operation is done if and only if
        the correct parameters are suplied.

        Args:
            email:
            password:
            password_confirmation:
            reset_token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'email': email,
            'password': password,
            'password_confirmation': password_confirmation,
            'reset_token': reset_token,
        }
        return self._client.query('/api/reset/update/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Run:
    r"""RunController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def create(
            self,
            *,
            contest_alias: str,
            problem_alias: str,
            source: str,
            language: Optional[Any] = None,
            problemset_id: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Create a new run

        Args:
            contest_alias:
            problem_alias:
            source:
            language:
            problemset_id:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'problem_alias': problem_alias,
            'source': source,
        }
        if language is not None:
            parameters['language'] = str(language)
        if problemset_id is not None:
            parameters['problemset_id'] = str(problemset_id)
        return self._client.query('/api/run/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def status(
            self,
            *,
            run_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get basic details of a run

        Args:
            run_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        return self._client.query('/api/run/status/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def rejudge(
            self,
            *,
            run_alias: str,
            debug: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Re-sends a problem to Grader.

        Args:
            run_alias:
            debug:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        if debug is not None:
            parameters['debug'] = str(debug)
        return self._client.query('/api/run/rejudge/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def disqualify(
            self,
            *,
            run_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Disqualify a submission

        Args:
            run_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        return self._client.query('/api/run/disqualify/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def details(
            self,
            *,
            run_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets the details of a run. Includes admin details if admin.

        Args:
            run_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        return self._client.query('/api/run/details/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def source(
            self,
            *,
            run_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Given the run alias, returns the source code and any compile errors if any
        Used in the arena, any contestant can view its own codes and compile errors

        Args:
            run_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        return self._client.query('/api/run/source/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def counts(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get total of last 6 months

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/run/counts/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def list(
            self,
            *,
            offset: int,
            problem_alias: str,
            rowcount: int,
            username: str,
            language: Optional[str] = None,
            status: Optional[str] = None,
            verdict: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets a list of latest runs overall

        Args:
            offset:
            problem_alias:
            rowcount:
            username:
            language:
            status:
            verdict:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'offset': str(offset),
            'problem_alias': problem_alias,
            'rowcount': str(rowcount),
            'username': username,
        }
        if language is not None:
            parameters['language'] = language
        if status is not None:
            parameters['status'] = status
        if verdict is not None:
            parameters['verdict'] = verdict
        return self._client.query('/api/run/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class School:
    r"""SchoolController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def list(
            self,
            *,
            query: Optional[Any] = None,
            term: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets a list of schools

        Args:
            query:
            term:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if query is not None:
            parameters['query'] = str(query)
        if term is not None:
            parameters['term'] = str(term)
        return self._client.query('/api/school/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def create(
            self,
            *,
            name: str,
            country_id: Optional[str] = None,
            state_id: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Api to create new school

        Args:
            name:
            country_id:
            state_id:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'name': name,
        }
        if country_id is not None:
            parameters['country_id'] = country_id
        if state_id is not None:
            parameters['state_id'] = state_id
        return self._client.query('/api/school/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def selectSchoolOfTheMonth(
            self,
            *,
            school_id: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Selects a certain school as school of the month

        Args:
            school_id:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'school_id': str(school_id),
        }
        return self._client.query('/api/school/selectSchoolOfTheMonth/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Scoreboard:
    r"""ScoreboardController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def refresh(
            self,
            *,
            alias: str,
            course_alias: Optional[str] = None,
            token: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of contests

        Args:
            alias:
            course_alias:
            token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
        }
        if course_alias is not None:
            parameters['course_alias'] = course_alias
        if token is not None:
            parameters['token'] = str(token)
        return self._client.query('/api/scoreboard/refresh/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Session:
    r"""Session controller handles sessions.
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def currentSession(
            self,
            *,
            auth_token: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns information about current session. In order to avoid one full
        server roundtrip (about ~100msec on each pageload), it also returns the
        current time to be able to calculate the time delta between the
        contestant's machine and the server.

        Args:
            auth_token:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if auth_token is not None:
            parameters['auth_token'] = auth_token
        return self._client.query('/api/session/currentSession/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def googleLogin(
            self,
            *,
            storeToken: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            storeToken:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'storeToken': storeToken,
        }
        return self._client.query('/api/session/googleLogin/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Submission:
    r"""SubmissionController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def setFeedback(
            self,
            *,
            assignment_alias: str,
            course_alias: str,
            feedback: str,
            guid: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Updates the admin feedback for a submission

        Args:
            assignment_alias:
            course_alias:
            feedback:
            guid:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'feedback': feedback,
            'guid': guid,
        }
        return self._client.query('/api/submission/setFeedback/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Tag:
    r"""TagController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def list(
            self,
            *,
            query: Optional[Any] = None,
            term: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets a list of tags

        Args:
            query:
            term:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if query is not None:
            parameters['query'] = str(query)
        if term is not None:
            parameters['term'] = str(term)
        return self._client.query('/api/tag/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def frequentTags(
            self,
            *,
            problemLevel: str,
            rows: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Return most frequent public tags of a certain level

        Args:
            problemLevel:
            rows:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'problemLevel': problemLevel,
            'rows': str(rows),
        }
        return self._client.query('/api/tag/frequentTags/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class TeamsGroup:
    r"""TeamsGroupController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def details(
            self,
            *,
            team_group_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Details of a team group

        Args:
            team_group_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
        }
        return self._client.query('/api/teamsGroup/details/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def create(
            self,
            *,
            alias: str,
            description: str,
            name: str,
            numberOfContestants: Optional[int] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""New team group

        Args:
            alias:
            description:
            name:
            numberOfContestants:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'description': description,
            'name': name,
        }
        if numberOfContestants is not None:
            parameters['numberOfContestants'] = str(numberOfContestants)
        return self._client.query('/api/teamsGroup/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def update(
            self,
            *,
            alias: str,
            description: str,
            name: str,
            numberOfContestants: Optional[int] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Update an existing teams group

        Args:
            alias:
            description:
            name:
            numberOfContestants:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'description': description,
            'name': name,
        }
        if numberOfContestants is not None:
            parameters['numberOfContestants'] = str(numberOfContestants)
        return self._client.query('/api/teamsGroup/update/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def teams(
            self,
            *,
            team_group_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Teams of a teams group

        Args:
            team_group_alias:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
        }
        return self._client.query('/api/teamsGroup/teams/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeTeam(
            self,
            *,
            team_group_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Remove team from teams group

        Args:
            team_group_alias:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/teamsGroup/removeTeam/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addMembers(
            self,
            *,
            team_group_alias: str,
            usernames: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Add one or more users to a given team

        Args:
            team_group_alias: The username of the team.
            usernames: Username of all members to add

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
            'usernames': usernames,
        }
        return self._client.query('/api/teamsGroup/addMembers/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def list(
            self,
            *,
            query: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets a list of teams groups. This returns an array instead of an object
        since it is used by typeahead.

        Args:
            query:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if query is not None:
            parameters['query'] = query
        return self._client.query('/api/teamsGroup/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeMember(
            self,
            *,
            team_group_alias: str,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Remove an existing team member of a teams group

        Args:
            team_group_alias: The username of the team
            username: The username of user to remove

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
            'username': username,
        }
        return self._client.query('/api/teamsGroup/removeMember/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def teamsMembers(
            self,
            *,
            page: int,
            page_size: int,
            team_group_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get a list of team members of a teams group

        Args:
            page:
            page_size:
            team_group_alias: The username of the team.

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'page': str(page),
            'page_size': str(page_size),
            'team_group_alias': team_group_alias,
        }
        return self._client.query('/api/teamsGroup/teamsMembers/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Time:
    r"""TimeController

    Used by arena to sync time between client and server from time to time
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def get(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for /time API

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/time/get/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class User:
    r"""UserController
    """
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def create(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Entry point for Create a User API

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/user/create/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def login(
            self,
            *,
            password: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Exposes API /user/login
        Expects in request:
        user
        password

        Args:
            password:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'password': password,
            'usernameOrEmail': usernameOrEmail,
        }
        return self._client.query('/api/user/login/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def changePassword(
            self,
            *,
            old_password: str,
            username: str,
            password: Optional[str] = None,
            permission_key: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Changes the password of a user

        Args:
            old_password:
            username:
            password:
            permission_key:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'old_password': old_password,
            'username': username,
        }
        if password is not None:
            parameters['password'] = password
        if permission_key is not None:
            parameters['permission_key'] = str(permission_key)
        return self._client.query('/api/user/changePassword/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def verifyEmail(
            self,
            *,
            id: str,
            usernameOrEmail: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Verifies the user given its verification id

        Args:
            id:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'id': id,
        }
        if usernameOrEmail is not None:
            parameters['usernameOrEmail'] = usernameOrEmail
        return self._client.query('/api/user/verifyEmail/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def mailingListBackfill(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Registers to the mailing list all users that have not been added before. Admin only

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/user/mailingListBackfill/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def generateOmiUsers(
            self,
            *,
            auth_token: str,
            contest_alias: str,
            contest_type: str,
            id: str,
            old_password: str,
            permission_key: str,
            username: str,
            change_password: Optional[Any] = None,
            password: Optional[str] = None,
            usernameOrEmail: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""

        Args:
            auth_token:
            contest_alias:
            contest_type:
            id:
            old_password:
            permission_key:
            username:
            change_password:
            password:
            usernameOrEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'auth_token': auth_token,
            'contest_alias': contest_alias,
            'contest_type': contest_type,
            'id': id,
            'old_password': old_password,
            'permission_key': permission_key,
            'username': username,
        }
        if change_password is not None:
            parameters['change_password'] = str(change_password)
        if password is not None:
            parameters['password'] = password
        if usernameOrEmail is not None:
            parameters['usernameOrEmail'] = usernameOrEmail
        return self._client.query('/api/user/generateOmiUsers/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def profile(
            self,
            *,
            category: Optional[Any] = None,
            omit_rank: Optional[bool] = None,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get general user info

        Args:
            category:
            omit_rank:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if category is not None:
            parameters['category'] = str(category)
        if omit_rank is not None:
            parameters['omit_rank'] = str(omit_rank)
        if username is not None:
            parameters['username'] = username
        return self._client.query('/api/user/profile/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def statusVerified(
            self,
            *,
            email: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets verify status of a user

        Args:
            email:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'email': email,
        }
        return self._client.query('/api/user/statusVerified/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def extraInformation(
            self,
            *,
            email: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets extra information of the identity:
        - last password change request
        - verify status
        - birth date to verify the user identity

        Args:
            email:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'email': email,
        }
        return self._client.query('/api/user/extraInformation/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def coderOfTheMonth(
            self,
            *,
            category: Optional[Any] = None,
            date: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get coder of the month by trying to find it in the table using the first
        day of the current month. If there's no coder of the month for the given
        date, calculate it and save it.

        Args:
            category:
            date:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if category is not None:
            parameters['category'] = str(category)
        if date is not None:
            parameters['date'] = date
        return self._client.query('/api/user/coderOfTheMonth/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def coderOfTheMonthList(
            self,
            *,
            category: Optional[Any] = None,
            date: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns the list of coders of the month

        Args:
            category:
            date:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if category is not None:
            parameters['category'] = str(category)
        if date is not None:
            parameters['date'] = date
        return self._client.query('/api/user/coderOfTheMonthList/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def selectCoderOfTheMonth(
            self,
            *,
            username: str,
            category: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Selects coder of the month for next month.

        Args:
            username:
            category:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'username': username,
        }
        if category is not None:
            parameters['category'] = str(category)
        return self._client.query('/api/user/selectCoderOfTheMonth/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def contestStats(
            self,
            *,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get Contests which a certain user has participated in

        Args:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return self._client.query('/api/user/contestStats/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def problemsSolved(
            self,
            *,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get Problems solved by user

        Args:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return self._client.query('/api/user/problemsSolved/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def listUnsolvedProblems(
            self,
            *,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get Problems unsolved by user

        Args:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return self._client.query('/api/user/listUnsolvedProblems/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def problemsCreated(
            self,
            *,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get Problems created by user

        Args:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return self._client.query('/api/user/problemsCreated/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def list(
            self,
            *,
            query: Optional[str] = None,
            rowcount: Optional[int] = None,
            term: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets a list of users.

        Args:
            query:
            rowcount:
            term:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if query is not None:
            parameters['query'] = query
        if rowcount is not None:
            parameters['rowcount'] = str(rowcount)
        if term is not None:
            parameters['term'] = term
        return self._client.query('/api/user/list/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def stats(
            self,
            *,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get stats

        Args:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return self._client.query('/api/user/stats/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def updateBasicInfo(
            self,
            *,
            password: str,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Update basic user profile info when logged with fb/gool

        Args:
            password:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'password': password,
            'username': username,
        }
        return self._client.query('/api/user/updateBasicInfo/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def update(
            self,
            *,
            birth_date: str,
            country_id: str,
            graduation_date: str,
            locale: str,
            state_id: str,
            auth_token: Optional[Any] = None,
            gender: Optional[str] = None,
            has_competitive_objective: Optional[bool] = None,
            has_learning_objective: Optional[bool] = None,
            has_scholar_objective: Optional[bool] = None,
            has_teaching_objective: Optional[bool] = None,
            hide_problem_tags: Optional[bool] = None,
            is_private: Optional[bool] = None,
            name: Optional[str] = None,
            scholar_degree: Optional[str] = None,
            school_id: Optional[int] = None,
            school_name: Optional[Any] = None,
            username: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Update user profile

        Args:
            birth_date:
            country_id:
            graduation_date:
            locale:
            state_id:
            auth_token:
            gender:
            has_competitive_objective:
            has_learning_objective:
            has_scholar_objective:
            has_teaching_objective:
            hide_problem_tags:
            is_private:
            name:
            scholar_degree:
            school_id:
            school_name:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'birth_date': birth_date,
            'country_id': country_id,
            'graduation_date': graduation_date,
            'locale': locale,
            'state_id': state_id,
        }
        if auth_token is not None:
            parameters['auth_token'] = str(auth_token)
        if gender is not None:
            parameters['gender'] = gender
        if has_competitive_objective is not None:
            parameters['has_competitive_objective'] = str(
                has_competitive_objective)
        if has_learning_objective is not None:
            parameters['has_learning_objective'] = str(has_learning_objective)
        if has_scholar_objective is not None:
            parameters['has_scholar_objective'] = str(has_scholar_objective)
        if has_teaching_objective is not None:
            parameters['has_teaching_objective'] = str(has_teaching_objective)
        if hide_problem_tags is not None:
            parameters['hide_problem_tags'] = str(hide_problem_tags)
        if is_private is not None:
            parameters['is_private'] = str(is_private)
        if name is not None:
            parameters['name'] = name
        if scholar_degree is not None:
            parameters['scholar_degree'] = scholar_degree
        if school_id is not None:
            parameters['school_id'] = str(school_id)
        if school_name is not None:
            parameters['school_name'] = str(school_name)
        if username is not None:
            parameters['username'] = str(username)
        return self._client.query('/api/user/update/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def updateMainEmail(
            self,
            *,
            email: str,
            originalEmail: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Updates the main email of the current user

        Args:
            email:
            originalEmail:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'email': email,
        }
        if originalEmail is not None:
            parameters['originalEmail'] = originalEmail
        return self._client.query('/api/user/updateMainEmail/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def validateFilter(
            self,
            *,
            filter: str,
            problemset_id: int,
            auth_token: Optional[str] = None,
            contest_admin: Optional[str] = None,
            contest_alias: Optional[str] = None,
            token: Optional[str] = None,
            tokens: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Parses and validates a filter string to be used for event notification
        filtering.

        The Request must have a 'filter' key with comma-delimited URI paths
        representing the resources the caller is interested in receiving events
        for. If the caller has enough privileges to receive notifications for
        ALL the requested filters, the request will return successfully,
        otherwise an exception will be thrown.

        This API does not need authentication to be used. This allows to track
        contest updates with an access token.

        Args:
            filter:
            problemset_id:
            auth_token:
            contest_admin:
            contest_alias:
            token:
            tokens:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'filter': filter,
            'problemset_id': str(problemset_id),
        }
        if auth_token is not None:
            parameters['auth_token'] = auth_token
        if contest_admin is not None:
            parameters['contest_admin'] = contest_admin
        if contest_alias is not None:
            parameters['contest_alias'] = contest_alias
        if token is not None:
            parameters['token'] = token
        if tokens is not None:
            parameters['tokens'] = str(tokens)
        return self._client.query('/api/user/validateFilter/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addRole(
            self,
            *,
            role: str,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds the role to the user.

        Args:
            role:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'role': role,
            'username': username,
        }
        return self._client.query('/api/user/addRole/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeRole(
            self,
            *,
            role: str,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes the role from the user.

        Args:
            role:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'role': role,
            'username': username,
        }
        return self._client.query('/api/user/removeRole/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addGroup(
            self,
            *,
            group: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds the identity to the group.

        Args:
            group:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group': group,
        }
        return self._client.query('/api/user/addGroup/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeGroup(
            self,
            *,
            group: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes the user to the group.

        Args:
            group:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'group': group,
        }
        return self._client.query('/api/user/removeGroup/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def addExperiment(
            self,
            *,
            experiment: str,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Adds the experiment to the user.

        Args:
            experiment:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'experiment': experiment,
            'username': username,
        }
        return self._client.query('/api/user/addExperiment/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def removeExperiment(
            self,
            *,
            experiment: str,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Removes the experiment from the user.

        Args:
            experiment:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'experiment': experiment,
            'username': username,
        }
        return self._client.query('/api/user/removeExperiment/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def lastPrivacyPolicyAccepted(
            self,
            *,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Gets the last privacy policy accepted by user

        Args:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return self._client.query('/api/user/lastPrivacyPolicyAccepted/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def acceptPrivacyPolicy(
            self,
            *,
            privacy_git_object_id: str,
            statement_type: str,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Keeps a record of a user who accepts the privacy policy

        Args:
            privacy_git_object_id:
            statement_type:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'privacy_git_object_id': privacy_git_object_id,
            'statement_type': statement_type,
        }
        if username is not None:
            parameters['username'] = username
        return self._client.query('/api/user/acceptPrivacyPolicy/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def associateIdentity(
            self,
            *,
            password: str,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Associates an identity to the logged user given the username

        Args:
            password:
            username:

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'password': password,
            'username': username,
        }
        return self._client.query('/api/user/associateIdentity/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def listAssociatedIdentities(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Get the identities that have been associated to the logged user

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/user/listAssociatedIdentities/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def generateGitToken(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Generate a new gitserver token. This token can be used to authenticate
        against the gitserver.

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/user/generateGitToken/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def createAPIToken(
            self,
            *,
            name: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Creates a new API token associated with the user.

        This token can be used to authenticate against the API in other calls
        through the [HTTP `Authorization`
        header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
        in the request:

        ```
        Authorization: token 92d8c5a0eceef3c05f4149fc04b62bb2cd50d9c6
        ```

        The following alternative syntax allows to specify an associated
        identity:

        ```
        Authorization: token Credential=92d8c5a0eceef3c05f4149fc04b62bb2cd50d9c6,Username=groupname:username
        ```

        There is a limit of 1000 requests that can be done every hour, after
        which point all requests will fail with [HTTP 429 Too Many
        Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429).
        The `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and
        `X-RateLimit-Reset` response headers will be set whenever an API token
        is used and will contain useful information about the limit to the
        caller.

        There is a limit of 5 API tokens that each user can have.

        Args:
            name: A non-empty alphanumeric string. May contain underscores and dashes.

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'name': name,
        }
        return self._client.query('/api/user/createAPIToken/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def listAPITokens(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Returns a list of all the API tokens associated with the user.

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {}
        return self._client.query('/api/user/listAPITokens/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)

    def revokeAPIToken(
            self,
            *,
            name: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> ApiReturnType:
        r"""Revokes an API token associated with the user.

        Args:
            name: A non-empty alphanumeric string. May contain underscores and dashes.

        Returns:
            The API result dict.
        """
        parameters: Dict[str, str] = {
            'name': name,
        }
        return self._client.query('/api/user/revokeAPIToken/',
                                  payload=parameters,
                                  files_=files_,
                                  timeout_=timeout_,
                                  check_=check_)


class Client:
    """.""",

    def __init__(self,
                 *,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 api_token: Optional[str] = None,
                 auth_token: Optional[str] = None,
                 url: str = 'https://omegaup.com') -> None:
        self._url = url
        self.username: Optional[str] = username
        self.api_token: Optional[str] = api_token
        self.auth_token: Optional[str] = None
        if api_token is None:
            if username is None:
                raise ValueError(
                    'username cannot be None if api_token is not provided', )
            if auth_token is not None:
                self.auth_token = auth_token
            elif password is not None:
                self.auth_token = self.query('/api/user/login/',
                                             payload={
                                                 'usernameOrEmail': username,
                                                 'password': password,
                                             })['auth_token']
        self._admin: Optional[Admin] = None
        self._authorization: Optional[Authorization] = None
        self._badge: Optional[Badge] = None
        self._clarification: Optional[Clarification] = None
        self._contest: Optional[Contest] = None
        self._course: Optional[Course] = None
        self._grader: Optional[Grader] = None
        self._group: Optional[Group] = None
        self._groupScoreboard: Optional[GroupScoreboard] = None
        self._identity: Optional[Identity] = None
        self._notification: Optional[Notification] = None
        self._problem: Optional[Problem] = None
        self._problemForfeited: Optional[ProblemForfeited] = None
        self._problemset: Optional[Problemset] = None
        self._qualityNomination: Optional[QualityNomination] = None
        self._reset: Optional[Reset] = None
        self._run: Optional[Run] = None
        self._school: Optional[School] = None
        self._scoreboard: Optional[Scoreboard] = None
        self._session: Optional[Session] = None
        self._submission: Optional[Submission] = None
        self._tag: Optional[Tag] = None
        self._teamsGroup: Optional[TeamsGroup] = None
        self._time: Optional[Time] = None
        self._user: Optional[User] = None

    def query(self,
              endpoint: str,
              payload: Optional[Mapping[str, str]] = None,
              files_: Optional[Mapping[str, BinaryIO]] = None,
              timeout_: datetime.timedelta = _DEFAULT_TIMEOUT,
              check_: bool = True) -> ApiReturnType:
        """Issues a raw query to the omegaUp API."""
        logger = logging.getLogger('omegaup')
        if payload is None:
            payload = {}
        else:
            payload = dict(payload)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Calling endpoint: %s', endpoint)
            logger.debug('Payload: %s', _filterKeys(payload, {'password'}))

        headers = {}
        if self.api_token is not None:
            if self.username is not None:
                headers['Authorization'] = ','.join((
                    f'Credential={self.api_token}',
                    f'Username={self.username}',
                ))
            else:
                headers['Authorization'] = f'token {self.api_token}'
        elif self.auth_token is not None:
            payload['ouat'] = self.auth_token

        r = requests.post(urllib.parse.urljoin(self._url, endpoint),
                          data=payload,
                          headers=headers,
                          files=files_,
                          timeout=timeout_.total_seconds())

        try:
            response: ApiReturnType = r.json()
        except:  # noqa: bare-except Re-raised below
            logger.exception(r.text)
            raise

        if logger.isEnabledFor(logging.DEBUG):
            logger.info('Response: %s', _filterKeys(response, {'auth_token'}))

        if check_ and r.status_code != 200:
            raise Exception(response)

        return response

    @property
    def admin(self) -> Admin:
        """Returns the Admin API."""
        if self._admin is None:
            self._admin = Admin(self)
        return self._admin

    @property
    def authorization(self) -> Authorization:
        """Returns the Authorization API."""
        if self._authorization is None:
            self._authorization = Authorization(self)
        return self._authorization

    @property
    def badge(self) -> Badge:
        """Returns the Badge API."""
        if self._badge is None:
            self._badge = Badge(self)
        return self._badge

    @property
    def clarification(self) -> Clarification:
        """Returns the Clarification API."""
        if self._clarification is None:
            self._clarification = Clarification(self)
        return self._clarification

    @property
    def contest(self) -> Contest:
        """Returns the Contest API."""
        if self._contest is None:
            self._contest = Contest(self)
        return self._contest

    @property
    def course(self) -> Course:
        """Returns the Course API."""
        if self._course is None:
            self._course = Course(self)
        return self._course

    @property
    def grader(self) -> Grader:
        """Returns the Grader API."""
        if self._grader is None:
            self._grader = Grader(self)
        return self._grader

    @property
    def group(self) -> Group:
        """Returns the Group API."""
        if self._group is None:
            self._group = Group(self)
        return self._group

    @property
    def groupScoreboard(self) -> GroupScoreboard:
        """Returns the GroupScoreboard API."""
        if self._groupScoreboard is None:
            self._groupScoreboard = GroupScoreboard(self)
        return self._groupScoreboard

    @property
    def identity(self) -> Identity:
        """Returns the Identity API."""
        if self._identity is None:
            self._identity = Identity(self)
        return self._identity

    @property
    def notification(self) -> Notification:
        """Returns the Notification API."""
        if self._notification is None:
            self._notification = Notification(self)
        return self._notification

    @property
    def problem(self) -> Problem:
        """Returns the Problem API."""
        if self._problem is None:
            self._problem = Problem(self)
        return self._problem

    @property
    def problemForfeited(self) -> ProblemForfeited:
        """Returns the ProblemForfeited API."""
        if self._problemForfeited is None:
            self._problemForfeited = ProblemForfeited(self)
        return self._problemForfeited

    @property
    def problemset(self) -> Problemset:
        """Returns the Problemset API."""
        if self._problemset is None:
            self._problemset = Problemset(self)
        return self._problemset

    @property
    def qualityNomination(self) -> QualityNomination:
        """Returns the QualityNomination API."""
        if self._qualityNomination is None:
            self._qualityNomination = QualityNomination(self)
        return self._qualityNomination

    @property
    def reset(self) -> Reset:
        """Returns the Reset API."""
        if self._reset is None:
            self._reset = Reset(self)
        return self._reset

    @property
    def run(self) -> Run:
        """Returns the Run API."""
        if self._run is None:
            self._run = Run(self)
        return self._run

    @property
    def school(self) -> School:
        """Returns the School API."""
        if self._school is None:
            self._school = School(self)
        return self._school

    @property
    def scoreboard(self) -> Scoreboard:
        """Returns the Scoreboard API."""
        if self._scoreboard is None:
            self._scoreboard = Scoreboard(self)
        return self._scoreboard

    @property
    def session(self) -> Session:
        """Returns the Session API."""
        if self._session is None:
            self._session = Session(self)
        return self._session

    @property
    def submission(self) -> Submission:
        """Returns the Submission API."""
        if self._submission is None:
            self._submission = Submission(self)
        return self._submission

    @property
    def tag(self) -> Tag:
        """Returns the Tag API."""
        if self._tag is None:
            self._tag = Tag(self)
        return self._tag

    @property
    def teamsGroup(self) -> TeamsGroup:
        """Returns the TeamsGroup API."""
        if self._teamsGroup is None:
            self._teamsGroup = TeamsGroup(self)
        return self._teamsGroup

    @property
    def time(self) -> Time:
        """Returns the Time API."""
        if self._time is None:
            self._time = Time(self)
        return self._time

    @property
    def user(self) -> User:
        """Returns the User API."""
        if self._user is None:
            self._user = User(self)
        return self._user
