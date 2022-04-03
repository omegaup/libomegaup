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
import dataclasses
import datetime
import logging
import urllib.parse

from typing import Any, BinaryIO, Dict, Iterable, Mapping, Optional, Sequence, Union

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


ApiReturnType = Any
"""The return type of any of the API requests."""

# DAO types


@dataclasses.dataclass
class _OmegaUp_DAO_VO_Contests:
    """Type definition for the \\OmegaUp\\DAO\\VO\\Contests Data Object."""
    acl_id: Optional[int]
    admission_mode: Optional[str]
    alias: Optional[str]
    archived: Optional[bool]
    certificate_cutoff: Optional[int]
    certificates_status: Optional[str]
    contest_for_teams: Optional[bool]
    contest_id: Optional[int]
    default_show_all_contestants_in_scoreboard: Optional[bool]
    description: Optional[str]
    feedback: Optional[str]
    finish_time: Optional[datetime.datetime]
    languages: Optional[str]
    last_updated: Optional[datetime.datetime]
    partial_score: Optional[bool]
    penalty: Optional[int]
    penalty_calc_policy: Optional[str]
    penalty_type: Optional[str]
    points_decay_factor: Optional[float]
    problemset_id: Optional[int]
    recommended: Optional[bool]
    rerun_id: Optional[int]
    scoreboard: Optional[int]
    show_scoreboard_after: Optional[bool]
    start_time: Optional[datetime.datetime]
    submissions_gap: Optional[int]
    title: Optional[str]
    urgent: Optional[bool]
    window_length: Optional[int]

    def __init__(
        self,
        *,
        acl_id: Optional[int] = None,
        admission_mode: Optional[str] = None,
        alias: Optional[str] = None,
        archived: Optional[bool] = None,
        certificate_cutoff: Optional[int] = None,
        certificates_status: Optional[str] = None,
        contest_for_teams: Optional[bool] = None,
        contest_id: Optional[int] = None,
        default_show_all_contestants_in_scoreboard: Optional[bool] = None,
        description: Optional[str] = None,
        feedback: Optional[str] = None,
        finish_time: Optional[int] = None,
        languages: Optional[str] = None,
        last_updated: Optional[int] = None,
        partial_score: Optional[bool] = None,
        penalty: Optional[int] = None,
        penalty_calc_policy: Optional[str] = None,
        penalty_type: Optional[str] = None,
        points_decay_factor: Optional[float] = None,
        problemset_id: Optional[int] = None,
        recommended: Optional[bool] = None,
        rerun_id: Optional[int] = None,
        scoreboard: Optional[int] = None,
        show_scoreboard_after: Optional[bool] = None,
        start_time: Optional[int] = None,
        submissions_gap: Optional[int] = None,
        title: Optional[str] = None,
        urgent: Optional[bool] = None,
        window_length: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        """Create a new \\OmegaUp\\DAO\\VO\\Contests Data Object."""
        self.acl_id = acl_id
        self.admission_mode = admission_mode
        self.alias = alias
        self.archived = archived
        self.certificate_cutoff = certificate_cutoff
        self.certificates_status = certificates_status
        self.contest_for_teams = contest_for_teams
        self.contest_id = contest_id
        self.default_show_all_contestants_in_scoreboard = default_show_all_contestants_in_scoreboard
        self.description = description
        self.feedback = feedback
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        self.languages = languages
        if last_updated is not None:
            self.last_updated = datetime.datetime.fromtimestamp(last_updated)
        else:
            self.last_updated = None
        self.partial_score = partial_score
        self.penalty = penalty
        self.penalty_calc_policy = penalty_calc_policy
        self.penalty_type = penalty_type
        self.points_decay_factor = points_decay_factor
        self.problemset_id = problemset_id
        self.recommended = recommended
        self.rerun_id = rerun_id
        self.scoreboard = scoreboard
        self.show_scoreboard_after = show_scoreboard_after
        if start_time is not None:
            self.start_time = datetime.datetime.fromtimestamp(start_time)
        else:
            self.start_time = None
        self.submissions_gap = submissions_gap
        self.title = title
        self.urgent = urgent
        self.window_length = window_length


@dataclasses.dataclass
class _OmegaUp_DAO_VO_Countries:
    """Type definition for the \\OmegaUp\\DAO\\VO\\Countries Data Object."""
    country_id: Optional[str]
    name: Optional[str]

    def __init__(
        self,
        *,
        country_id: Optional[str] = None,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        """Create a new \\OmegaUp\\DAO\\VO\\Countries Data Object."""
        self.country_id = country_id
        self.name = name


@dataclasses.dataclass
class _OmegaUp_DAO_VO_Identities:
    """Type definition for the \\OmegaUp\\DAO\\VO\\Identities Data Object."""
    country_id: Optional[str]
    current_identity_school_id: Optional[int]
    gender: Optional[str]
    identity_id: Optional[int]
    language_id: Optional[int]
    name: Optional[str]
    password: Optional[str]
    state_id: Optional[str]
    user_id: Optional[int]
    username: Optional[str]

    def __init__(
        self,
        *,
        country_id: Optional[str] = None,
        current_identity_school_id: Optional[int] = None,
        gender: Optional[str] = None,
        identity_id: Optional[int] = None,
        language_id: Optional[int] = None,
        name: Optional[str] = None,
        password: Optional[str] = None,
        state_id: Optional[str] = None,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        """Create a new \\OmegaUp\\DAO\\VO\\Identities Data Object."""
        self.country_id = country_id
        self.current_identity_school_id = current_identity_school_id
        self.gender = gender
        self.identity_id = identity_id
        self.language_id = language_id
        self.name = name
        self.password = password
        self.state_id = state_id
        self.user_id = user_id
        self.username = username


@dataclasses.dataclass
class _OmegaUp_DAO_VO_Users:
    """Type definition for the \\OmegaUp\\DAO\\VO\\Users Data Object."""
    birth_date: Optional[str]
    facebook_user_id: Optional[str]
    git_token: Optional[str]
    has_competitive_objective: Optional[bool]
    has_learning_objective: Optional[bool]
    has_scholar_objective: Optional[bool]
    has_teaching_objective: Optional[bool]
    hide_problem_tags: Optional[bool]
    in_mailing_list: Optional[bool]
    is_private: Optional[bool]
    main_email_id: Optional[int]
    main_identity_id: Optional[int]
    preferred_language: Optional[str]
    reset_digest: Optional[str]
    reset_sent_at: Optional[datetime.datetime]
    scholar_degree: Optional[str]
    user_id: Optional[int]
    verification_id: Optional[str]
    verified: Optional[bool]

    def __init__(
        self,
        *,
        birth_date: Optional[str] = None,
        facebook_user_id: Optional[str] = None,
        git_token: Optional[str] = None,
        has_competitive_objective: Optional[bool] = None,
        has_learning_objective: Optional[bool] = None,
        has_scholar_objective: Optional[bool] = None,
        has_teaching_objective: Optional[bool] = None,
        hide_problem_tags: Optional[bool] = None,
        in_mailing_list: Optional[bool] = None,
        is_private: Optional[bool] = None,
        main_email_id: Optional[int] = None,
        main_identity_id: Optional[int] = None,
        preferred_language: Optional[str] = None,
        reset_digest: Optional[str] = None,
        reset_sent_at: Optional[int] = None,
        scholar_degree: Optional[str] = None,
        user_id: Optional[int] = None,
        verification_id: Optional[str] = None,
        verified: Optional[bool] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        """Create a new \\OmegaUp\\DAO\\VO\\Users Data Object."""
        self.birth_date = birth_date
        self.facebook_user_id = facebook_user_id
        self.git_token = git_token
        self.has_competitive_objective = has_competitive_objective
        self.has_learning_objective = has_learning_objective
        self.has_scholar_objective = has_scholar_objective
        self.has_teaching_objective = has_teaching_objective
        self.hide_problem_tags = hide_problem_tags
        self.in_mailing_list = in_mailing_list
        self.is_private = is_private
        self.main_email_id = main_email_id
        self.main_identity_id = main_identity_id
        self.preferred_language = preferred_language
        self.reset_digest = reset_digest
        if reset_sent_at is not None:
            self.reset_sent_at = datetime.datetime.fromtimestamp(reset_sent_at)
        else:
            self.reset_sent_at = None
        self.scholar_degree = scholar_degree
        self.user_id = user_id
        self.verification_id = verification_id
        self.verified = verified


# Type aliases


@dataclasses.dataclass
class _ActivityEvent:
    """_ActivityEvent"""
    classname: str
    event: '_Event'
    ip: Optional[int]
    time: datetime.datetime
    username: str

    def __init__(
        self,
        *,
        classname: str,
        event: Dict[str, Any],
        time: int,
        username: str,
        ip: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        self.event = _Event(**event)
        if ip is not None:
            self.ip = ip
        else:
            self.ip = None
        self.time = datetime.datetime.fromtimestamp(time)
        self.username = username


@dataclasses.dataclass
class _ActivityFeedPayload:
    """_ActivityFeedPayload"""
    alias: str
    events: Sequence['_ActivityEvent']
    length: int
    page: int
    pagerItems: Sequence['_PageItem']
    type: str

    def __init__(
        self,
        *,
        alias: str,
        events: Sequence[Dict[str, Any]],
        length: int,
        page: int,
        pagerItems: Sequence[Dict[str, Any]],
        type: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.events = [_ActivityEvent(**v) for v in events]
        self.length = length
        self.page = page
        self.pagerItems = [_PageItem(**v) for v in pagerItems]
        self.type = type


@dataclasses.dataclass
class _AddedProblem:
    """_AddedProblem"""
    alias: str
    commit: Optional[str]
    is_extra_problem: Optional[bool]
    points: float

    def __init__(
        self,
        *,
        alias: str,
        points: float,
        commit: Optional[str] = None,
        is_extra_problem: Optional[bool] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        if commit is not None:
            self.commit = commit
        else:
            self.commit = None
        if is_extra_problem is not None:
            self.is_extra_problem = is_extra_problem
        else:
            self.is_extra_problem = None
        self.points = points


@dataclasses.dataclass
class _AdminCourses:
    """_AdminCourses"""
    admin: '_AdminCourses_admin'

    def __init__(
        self,
        *,
        admin: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = _AdminCourses_admin(**admin)


@dataclasses.dataclass
class _AdminCourses_admin:
    """_AdminCourses_admin"""
    accessMode: str
    activeTab: str
    filteredCourses: '_AdminCourses_admin_filteredCourses'

    def __init__(
        self,
        *,
        accessMode: str,
        activeTab: str,
        filteredCourses: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.accessMode = accessMode
        self.activeTab = activeTab
        self.filteredCourses = _AdminCourses_admin_filteredCourses(
            **filteredCourses)


@dataclasses.dataclass
class _AdminCourses_admin_filteredCourses:
    """_AdminCourses_admin_filteredCourses"""
    archived: '_CoursesByTimeType'
    current: '_CoursesByTimeType'
    past: '_CoursesByTimeType'

    def __init__(
        self,
        *,
        archived: Dict[str, Any],
        current: Dict[str, Any],
        past: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.archived = _CoursesByTimeType(**archived)
        self.current = _CoursesByTimeType(**current)
        self.past = _CoursesByTimeType(**past)


@dataclasses.dataclass
class _ArenaAssignment:
    """_ArenaAssignment"""
    alias: Optional[str]
    assignment_type: str
    description: Optional[str]
    director: str
    finish_time: Optional[datetime.datetime]
    name: Optional[str]
    problems: Sequence['_NavbarProblemsetProblem']
    problemset_id: int
    runs: Sequence['_Run']
    start_time: datetime.datetime
    totalRuns: Optional[int]

    def __init__(
        self,
        *,
        assignment_type: str,
        director: str,
        problems: Sequence[Dict[str, Any]],
        problemset_id: int,
        runs: Sequence[Dict[str, Any]],
        start_time: int,
        alias: Optional[str] = None,
        description: Optional[str] = None,
        finish_time: Optional[int] = None,
        name: Optional[str] = None,
        totalRuns: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if alias is not None:
            self.alias = alias
        else:
            self.alias = None
        self.assignment_type = assignment_type
        if description is not None:
            self.description = description
        else:
            self.description = None
        self.director = director
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.problems = [_NavbarProblemsetProblem(**v) for v in problems]
        self.problemset_id = problemset_id
        self.runs = [_Run(**v) for v in runs]
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        if totalRuns is not None:
            self.totalRuns = totalRuns
        else:
            self.totalRuns = None


@dataclasses.dataclass
class _ArenaContest:
    """_ArenaContest"""
    alias: str
    director: str
    finish_time: Optional[datetime.datetime]
    rerun_id: Optional[int]
    start_time: Optional[datetime.datetime]
    title: str
    window_length: Optional[int]

    def __init__(
        self,
        *,
        alias: str,
        director: str,
        title: str,
        finish_time: Optional[int] = None,
        rerun_id: Optional[int] = None,
        start_time: Optional[int] = None,
        window_length: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.director = director
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        if rerun_id is not None:
            self.rerun_id = rerun_id
        else:
            self.rerun_id = None
        if start_time is not None:
            self.start_time = datetime.datetime.fromtimestamp(start_time)
        else:
            self.start_time = None
        self.title = title
        if window_length is not None:
            self.window_length = window_length
        else:
            self.window_length = None


@dataclasses.dataclass
class _ArenaCourseAssignment:
    """_ArenaCourseAssignment"""
    alias: str
    description: str
    name: str
    problemset_id: int

    def __init__(
        self,
        *,
        alias: str,
        description: str,
        name: str,
        problemset_id: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.description = description
        self.name = name
        self.problemset_id = problemset_id


@dataclasses.dataclass
class _ArenaCourseDetails:
    """_ArenaCourseDetails"""
    alias: str
    assignments: Sequence['_CourseAssignment']
    languages: Optional[Sequence[str]]
    name: str

    def __init__(
        self,
        *,
        alias: str,
        assignments: Sequence[Dict[str, Any]],
        name: str,
        languages: Optional[Sequence[str]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.assignments = [_CourseAssignment(**v) for v in assignments]
        if languages is not None:
            self.languages = [v for v in languages]
        else:
            self.languages = None
        self.name = name


@dataclasses.dataclass
class _ArenaCoursePayload:
    """_ArenaCoursePayload"""
    assignment: '_ArenaCourseAssignment'
    clarifications: Sequence['_Clarification']
    course: '_ArenaCourseDetails'
    currentProblem: Optional['_ProblemDetails']
    problems: Sequence['_ArenaCourseProblem']
    runs: Sequence['_Run']
    scoreboard: Optional['_Scoreboard']

    def __init__(
        self,
        *,
        assignment: Dict[str, Any],
        clarifications: Sequence[Dict[str, Any]],
        course: Dict[str, Any],
        problems: Sequence[Dict[str, Any]],
        runs: Sequence[Dict[str, Any]],
        currentProblem: Optional[Dict[str, Any]] = None,
        scoreboard: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.assignment = _ArenaCourseAssignment(**assignment)
        self.clarifications = [_Clarification(**v) for v in clarifications]
        self.course = _ArenaCourseDetails(**course)
        if currentProblem is not None:
            self.currentProblem = _ProblemDetails(**currentProblem)
        else:
            self.currentProblem = None
        self.problems = [_ArenaCourseProblem(**v) for v in problems]
        self.runs = [_Run(**v) for v in runs]
        if scoreboard is not None:
            self.scoreboard = _Scoreboard(**scoreboard)
        else:
            self.scoreboard = None


@dataclasses.dataclass
class _ArenaCourseProblem:
    """_ArenaCourseProblem"""
    alias: str
    letter: str
    title: str

    def __init__(
        self,
        *,
        alias: str,
        letter: str,
        title: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.letter = letter
        self.title = title


@dataclasses.dataclass
class _ArenaProblemDetails:
    """_ArenaProblemDetails"""
    accepts_submissions: bool
    alias: str
    commit: str
    input_limit: int
    languages: Sequence[str]
    letter: Optional[str]
    points: float
    problem_id: Optional[int]
    problemsetter: Optional['_ProblemsetterInfo']
    quality_seal: bool
    runs: Optional[Sequence['_Run']]
    settings: Optional['_ProblemSettingsDistrib']
    source: Optional[str]
    statement: Optional['_ProblemStatement']
    title: str
    visibility: int

    def __init__(
        self,
        *,
        accepts_submissions: bool,
        alias: str,
        commit: str,
        input_limit: int,
        languages: Sequence[str],
        points: float,
        quality_seal: bool,
        title: str,
        visibility: int,
        letter: Optional[str] = None,
        problem_id: Optional[int] = None,
        problemsetter: Optional[Dict[str, Any]] = None,
        runs: Optional[Sequence[Dict[str, Any]]] = None,
        settings: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        statement: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.accepts_submissions = accepts_submissions
        self.alias = alias
        self.commit = commit
        self.input_limit = input_limit
        self.languages = [v for v in languages]
        if letter is not None:
            self.letter = letter
        else:
            self.letter = None
        self.points = points
        if problem_id is not None:
            self.problem_id = problem_id
        else:
            self.problem_id = None
        if problemsetter is not None:
            self.problemsetter = _ProblemsetterInfo(**problemsetter)
        else:
            self.problemsetter = None
        self.quality_seal = quality_seal
        if runs is not None:
            self.runs = [_Run(**v) for v in runs]
        else:
            self.runs = None
        if settings is not None:
            self.settings = _ProblemSettingsDistrib(**settings)
        else:
            self.settings = None
        if source is not None:
            self.source = source
        else:
            self.source = None
        if statement is not None:
            self.statement = _ProblemStatement(**statement)
        else:
            self.statement = None
        self.title = title
        self.visibility = visibility


@dataclasses.dataclass
class _ArenaProblemset:
    """_ArenaProblemset"""
    admin: Optional[bool]
    admission_mode: Optional[str]
    alias: Optional[str]
    courseAssignments: Optional[Sequence['_CourseAssignment']]
    director: Optional[str]
    feedback: Optional[str]
    finish_time: Optional[datetime.datetime]
    name: Optional[str]
    opened: Optional[bool]
    original_contest_alias: Optional[str]
    original_problemset_id: Optional[int]
    problems: Optional[Sequence['_ProblemsetProblem']]
    problemset_id: Optional[int]
    requests_user_information: Optional[str]
    show_penalty: Optional[bool]
    start_time: Optional[datetime.datetime]
    submission_deadline: Optional[datetime.datetime]
    submissions_gap: Optional[int]
    title: Optional[str]

    def __init__(
        self,
        *,
        admin: Optional[bool] = None,
        admission_mode: Optional[str] = None,
        alias: Optional[str] = None,
        courseAssignments: Optional[Sequence[Dict[str, Any]]] = None,
        director: Optional[str] = None,
        feedback: Optional[str] = None,
        finish_time: Optional[int] = None,
        name: Optional[str] = None,
        opened: Optional[bool] = None,
        original_contest_alias: Optional[str] = None,
        original_problemset_id: Optional[int] = None,
        problems: Optional[Sequence[Dict[str, Any]]] = None,
        problemset_id: Optional[int] = None,
        requests_user_information: Optional[str] = None,
        show_penalty: Optional[bool] = None,
        start_time: Optional[int] = None,
        submission_deadline: Optional[int] = None,
        submissions_gap: Optional[int] = None,
        title: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if admin is not None:
            self.admin = admin
        else:
            self.admin = None
        if admission_mode is not None:
            self.admission_mode = admission_mode
        else:
            self.admission_mode = None
        if alias is not None:
            self.alias = alias
        else:
            self.alias = None
        if courseAssignments is not None:
            self.courseAssignments = [
                _CourseAssignment(**v) for v in courseAssignments
            ]
        else:
            self.courseAssignments = None
        if director is not None:
            self.director = director
        else:
            self.director = None
        if feedback is not None:
            self.feedback = feedback
        else:
            self.feedback = None
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        if opened is not None:
            self.opened = opened
        else:
            self.opened = None
        if original_contest_alias is not None:
            self.original_contest_alias = original_contest_alias
        else:
            self.original_contest_alias = None
        if original_problemset_id is not None:
            self.original_problemset_id = original_problemset_id
        else:
            self.original_problemset_id = None
        if problems is not None:
            self.problems = [_ProblemsetProblem(**v) for v in problems]
        else:
            self.problems = None
        if problemset_id is not None:
            self.problemset_id = problemset_id
        else:
            self.problemset_id = None
        if requests_user_information is not None:
            self.requests_user_information = requests_user_information
        else:
            self.requests_user_information = None
        if show_penalty is not None:
            self.show_penalty = show_penalty
        else:
            self.show_penalty = None
        if start_time is not None:
            self.start_time = datetime.datetime.fromtimestamp(start_time)
        else:
            self.start_time = None
        if submission_deadline is not None:
            self.submission_deadline = datetime.datetime.fromtimestamp(
                submission_deadline)
        else:
            self.submission_deadline = None
        if submissions_gap is not None:
            self.submissions_gap = submissions_gap
        else:
            self.submissions_gap = None
        if title is not None:
            self.title = title
        else:
            self.title = None


@dataclasses.dataclass
class _AssignmentDetails:
    """_AssignmentDetails"""
    admin: bool
    alias: str
    assignmentType: str
    courseAssignments: Sequence['_CourseAssignment']
    description: str
    director: str
    finishTime: Optional[datetime.datetime]
    name: str
    problems: Sequence['_ProblemsetProblem']
    problemsetId: int
    startTime: datetime.datetime

    def __init__(
        self,
        *,
        admin: bool,
        alias: str,
        assignmentType: str,
        courseAssignments: Sequence[Dict[str, Any]],
        description: str,
        director: str,
        name: str,
        problems: Sequence[Dict[str, Any]],
        problemsetId: int,
        startTime: int,
        finishTime: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = admin
        self.alias = alias
        self.assignmentType = assignmentType
        self.courseAssignments = [
            _CourseAssignment(**v) for v in courseAssignments
        ]
        self.description = description
        self.director = director
        if finishTime is not None:
            self.finishTime = datetime.datetime.fromtimestamp(finishTime)
        else:
            self.finishTime = None
        self.name = name
        self.problems = [_ProblemsetProblem(**v) for v in problems]
        self.problemsetId = problemsetId
        self.startTime = datetime.datetime.fromtimestamp(startTime)


@dataclasses.dataclass
class _AssignmentDetailsPayload:
    """_AssignmentDetailsPayload"""
    courseDetails: '_CourseDetails'
    currentAssignment: '_ArenaAssignment'
    scoreboard: '_Scoreboard'
    shouldShowFirstAssociatedIdentityRunWarning: bool
    showRanking: bool

    def __init__(
        self,
        *,
        courseDetails: Dict[str, Any],
        currentAssignment: Dict[str, Any],
        scoreboard: Dict[str, Any],
        shouldShowFirstAssociatedIdentityRunWarning: bool,
        showRanking: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.courseDetails = _CourseDetails(**courseDetails)
        self.currentAssignment = _ArenaAssignment(**currentAssignment)
        self.scoreboard = _Scoreboard(**scoreboard)
        self.shouldShowFirstAssociatedIdentityRunWarning = shouldShowFirstAssociatedIdentityRunWarning
        self.showRanking = showRanking


@dataclasses.dataclass
class _AssignmentsProblemsPoints:
    """_AssignmentsProblemsPoints"""
    alias: str
    extraPoints: float
    name: str
    order: int
    points: float
    problems: Sequence['_AssignmentsProblemsPoints_problems_entry']

    def __init__(
        self,
        *,
        alias: str,
        extraPoints: float,
        name: str,
        order: int,
        points: float,
        problems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.extraPoints = extraPoints
        self.name = name
        self.order = order
        self.points = points
        self.problems = [
            _AssignmentsProblemsPoints_problems_entry(**v) for v in problems
        ]


@dataclasses.dataclass
class _AssignmentsProblemsPoints_problems_entry:
    """_AssignmentsProblemsPoints_problems_entry"""
    alias: str
    isExtraProblem: bool
    order: int
    points: float
    title: str

    def __init__(
        self,
        *,
        alias: str,
        isExtraProblem: bool,
        order: int,
        points: float,
        title: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.isExtraProblem = isExtraProblem
        self.order = order
        self.points = points
        self.title = title


@dataclasses.dataclass
class _AssociatedIdentity:
    """_AssociatedIdentity"""
    default: bool
    username: str

    def __init__(
        self,
        *,
        default: bool,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.default = default
        self.username = username


@dataclasses.dataclass
class _AuthIdentityExt:
    """_AuthIdentityExt"""
    currentIdentity: '_IdentityExt'
    loginIdentity: '_IdentityExt'

    def __init__(
        self,
        *,
        currentIdentity: Dict[str, Any],
        loginIdentity: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.currentIdentity = _IdentityExt(**currentIdentity)
        self.loginIdentity = _IdentityExt(**loginIdentity)


@dataclasses.dataclass
class _AuthorRankTablePayload:
    """_AuthorRankTablePayload"""
    length: int
    page: int
    pagerItems: Sequence['_PageItem']
    ranking: '_AuthorsRank'

    def __init__(
        self,
        *,
        length: int,
        page: int,
        pagerItems: Sequence[Dict[str, Any]],
        ranking: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.length = length
        self.page = page
        self.pagerItems = [_PageItem(**v) for v in pagerItems]
        self.ranking = _AuthorsRank(**ranking)


@dataclasses.dataclass
class _AuthorsRank:
    """_AuthorsRank"""
    ranking: Sequence['_AuthorsRank_ranking_entry']
    total: int

    def __init__(
        self,
        *,
        ranking: Sequence[Dict[str, Any]],
        total: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.ranking = [_AuthorsRank_ranking_entry(**v) for v in ranking]
        self.total = total


@dataclasses.dataclass
class _AuthorsRank_ranking_entry:
    """_AuthorsRank_ranking_entry"""
    author_ranking: Optional[int]
    author_score: float
    classname: str
    country_id: Optional[str]
    name: Optional[str]
    username: str

    def __init__(
        self,
        *,
        author_score: float,
        classname: str,
        username: str,
        author_ranking: Optional[int] = None,
        country_id: Optional[str] = None,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if author_ranking is not None:
            self.author_ranking = author_ranking
        else:
            self.author_ranking = None
        self.author_score = author_score
        self.classname = classname
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.username = username


@dataclasses.dataclass
class _Badge:
    """_Badge"""
    assignation_time: Optional[datetime.datetime]
    badge_alias: str
    first_assignation: Optional[datetime.datetime]
    owners_count: int
    total_users: int

    def __init__(
        self,
        *,
        badge_alias: str,
        owners_count: int,
        total_users: int,
        assignation_time: Optional[int] = None,
        first_assignation: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if assignation_time is not None:
            self.assignation_time = datetime.datetime.fromtimestamp(
                assignation_time)
        else:
            self.assignation_time = None
        self.badge_alias = badge_alias
        if first_assignation is not None:
            self.first_assignation = datetime.datetime.fromtimestamp(
                first_assignation)
        else:
            self.first_assignation = None
        self.owners_count = owners_count
        self.total_users = total_users


@dataclasses.dataclass
class _BadgeDetailsPayload:
    """_BadgeDetailsPayload"""
    badge: '_Badge'

    def __init__(
        self,
        *,
        badge: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.badge = _Badge(**badge)


@dataclasses.dataclass
class _BadgeListPayload:
    """_BadgeListPayload"""
    badges: Sequence[str]
    ownedBadges: Sequence['_Badge']

    def __init__(
        self,
        *,
        badges: Sequence[str],
        ownedBadges: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.badges = [v for v in badges]
        self.ownedBadges = [_Badge(**v) for v in ownedBadges]


@dataclasses.dataclass
class _BestSolvers:
    """_BestSolvers"""
    classname: str
    language: str
    memory: float
    runtime: float
    time: datetime.datetime
    username: str

    def __init__(
        self,
        *,
        classname: str,
        language: str,
        memory: float,
        runtime: float,
        time: int,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        self.language = language
        self.memory = memory
        self.runtime = runtime
        self.time = datetime.datetime.fromtimestamp(time)
        self.username = username


@dataclasses.dataclass
class _CachedExtraProfileDetails:
    """_CachedExtraProfileDetails"""
    badges: Sequence[str]
    contests: Dict[str, '_UserProfileContests_value']
    createdContests: Sequence['_Contest']
    createdCourses: Sequence['_Course']
    createdProblems: Sequence['_Problem']
    solvedProblems: Sequence['_Problem']
    stats: Sequence['_UserProfileStats']
    unsolvedProblems: Sequence['_Problem']

    def __init__(
        self,
        *,
        badges: Sequence[str],
        contests: Dict[str, Dict[str, Any]],
        createdContests: Sequence[Dict[str, Any]],
        createdCourses: Sequence[Dict[str, Any]],
        createdProblems: Sequence[Dict[str, Any]],
        solvedProblems: Sequence[Dict[str, Any]],
        stats: Sequence[Dict[str, Any]],
        unsolvedProblems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.badges = [v for v in badges]
        self.contests = {
            k: _UserProfileContests_value(**v)
            for k, v in contests.items()
        }
        self.createdContests = [_Contest(**v) for v in createdContests]
        self.createdCourses = [_Course(**v) for v in createdCourses]
        self.createdProblems = [_Problem(**v) for v in createdProblems]
        self.solvedProblems = [_Problem(**v) for v in solvedProblems]
        self.stats = [_UserProfileStats(**v) for v in stats]
        self.unsolvedProblems = [_Problem(**v) for v in unsolvedProblems]


@dataclasses.dataclass
class _CaseResult:
    """_CaseResult"""
    contest_score: float
    max_score: float
    meta: '_RunMetadata'
    name: str
    out_diff: Optional[str]
    score: float
    verdict: str

    def __init__(
        self,
        *,
        contest_score: float,
        max_score: float,
        meta: Dict[str, Any],
        name: str,
        score: float,
        verdict: str,
        out_diff: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contest_score = contest_score
        self.max_score = max_score
        self.meta = _RunMetadata(**meta)
        self.name = name
        if out_diff is not None:
            self.out_diff = out_diff
        else:
            self.out_diff = None
        self.score = score
        self.verdict = verdict


@dataclasses.dataclass
class _CertificateDetailsPayload:
    """_CertificateDetailsPayload"""
    uuid: str

    def __init__(
        self,
        *,
        uuid: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.uuid = uuid


@dataclasses.dataclass
class _Clarification:
    """_Clarification"""
    answer: Optional[str]
    assignment_alias: Optional[str]
    author: str
    clarification_id: int
    contest_alias: Optional[str]
    message: str
    problem_alias: str
    public: bool
    receiver: Optional[str]
    time: datetime.datetime

    def __init__(
        self,
        *,
        author: str,
        clarification_id: int,
        message: str,
        problem_alias: str,
        public: bool,
        time: int,
        answer: Optional[str] = None,
        assignment_alias: Optional[str] = None,
        contest_alias: Optional[str] = None,
        receiver: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if answer is not None:
            self.answer = answer
        else:
            self.answer = None
        if assignment_alias is not None:
            self.assignment_alias = assignment_alias
        else:
            self.assignment_alias = None
        self.author = author
        self.clarification_id = clarification_id
        if contest_alias is not None:
            self.contest_alias = contest_alias
        else:
            self.contest_alias = None
        self.message = message
        self.problem_alias = problem_alias
        self.public = public
        if receiver is not None:
            self.receiver = receiver
        else:
            self.receiver = None
        self.time = datetime.datetime.fromtimestamp(time)


@dataclasses.dataclass
class _CoderOfTheMonth:
    """_CoderOfTheMonth"""
    category: str
    classname: str
    coder_of_the_month_id: int
    country_id: str
    description: Optional[str]
    problems_solved: int
    ranking: int
    school_id: Optional[int]
    score: float
    selected_by: Optional[int]
    time: str
    user_id: int
    username: str

    def __init__(
        self,
        *,
        category: str,
        classname: str,
        coder_of_the_month_id: int,
        country_id: str,
        problems_solved: int,
        ranking: int,
        score: float,
        time: str,
        user_id: int,
        username: str,
        description: Optional[str] = None,
        school_id: Optional[int] = None,
        selected_by: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.category = category
        self.classname = classname
        self.coder_of_the_month_id = coder_of_the_month_id
        self.country_id = country_id
        if description is not None:
            self.description = description
        else:
            self.description = None
        self.problems_solved = problems_solved
        self.ranking = ranking
        if school_id is not None:
            self.school_id = school_id
        else:
            self.school_id = None
        self.score = score
        if selected_by is not None:
            self.selected_by = selected_by
        else:
            self.selected_by = None
        self.time = time
        self.user_id = user_id
        self.username = username


@dataclasses.dataclass
class _CoderOfTheMonthList_entry:
    """_CoderOfTheMonthList_entry"""
    classname: str
    country_id: str
    date: str
    gravatar_32: str
    username: str

    def __init__(
        self,
        *,
        classname: str,
        country_id: str,
        date: str,
        gravatar_32: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        self.country_id = country_id
        self.date = date
        self.gravatar_32 = gravatar_32
        self.username = username


@dataclasses.dataclass
class _CoderOfTheMonthPayload:
    """_CoderOfTheMonthPayload"""
    candidatesToCoderOfTheMonth: Sequence[
        '_CoderOfTheMonthPayload_candidatesToCoderOfTheMonth_entry']
    category: str
    codersOfCurrentMonth: Sequence['_CoderOfTheMonthList_entry']
    codersOfPreviousMonth: Sequence['_CoderOfTheMonthList_entry']
    isMentor: bool
    options: Optional['_CoderOfTheMonthPayload_options']

    def __init__(
        self,
        *,
        candidatesToCoderOfTheMonth: Sequence[Dict[str, Any]],
        category: str,
        codersOfCurrentMonth: Sequence[Dict[str, Any]],
        codersOfPreviousMonth: Sequence[Dict[str, Any]],
        isMentor: bool,
        options: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.candidatesToCoderOfTheMonth = [
            _CoderOfTheMonthPayload_candidatesToCoderOfTheMonth_entry(**v)
            for v in candidatesToCoderOfTheMonth
        ]
        self.category = category
        self.codersOfCurrentMonth = [
            _CoderOfTheMonthList_entry(**v) for v in codersOfCurrentMonth
        ]
        self.codersOfPreviousMonth = [
            _CoderOfTheMonthList_entry(**v) for v in codersOfPreviousMonth
        ]
        self.isMentor = isMentor
        if options is not None:
            self.options = _CoderOfTheMonthPayload_options(**options)
        else:
            self.options = None


@dataclasses.dataclass
class _CoderOfTheMonthPayload_candidatesToCoderOfTheMonth_entry:
    """_CoderOfTheMonthPayload_candidatesToCoderOfTheMonth_entry"""
    category: str
    classname: str
    coder_of_the_month_id: int
    country_id: str
    description: Optional[str]
    problems_solved: int
    ranking: int
    school_id: Optional[int]
    score: float
    selected_by: Optional[int]
    time: str
    username: str

    def __init__(
        self,
        *,
        category: str,
        classname: str,
        coder_of_the_month_id: int,
        country_id: str,
        problems_solved: int,
        ranking: int,
        score: float,
        time: str,
        username: str,
        description: Optional[str] = None,
        school_id: Optional[int] = None,
        selected_by: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.category = category
        self.classname = classname
        self.coder_of_the_month_id = coder_of_the_month_id
        self.country_id = country_id
        if description is not None:
            self.description = description
        else:
            self.description = None
        self.problems_solved = problems_solved
        self.ranking = ranking
        if school_id is not None:
            self.school_id = school_id
        else:
            self.school_id = None
        self.score = score
        if selected_by is not None:
            self.selected_by = selected_by
        else:
            self.selected_by = None
        self.time = time
        self.username = username


@dataclasses.dataclass
class _CoderOfTheMonthPayload_options:
    """_CoderOfTheMonthPayload_options"""
    canChooseCoder: bool
    coderIsSelected: bool

    def __init__(
        self,
        *,
        canChooseCoder: bool,
        coderIsSelected: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.canChooseCoder = canChooseCoder
        self.coderIsSelected = coderIsSelected


@dataclasses.dataclass
class _CollectionDetailsByAuthorPayload:
    """_CollectionDetailsByAuthorPayload"""
    authors: Sequence[str]
    authorsRanking: '_AuthorsRank'
    column: str
    columns: Sequence[str]
    keyword: str
    language: str
    languages: Sequence[str]
    loggedIn: bool
    mode: str
    modes: Sequence[str]
    pagerItems: Sequence['_PageItem']
    problems: Sequence['_ProblemListItem']
    selectedTags: Sequence[str]
    tagData: Sequence['_CollectionDetailsByAuthorPayload_tagData_entry']
    tags: Sequence[str]

    def __init__(
        self,
        *,
        authors: Sequence[str],
        authorsRanking: Dict[str, Any],
        column: str,
        columns: Sequence[str],
        keyword: str,
        language: str,
        languages: Sequence[str],
        loggedIn: bool,
        mode: str,
        modes: Sequence[str],
        pagerItems: Sequence[Dict[str, Any]],
        problems: Sequence[Dict[str, Any]],
        selectedTags: Sequence[str],
        tagData: Sequence[Dict[str, Any]],
        tags: Sequence[str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.authors = [v for v in authors]
        self.authorsRanking = _AuthorsRank(**authorsRanking)
        self.column = column
        self.columns = [v for v in columns]
        self.keyword = keyword
        self.language = language
        self.languages = [v for v in languages]
        self.loggedIn = loggedIn
        self.mode = mode
        self.modes = [v for v in modes]
        self.pagerItems = [_PageItem(**v) for v in pagerItems]
        self.problems = [_ProblemListItem(**v) for v in problems]
        self.selectedTags = [v for v in selectedTags]
        self.tagData = [
            _CollectionDetailsByAuthorPayload_tagData_entry(**v)
            for v in tagData
        ]
        self.tags = [v for v in tags]


@dataclasses.dataclass
class _CollectionDetailsByAuthorPayload_tagData_entry:
    """_CollectionDetailsByAuthorPayload_tagData_entry"""
    name: Optional[str]

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if name is not None:
            self.name = name
        else:
            self.name = None


@dataclasses.dataclass
class _CollectionDetailsByLevelPayload:
    """_CollectionDetailsByLevelPayload"""
    column: str
    columns: Sequence[str]
    difficulty: str
    frequentTags: Sequence['_TagWithProblemCount']
    keyword: str
    language: str
    languages: Sequence[str]
    level: str
    loggedIn: bool
    mode: str
    modes: Sequence[str]
    pagerItems: Sequence['_PageItem']
    problems: Sequence['_ProblemListItem']
    publicTags: Sequence['_TagWithProblemCount']
    selectedTags: Sequence[str]
    tagData: Sequence['_CollectionDetailsByLevelPayload_tagData_entry']
    tagsList: Sequence[str]

    def __init__(
        self,
        *,
        column: str,
        columns: Sequence[str],
        difficulty: str,
        frequentTags: Sequence[Dict[str, Any]],
        keyword: str,
        language: str,
        languages: Sequence[str],
        level: str,
        loggedIn: bool,
        mode: str,
        modes: Sequence[str],
        pagerItems: Sequence[Dict[str, Any]],
        problems: Sequence[Dict[str, Any]],
        publicTags: Sequence[Dict[str, Any]],
        selectedTags: Sequence[str],
        tagData: Sequence[Dict[str, Any]],
        tagsList: Sequence[str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.column = column
        self.columns = [v for v in columns]
        self.difficulty = difficulty
        self.frequentTags = [_TagWithProblemCount(**v) for v in frequentTags]
        self.keyword = keyword
        self.language = language
        self.languages = [v for v in languages]
        self.level = level
        self.loggedIn = loggedIn
        self.mode = mode
        self.modes = [v for v in modes]
        self.pagerItems = [_PageItem(**v) for v in pagerItems]
        self.problems = [_ProblemListItem(**v) for v in problems]
        self.publicTags = [_TagWithProblemCount(**v) for v in publicTags]
        self.selectedTags = [v for v in selectedTags]
        self.tagData = [
            _CollectionDetailsByLevelPayload_tagData_entry(**v)
            for v in tagData
        ]
        self.tagsList = [v for v in tagsList]


@dataclasses.dataclass
class _CollectionDetailsByLevelPayload_tagData_entry:
    """_CollectionDetailsByLevelPayload_tagData_entry"""
    name: Optional[str]

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if name is not None:
            self.name = name
        else:
            self.name = None


@dataclasses.dataclass
class _CommonPayload:
    """_CommonPayload"""
    associatedIdentities: Sequence['_AssociatedIdentity']
    currentEmail: str
    currentName: Optional[str]
    currentUsername: str
    gravatarURL128: str
    gravatarURL51: str
    inContest: bool
    isAdmin: bool
    isLoggedIn: bool
    isMainUserIdentity: bool
    isReviewer: bool
    lockDownImage: str
    navbarSection: str
    omegaUpLockDown: bool
    profileProgress: float
    userClassname: str
    userCountry: str
    userTypes: Sequence[str]

    def __init__(
        self,
        *,
        associatedIdentities: Sequence[Dict[str, Any]],
        currentEmail: str,
        currentUsername: str,
        gravatarURL128: str,
        gravatarURL51: str,
        inContest: bool,
        isAdmin: bool,
        isLoggedIn: bool,
        isMainUserIdentity: bool,
        isReviewer: bool,
        lockDownImage: str,
        navbarSection: str,
        omegaUpLockDown: bool,
        profileProgress: float,
        userClassname: str,
        userCountry: str,
        userTypes: Sequence[str],
        currentName: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.associatedIdentities = [
            _AssociatedIdentity(**v) for v in associatedIdentities
        ]
        self.currentEmail = currentEmail
        if currentName is not None:
            self.currentName = currentName
        else:
            self.currentName = None
        self.currentUsername = currentUsername
        self.gravatarURL128 = gravatarURL128
        self.gravatarURL51 = gravatarURL51
        self.inContest = inContest
        self.isAdmin = isAdmin
        self.isLoggedIn = isLoggedIn
        self.isMainUserIdentity = isMainUserIdentity
        self.isReviewer = isReviewer
        self.lockDownImage = lockDownImage
        self.navbarSection = navbarSection
        self.omegaUpLockDown = omegaUpLockDown
        self.profileProgress = profileProgress
        self.userClassname = userClassname
        self.userCountry = userCountry
        self.userTypes = [v for v in userTypes]


@dataclasses.dataclass
class _ConsentStatement:
    """_ConsentStatement"""
    contest_alias: str
    privacy_git_object_id: Optional[str]
    share_user_information: Optional[bool]
    statement_type: Optional[str]

    def __init__(
        self,
        *,
        contest_alias: str,
        privacy_git_object_id: Optional[str] = None,
        share_user_information: Optional[bool] = None,
        statement_type: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contest_alias = contest_alias
        if privacy_git_object_id is not None:
            self.privacy_git_object_id = privacy_git_object_id
        else:
            self.privacy_git_object_id = None
        if share_user_information is not None:
            self.share_user_information = share_user_information
        else:
            self.share_user_information = None
        if statement_type is not None:
            self.statement_type = statement_type
        else:
            self.statement_type = None


@dataclasses.dataclass
class _Contest:
    """_Contest"""
    acl_id: Optional[int]
    admission_mode: str
    alias: str
    contest_id: int
    description: str
    feedback: Optional[str]
    finish_time: datetime.datetime
    languages: Optional[str]
    last_updated: datetime.datetime
    original_finish_time: Optional[datetime.datetime]
    partial_score: bool
    penalty: Optional[int]
    penalty_calc_policy: Optional[str]
    penalty_type: Optional[str]
    points_decay_factor: Optional[float]
    problemset_id: int
    recommended: bool
    rerun_id: Optional[int]
    scoreboard: Optional[int]
    scoreboard_url: str
    scoreboard_url_admin: str
    show_scoreboard_after: Optional[int]
    start_time: datetime.datetime
    submissions_gap: Optional[int]
    title: str
    urgent: Optional[int]
    window_length: Optional[int]

    def __init__(
        self,
        *,
        admission_mode: str,
        alias: str,
        contest_id: int,
        description: str,
        finish_time: int,
        last_updated: int,
        partial_score: bool,
        problemset_id: int,
        recommended: bool,
        scoreboard_url: str,
        scoreboard_url_admin: str,
        start_time: int,
        title: str,
        acl_id: Optional[int] = None,
        feedback: Optional[str] = None,
        languages: Optional[str] = None,
        original_finish_time: Optional[int] = None,
        penalty: Optional[int] = None,
        penalty_calc_policy: Optional[str] = None,
        penalty_type: Optional[str] = None,
        points_decay_factor: Optional[float] = None,
        rerun_id: Optional[int] = None,
        scoreboard: Optional[int] = None,
        show_scoreboard_after: Optional[int] = None,
        submissions_gap: Optional[int] = None,
        urgent: Optional[int] = None,
        window_length: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if acl_id is not None:
            self.acl_id = acl_id
        else:
            self.acl_id = None
        self.admission_mode = admission_mode
        self.alias = alias
        self.contest_id = contest_id
        self.description = description
        if feedback is not None:
            self.feedback = feedback
        else:
            self.feedback = None
        self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        if languages is not None:
            self.languages = languages
        else:
            self.languages = None
        self.last_updated = datetime.datetime.fromtimestamp(last_updated)
        if original_finish_time is not None:
            self.original_finish_time = datetime.datetime.fromtimestamp(
                original_finish_time)
        else:
            self.original_finish_time = None
        self.partial_score = partial_score
        if penalty is not None:
            self.penalty = penalty
        else:
            self.penalty = None
        if penalty_calc_policy is not None:
            self.penalty_calc_policy = penalty_calc_policy
        else:
            self.penalty_calc_policy = None
        if penalty_type is not None:
            self.penalty_type = penalty_type
        else:
            self.penalty_type = None
        if points_decay_factor is not None:
            self.points_decay_factor = points_decay_factor
        else:
            self.points_decay_factor = None
        self.problemset_id = problemset_id
        self.recommended = recommended
        if rerun_id is not None:
            self.rerun_id = rerun_id
        else:
            self.rerun_id = None
        if scoreboard is not None:
            self.scoreboard = scoreboard
        else:
            self.scoreboard = None
        self.scoreboard_url = scoreboard_url
        self.scoreboard_url_admin = scoreboard_url_admin
        if show_scoreboard_after is not None:
            self.show_scoreboard_after = show_scoreboard_after
        else:
            self.show_scoreboard_after = None
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        if submissions_gap is not None:
            self.submissions_gap = submissions_gap
        else:
            self.submissions_gap = None
        self.title = title
        if urgent is not None:
            self.urgent = urgent
        else:
            self.urgent = None
        if window_length is not None:
            self.window_length = window_length
        else:
            self.window_length = None


@dataclasses.dataclass
class _ContestAdmin:
    """_ContestAdmin"""
    role: str
    username: str

    def __init__(
        self,
        *,
        role: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.role = role
        self.username = username


@dataclasses.dataclass
class _ContestAdminDetails:
    """_ContestAdminDetails"""
    admin: bool
    admission_mode: str
    alias: str
    archived: bool
    available_languages: Dict[str, str]
    contest_for_teams: bool
    default_show_all_contestants_in_scoreboard: bool
    description: str
    director: str
    feedback: str
    finish_time: datetime.datetime
    has_submissions: bool
    languages: Sequence[str]
    needs_basic_information: bool
    opened: bool
    original_contest_alias: Optional[str]
    original_problemset_id: Optional[int]
    partial_score: bool
    penalty: int
    penalty_calc_policy: str
    penalty_type: str
    points_decay_factor: float
    problems: Optional[Sequence['_ProblemsetProblem']]
    problemset_id: int
    requests_user_information: str
    rerun_id: Optional[int]
    scoreboard: int
    scoreboard_url: Optional[str]
    scoreboard_url_admin: Optional[str]
    show_penalty: bool
    show_scoreboard_after: bool
    start_time: datetime.datetime
    submission_deadline: Optional[datetime.datetime]
    submissions_gap: int
    title: str
    window_length: Optional[int]

    def __init__(
        self,
        *,
        admin: bool,
        admission_mode: str,
        alias: str,
        archived: bool,
        available_languages: Dict[str, str],
        contest_for_teams: bool,
        default_show_all_contestants_in_scoreboard: bool,
        description: str,
        director: str,
        feedback: str,
        finish_time: int,
        has_submissions: bool,
        languages: Sequence[str],
        needs_basic_information: bool,
        opened: bool,
        partial_score: bool,
        penalty: int,
        penalty_calc_policy: str,
        penalty_type: str,
        points_decay_factor: float,
        problemset_id: int,
        requests_user_information: str,
        scoreboard: int,
        show_penalty: bool,
        show_scoreboard_after: bool,
        start_time: int,
        submissions_gap: int,
        title: str,
        original_contest_alias: Optional[str] = None,
        original_problemset_id: Optional[int] = None,
        problems: Optional[Sequence[Dict[str, Any]]] = None,
        rerun_id: Optional[int] = None,
        scoreboard_url: Optional[str] = None,
        scoreboard_url_admin: Optional[str] = None,
        submission_deadline: Optional[int] = None,
        window_length: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = admin
        self.admission_mode = admission_mode
        self.alias = alias
        self.archived = archived
        self.available_languages = {
            k: v
            for k, v in available_languages.items()
        }
        self.contest_for_teams = contest_for_teams
        self.default_show_all_contestants_in_scoreboard = default_show_all_contestants_in_scoreboard
        self.description = description
        self.director = director
        self.feedback = feedback
        self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        self.has_submissions = has_submissions
        self.languages = [v for v in languages]
        self.needs_basic_information = needs_basic_information
        self.opened = opened
        if original_contest_alias is not None:
            self.original_contest_alias = original_contest_alias
        else:
            self.original_contest_alias = None
        if original_problemset_id is not None:
            self.original_problemset_id = original_problemset_id
        else:
            self.original_problemset_id = None
        self.partial_score = partial_score
        self.penalty = penalty
        self.penalty_calc_policy = penalty_calc_policy
        self.penalty_type = penalty_type
        self.points_decay_factor = points_decay_factor
        if problems is not None:
            self.problems = [_ProblemsetProblem(**v) for v in problems]
        else:
            self.problems = None
        self.problemset_id = problemset_id
        self.requests_user_information = requests_user_information
        if rerun_id is not None:
            self.rerun_id = rerun_id
        else:
            self.rerun_id = None
        self.scoreboard = scoreboard
        if scoreboard_url is not None:
            self.scoreboard_url = scoreboard_url
        else:
            self.scoreboard_url = None
        if scoreboard_url_admin is not None:
            self.scoreboard_url_admin = scoreboard_url_admin
        else:
            self.scoreboard_url_admin = None
        self.show_penalty = show_penalty
        self.show_scoreboard_after = show_scoreboard_after
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        if submission_deadline is not None:
            self.submission_deadline = datetime.datetime.fromtimestamp(
                submission_deadline)
        else:
            self.submission_deadline = None
        self.submissions_gap = submissions_gap
        self.title = title
        if window_length is not None:
            self.window_length = window_length
        else:
            self.window_length = None


@dataclasses.dataclass
class _ContestDetails:
    """_ContestDetails"""
    admin: bool
    admission_mode: str
    alias: str
    archived: bool
    contest_for_teams: bool
    default_show_all_contestants_in_scoreboard: bool
    description: str
    director: str
    feedback: str
    finish_time: datetime.datetime
    has_submissions: bool
    languages: Sequence[str]
    needs_basic_information: bool
    opened: bool
    original_contest_alias: Optional[str]
    original_problemset_id: Optional[int]
    partial_score: bool
    penalty: int
    penalty_calc_policy: str
    penalty_type: str
    points_decay_factor: float
    problems: Sequence['_ProblemsetProblem']
    problemset_id: int
    requests_user_information: str
    rerun_id: Optional[int]
    scoreboard: int
    scoreboard_url: Optional[str]
    scoreboard_url_admin: Optional[str]
    show_penalty: bool
    show_scoreboard_after: bool
    start_time: datetime.datetime
    submission_deadline: Optional[datetime.datetime]
    submissions_gap: int
    title: str
    window_length: Optional[int]

    def __init__(
        self,
        *,
        admin: bool,
        admission_mode: str,
        alias: str,
        archived: bool,
        contest_for_teams: bool,
        default_show_all_contestants_in_scoreboard: bool,
        description: str,
        director: str,
        feedback: str,
        finish_time: int,
        has_submissions: bool,
        languages: Sequence[str],
        needs_basic_information: bool,
        opened: bool,
        partial_score: bool,
        penalty: int,
        penalty_calc_policy: str,
        penalty_type: str,
        points_decay_factor: float,
        problems: Sequence[Dict[str, Any]],
        problemset_id: int,
        requests_user_information: str,
        scoreboard: int,
        show_penalty: bool,
        show_scoreboard_after: bool,
        start_time: int,
        submissions_gap: int,
        title: str,
        original_contest_alias: Optional[str] = None,
        original_problemset_id: Optional[int] = None,
        rerun_id: Optional[int] = None,
        scoreboard_url: Optional[str] = None,
        scoreboard_url_admin: Optional[str] = None,
        submission_deadline: Optional[int] = None,
        window_length: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = admin
        self.admission_mode = admission_mode
        self.alias = alias
        self.archived = archived
        self.contest_for_teams = contest_for_teams
        self.default_show_all_contestants_in_scoreboard = default_show_all_contestants_in_scoreboard
        self.description = description
        self.director = director
        self.feedback = feedback
        self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        self.has_submissions = has_submissions
        self.languages = [v for v in languages]
        self.needs_basic_information = needs_basic_information
        self.opened = opened
        if original_contest_alias is not None:
            self.original_contest_alias = original_contest_alias
        else:
            self.original_contest_alias = None
        if original_problemset_id is not None:
            self.original_problemset_id = original_problemset_id
        else:
            self.original_problemset_id = None
        self.partial_score = partial_score
        self.penalty = penalty
        self.penalty_calc_policy = penalty_calc_policy
        self.penalty_type = penalty_type
        self.points_decay_factor = points_decay_factor
        self.problems = [_ProblemsetProblem(**v) for v in problems]
        self.problemset_id = problemset_id
        self.requests_user_information = requests_user_information
        if rerun_id is not None:
            self.rerun_id = rerun_id
        else:
            self.rerun_id = None
        self.scoreboard = scoreboard
        if scoreboard_url is not None:
            self.scoreboard_url = scoreboard_url
        else:
            self.scoreboard_url = None
        if scoreboard_url_admin is not None:
            self.scoreboard_url_admin = scoreboard_url_admin
        else:
            self.scoreboard_url_admin = None
        self.show_penalty = show_penalty
        self.show_scoreboard_after = show_scoreboard_after
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        if submission_deadline is not None:
            self.submission_deadline = datetime.datetime.fromtimestamp(
                submission_deadline)
        else:
            self.submission_deadline = None
        self.submissions_gap = submissions_gap
        self.title = title
        if window_length is not None:
            self.window_length = window_length
        else:
            self.window_length = None


@dataclasses.dataclass
class _ContestDetailsPayload:
    """_ContestDetailsPayload"""
    adminPayload: Optional['_ContestDetailsPayload_adminPayload']
    clarifications: Sequence['_Clarification']
    contest: '_ContestPublicDetails'
    original: Optional['_ContestDetailsPayload_original']
    problems: Sequence['_NavbarProblemsetProblem']
    scoreboard: '_Scoreboard'
    scoreboardEvents: Sequence['_ScoreboardEvent']
    shouldShowFirstAssociatedIdentityRunWarning: bool
    submissionDeadline: Optional[datetime.datetime]

    def __init__(
        self,
        *,
        clarifications: Sequence[Dict[str, Any]],
        contest: Dict[str, Any],
        problems: Sequence[Dict[str, Any]],
        scoreboard: Dict[str, Any],
        scoreboardEvents: Sequence[Dict[str, Any]],
        shouldShowFirstAssociatedIdentityRunWarning: bool,
        adminPayload: Optional[Dict[str, Any]] = None,
        original: Optional[Dict[str, Any]] = None,
        submissionDeadline: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if adminPayload is not None:
            self.adminPayload = _ContestDetailsPayload_adminPayload(
                **adminPayload)
        else:
            self.adminPayload = None
        self.clarifications = [_Clarification(**v) for v in clarifications]
        self.contest = _ContestPublicDetails(**contest)
        if original is not None:
            self.original = _ContestDetailsPayload_original(**original)
        else:
            self.original = None
        self.problems = [_NavbarProblemsetProblem(**v) for v in problems]
        self.scoreboard = _Scoreboard(**scoreboard)
        self.scoreboardEvents = [
            _ScoreboardEvent(**v) for v in scoreboardEvents
        ]
        self.shouldShowFirstAssociatedIdentityRunWarning = shouldShowFirstAssociatedIdentityRunWarning
        if submissionDeadline is not None:
            self.submissionDeadline = datetime.datetime.fromtimestamp(
                submissionDeadline)
        else:
            self.submissionDeadline = None


@dataclasses.dataclass
class _ContestDetailsPayload_adminPayload:
    """_ContestDetailsPayload_adminPayload"""
    allRuns: Sequence['_Run']
    totalRuns: int
    users: Sequence['_ContestUser']

    def __init__(
        self,
        *,
        allRuns: Sequence[Dict[str, Any]],
        totalRuns: int,
        users: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.allRuns = [_Run(**v) for v in allRuns]
        self.totalRuns = totalRuns
        self.users = [_ContestUser(**v) for v in users]


@dataclasses.dataclass
class _ContestDetailsPayload_original:
    """_ContestDetailsPayload_original"""
    contest: _OmegaUp_DAO_VO_Contests
    scoreboard: Optional['_Scoreboard']
    scoreboardEvents: Optional[Sequence['_ScoreboardEvent']]

    def __init__(
        self,
        *,
        contest: Dict[str, Any],
        scoreboard: Optional[Dict[str, Any]] = None,
        scoreboardEvents: Optional[Sequence[Dict[str, Any]]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contest = _OmegaUp_DAO_VO_Contests(**contest)
        if scoreboard is not None:
            self.scoreboard = _Scoreboard(**scoreboard)
        else:
            self.scoreboard = None
        if scoreboardEvents is not None:
            self.scoreboardEvents = [
                _ScoreboardEvent(**v) for v in scoreboardEvents
            ]
        else:
            self.scoreboardEvents = None


@dataclasses.dataclass
class _ContestEditPayload:
    """_ContestEditPayload"""
    admins: Sequence['_ContestAdmin']
    details: '_ContestAdminDetails'
    group_admins: Sequence['_ContestGroupAdmin']
    groups: Sequence['_ContestGroup']
    problems: Sequence['_ProblemsetProblemWithVersions']
    requests: Sequence['_ContestRequest']
    teams_group: Optional['_ContestGroup']
    users: Sequence['_ContestUser']

    def __init__(
        self,
        *,
        admins: Sequence[Dict[str, Any]],
        details: Dict[str, Any],
        group_admins: Sequence[Dict[str, Any]],
        groups: Sequence[Dict[str, Any]],
        problems: Sequence[Dict[str, Any]],
        requests: Sequence[Dict[str, Any]],
        users: Sequence[Dict[str, Any]],
        teams_group: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admins = [_ContestAdmin(**v) for v in admins]
        self.details = _ContestAdminDetails(**details)
        self.group_admins = [_ContestGroupAdmin(**v) for v in group_admins]
        self.groups = [_ContestGroup(**v) for v in groups]
        self.problems = [_ProblemsetProblemWithVersions(**v) for v in problems]
        self.requests = [_ContestRequest(**v) for v in requests]
        if teams_group is not None:
            self.teams_group = _ContestGroup(**teams_group)
        else:
            self.teams_group = None
        self.users = [_ContestUser(**v) for v in users]


@dataclasses.dataclass
class _ContestGroup:
    """_ContestGroup"""
    alias: str
    name: str

    def __init__(
        self,
        *,
        alias: str,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.name = name


@dataclasses.dataclass
class _ContestGroupAdmin:
    """_ContestGroupAdmin"""
    alias: str
    name: str
    role: str

    def __init__(
        self,
        *,
        alias: str,
        name: str,
        role: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.name = name
        self.role = role


@dataclasses.dataclass
class _ContestIntroPayload:
    """_ContestIntroPayload"""
    contest: '_ContestPublicDetails'
    needsBasicInformation: bool
    privacyStatement: '_PrivacyStatement'
    requestsUserInformation: str

    def __init__(
        self,
        *,
        contest: Dict[str, Any],
        needsBasicInformation: bool,
        privacyStatement: Dict[str, Any],
        requestsUserInformation: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contest = _ContestPublicDetails(**contest)
        self.needsBasicInformation = needsBasicInformation
        self.privacyStatement = _PrivacyStatement(**privacyStatement)
        self.requestsUserInformation = requestsUserInformation


@dataclasses.dataclass
class _ContestList:
    """_ContestList"""
    current: Sequence['_ContestListItem']
    future: Sequence['_ContestListItem']
    past: Sequence['_ContestListItem']

    def __init__(
        self,
        *,
        current: Sequence[Dict[str, Any]],
        future: Sequence[Dict[str, Any]],
        past: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.current = [_ContestListItem(**v) for v in current]
        self.future = [_ContestListItem(**v) for v in future]
        self.past = [_ContestListItem(**v) for v in past]


@dataclasses.dataclass
class _ContestListItem:
    """_ContestListItem"""
    admission_mode: str
    alias: str
    contest_id: int
    contestants: int
    description: str
    finish_time: datetime.datetime
    last_updated: datetime.datetime
    organizer: str
    original_finish_time: datetime.datetime
    partial_score: bool
    participating: bool
    problemset_id: int
    recommended: bool
    rerun_id: Optional[int]
    start_time: datetime.datetime
    title: str
    window_length: Optional[int]

    def __init__(
        self,
        *,
        admission_mode: str,
        alias: str,
        contest_id: int,
        contestants: int,
        description: str,
        finish_time: int,
        last_updated: int,
        organizer: str,
        original_finish_time: int,
        partial_score: bool,
        participating: bool,
        problemset_id: int,
        recommended: bool,
        start_time: int,
        title: str,
        rerun_id: Optional[int] = None,
        window_length: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admission_mode = admission_mode
        self.alias = alias
        self.contest_id = contest_id
        self.contestants = contestants
        self.description = description
        self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        self.last_updated = datetime.datetime.fromtimestamp(last_updated)
        self.organizer = organizer
        self.original_finish_time = datetime.datetime.fromtimestamp(
            original_finish_time)
        self.partial_score = partial_score
        self.participating = participating
        self.problemset_id = problemset_id
        self.recommended = recommended
        if rerun_id is not None:
            self.rerun_id = rerun_id
        else:
            self.rerun_id = None
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        self.title = title
        if window_length is not None:
            self.window_length = window_length
        else:
            self.window_length = None


@dataclasses.dataclass
class _ContestListMinePayload:
    """_ContestListMinePayload"""
    contests: Sequence['_Contest']
    privateContestsAlert: bool

    def __init__(
        self,
        *,
        contests: Sequence[Dict[str, Any]],
        privateContestsAlert: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = [_Contest(**v) for v in contests]
        self.privateContestsAlert = privateContestsAlert


@dataclasses.dataclass
class _ContestListPayload:
    """_ContestListPayload"""
    contests: Dict[str, Sequence['_ContestListItem']]
    isLogged: bool
    query: str

    def __init__(
        self,
        *,
        contests: Dict[str, Sequence[Dict[str, Any]]],
        isLogged: bool,
        query: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = {
            k: [_ContestListItem(**v) for v in v]
            for k, v in contests.items()
        }
        self.isLogged = isLogged
        self.query = query


@dataclasses.dataclass
class _ContestListv2Payload:
    """_ContestListv2Payload"""
    contests: '_ContestList'
    query: Optional[str]

    def __init__(
        self,
        *,
        contests: Dict[str, Any],
        query: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = _ContestList(**contests)
        if query is not None:
            self.query = query
        else:
            self.query = None


@dataclasses.dataclass
class _ContestNewPayload:
    """_ContestNewPayload"""
    languages: Dict[str, str]

    def __init__(
        self,
        *,
        languages: Dict[str, str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.languages = {k: v for k, v in languages.items()}


@dataclasses.dataclass
class _ContestParticipated:
    """_ContestParticipated"""
    alias: str
    finish_time: datetime.datetime
    last_updated: datetime.datetime
    start_time: datetime.datetime
    title: str

    def __init__(
        self,
        *,
        alias: str,
        finish_time: int,
        last_updated: int,
        start_time: int,
        title: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        self.last_updated = datetime.datetime.fromtimestamp(last_updated)
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        self.title = title


@dataclasses.dataclass
class _ContestPracticeDetailsPayload:
    """_ContestPracticeDetailsPayload"""
    adminPayload: Optional['_ContestPracticeDetailsPayload_adminPayload']
    clarifications: Sequence['_Clarification']
    contest: '_ContestPublicDetails'
    contestAdmin: bool
    original: Optional['_ContestPracticeDetailsPayload_original']
    problems: Sequence['_NavbarProblemsetProblem']
    shouldShowFirstAssociatedIdentityRunWarning: bool
    submissionDeadline: Optional[datetime.datetime]

    def __init__(
        self,
        *,
        clarifications: Sequence[Dict[str, Any]],
        contest: Dict[str, Any],
        contestAdmin: bool,
        problems: Sequence[Dict[str, Any]],
        shouldShowFirstAssociatedIdentityRunWarning: bool,
        adminPayload: Optional[Dict[str, Any]] = None,
        original: Optional[Dict[str, Any]] = None,
        submissionDeadline: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if adminPayload is not None:
            self.adminPayload = _ContestPracticeDetailsPayload_adminPayload(
                **adminPayload)
        else:
            self.adminPayload = None
        self.clarifications = [_Clarification(**v) for v in clarifications]
        self.contest = _ContestPublicDetails(**contest)
        self.contestAdmin = contestAdmin
        if original is not None:
            self.original = _ContestPracticeDetailsPayload_original(**original)
        else:
            self.original = None
        self.problems = [_NavbarProblemsetProblem(**v) for v in problems]
        self.shouldShowFirstAssociatedIdentityRunWarning = shouldShowFirstAssociatedIdentityRunWarning
        if submissionDeadline is not None:
            self.submissionDeadline = datetime.datetime.fromtimestamp(
                submissionDeadline)
        else:
            self.submissionDeadline = None


@dataclasses.dataclass
class _ContestPracticeDetailsPayload_adminPayload:
    """_ContestPracticeDetailsPayload_adminPayload"""
    allRuns: Sequence['_Run']
    users: Sequence['_ContestUser']

    def __init__(
        self,
        *,
        allRuns: Sequence[Dict[str, Any]],
        users: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.allRuns = [_Run(**v) for v in allRuns]
        self.users = [_ContestUser(**v) for v in users]


@dataclasses.dataclass
class _ContestPracticeDetailsPayload_original:
    """_ContestPracticeDetailsPayload_original"""
    contest: _OmegaUp_DAO_VO_Contests
    scoreboard: Optional['_Scoreboard']
    scoreboardEvents: Optional[Sequence['_ScoreboardEvent']]

    def __init__(
        self,
        *,
        contest: Dict[str, Any],
        scoreboard: Optional[Dict[str, Any]] = None,
        scoreboardEvents: Optional[Sequence[Dict[str, Any]]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contest = _OmegaUp_DAO_VO_Contests(**contest)
        if scoreboard is not None:
            self.scoreboard = _Scoreboard(**scoreboard)
        else:
            self.scoreboard = None
        if scoreboardEvents is not None:
            self.scoreboardEvents = [
                _ScoreboardEvent(**v) for v in scoreboardEvents
            ]
        else:
            self.scoreboardEvents = None


@dataclasses.dataclass
class _ContestPrintDetailsPayload:
    """_ContestPrintDetailsPayload"""
    contestTitle: str
    problems: Dict[int, Optional['_ProblemDetails']]

    def __init__(
        self,
        *,
        contestTitle: str,
        problems: Dict[int, Optional[Dict[str, Any]]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contestTitle = contestTitle
        self.problems = {
            k: _ProblemDetails(**v) if v is not None else None
            for k, v in problems.items()
        }


@dataclasses.dataclass
class _ContestPublicDetails:
    """_ContestPublicDetails"""
    admission_mode: str
    alias: str
    default_show_all_contestants_in_scoreboard: bool
    description: str
    director: str
    feedback: str
    finish_time: datetime.datetime
    languages: str
    partial_score: bool
    penalty: int
    penalty_calc_policy: str
    penalty_type: str
    points_decay_factor: float
    problemset_id: int
    rerun_id: Optional[int]
    scoreboard: int
    show_penalty: bool
    show_scoreboard_after: bool
    start_time: datetime.datetime
    submissions_gap: int
    title: str
    user_registration_accepted: Optional[bool]
    user_registration_answered: Optional[bool]
    user_registration_requested: Optional[bool]
    window_length: Optional[int]

    def __init__(
        self,
        *,
        admission_mode: str,
        alias: str,
        default_show_all_contestants_in_scoreboard: bool,
        description: str,
        director: str,
        feedback: str,
        finish_time: int,
        languages: str,
        partial_score: bool,
        penalty: int,
        penalty_calc_policy: str,
        penalty_type: str,
        points_decay_factor: float,
        problemset_id: int,
        scoreboard: int,
        show_penalty: bool,
        show_scoreboard_after: bool,
        start_time: int,
        submissions_gap: int,
        title: str,
        rerun_id: Optional[int] = None,
        user_registration_accepted: Optional[bool] = None,
        user_registration_answered: Optional[bool] = None,
        user_registration_requested: Optional[bool] = None,
        window_length: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admission_mode = admission_mode
        self.alias = alias
        self.default_show_all_contestants_in_scoreboard = default_show_all_contestants_in_scoreboard
        self.description = description
        self.director = director
        self.feedback = feedback
        self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        self.languages = languages
        self.partial_score = partial_score
        self.penalty = penalty
        self.penalty_calc_policy = penalty_calc_policy
        self.penalty_type = penalty_type
        self.points_decay_factor = points_decay_factor
        self.problemset_id = problemset_id
        if rerun_id is not None:
            self.rerun_id = rerun_id
        else:
            self.rerun_id = None
        self.scoreboard = scoreboard
        self.show_penalty = show_penalty
        self.show_scoreboard_after = show_scoreboard_after
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        self.submissions_gap = submissions_gap
        self.title = title
        if user_registration_accepted is not None:
            self.user_registration_accepted = user_registration_accepted
        else:
            self.user_registration_accepted = None
        if user_registration_answered is not None:
            self.user_registration_answered = user_registration_answered
        else:
            self.user_registration_answered = None
        if user_registration_requested is not None:
            self.user_registration_requested = user_registration_requested
        else:
            self.user_registration_requested = None
        if window_length is not None:
            self.window_length = window_length
        else:
            self.window_length = None


@dataclasses.dataclass
class _ContestReport:
    """_ContestReport"""
    country: Optional[str]
    is_invited: bool
    name: Optional[str]
    place: Optional[int]
    problems: Sequence['_ScoreboardRankingProblem']
    total: '_ContestReport_total'
    username: str

    def __init__(
        self,
        *,
        is_invited: bool,
        problems: Sequence[Dict[str, Any]],
        total: Dict[str, Any],
        username: str,
        country: Optional[str] = None,
        name: Optional[str] = None,
        place: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if country is not None:
            self.country = country
        else:
            self.country = None
        self.is_invited = is_invited
        if name is not None:
            self.name = name
        else:
            self.name = None
        if place is not None:
            self.place = place
        else:
            self.place = None
        self.problems = [_ScoreboardRankingProblem(**v) for v in problems]
        self.total = _ContestReport_total(**total)
        self.username = username


@dataclasses.dataclass
class _ContestReportDetailsPayload:
    """_ContestReportDetailsPayload"""
    contestAlias: str
    contestReport: Sequence['_ContestReport']

    def __init__(
        self,
        *,
        contestAlias: str,
        contestReport: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contestAlias = contestAlias
        self.contestReport = [_ContestReport(**v) for v in contestReport]


@dataclasses.dataclass
class _ContestReport_total:
    """_ContestReport_total"""
    penalty: float
    points: float

    def __init__(
        self,
        *,
        penalty: float,
        points: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.penalty = penalty
        self.points = points


@dataclasses.dataclass
class _ContestRequest:
    """_ContestRequest"""
    accepted: Optional[bool]
    admin: Optional['_ContestRequest_admin']
    country: Optional[str]
    last_update: Optional[datetime.datetime]
    request_time: datetime.datetime
    username: str

    def __init__(
        self,
        *,
        request_time: int,
        username: str,
        accepted: Optional[bool] = None,
        admin: Optional[Dict[str, Any]] = None,
        country: Optional[str] = None,
        last_update: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if accepted is not None:
            self.accepted = accepted
        else:
            self.accepted = None
        if admin is not None:
            self.admin = _ContestRequest_admin(**admin)
        else:
            self.admin = None
        if country is not None:
            self.country = country
        else:
            self.country = None
        if last_update is not None:
            self.last_update = datetime.datetime.fromtimestamp(last_update)
        else:
            self.last_update = None
        self.request_time = datetime.datetime.fromtimestamp(request_time)
        self.username = username


@dataclasses.dataclass
class _ContestRequest_admin:
    """_ContestRequest_admin"""
    username: Optional[str]

    def __init__(
        self,
        *,
        username: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if username is not None:
            self.username = username
        else:
            self.username = None


@dataclasses.dataclass
class _ContestScoreboardPayload:
    """_ContestScoreboardPayload"""
    contest: '_ContestDetails'
    contestAdmin: bool
    problems: Sequence['_NavbarProblemsetProblem']
    scoreboard: '_Scoreboard'
    scoreboardEvents: Sequence['_ScoreboardEvent']
    scoreboardToken: Optional[str]

    def __init__(
        self,
        *,
        contest: Dict[str, Any],
        contestAdmin: bool,
        problems: Sequence[Dict[str, Any]],
        scoreboard: Dict[str, Any],
        scoreboardEvents: Sequence[Dict[str, Any]],
        scoreboardToken: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contest = _ContestDetails(**contest)
        self.contestAdmin = contestAdmin
        self.problems = [_NavbarProblemsetProblem(**v) for v in problems]
        self.scoreboard = _Scoreboard(**scoreboard)
        self.scoreboardEvents = [
            _ScoreboardEvent(**v) for v in scoreboardEvents
        ]
        if scoreboardToken is not None:
            self.scoreboardToken = scoreboardToken
        else:
            self.scoreboardToken = None


@dataclasses.dataclass
class _ContestUser:
    """_ContestUser"""
    access_time: Optional[datetime.datetime]
    country_id: Optional[str]
    end_time: Optional[datetime.datetime]
    is_owner: Optional[int]
    username: str

    def __init__(
        self,
        *,
        username: str,
        access_time: Optional[int] = None,
        country_id: Optional[str] = None,
        end_time: Optional[int] = None,
        is_owner: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if access_time is not None:
            self.access_time = datetime.datetime.fromtimestamp(access_time)
        else:
            self.access_time = None
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        if end_time is not None:
            self.end_time = datetime.datetime.fromtimestamp(end_time)
        else:
            self.end_time = None
        if is_owner is not None:
            self.is_owner = is_owner
        else:
            self.is_owner = None
        self.username = username


@dataclasses.dataclass
class _ContestVirtualDetailsPayload:
    """_ContestVirtualDetailsPayload"""
    contest: '_ContestPublicDetails'

    def __init__(
        self,
        *,
        contest: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contest = _ContestPublicDetails(**contest)


@dataclasses.dataclass
class _Contestant:
    """_Contestant"""
    country: Optional[str]
    email: Optional[str]
    gender: Optional[str]
    name: Optional[str]
    school: Optional[str]
    state: Optional[str]
    username: str

    def __init__(
        self,
        *,
        username: str,
        country: Optional[str] = None,
        email: Optional[str] = None,
        gender: Optional[str] = None,
        name: Optional[str] = None,
        school: Optional[str] = None,
        state: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if country is not None:
            self.country = country
        else:
            self.country = None
        if email is not None:
            self.email = email
        else:
            self.email = None
        if gender is not None:
            self.gender = gender
        else:
            self.gender = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        if school is not None:
            self.school = school
        else:
            self.school = None
        if state is not None:
            self.state = state
        else:
            self.state = None
        self.username = username


@dataclasses.dataclass
class _Course:
    """_Course"""
    acl_id: Optional[int]
    admission_mode: str
    alias: str
    archived: bool
    course_id: int
    description: str
    finish_time: Optional[datetime.datetime]
    group_id: Optional[int]
    languages: Optional[str]
    level: Optional[str]
    minimum_progress_for_certificate: Optional[int]
    name: str
    needs_basic_information: bool
    objective: Optional[str]
    requests_user_information: str
    school_id: Optional[int]
    show_scoreboard: bool
    start_time: datetime.datetime

    def __init__(
        self,
        *,
        admission_mode: str,
        alias: str,
        archived: bool,
        course_id: int,
        description: str,
        name: str,
        needs_basic_information: bool,
        requests_user_information: str,
        show_scoreboard: bool,
        start_time: int,
        acl_id: Optional[int] = None,
        finish_time: Optional[int] = None,
        group_id: Optional[int] = None,
        languages: Optional[str] = None,
        level: Optional[str] = None,
        minimum_progress_for_certificate: Optional[int] = None,
        objective: Optional[str] = None,
        school_id: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if acl_id is not None:
            self.acl_id = acl_id
        else:
            self.acl_id = None
        self.admission_mode = admission_mode
        self.alias = alias
        self.archived = archived
        self.course_id = course_id
        self.description = description
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        if group_id is not None:
            self.group_id = group_id
        else:
            self.group_id = None
        if languages is not None:
            self.languages = languages
        else:
            self.languages = None
        if level is not None:
            self.level = level
        else:
            self.level = None
        if minimum_progress_for_certificate is not None:
            self.minimum_progress_for_certificate = minimum_progress_for_certificate
        else:
            self.minimum_progress_for_certificate = None
        self.name = name
        self.needs_basic_information = needs_basic_information
        if objective is not None:
            self.objective = objective
        else:
            self.objective = None
        self.requests_user_information = requests_user_information
        if school_id is not None:
            self.school_id = school_id
        else:
            self.school_id = None
        self.show_scoreboard = show_scoreboard
        self.start_time = datetime.datetime.fromtimestamp(start_time)


@dataclasses.dataclass
class _CourseAdmin:
    """_CourseAdmin"""
    role: str
    username: str

    def __init__(
        self,
        *,
        role: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.role = role
        self.username = username


@dataclasses.dataclass
class _CourseAssignment:
    """_CourseAssignment"""
    alias: str
    assignment_type: str
    description: str
    finish_time: Optional[datetime.datetime]
    has_runs: bool
    max_points: float
    name: str
    opened: bool
    order: int
    problemCount: int
    problemset_id: int
    publish_time_delay: Optional[int]
    scoreboard_url: str
    scoreboard_url_admin: str
    start_time: datetime.datetime

    def __init__(
        self,
        *,
        alias: str,
        assignment_type: str,
        description: str,
        has_runs: bool,
        max_points: float,
        name: str,
        opened: bool,
        order: int,
        problemCount: int,
        problemset_id: int,
        scoreboard_url: str,
        scoreboard_url_admin: str,
        start_time: int,
        finish_time: Optional[int] = None,
        publish_time_delay: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.assignment_type = assignment_type
        self.description = description
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        self.has_runs = has_runs
        self.max_points = max_points
        self.name = name
        self.opened = opened
        self.order = order
        self.problemCount = problemCount
        self.problemset_id = problemset_id
        if publish_time_delay is not None:
            self.publish_time_delay = publish_time_delay
        else:
            self.publish_time_delay = None
        self.scoreboard_url = scoreboard_url
        self.scoreboard_url_admin = scoreboard_url_admin
        self.start_time = datetime.datetime.fromtimestamp(start_time)


@dataclasses.dataclass
class _CourseCardEnrolled:
    """_CourseCardEnrolled"""
    alias: str
    name: str
    progress: float
    school_name: Optional[str]

    def __init__(
        self,
        *,
        alias: str,
        name: str,
        progress: float,
        school_name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.name = name
        self.progress = progress
        if school_name is not None:
            self.school_name = school_name
        else:
            self.school_name = None


@dataclasses.dataclass
class _CourseCardFinished:
    """_CourseCardFinished"""
    alias: str
    name: str

    def __init__(
        self,
        *,
        alias: str,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.name = name


@dataclasses.dataclass
class _CourseCardPublic:
    """_CourseCardPublic"""
    alias: str
    alreadyStarted: bool
    lessonCount: int
    level: Optional[str]
    name: str
    school_name: Optional[str]
    studentCount: int

    def __init__(
        self,
        *,
        alias: str,
        alreadyStarted: bool,
        lessonCount: int,
        name: str,
        studentCount: int,
        level: Optional[str] = None,
        school_name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.alreadyStarted = alreadyStarted
        self.lessonCount = lessonCount
        if level is not None:
            self.level = level
        else:
            self.level = None
        self.name = name
        if school_name is not None:
            self.school_name = school_name
        else:
            self.school_name = None
        self.studentCount = studentCount


@dataclasses.dataclass
class _CourseClarificationsPayload:
    """_CourseClarificationsPayload"""
    clarifications: Sequence['_Clarification']
    length: int
    page: int
    pagerItems: Sequence['_PageItem']

    def __init__(
        self,
        *,
        clarifications: Sequence[Dict[str, Any]],
        length: int,
        page: int,
        pagerItems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.clarifications = [_Clarification(**v) for v in clarifications]
        self.length = length
        self.page = page
        self.pagerItems = [_PageItem(**v) for v in pagerItems]


@dataclasses.dataclass
class _CourseCloneDetailsPayload:
    """_CourseCloneDetailsPayload"""
    creator: '_CourseCloneDetailsPayload_creator'
    details: '_CourseDetails'
    token: Optional[str]

    def __init__(
        self,
        *,
        creator: Dict[str, Any],
        details: Dict[str, Any],
        token: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.creator = _CourseCloneDetailsPayload_creator(**creator)
        self.details = _CourseDetails(**details)
        if token is not None:
            self.token = token
        else:
            self.token = None


@dataclasses.dataclass
class _CourseCloneDetailsPayload_creator:
    """_CourseCloneDetailsPayload_creator"""
    classname: str
    username: str

    def __init__(
        self,
        *,
        classname: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        self.username = username


@dataclasses.dataclass
class _CourseDetails:
    """_CourseDetails"""
    admission_mode: str
    alias: str
    archived: bool
    assignments: Sequence['_CourseAssignment']
    clarifications: Sequence['_Clarification']
    description: str
    finish_time: Optional[datetime.datetime]
    is_admin: bool
    is_curator: bool
    languages: Optional[Sequence[str]]
    level: Optional[str]
    name: str
    needs_basic_information: bool
    objective: Optional[str]
    requests_user_information: str
    school_id: Optional[int]
    school_name: Optional[str]
    show_scoreboard: bool
    start_time: datetime.datetime
    student_count: Optional[int]
    unlimited_duration: bool

    def __init__(
        self,
        *,
        admission_mode: str,
        alias: str,
        archived: bool,
        assignments: Sequence[Dict[str, Any]],
        clarifications: Sequence[Dict[str, Any]],
        description: str,
        is_admin: bool,
        is_curator: bool,
        name: str,
        needs_basic_information: bool,
        requests_user_information: str,
        show_scoreboard: bool,
        start_time: int,
        unlimited_duration: bool,
        finish_time: Optional[int] = None,
        languages: Optional[Sequence[str]] = None,
        level: Optional[str] = None,
        objective: Optional[str] = None,
        school_id: Optional[int] = None,
        school_name: Optional[str] = None,
        student_count: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admission_mode = admission_mode
        self.alias = alias
        self.archived = archived
        self.assignments = [_CourseAssignment(**v) for v in assignments]
        self.clarifications = [_Clarification(**v) for v in clarifications]
        self.description = description
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        self.is_admin = is_admin
        self.is_curator = is_curator
        if languages is not None:
            self.languages = [v for v in languages]
        else:
            self.languages = None
        if level is not None:
            self.level = level
        else:
            self.level = None
        self.name = name
        self.needs_basic_information = needs_basic_information
        if objective is not None:
            self.objective = objective
        else:
            self.objective = None
        self.requests_user_information = requests_user_information
        if school_id is not None:
            self.school_id = school_id
        else:
            self.school_id = None
        if school_name is not None:
            self.school_name = school_name
        else:
            self.school_name = None
        self.show_scoreboard = show_scoreboard
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        if student_count is not None:
            self.student_count = student_count
        else:
            self.student_count = None
        self.unlimited_duration = unlimited_duration


@dataclasses.dataclass
class _CourseDetailsPayload:
    """_CourseDetailsPayload"""
    details: '_CourseDetails'
    progress: Optional[Dict[str, '_Progress']]

    def __init__(
        self,
        *,
        details: Dict[str, Any],
        progress: Optional[Dict[str, Dict[str, Any]]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.details = _CourseDetails(**details)
        if progress is not None:
            self.progress = {k: _Progress(**v) for k, v in progress.items()}
        else:
            self.progress = None


@dataclasses.dataclass
class _CourseEditPayload:
    """_CourseEditPayload"""
    admins: Sequence['_CourseAdmin']
    allLanguages: Dict[str, str]
    assignmentProblems: Sequence['_ProblemsetProblem']
    course: '_CourseDetails'
    groupsAdmins: Sequence['_CourseGroupAdmin']
    identityRequests: Sequence['_IdentityRequest']
    selectedAssignment: Optional['_CourseAssignment']
    students: Sequence['_CourseStudent']
    tags: Sequence[str]

    def __init__(
        self,
        *,
        admins: Sequence[Dict[str, Any]],
        allLanguages: Dict[str, str],
        assignmentProblems: Sequence[Dict[str, Any]],
        course: Dict[str, Any],
        groupsAdmins: Sequence[Dict[str, Any]],
        identityRequests: Sequence[Dict[str, Any]],
        students: Sequence[Dict[str, Any]],
        tags: Sequence[str],
        selectedAssignment: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admins = [_CourseAdmin(**v) for v in admins]
        self.allLanguages = {k: v for k, v in allLanguages.items()}
        self.assignmentProblems = [
            _ProblemsetProblem(**v) for v in assignmentProblems
        ]
        self.course = _CourseDetails(**course)
        self.groupsAdmins = [_CourseGroupAdmin(**v) for v in groupsAdmins]
        self.identityRequests = [
            _IdentityRequest(**v) for v in identityRequests
        ]
        if selectedAssignment is not None:
            self.selectedAssignment = _CourseAssignment(**selectedAssignment)
        else:
            self.selectedAssignment = None
        self.students = [_CourseStudent(**v) for v in students]
        self.tags = [v for v in tags]


@dataclasses.dataclass
class _CourseGroupAdmin:
    """_CourseGroupAdmin"""
    alias: str
    name: str
    role: str

    def __init__(
        self,
        *,
        alias: str,
        name: str,
        role: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.name = name
        self.role = role


@dataclasses.dataclass
class _CourseListMinePayload:
    """_CourseListMinePayload"""
    courses: '_AdminCourses'

    def __init__(
        self,
        *,
        courses: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.courses = _AdminCourses(**courses)


@dataclasses.dataclass
class _CourseNewPayload:
    """_CourseNewPayload"""
    is_admin: bool
    is_curator: bool
    languages: Dict[str, str]

    def __init__(
        self,
        *,
        is_admin: bool,
        is_curator: bool,
        languages: Dict[str, str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.is_admin = is_admin
        self.is_curator = is_curator
        self.languages = {k: v for k, v in languages.items()}


@dataclasses.dataclass
class _CourseProblem:
    """_CourseProblem"""
    accepted: int
    alias: str
    commit: str
    difficulty: float
    languages: str
    letter: str
    order: int
    points: float
    runs: Sequence['_CourseRun']
    submissions: int
    title: str
    version: str
    visibility: int
    visits: int

    def __init__(
        self,
        *,
        accepted: int,
        alias: str,
        commit: str,
        difficulty: float,
        languages: str,
        letter: str,
        order: int,
        points: float,
        runs: Sequence[Dict[str, Any]],
        submissions: int,
        title: str,
        version: str,
        visibility: int,
        visits: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.accepted = accepted
        self.alias = alias
        self.commit = commit
        self.difficulty = difficulty
        self.languages = languages
        self.letter = letter
        self.order = order
        self.points = points
        self.runs = [_CourseRun(**v) for v in runs]
        self.submissions = submissions
        self.title = title
        self.version = version
        self.visibility = visibility
        self.visits = visits


@dataclasses.dataclass
class _CourseProblemStatistics:
    """_CourseProblemStatistics"""
    assignment_alias: str
    average: float
    avg_runs: float
    completed_score_percentage: float
    high_score_percentage: float
    low_score_percentage: float
    max_points: float
    maximum: float
    minimum: float
    problem_alias: str
    variance: float

    def __init__(
        self,
        *,
        assignment_alias: str,
        average: float,
        avg_runs: float,
        completed_score_percentage: float,
        high_score_percentage: float,
        low_score_percentage: float,
        max_points: float,
        maximum: float,
        minimum: float,
        problem_alias: str,
        variance: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.assignment_alias = assignment_alias
        self.average = average
        self.avg_runs = avg_runs
        self.completed_score_percentage = completed_score_percentage
        self.high_score_percentage = high_score_percentage
        self.low_score_percentage = low_score_percentage
        self.max_points = max_points
        self.maximum = maximum
        self.minimum = minimum
        self.problem_alias = problem_alias
        self.variance = variance


@dataclasses.dataclass
class _CourseProblemTried:
    """_CourseProblemTried"""
    alias: str
    title: str
    username: str

    def __init__(
        self,
        *,
        alias: str,
        title: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.title = title
        self.username = username


@dataclasses.dataclass
class _CourseProblemVerdict:
    """_CourseProblemVerdict"""
    assignment_alias: str
    problem_alias: str
    problem_id: int
    runs: int
    verdict: Optional[str]

    def __init__(
        self,
        *,
        assignment_alias: str,
        problem_alias: str,
        problem_id: int,
        runs: int,
        verdict: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.assignment_alias = assignment_alias
        self.problem_alias = problem_alias
        self.problem_id = problem_id
        self.runs = runs
        if verdict is not None:
            self.verdict = verdict
        else:
            self.verdict = None


@dataclasses.dataclass
class _CourseRun:
    """_CourseRun"""
    contest_score: Optional[float]
    feedback: Optional['_SubmissionFeedback']
    guid: str
    language: str
    memory: int
    penalty: int
    runtime: int
    score: float
    source: Optional[str]
    status: str
    submit_delay: int
    time: datetime.datetime
    verdict: str

    def __init__(
        self,
        *,
        guid: str,
        language: str,
        memory: int,
        penalty: int,
        runtime: int,
        score: float,
        status: str,
        submit_delay: int,
        time: int,
        verdict: str,
        contest_score: Optional[float] = None,
        feedback: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if contest_score is not None:
            self.contest_score = contest_score
        else:
            self.contest_score = None
        if feedback is not None:
            self.feedback = _SubmissionFeedback(**feedback)
        else:
            self.feedback = None
        self.guid = guid
        self.language = language
        self.memory = memory
        self.penalty = penalty
        self.runtime = runtime
        self.score = score
        if source is not None:
            self.source = source
        else:
            self.source = None
        self.status = status
        self.submit_delay = submit_delay
        self.time = datetime.datetime.fromtimestamp(time)
        self.verdict = verdict


@dataclasses.dataclass
class _CourseScoreboardPayload:
    """_CourseScoreboardPayload"""
    assignment: '_AssignmentDetails'
    problems: Sequence['_NavbarProblemsetProblem']
    scoreboard: '_Scoreboard'
    scoreboardToken: Optional[str]

    def __init__(
        self,
        *,
        assignment: Dict[str, Any],
        problems: Sequence[Dict[str, Any]],
        scoreboard: Dict[str, Any],
        scoreboardToken: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.assignment = _AssignmentDetails(**assignment)
        self.problems = [_NavbarProblemsetProblem(**v) for v in problems]
        self.scoreboard = _Scoreboard(**scoreboard)
        if scoreboardToken is not None:
            self.scoreboardToken = scoreboardToken
        else:
            self.scoreboardToken = None


@dataclasses.dataclass
class _CourseStatisticsPayload:
    """_CourseStatisticsPayload"""
    course: '_CourseDetails'
    problemStats: Sequence['_CourseProblemStatistics']
    verdicts: Sequence['_CourseProblemVerdict']

    def __init__(
        self,
        *,
        course: Dict[str, Any],
        problemStats: Sequence[Dict[str, Any]],
        verdicts: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.course = _CourseDetails(**course)
        self.problemStats = [
            _CourseProblemStatistics(**v) for v in problemStats
        ]
        self.verdicts = [_CourseProblemVerdict(**v) for v in verdicts]


@dataclasses.dataclass
class _CourseStudent:
    """_CourseStudent"""
    name: Optional[str]
    username: str

    def __init__(
        self,
        *,
        username: str,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.username = username


@dataclasses.dataclass
class _CourseSubmissionsListPayload:
    """_CourseSubmissionsListPayload"""
    solvedProblems: Dict[str, Sequence['_CourseProblemTried']]
    unsolvedProblems: Dict[str, Sequence['_CourseProblemTried']]

    def __init__(
        self,
        *,
        solvedProblems: Dict[str, Sequence[Dict[str, Any]]],
        unsolvedProblems: Dict[str, Sequence[Dict[str, Any]]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.solvedProblems = {
            k: [_CourseProblemTried(**v) for v in v]
            for k, v in solvedProblems.items()
        }
        self.unsolvedProblems = {
            k: [_CourseProblemTried(**v) for v in v]
            for k, v in unsolvedProblems.items()
        }


@dataclasses.dataclass
class _CourseTabsPayload:
    """_CourseTabsPayload"""
    courses: '_CourseTabsPayload_courses'

    def __init__(
        self,
        *,
        courses: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.courses = _CourseTabsPayload_courses(**courses)


@dataclasses.dataclass
class _CourseTabsPayload_courses:
    """_CourseTabsPayload_courses"""
    enrolled: Sequence['_CourseCardEnrolled']
    finished: Sequence['_CourseCardFinished']
    public: Sequence['_CourseCardPublic']

    def __init__(
        self,
        *,
        enrolled: Sequence[Dict[str, Any]],
        finished: Sequence[Dict[str, Any]],
        public: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.enrolled = [_CourseCardEnrolled(**v) for v in enrolled]
        self.finished = [_CourseCardFinished(**v) for v in finished]
        self.public = [_CourseCardPublic(**v) for v in public]


@dataclasses.dataclass
class _CoursesByAccessMode:
    """_CoursesByAccessMode"""
    accessMode: str
    activeTab: str
    filteredCourses: '_CoursesByAccessMode_filteredCourses'

    def __init__(
        self,
        *,
        accessMode: str,
        activeTab: str,
        filteredCourses: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.accessMode = accessMode
        self.activeTab = activeTab
        self.filteredCourses = _CoursesByAccessMode_filteredCourses(
            **filteredCourses)


@dataclasses.dataclass
class _CoursesByAccessMode_filteredCourses:
    """_CoursesByAccessMode_filteredCourses"""
    current: '_CoursesByTimeType'
    past: '_CoursesByTimeType'

    def __init__(
        self,
        *,
        current: Dict[str, Any],
        past: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.current = _CoursesByTimeType(**current)
        self.past = _CoursesByTimeType(**past)


@dataclasses.dataclass
class _CoursesByTimeType:
    """_CoursesByTimeType"""
    courses: Sequence['_FilteredCourse']
    timeType: str

    def __init__(
        self,
        *,
        courses: Sequence[Dict[str, Any]],
        timeType: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.courses = [_FilteredCourse(**v) for v in courses]
        self.timeType = timeType


@dataclasses.dataclass
class _CoursesList:
    """_CoursesList"""
    admin: Sequence['_FilteredCourse']
    archived: Optional[Sequence['_FilteredCourse']]
    public: Sequence['_FilteredCourse']
    student: Sequence['_FilteredCourse']

    def __init__(
        self,
        *,
        admin: Sequence[Dict[str, Any]],
        public: Sequence[Dict[str, Any]],
        student: Sequence[Dict[str, Any]],
        archived: Optional[Sequence[Dict[str, Any]]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = [_FilteredCourse(**v) for v in admin]
        if archived is not None:
            self.archived = [_FilteredCourse(**v) for v in archived]
        else:
            self.archived = None
        self.public = [_FilteredCourse(**v) for v in public]
        self.student = [_FilteredCourse(**v) for v in student]


@dataclasses.dataclass
class _CurrentSession:
    """_CurrentSession"""
    apiTokenId: Optional[int]
    associated_identities: Sequence['_AssociatedIdentity']
    auth_token: Optional[str]
    cacheKey: Optional[str]
    classname: str
    email: Optional[str]
    identity: Optional[_OmegaUp_DAO_VO_Identities]
    is_admin: bool
    loginIdentity: Optional[_OmegaUp_DAO_VO_Identities]
    user: Optional[_OmegaUp_DAO_VO_Users]
    valid: bool

    def __init__(
        self,
        *,
        associated_identities: Sequence[Dict[str, Any]],
        classname: str,
        is_admin: bool,
        valid: bool,
        apiTokenId: Optional[int] = None,
        auth_token: Optional[str] = None,
        cacheKey: Optional[str] = None,
        email: Optional[str] = None,
        identity: Optional[Dict[str, Any]] = None,
        loginIdentity: Optional[Dict[str, Any]] = None,
        user: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if apiTokenId is not None:
            self.apiTokenId = apiTokenId
        else:
            self.apiTokenId = None
        self.associated_identities = [
            _AssociatedIdentity(**v) for v in associated_identities
        ]
        if auth_token is not None:
            self.auth_token = auth_token
        else:
            self.auth_token = None
        if cacheKey is not None:
            self.cacheKey = cacheKey
        else:
            self.cacheKey = None
        self.classname = classname
        if email is not None:
            self.email = email
        else:
            self.email = None
        if identity is not None:
            self.identity = _OmegaUp_DAO_VO_Identities(**identity)
        else:
            self.identity = None
        self.is_admin = is_admin
        if loginIdentity is not None:
            self.loginIdentity = _OmegaUp_DAO_VO_Identities(**loginIdentity)
        else:
            self.loginIdentity = None
        if user is not None:
            self.user = _OmegaUp_DAO_VO_Users(**user)
        else:
            self.user = None
        self.valid = valid


@dataclasses.dataclass
class _EmailEditDetailsPayload:
    """_EmailEditDetailsPayload"""
    email: Optional[str]
    profile: Optional['_UserProfileInfo']

    def __init__(
        self,
        *,
        email: Optional[str] = None,
        profile: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if email is not None:
            self.email = email
        else:
            self.email = None
        if profile is not None:
            self.profile = _UserProfileInfo(**profile)
        else:
            self.profile = None


@dataclasses.dataclass
class _Event:
    """_Event"""
    courseAlias: Optional[str]
    courseName: Optional[str]
    name: str
    problem: Optional[str]

    def __init__(
        self,
        *,
        name: str,
        courseAlias: Optional[str] = None,
        courseName: Optional[str] = None,
        problem: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if courseAlias is not None:
            self.courseAlias = courseAlias
        else:
            self.courseAlias = None
        if courseName is not None:
            self.courseName = courseName
        else:
            self.courseName = None
        self.name = name
        if problem is not None:
            self.problem = problem
        else:
            self.problem = None


@dataclasses.dataclass
class _Experiment:
    """_Experiment"""
    config: bool
    hash: str
    name: str

    def __init__(
        self,
        *,
        config: bool,
        hash: str,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.config = config
        self.hash = hash
        self.name = name


@dataclasses.dataclass
class _ExtraProfileDetails:
    """_ExtraProfileDetails"""
    badges: Sequence[str]
    contests: Dict[str, '_UserProfileContests_value']
    createdContests: Sequence['_Contest']
    createdCourses: Sequence['_Course']
    createdProblems: Sequence['_Problem']
    hasPassword: bool
    ownedBadges: Sequence['_Badge']
    solvedProblems: Sequence['_Problem']
    stats: Sequence['_UserProfileStats']
    unsolvedProblems: Sequence['_Problem']

    def __init__(
        self,
        *,
        badges: Sequence[str],
        contests: Dict[str, Dict[str, Any]],
        createdContests: Sequence[Dict[str, Any]],
        createdCourses: Sequence[Dict[str, Any]],
        createdProblems: Sequence[Dict[str, Any]],
        hasPassword: bool,
        ownedBadges: Sequence[Dict[str, Any]],
        solvedProblems: Sequence[Dict[str, Any]],
        stats: Sequence[Dict[str, Any]],
        unsolvedProblems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.badges = [v for v in badges]
        self.contests = {
            k: _UserProfileContests_value(**v)
            for k, v in contests.items()
        }
        self.createdContests = [_Contest(**v) for v in createdContests]
        self.createdCourses = [_Course(**v) for v in createdCourses]
        self.createdProblems = [_Problem(**v) for v in createdProblems]
        self.hasPassword = hasPassword
        self.ownedBadges = [_Badge(**v) for v in ownedBadges]
        self.solvedProblems = [_Problem(**v) for v in solvedProblems]
        self.stats = [_UserProfileStats(**v) for v in stats]
        self.unsolvedProblems = [_Problem(**v) for v in unsolvedProblems]


@dataclasses.dataclass
class _FilteredCourse:
    """_FilteredCourse"""
    accept_teacher: Optional[bool]
    admission_mode: str
    alias: str
    assignments: Sequence['_CourseAssignment']
    counts: Dict[str, int]
    description: str
    finish_time: Optional[datetime.datetime]
    is_open: bool
    name: str
    progress: Optional[float]
    school_name: Optional[str]
    start_time: datetime.datetime

    def __init__(
        self,
        *,
        admission_mode: str,
        alias: str,
        assignments: Sequence[Dict[str, Any]],
        counts: Dict[str, int],
        description: str,
        is_open: bool,
        name: str,
        start_time: int,
        accept_teacher: Optional[bool] = None,
        finish_time: Optional[int] = None,
        progress: Optional[float] = None,
        school_name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if accept_teacher is not None:
            self.accept_teacher = accept_teacher
        else:
            self.accept_teacher = None
        self.admission_mode = admission_mode
        self.alias = alias
        self.assignments = [_CourseAssignment(**v) for v in assignments]
        self.counts = {k: v for k, v in counts.items()}
        self.description = description
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        self.is_open = is_open
        self.name = name
        if progress is not None:
            self.progress = progress
        else:
            self.progress = None
        if school_name is not None:
            self.school_name = school_name
        else:
            self.school_name = None
        self.start_time = datetime.datetime.fromtimestamp(start_time)


@dataclasses.dataclass
class _GraderStatus:
    """_GraderStatus"""
    broadcaster_sockets: int
    embedded_runner: bool
    queue: '_GraderStatus_queue'
    status: str

    def __init__(
        self,
        *,
        broadcaster_sockets: int,
        embedded_runner: bool,
        queue: Dict[str, Any],
        status: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.broadcaster_sockets = broadcaster_sockets
        self.embedded_runner = embedded_runner
        self.queue = _GraderStatus_queue(**queue)
        self.status = status


@dataclasses.dataclass
class _GraderStatus_queue:
    """_GraderStatus_queue"""
    run_queue_length: int
    runner_queue_length: int
    runners: Sequence[str]
    running: Sequence['_GraderStatus_queue_running_entry']

    def __init__(
        self,
        *,
        run_queue_length: int,
        runner_queue_length: int,
        runners: Sequence[str],
        running: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.run_queue_length = run_queue_length
        self.runner_queue_length = runner_queue_length
        self.runners = [v for v in runners]
        self.running = [
            _GraderStatus_queue_running_entry(**v) for v in running
        ]


@dataclasses.dataclass
class _GraderStatus_queue_running_entry:
    """_GraderStatus_queue_running_entry"""
    id: int
    name: str

    def __init__(
        self,
        *,
        id: int,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.id = id
        self.name = name


@dataclasses.dataclass
class _Group:
    """_Group"""
    alias: str
    create_time: datetime.datetime
    description: Optional[str]
    name: str

    def __init__(
        self,
        *,
        alias: str,
        create_time: int,
        name: str,
        description: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.create_time = datetime.datetime.fromtimestamp(create_time)
        if description is not None:
            self.description = description
        else:
            self.description = None
        self.name = name


@dataclasses.dataclass
class _GroupEditPayload:
    """_GroupEditPayload"""
    countries: Sequence['_OmegaUp_DAO_VO_Countries']
    groupAlias: str
    groupDescription: Optional[str]
    groupName: Optional[str]
    identities: Sequence['_Identity']
    isOrganizer: bool
    scoreboards: Sequence['_GroupScoreboard']

    def __init__(
        self,
        *,
        countries: Sequence[Dict[str, Any]],
        groupAlias: str,
        identities: Sequence[Dict[str, Any]],
        isOrganizer: bool,
        scoreboards: Sequence[Dict[str, Any]],
        groupDescription: Optional[str] = None,
        groupName: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.countries = [_OmegaUp_DAO_VO_Countries(**v) for v in countries]
        self.groupAlias = groupAlias
        if groupDescription is not None:
            self.groupDescription = groupDescription
        else:
            self.groupDescription = None
        if groupName is not None:
            self.groupName = groupName
        else:
            self.groupName = None
        self.identities = [_Identity(**v) for v in identities]
        self.isOrganizer = isOrganizer
        self.scoreboards = [_GroupScoreboard(**v) for v in scoreboards]


@dataclasses.dataclass
class _GroupListItem:
    """_GroupListItem"""
    label: str
    value: str

    def __init__(
        self,
        *,
        label: str,
        value: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.label = label
        self.value = value


@dataclasses.dataclass
class _GroupListPayload:
    """_GroupListPayload"""
    groups: Sequence['_Group']

    def __init__(
        self,
        *,
        groups: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.groups = [_Group(**v) for v in groups]


@dataclasses.dataclass
class _GroupScoreboard:
    """_GroupScoreboard"""
    alias: str
    create_time: str
    description: Optional[str]
    name: str

    def __init__(
        self,
        *,
        alias: str,
        create_time: str,
        name: str,
        description: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.create_time = create_time
        if description is not None:
            self.description = description
        else:
            self.description = None
        self.name = name


@dataclasses.dataclass
class _GroupScoreboardContestsPayload:
    """_GroupScoreboardContestsPayload"""
    availableContests: Sequence['_ContestListItem']
    contests: Sequence['_ScoreboardContest']
    groupAlias: str
    scoreboardAlias: str

    def __init__(
        self,
        *,
        availableContests: Sequence[Dict[str, Any]],
        contests: Sequence[Dict[str, Any]],
        groupAlias: str,
        scoreboardAlias: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.availableContests = [
            _ContestListItem(**v) for v in availableContests
        ]
        self.contests = [_ScoreboardContest(**v) for v in contests]
        self.groupAlias = groupAlias
        self.scoreboardAlias = scoreboardAlias


@dataclasses.dataclass
class _GroupScoreboardDetails:
    """_GroupScoreboardDetails"""
    contests: Sequence['_ScoreboardContest']
    ranking: Sequence['_ScoreboardRanking']
    scoreboard: '_ScoreboardDetails'

    def __init__(
        self,
        *,
        contests: Sequence[Dict[str, Any]],
        ranking: Sequence[Dict[str, Any]],
        scoreboard: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = [_ScoreboardContest(**v) for v in contests]
        self.ranking = [_ScoreboardRanking(**v) for v in ranking]
        self.scoreboard = _ScoreboardDetails(**scoreboard)


@dataclasses.dataclass
class _GroupScoreboardDetailsPayload:
    """_GroupScoreboardDetailsPayload"""
    details: '_GroupScoreboardDetails'
    groupAlias: str
    scoreboardAlias: str

    def __init__(
        self,
        *,
        details: Dict[str, Any],
        groupAlias: str,
        scoreboardAlias: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.details = _GroupScoreboardDetails(**details)
        self.groupAlias = groupAlias
        self.scoreboardAlias = scoreboardAlias


@dataclasses.dataclass
class _Histogram:
    """_Histogram"""
    difficulty: float
    difficultyHistogram: Optional[str]
    quality: float
    qualityHistogram: Optional[str]

    def __init__(
        self,
        *,
        difficulty: float,
        quality: float,
        difficultyHistogram: Optional[str] = None,
        qualityHistogram: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.difficulty = difficulty
        if difficultyHistogram is not None:
            self.difficultyHistogram = difficultyHistogram
        else:
            self.difficultyHistogram = None
        self.quality = quality
        if qualityHistogram is not None:
            self.qualityHistogram = qualityHistogram
        else:
            self.qualityHistogram = None


@dataclasses.dataclass
class _Identity:
    """_Identity"""
    classname: Optional[str]
    country: Optional[str]
    country_id: Optional[str]
    gender: Optional[str]
    name: Optional[str]
    password: Optional[str]
    school: Optional[str]
    school_id: Optional[int]
    school_name: Optional[str]
    state: Optional[str]
    state_id: Optional[str]
    username: str

    def __init__(
        self,
        *,
        username: str,
        classname: Optional[str] = None,
        country: Optional[str] = None,
        country_id: Optional[str] = None,
        gender: Optional[str] = None,
        name: Optional[str] = None,
        password: Optional[str] = None,
        school: Optional[str] = None,
        school_id: Optional[int] = None,
        school_name: Optional[str] = None,
        state: Optional[str] = None,
        state_id: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if classname is not None:
            self.classname = classname
        else:
            self.classname = None
        if country is not None:
            self.country = country
        else:
            self.country = None
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        if gender is not None:
            self.gender = gender
        else:
            self.gender = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        if password is not None:
            self.password = password
        else:
            self.password = None
        if school is not None:
            self.school = school
        else:
            self.school = None
        if school_id is not None:
            self.school_id = school_id
        else:
            self.school_id = None
        if school_name is not None:
            self.school_name = school_name
        else:
            self.school_name = None
        if state is not None:
            self.state = state
        else:
            self.state = None
        if state_id is not None:
            self.state_id = state_id
        else:
            self.state_id = None
        self.username = username


@dataclasses.dataclass
class _IdentityExt:
    """_IdentityExt"""
    classname: str
    country_id: Optional[str]
    current_identity_school_id: Optional[int]
    gender: Optional[str]
    identity_id: int
    language_id: Optional[int]
    name: Optional[str]
    password: Optional[str]
    state_id: Optional[str]
    user_id: Optional[int]
    username: str

    def __init__(
        self,
        *,
        classname: str,
        identity_id: int,
        username: str,
        country_id: Optional[str] = None,
        current_identity_school_id: Optional[int] = None,
        gender: Optional[str] = None,
        language_id: Optional[int] = None,
        name: Optional[str] = None,
        password: Optional[str] = None,
        state_id: Optional[str] = None,
        user_id: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        if current_identity_school_id is not None:
            self.current_identity_school_id = current_identity_school_id
        else:
            self.current_identity_school_id = None
        if gender is not None:
            self.gender = gender
        else:
            self.gender = None
        self.identity_id = identity_id
        if language_id is not None:
            self.language_id = language_id
        else:
            self.language_id = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        if password is not None:
            self.password = password
        else:
            self.password = None
        if state_id is not None:
            self.state_id = state_id
        else:
            self.state_id = None
        if user_id is not None:
            self.user_id = user_id
        else:
            self.user_id = None
        self.username = username


@dataclasses.dataclass
class _IdentityRequest:
    """_IdentityRequest"""
    accepted: Optional[bool]
    admin: Optional['_IdentityRequest_admin']
    classname: str
    country: Optional[str]
    country_id: Optional[str]
    last_update: Optional[datetime.datetime]
    name: Optional[str]
    request_time: datetime.datetime
    username: str

    def __init__(
        self,
        *,
        classname: str,
        request_time: int,
        username: str,
        accepted: Optional[bool] = None,
        admin: Optional[Dict[str, Any]] = None,
        country: Optional[str] = None,
        country_id: Optional[str] = None,
        last_update: Optional[int] = None,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if accepted is not None:
            self.accepted = accepted
        else:
            self.accepted = None
        if admin is not None:
            self.admin = _IdentityRequest_admin(**admin)
        else:
            self.admin = None
        self.classname = classname
        if country is not None:
            self.country = country
        else:
            self.country = None
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        if last_update is not None:
            self.last_update = datetime.datetime.fromtimestamp(last_update)
        else:
            self.last_update = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.request_time = datetime.datetime.fromtimestamp(request_time)
        self.username = username


@dataclasses.dataclass
class _IdentityRequest_admin:
    """_IdentityRequest_admin"""
    name: Optional[str]
    username: str

    def __init__(
        self,
        *,
        username: str,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.username = username


@dataclasses.dataclass
class _IndexPayload:
    """_IndexPayload"""
    coderOfTheMonthData: '_IndexPayload_coderOfTheMonthData'
    currentUserInfo: '_IndexPayload_currentUserInfo'
    schoolOfTheMonthData: Optional['_IndexPayload_schoolOfTheMonthData']
    schoolRank: Sequence['_IndexPayload_schoolRank_entry']
    userRank: Sequence['_CoderOfTheMonth']

    def __init__(
        self,
        *,
        coderOfTheMonthData: Dict[str, Any],
        currentUserInfo: Dict[str, Any],
        schoolRank: Sequence[Dict[str, Any]],
        userRank: Sequence[Dict[str, Any]],
        schoolOfTheMonthData: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.coderOfTheMonthData = _IndexPayload_coderOfTheMonthData(
            **coderOfTheMonthData)
        self.currentUserInfo = _IndexPayload_currentUserInfo(**currentUserInfo)
        if schoolOfTheMonthData is not None:
            self.schoolOfTheMonthData = _IndexPayload_schoolOfTheMonthData(
                **schoolOfTheMonthData)
        else:
            self.schoolOfTheMonthData = None
        self.schoolRank = [
            _IndexPayload_schoolRank_entry(**v) for v in schoolRank
        ]
        self.userRank = [_CoderOfTheMonth(**v) for v in userRank]


@dataclasses.dataclass
class _IndexPayload_coderOfTheMonthData:
    """_IndexPayload_coderOfTheMonthData"""
    all: Optional['_UserProfile']
    female: Optional['_UserProfile']

    def __init__(
        self,
        *,
        all: Optional[Dict[str, Any]] = None,
        female: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if all is not None:
            self.all = _UserProfile(**all)
        else:
            self.all = None
        if female is not None:
            self.female = _UserProfile(**female)
        else:
            self.female = None


@dataclasses.dataclass
class _IndexPayload_currentUserInfo:
    """_IndexPayload_currentUserInfo"""
    username: Optional[str]

    def __init__(
        self,
        *,
        username: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if username is not None:
            self.username = username
        else:
            self.username = None


@dataclasses.dataclass
class _IndexPayload_schoolOfTheMonthData:
    """_IndexPayload_schoolOfTheMonthData"""
    country: Optional[str]
    country_id: Optional[str]
    name: str
    school_id: int
    state: Optional[str]

    def __init__(
        self,
        *,
        name: str,
        school_id: int,
        country: Optional[str] = None,
        country_id: Optional[str] = None,
        state: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if country is not None:
            self.country = country
        else:
            self.country = None
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        self.name = name
        self.school_id = school_id
        if state is not None:
            self.state = state
        else:
            self.state = None


@dataclasses.dataclass
class _IndexPayload_schoolRank_entry:
    """_IndexPayload_schoolRank_entry"""
    name: str
    ranking: int
    school_id: int
    school_of_the_month_id: int
    score: float

    def __init__(
        self,
        *,
        name: str,
        ranking: int,
        school_id: int,
        school_of_the_month_id: int,
        score: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.ranking = ranking
        self.school_id = school_id
        self.school_of_the_month_id = school_of_the_month_id
        self.score = score


@dataclasses.dataclass
class _InteractiveInterface:
    """_InteractiveInterface"""
    ExecutableDescription: '_InteractiveInterface_ExecutableDescription'
    Files: Dict[str, str]
    MakefileRules: Sequence['_InteractiveInterface_MakefileRules_entry']

    def __init__(
        self,
        *,
        ExecutableDescription: Dict[str, Any],
        Files: Dict[str, str],
        MakefileRules: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.ExecutableDescription = _InteractiveInterface_ExecutableDescription(
            **ExecutableDescription)
        self.Files = {k: v for k, v in Files.items()}
        self.MakefileRules = [
            _InteractiveInterface_MakefileRules_entry(**v)
            for v in MakefileRules
        ]


@dataclasses.dataclass
class _InteractiveInterface_ExecutableDescription:
    """_InteractiveInterface_ExecutableDescription"""
    Args: Sequence[str]
    Env: Dict[str, str]

    def __init__(
        self,
        *,
        Args: Sequence[str],
        Env: Dict[str, str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.Args = [v for v in Args]
        self.Env = {k: v for k, v in Env.items()}


@dataclasses.dataclass
class _InteractiveInterface_MakefileRules_entry:
    """_InteractiveInterface_MakefileRules_entry"""
    Compiler: str
    Debug: bool
    Params: str
    Requisites: Sequence[str]
    Targets: Sequence[str]

    def __init__(
        self,
        *,
        Compiler: str,
        Debug: bool,
        Params: str,
        Requisites: Sequence[str],
        Targets: Sequence[str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.Compiler = Compiler
        self.Debug = Debug
        self.Params = Params
        self.Requisites = [v for v in Requisites]
        self.Targets = [v for v in Targets]


@dataclasses.dataclass
class _InteractiveSettingsDistrib:
    """_InteractiveSettingsDistrib"""
    idl: str
    language: str
    main_source: str
    module_name: str
    templates: Dict[str, str]

    def __init__(
        self,
        *,
        idl: str,
        language: str,
        main_source: str,
        module_name: str,
        templates: Dict[str, str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.idl = idl
        self.language = language
        self.main_source = main_source
        self.module_name = module_name
        self.templates = {k: v for k, v in templates.items()}


@dataclasses.dataclass
class _IntroCourseDetails:
    """_IntroCourseDetails"""
    details: '_CourseDetails'
    progress: Dict[str, Dict[str, float]]

    def __init__(
        self,
        *,
        details: Dict[str, Any],
        progress: Dict[str, Dict[str, float]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.details = _CourseDetails(**details)
        self.progress = {
            k: {k: v
                for k, v in v.items()}
            for k, v in progress.items()
        }


@dataclasses.dataclass
class _IntroDetailsPayload:
    """_IntroDetailsPayload"""
    course: '_CourseDetails'
    isFirstTimeAccess: bool
    needsBasicInformation: bool
    shouldShowAcceptTeacher: bool
    shouldShowResults: bool
    statements: '_IntroDetailsPayload_statements'
    userRegistrationAccepted: Optional[bool]
    userRegistrationAnswered: Optional[bool]
    userRegistrationRequested: Optional[bool]

    def __init__(
        self,
        *,
        course: Dict[str, Any],
        isFirstTimeAccess: bool,
        needsBasicInformation: bool,
        shouldShowAcceptTeacher: bool,
        shouldShowResults: bool,
        statements: Dict[str, Any],
        userRegistrationAccepted: Optional[bool] = None,
        userRegistrationAnswered: Optional[bool] = None,
        userRegistrationRequested: Optional[bool] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.course = _CourseDetails(**course)
        self.isFirstTimeAccess = isFirstTimeAccess
        self.needsBasicInformation = needsBasicInformation
        self.shouldShowAcceptTeacher = shouldShowAcceptTeacher
        self.shouldShowResults = shouldShowResults
        self.statements = _IntroDetailsPayload_statements(**statements)
        if userRegistrationAccepted is not None:
            self.userRegistrationAccepted = userRegistrationAccepted
        else:
            self.userRegistrationAccepted = None
        if userRegistrationAnswered is not None:
            self.userRegistrationAnswered = userRegistrationAnswered
        else:
            self.userRegistrationAnswered = None
        if userRegistrationRequested is not None:
            self.userRegistrationRequested = userRegistrationRequested
        else:
            self.userRegistrationRequested = None


@dataclasses.dataclass
class _IntroDetailsPayload_statements:
    """_IntroDetailsPayload_statements"""
    acceptTeacher: Optional['_PrivacyStatement']
    privacy: Optional['_PrivacyStatement']

    def __init__(
        self,
        *,
        acceptTeacher: Optional[Dict[str, Any]] = None,
        privacy: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if acceptTeacher is not None:
            self.acceptTeacher = _PrivacyStatement(**acceptTeacher)
        else:
            self.acceptTeacher = None
        if privacy is not None:
            self.privacy = _PrivacyStatement(**privacy)
        else:
            self.privacy = None


@dataclasses.dataclass
class _LibinteractiveError:
    """_LibinteractiveError"""
    description: str
    field: str

    def __init__(
        self,
        *,
        description: str,
        field: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.description = description
        self.field = field


@dataclasses.dataclass
class _LibinteractiveGenPayload:
    """_LibinteractiveGenPayload"""
    error: Optional['_LibinteractiveError']
    idl: Optional[str]
    language: Optional[str]
    name: Optional[str]
    os: Optional[str]

    def __init__(
        self,
        *,
        error: Optional[Dict[str, Any]] = None,
        idl: Optional[str] = None,
        language: Optional[str] = None,
        name: Optional[str] = None,
        os: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if error is not None:
            self.error = _LibinteractiveError(**error)
        else:
            self.error = None
        if idl is not None:
            self.idl = idl
        else:
            self.idl = None
        if language is not None:
            self.language = language
        else:
            self.language = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        if os is not None:
            self.os = os
        else:
            self.os = None


@dataclasses.dataclass
class _LimitsSettings:
    """_LimitsSettings"""
    ExtraWallTime: str
    MemoryLimit: Union[int, str]
    OutputLimit: Union[int, str]
    OverallWallTimeLimit: str
    TimeLimit: str

    def __init__(
        self,
        *,
        ExtraWallTime: str,
        MemoryLimit: Union[int, str],
        OutputLimit: Union[int, str],
        OverallWallTimeLimit: str,
        TimeLimit: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.ExtraWallTime = ExtraWallTime
        self.MemoryLimit = MemoryLimit
        self.OutputLimit = OutputLimit
        self.OverallWallTimeLimit = OverallWallTimeLimit
        self.TimeLimit = TimeLimit


@dataclasses.dataclass
class _ListItem:
    """_ListItem"""
    key: str
    value: str

    def __init__(
        self,
        *,
        key: str,
        value: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.key = key
        self.value = value


@dataclasses.dataclass
class _LoginDetailsPayload:
    """_LoginDetailsPayload"""
    facebookUrl: Optional[str]
    statusError: Optional[str]
    validateRecaptcha: bool
    verifyEmailSuccessfully: Optional[str]

    def __init__(
        self,
        *,
        validateRecaptcha: bool,
        facebookUrl: Optional[str] = None,
        statusError: Optional[str] = None,
        verifyEmailSuccessfully: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if facebookUrl is not None:
            self.facebookUrl = facebookUrl
        else:
            self.facebookUrl = None
        if statusError is not None:
            self.statusError = statusError
        else:
            self.statusError = None
        self.validateRecaptcha = validateRecaptcha
        if verifyEmailSuccessfully is not None:
            self.verifyEmailSuccessfully = verifyEmailSuccessfully
        else:
            self.verifyEmailSuccessfully = None


@dataclasses.dataclass
class _MergedScoreboardEntry:
    """_MergedScoreboardEntry"""
    contests: Dict[str, '_MergedScoreboardEntry_contests_value']
    name: Optional[str]
    place: Optional[int]
    total: '_MergedScoreboardEntry_total'
    username: str

    def __init__(
        self,
        *,
        contests: Dict[str, Dict[str, Any]],
        total: Dict[str, Any],
        username: str,
        name: Optional[str] = None,
        place: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = {
            k: _MergedScoreboardEntry_contests_value(**v)
            for k, v in contests.items()
        }
        if name is not None:
            self.name = name
        else:
            self.name = None
        if place is not None:
            self.place = place
        else:
            self.place = None
        self.total = _MergedScoreboardEntry_total(**total)
        self.username = username


@dataclasses.dataclass
class _MergedScoreboardEntry_contests_value:
    """_MergedScoreboardEntry_contests_value"""
    penalty: float
    points: float

    def __init__(
        self,
        *,
        penalty: float,
        points: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.penalty = penalty
        self.points = points


@dataclasses.dataclass
class _MergedScoreboardEntry_total:
    """_MergedScoreboardEntry_total"""
    penalty: float
    points: float

    def __init__(
        self,
        *,
        penalty: float,
        points: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.penalty = penalty
        self.points = points


@dataclasses.dataclass
class _NavbarProblemsetProblem:
    """_NavbarProblemsetProblem"""
    acceptsSubmissions: bool
    alias: str
    bestScore: int
    hasRuns: bool
    maxScore: Union[float, int]
    text: str

    def __init__(
        self,
        *,
        acceptsSubmissions: bool,
        alias: str,
        bestScore: int,
        hasRuns: bool,
        maxScore: Union[float, int],
        text: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.acceptsSubmissions = acceptsSubmissions
        self.alias = alias
        self.bestScore = bestScore
        self.hasRuns = hasRuns
        self.maxScore = maxScore
        self.text = text


@dataclasses.dataclass
class _NominationListItem:
    """_NominationListItem"""
    author: '_NominationListItem_author'
    contents: Optional['_NominationListItem_contents']
    nomination: str
    nominator: '_NominationListItem_nominator'
    problem: '_NominationListItem_problem'
    qualitynomination_id: int
    status: str
    time: datetime.datetime
    votes: Sequence['_NominationListItem_votes_entry']

    def __init__(
        self,
        *,
        author: Dict[str, Any],
        nomination: str,
        nominator: Dict[str, Any],
        problem: Dict[str, Any],
        qualitynomination_id: int,
        status: str,
        time: int,
        votes: Sequence[Dict[str, Any]],
        contents: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.author = _NominationListItem_author(**author)
        if contents is not None:
            self.contents = _NominationListItem_contents(**contents)
        else:
            self.contents = None
        self.nomination = nomination
        self.nominator = _NominationListItem_nominator(**nominator)
        self.problem = _NominationListItem_problem(**problem)
        self.qualitynomination_id = qualitynomination_id
        self.status = status
        self.time = datetime.datetime.fromtimestamp(time)
        self.votes = [_NominationListItem_votes_entry(**v) for v in votes]


@dataclasses.dataclass
class _NominationListItem_author:
    """_NominationListItem_author"""
    name: Optional[str]
    username: str

    def __init__(
        self,
        *,
        username: str,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.username = username


@dataclasses.dataclass
class _NominationListItem_contents:
    """_NominationListItem_contents"""
    before_ac: Optional[bool]
    difficulty: Optional[int]
    quality: Optional[int]
    rationale: Optional[str]
    reason: Optional[str]
    statements: Optional[Dict[str, str]]
    tags: Optional[Sequence[str]]

    def __init__(
        self,
        *,
        before_ac: Optional[bool] = None,
        difficulty: Optional[int] = None,
        quality: Optional[int] = None,
        rationale: Optional[str] = None,
        reason: Optional[str] = None,
        statements: Optional[Dict[str, str]] = None,
        tags: Optional[Sequence[str]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if before_ac is not None:
            self.before_ac = before_ac
        else:
            self.before_ac = None
        if difficulty is not None:
            self.difficulty = difficulty
        else:
            self.difficulty = None
        if quality is not None:
            self.quality = quality
        else:
            self.quality = None
        if rationale is not None:
            self.rationale = rationale
        else:
            self.rationale = None
        if reason is not None:
            self.reason = reason
        else:
            self.reason = None
        if statements is not None:
            self.statements = {k: v for k, v in statements.items()}
        else:
            self.statements = None
        if tags is not None:
            self.tags = [v for v in tags]
        else:
            self.tags = None


@dataclasses.dataclass
class _NominationListItem_nominator:
    """_NominationListItem_nominator"""
    name: Optional[str]
    username: str

    def __init__(
        self,
        *,
        username: str,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.username = username


@dataclasses.dataclass
class _NominationListItem_problem:
    """_NominationListItem_problem"""
    alias: str
    title: str

    def __init__(
        self,
        *,
        alias: str,
        title: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.title = title


@dataclasses.dataclass
class _NominationListItem_votes_entry:
    """_NominationListItem_votes_entry"""
    time: Optional[datetime.datetime]
    user: '_NominationListItem_votes_entry_user'
    vote: int

    def __init__(
        self,
        *,
        user: Dict[str, Any],
        vote: int,
        time: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if time is not None:
            self.time = datetime.datetime.fromtimestamp(time)
        else:
            self.time = None
        self.user = _NominationListItem_votes_entry_user(**user)
        self.vote = vote


@dataclasses.dataclass
class _NominationListItem_votes_entry_user:
    """_NominationListItem_votes_entry_user"""
    name: Optional[str]
    username: str

    def __init__(
        self,
        *,
        username: str,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.username = username


@dataclasses.dataclass
class _NominationStatus:
    """_NominationStatus"""
    alreadyReviewed: bool
    canNominateProblem: bool
    dismissed: bool
    dismissedBeforeAc: bool
    language: str
    nominated: bool
    nominatedBeforeAc: bool
    solved: bool
    tried: bool

    def __init__(
        self,
        *,
        alreadyReviewed: bool,
        canNominateProblem: bool,
        dismissed: bool,
        dismissedBeforeAc: bool,
        language: str,
        nominated: bool,
        nominatedBeforeAc: bool,
        solved: bool,
        tried: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alreadyReviewed = alreadyReviewed
        self.canNominateProblem = canNominateProblem
        self.dismissed = dismissed
        self.dismissedBeforeAc = dismissedBeforeAc
        self.language = language
        self.nominated = nominated
        self.nominatedBeforeAc = nominatedBeforeAc
        self.solved = solved
        self.tried = tried


@dataclasses.dataclass
class _Notification:
    """_Notification"""
    contents: '_NotificationContents'
    notification_id: int
    timestamp: datetime.datetime

    def __init__(
        self,
        *,
        contents: Dict[str, Any],
        notification_id: int,
        timestamp: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contents = _NotificationContents(**contents)
        self.notification_id = notification_id
        self.timestamp = datetime.datetime.fromtimestamp(timestamp)


@dataclasses.dataclass
class _NotificationContents:
    """_NotificationContents"""
    badge: Optional[str]
    body: Optional['_NotificationContents_body']
    message: Optional[str]
    status: Optional[str]
    type: str
    url: Optional[str]

    def __init__(
        self,
        *,
        type: str,
        badge: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
        message: Optional[str] = None,
        status: Optional[str] = None,
        url: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if badge is not None:
            self.badge = badge
        else:
            self.badge = None
        if body is not None:
            self.body = _NotificationContents_body(**body)
        else:
            self.body = None
        if message is not None:
            self.message = message
        else:
            self.message = None
        if status is not None:
            self.status = status
        else:
            self.status = None
        self.type = type
        if url is not None:
            self.url = url
        else:
            self.url = None


@dataclasses.dataclass
class _NotificationContents_body:
    """_NotificationContents_body"""
    iconUrl: str
    localizationParams: Sequence[str]
    localizationString: str
    url: str

    def __init__(
        self,
        *,
        iconUrl: str,
        localizationParams: Sequence[str],
        localizationString: str,
        url: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.iconUrl = iconUrl
        self.localizationParams = [v for v in localizationParams]
        self.localizationString = localizationString
        self.url = url


@dataclasses.dataclass
class _OmegaUp_Controllers_Admin__apiPlatformReportStats:
    """_OmegaUp_Controllers_Admin__apiPlatformReportStats"""
    report: '_OmegaUp_Controllers_Admin__apiPlatformReportStats_report'

    def __init__(
        self,
        *,
        report: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.report = _OmegaUp_Controllers_Admin__apiPlatformReportStats_report(
            **report)


@dataclasses.dataclass
class _OmegaUp_Controllers_Admin__apiPlatformReportStats_report:
    """_OmegaUp_Controllers_Admin__apiPlatformReportStats_report"""
    acceptedSubmissions: int
    activeSchools: int
    activeUsers: Dict[str, int]
    courses: int
    omiCourse: '_OmegaUp_Controllers_Admin__apiPlatformReportStats_report_omiCourse'

    def __init__(
        self,
        *,
        acceptedSubmissions: int,
        activeSchools: int,
        activeUsers: Dict[str, int],
        courses: int,
        omiCourse: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.acceptedSubmissions = acceptedSubmissions
        self.activeSchools = activeSchools
        self.activeUsers = {k: v for k, v in activeUsers.items()}
        self.courses = courses
        self.omiCourse = _OmegaUp_Controllers_Admin__apiPlatformReportStats_report_omiCourse(
            **omiCourse)


@dataclasses.dataclass
class _OmegaUp_Controllers_Admin__apiPlatformReportStats_report_omiCourse:
    """_OmegaUp_Controllers_Admin__apiPlatformReportStats_report_omiCourse"""
    attemptedUsers: int
    completedUsers: int
    passedUsers: int

    def __init__(
        self,
        *,
        attemptedUsers: int,
        completedUsers: int,
        passedUsers: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.attemptedUsers = attemptedUsers
        self.completedUsers = completedUsers
        self.passedUsers = passedUsers


@dataclasses.dataclass
class _OmegaUp_Controllers_Authorization__apiProblem:
    """_OmegaUp_Controllers_Authorization__apiProblem"""
    can_edit: bool
    can_view: bool
    has_solved: bool
    is_admin: bool

    def __init__(
        self,
        *,
        can_edit: bool,
        can_view: bool,
        has_solved: bool,
        is_admin: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.can_edit = can_edit
        self.can_view = can_view
        self.has_solved = has_solved
        self.is_admin = is_admin


@dataclasses.dataclass
class _OmegaUp_Controllers_Badge__apiMyBadgeAssignationTime:
    """_OmegaUp_Controllers_Badge__apiMyBadgeAssignationTime"""
    assignation_time: Optional[datetime.datetime]

    def __init__(
        self,
        *,
        assignation_time: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if assignation_time is not None:
            self.assignation_time = datetime.datetime.fromtimestamp(
                assignation_time)
        else:
            self.assignation_time = None


@dataclasses.dataclass
class _OmegaUp_Controllers_Badge__apiMyList:
    """_OmegaUp_Controllers_Badge__apiMyList"""
    badges: Sequence['_Badge']

    def __init__(
        self,
        *,
        badges: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.badges = [_Badge(**v) for v in badges]


@dataclasses.dataclass
class _OmegaUp_Controllers_Badge__apiUserList:
    """_OmegaUp_Controllers_Badge__apiUserList"""
    badges: Sequence['_Badge']

    def __init__(
        self,
        *,
        badges: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.badges = [_Badge(**v) for v in badges]


@dataclasses.dataclass
class _OmegaUp_Controllers_Clarification__apiDetails:
    """_OmegaUp_Controllers_Clarification__apiDetails"""
    answer: Optional[str]
    message: str
    problem_id: int
    problemset_id: Optional[int]
    time: datetime.datetime

    def __init__(
        self,
        *,
        message: str,
        problem_id: int,
        time: int,
        answer: Optional[str] = None,
        problemset_id: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if answer is not None:
            self.answer = answer
        else:
            self.answer = None
        self.message = message
        self.problem_id = problem_id
        if problemset_id is not None:
            self.problemset_id = problemset_id
        else:
            self.problemset_id = None
        self.time = datetime.datetime.fromtimestamp(time)


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiActivityReport:
    """_OmegaUp_Controllers_Contest__apiActivityReport"""
    events: Sequence['_ActivityEvent']
    pagerItems: Sequence['_PageItem']

    def __init__(
        self,
        *,
        events: Sequence[Dict[str, Any]],
        pagerItems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.events = [_ActivityEvent(**v) for v in events]
        self.pagerItems = [_PageItem(**v) for v in pagerItems]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiAdminList:
    """_OmegaUp_Controllers_Contest__apiAdminList"""
    contests: Sequence['_Contest']

    def __init__(
        self,
        *,
        contests: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = [_Contest(**v) for v in contests]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiAdmins:
    """_OmegaUp_Controllers_Contest__apiAdmins"""
    admins: Sequence['_OmegaUp_Controllers_Contest__apiAdmins_admins_entry']
    group_admins: Sequence[
        '_OmegaUp_Controllers_Contest__apiAdmins_group_admins_entry']

    def __init__(
        self,
        *,
        admins: Sequence[Dict[str, Any]],
        group_admins: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admins = [
            _OmegaUp_Controllers_Contest__apiAdmins_admins_entry(**v)
            for v in admins
        ]
        self.group_admins = [
            _OmegaUp_Controllers_Contest__apiAdmins_group_admins_entry(**v)
            for v in group_admins
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiAdmins_admins_entry:
    """_OmegaUp_Controllers_Contest__apiAdmins_admins_entry"""
    role: str
    username: str

    def __init__(
        self,
        *,
        role: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.role = role
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiAdmins_group_admins_entry:
    """_OmegaUp_Controllers_Contest__apiAdmins_group_admins_entry"""
    alias: str
    name: str
    role: str

    def __init__(
        self,
        *,
        alias: str,
        name: str,
        role: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.name = name
        self.role = role


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiClarifications:
    """_OmegaUp_Controllers_Contest__apiClarifications"""
    clarifications: Sequence['_Clarification']

    def __init__(
        self,
        *,
        clarifications: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.clarifications = [_Clarification(**v) for v in clarifications]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiClone:
    """_OmegaUp_Controllers_Contest__apiClone"""
    alias: str

    def __init__(
        self,
        *,
        alias: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiContestants:
    """_OmegaUp_Controllers_Contest__apiContestants"""
    contestants: Sequence['_Contestant']

    def __init__(
        self,
        *,
        contestants: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contestants = [_Contestant(**v) for v in contestants]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiCreateVirtual:
    """_OmegaUp_Controllers_Contest__apiCreateVirtual"""
    alias: str

    def __init__(
        self,
        *,
        alias: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiList:
    """_OmegaUp_Controllers_Contest__apiList"""
    number_of_results: int
    results: Sequence['_ContestListItem']

    def __init__(
        self,
        *,
        number_of_results: int,
        results: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.number_of_results = number_of_results
        self.results = [_ContestListItem(**v) for v in results]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiListParticipating:
    """_OmegaUp_Controllers_Contest__apiListParticipating"""
    contests: Sequence['_Contest']

    def __init__(
        self,
        *,
        contests: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = [_Contest(**v) for v in contests]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiMyList:
    """_OmegaUp_Controllers_Contest__apiMyList"""
    contests: Sequence['_Contest']

    def __init__(
        self,
        *,
        contests: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = [_Contest(**v) for v in contests]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiProblemClarifications:
    """_OmegaUp_Controllers_Contest__apiProblemClarifications"""
    clarifications: Sequence['_Clarification']

    def __init__(
        self,
        *,
        clarifications: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.clarifications = [_Clarification(**v) for v in clarifications]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiProblems:
    """_OmegaUp_Controllers_Contest__apiProblems"""
    problems: Sequence['_ProblemsetProblemWithVersions']

    def __init__(
        self,
        *,
        problems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.problems = [_ProblemsetProblemWithVersions(**v) for v in problems]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiReport:
    """_OmegaUp_Controllers_Contest__apiReport"""
    finish_time: Optional[datetime.datetime]
    problems: Sequence[
        '_OmegaUp_Controllers_Contest__apiReport_problems_entry']
    ranking: Sequence['_ContestReport']
    start_time: datetime.datetime
    time: datetime.datetime
    title: str

    def __init__(
        self,
        *,
        problems: Sequence[Dict[str, Any]],
        ranking: Sequence[Dict[str, Any]],
        start_time: int,
        time: int,
        title: str,
        finish_time: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        self.problems = [
            _OmegaUp_Controllers_Contest__apiReport_problems_entry(**v)
            for v in problems
        ]
        self.ranking = [_ContestReport(**v) for v in ranking]
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        self.time = datetime.datetime.fromtimestamp(time)
        self.title = title


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiReport_problems_entry:
    """_OmegaUp_Controllers_Contest__apiReport_problems_entry"""
    alias: str
    order: int

    def __init__(
        self,
        *,
        alias: str,
        order: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.order = order


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiRequests:
    """_OmegaUp_Controllers_Contest__apiRequests"""
    contest_alias: str
    users: Sequence['_OmegaUp_Controllers_Contest__apiRequests_users_entry']

    def __init__(
        self,
        *,
        contest_alias: str,
        users: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contest_alias = contest_alias
        self.users = [
            _OmegaUp_Controllers_Contest__apiRequests_users_entry(**v)
            for v in users
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiRequests_users_entry:
    """_OmegaUp_Controllers_Contest__apiRequests_users_entry"""
    accepted: bool
    admin: Optional[
        '_OmegaUp_Controllers_Contest__apiRequests_users_entry_admin']
    country: str
    last_update: datetime.datetime
    request_time: datetime.datetime
    username: str

    def __init__(
        self,
        *,
        accepted: bool,
        country: str,
        last_update: int,
        request_time: int,
        username: str,
        admin: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.accepted = accepted
        if admin is not None:
            self.admin = _OmegaUp_Controllers_Contest__apiRequests_users_entry_admin(
                **admin)
        else:
            self.admin = None
        self.country = country
        self.last_update = datetime.datetime.fromtimestamp(last_update)
        self.request_time = datetime.datetime.fromtimestamp(request_time)
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiRequests_users_entry_admin:
    """_OmegaUp_Controllers_Contest__apiRequests_users_entry_admin"""
    username: Optional[str]

    def __init__(
        self,
        *,
        username: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if username is not None:
            self.username = username
        else:
            self.username = None


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiRole:
    """_OmegaUp_Controllers_Contest__apiRole"""
    admin: bool

    def __init__(
        self,
        *,
        admin: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = admin


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiRuns:
    """_OmegaUp_Controllers_Contest__apiRuns"""
    runs: Sequence['_Run']
    totalRuns: int

    def __init__(
        self,
        *,
        runs: Sequence[Dict[str, Any]],
        totalRuns: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.runs = [_Run(**v) for v in runs]
        self.totalRuns = totalRuns


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiRunsDiff:
    """_OmegaUp_Controllers_Contest__apiRunsDiff"""
    diff: Sequence['_OmegaUp_Controllers_Contest__apiRunsDiff_diff_entry']

    def __init__(
        self,
        *,
        diff: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.diff = [
            _OmegaUp_Controllers_Contest__apiRunsDiff_diff_entry(**v)
            for v in diff
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiRunsDiff_diff_entry:
    """_OmegaUp_Controllers_Contest__apiRunsDiff_diff_entry"""
    guid: str
    new_score: float
    new_status: str
    new_verdict: str
    old_score: float
    old_status: str
    old_verdict: str
    problemset_id: int
    username: str

    def __init__(
        self,
        *,
        guid: str,
        new_score: float,
        new_status: str,
        new_verdict: str,
        old_score: float,
        old_status: str,
        old_verdict: str,
        problemset_id: int,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.guid = guid
        self.new_score = new_score
        self.new_status = new_status
        self.new_verdict = new_verdict
        self.old_score = old_score
        self.old_status = old_status
        self.old_verdict = old_verdict
        self.problemset_id = problemset_id
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiScoreboardEvents:
    """_OmegaUp_Controllers_Contest__apiScoreboardEvents"""
    events: Sequence['_ScoreboardEvent']

    def __init__(
        self,
        *,
        events: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.events = [_ScoreboardEvent(**v) for v in events]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiScoreboardMerge:
    """_OmegaUp_Controllers_Contest__apiScoreboardMerge"""
    ranking: Sequence['_MergedScoreboardEntry']

    def __init__(
        self,
        *,
        ranking: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.ranking = [_MergedScoreboardEntry(**v) for v in ranking]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiSearchUsers:
    """_OmegaUp_Controllers_Contest__apiSearchUsers"""
    results: Sequence['_ListItem']

    def __init__(
        self,
        *,
        results: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.results = [_ListItem(**v) for v in results]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiStats:
    """_OmegaUp_Controllers_Contest__apiStats"""
    distribution: Dict[int, int]
    max_wait_time: Optional[datetime.datetime]
    max_wait_time_guid: Optional[str]
    pending_runs: Sequence[str]
    size_of_bucket: float
    total_points: float
    total_runs: int
    verdict_counts: Dict[str, int]

    def __init__(
        self,
        *,
        distribution: Dict[int, int],
        pending_runs: Sequence[str],
        size_of_bucket: float,
        total_points: float,
        total_runs: int,
        verdict_counts: Dict[str, int],
        max_wait_time: Optional[int] = None,
        max_wait_time_guid: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.distribution = {k: v for k, v in distribution.items()}
        if max_wait_time is not None:
            self.max_wait_time = datetime.datetime.fromtimestamp(max_wait_time)
        else:
            self.max_wait_time = None
        if max_wait_time_guid is not None:
            self.max_wait_time_guid = max_wait_time_guid
        else:
            self.max_wait_time_guid = None
        self.pending_runs = [v for v in pending_runs]
        self.size_of_bucket = size_of_bucket
        self.total_points = total_points
        self.total_runs = total_runs
        self.verdict_counts = {k: v for k, v in verdict_counts.items()}


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiUpdate:
    """_OmegaUp_Controllers_Contest__apiUpdate"""
    teamsGroupName: Optional[str]
    title: str

    def __init__(
        self,
        *,
        title: str,
        teamsGroupName: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if teamsGroupName is not None:
            self.teamsGroupName = teamsGroupName
        else:
            self.teamsGroupName = None
        self.title = title


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiUsers:
    """_OmegaUp_Controllers_Contest__apiUsers"""
    groups: Sequence['_OmegaUp_Controllers_Contest__apiUsers_groups_entry']
    users: Sequence['_ContestUser']

    def __init__(
        self,
        *,
        groups: Sequence[Dict[str, Any]],
        users: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.groups = [
            _OmegaUp_Controllers_Contest__apiUsers_groups_entry(**v)
            for v in groups
        ]
        self.users = [_ContestUser(**v) for v in users]


@dataclasses.dataclass
class _OmegaUp_Controllers_Contest__apiUsers_groups_entry:
    """_OmegaUp_Controllers_Contest__apiUsers_groups_entry"""
    alias: str
    name: str

    def __init__(
        self,
        *,
        alias: str,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.name = name


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiActivityReport:
    """_OmegaUp_Controllers_Course__apiActivityReport"""
    events: Sequence['_ActivityEvent']
    pagerItems: Sequence['_PageItem']

    def __init__(
        self,
        *,
        events: Sequence[Dict[str, Any]],
        pagerItems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.events = [_ActivityEvent(**v) for v in events]
        self.pagerItems = [_PageItem(**v) for v in pagerItems]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiAdmins:
    """_OmegaUp_Controllers_Course__apiAdmins"""
    admins: Sequence['_OmegaUp_Controllers_Course__apiAdmins_admins_entry']
    group_admins: Sequence[
        '_OmegaUp_Controllers_Course__apiAdmins_group_admins_entry']

    def __init__(
        self,
        *,
        admins: Sequence[Dict[str, Any]],
        group_admins: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admins = [
            _OmegaUp_Controllers_Course__apiAdmins_admins_entry(**v)
            for v in admins
        ]
        self.group_admins = [
            _OmegaUp_Controllers_Course__apiAdmins_group_admins_entry(**v)
            for v in group_admins
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiAdmins_admins_entry:
    """_OmegaUp_Controllers_Course__apiAdmins_admins_entry"""
    role: str
    username: str

    def __init__(
        self,
        *,
        role: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.role = role
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiAdmins_group_admins_entry:
    """_OmegaUp_Controllers_Course__apiAdmins_group_admins_entry"""
    alias: str
    name: str
    role: str

    def __init__(
        self,
        *,
        alias: str,
        name: str,
        role: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.name = name
        self.role = role


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiAssignmentDetails:
    """_OmegaUp_Controllers_Course__apiAssignmentDetails"""
    admin: bool
    alias: str
    assignment_type: Optional[str]
    courseAssignments: Sequence['_CourseAssignment']
    description: Optional[str]
    director: str
    finish_time: Optional[datetime.datetime]
    name: str
    problems: Sequence['_ProblemsetProblem']
    problemset_id: int
    start_time: datetime.datetime

    def __init__(
        self,
        *,
        admin: bool,
        alias: str,
        courseAssignments: Sequence[Dict[str, Any]],
        director: str,
        name: str,
        problems: Sequence[Dict[str, Any]],
        problemset_id: int,
        start_time: int,
        assignment_type: Optional[str] = None,
        description: Optional[str] = None,
        finish_time: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = admin
        self.alias = alias
        if assignment_type is not None:
            self.assignment_type = assignment_type
        else:
            self.assignment_type = None
        self.courseAssignments = [
            _CourseAssignment(**v) for v in courseAssignments
        ]
        if description is not None:
            self.description = description
        else:
            self.description = None
        self.director = director
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        self.name = name
        self.problems = [_ProblemsetProblem(**v) for v in problems]
        self.problemset_id = problemset_id
        self.start_time = datetime.datetime.fromtimestamp(start_time)


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiAssignmentScoreboardEvents:
    """_OmegaUp_Controllers_Course__apiAssignmentScoreboardEvents"""
    events: Sequence['_ScoreboardEvent']

    def __init__(
        self,
        *,
        events: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.events = [_ScoreboardEvent(**v) for v in events]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiClarifications:
    """_OmegaUp_Controllers_Course__apiClarifications"""
    clarifications: Sequence['_Clarification']

    def __init__(
        self,
        *,
        clarifications: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.clarifications = [_Clarification(**v) for v in clarifications]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiClone:
    """_OmegaUp_Controllers_Course__apiClone"""
    alias: str

    def __init__(
        self,
        *,
        alias: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiGenerateTokenForCloneCourse:
    """_OmegaUp_Controllers_Course__apiGenerateTokenForCloneCourse"""
    token: str

    def __init__(
        self,
        *,
        token: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.token = token


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiGetProblemUsers:
    """_OmegaUp_Controllers_Course__apiGetProblemUsers"""
    identities: Sequence[str]

    def __init__(
        self,
        *,
        identities: Sequence[str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.identities = [v for v in identities]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiListAssignments:
    """_OmegaUp_Controllers_Course__apiListAssignments"""
    assignments: Sequence['_CourseAssignment']

    def __init__(
        self,
        *,
        assignments: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.assignments = [_CourseAssignment(**v) for v in assignments]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiListSolvedProblems:
    """_OmegaUp_Controllers_Course__apiListSolvedProblems"""
    user_problems: Dict[str, Sequence[
        '_OmegaUp_Controllers_Course__apiListSolvedProblems_user_problems_value_entry']]

    def __init__(
        self,
        *,
        user_problems: Dict[str, Sequence[Dict[str, Any]]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.user_problems = {
            k: [
                _OmegaUp_Controllers_Course__apiListSolvedProblems_user_problems_value_entry(
                    **v) for v in v
            ]
            for k, v in user_problems.items()
        }


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiListSolvedProblems_user_problems_value_entry:
    """_OmegaUp_Controllers_Course__apiListSolvedProblems_user_problems_value_entry"""
    alias: str
    title: str
    username: str

    def __init__(
        self,
        *,
        alias: str,
        title: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.title = title
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiListStudents:
    """_OmegaUp_Controllers_Course__apiListStudents"""
    students: Sequence['_CourseStudent']

    def __init__(
        self,
        *,
        students: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.students = [_CourseStudent(**v) for v in students]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiListUnsolvedProblems:
    """_OmegaUp_Controllers_Course__apiListUnsolvedProblems"""
    user_problems: Dict[str, Sequence[
        '_OmegaUp_Controllers_Course__apiListUnsolvedProblems_user_problems_value_entry']]

    def __init__(
        self,
        *,
        user_problems: Dict[str, Sequence[Dict[str, Any]]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.user_problems = {
            k: [
                _OmegaUp_Controllers_Course__apiListUnsolvedProblems_user_problems_value_entry(
                    **v) for v in v
            ]
            for k, v in user_problems.items()
        }


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiListUnsolvedProblems_user_problems_value_entry:
    """_OmegaUp_Controllers_Course__apiListUnsolvedProblems_user_problems_value_entry"""
    alias: str
    title: str
    username: str

    def __init__(
        self,
        *,
        alias: str,
        title: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.title = title
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiMyProgress:
    """_OmegaUp_Controllers_Course__apiMyProgress"""
    assignments: Dict[str, '_Progress']

    def __init__(
        self,
        *,
        assignments: Dict[str, Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.assignments = {k: _Progress(**v) for k, v in assignments.items()}


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiProblemClarifications:
    """_OmegaUp_Controllers_Course__apiProblemClarifications"""
    clarifications: Sequence['_Clarification']

    def __init__(
        self,
        *,
        clarifications: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.clarifications = [_Clarification(**v) for v in clarifications]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiRequests:
    """_OmegaUp_Controllers_Course__apiRequests"""
    users: Sequence['_IdentityRequest']

    def __init__(
        self,
        *,
        users: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.users = [_IdentityRequest(**v) for v in users]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiRuns:
    """_OmegaUp_Controllers_Course__apiRuns"""
    runs: Sequence['_Run']
    totalRuns: int

    def __init__(
        self,
        *,
        runs: Sequence[Dict[str, Any]],
        totalRuns: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.runs = [_Run(**v) for v in runs]
        self.totalRuns = totalRuns


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiSearchUsers:
    """_OmegaUp_Controllers_Course__apiSearchUsers"""
    results: Sequence['_ListItem']

    def __init__(
        self,
        *,
        results: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.results = [_ListItem(**v) for v in results]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiStudentProgress:
    """_OmegaUp_Controllers_Course__apiStudentProgress"""
    problems: Sequence['_CourseProblem']

    def __init__(
        self,
        *,
        problems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.problems = [_CourseProblem(**v) for v in problems]


@dataclasses.dataclass
class _OmegaUp_Controllers_Course__apiStudentsProgress:
    """_OmegaUp_Controllers_Course__apiStudentsProgress"""
    nextPage: Optional[int]
    progress: Sequence['_StudentProgressInCourse']

    def __init__(
        self,
        *,
        progress: Sequence[Dict[str, Any]],
        nextPage: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if nextPage is not None:
            self.nextPage = nextPage
        else:
            self.nextPage = None
        self.progress = [_StudentProgressInCourse(**v) for v in progress]


@dataclasses.dataclass
class _OmegaUp_Controllers_Grader__apiStatus:
    """_OmegaUp_Controllers_Grader__apiStatus"""
    grader: '_GraderStatus'

    def __init__(
        self,
        *,
        grader: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.grader = _GraderStatus(**grader)


@dataclasses.dataclass
class _OmegaUp_Controllers_GroupScoreboard__apiList:
    """_OmegaUp_Controllers_GroupScoreboard__apiList"""
    scoreboards: Sequence[
        '_OmegaUp_Controllers_GroupScoreboard__apiList_scoreboards_entry']

    def __init__(
        self,
        *,
        scoreboards: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.scoreboards = [
            _OmegaUp_Controllers_GroupScoreboard__apiList_scoreboards_entry(
                **v) for v in scoreboards
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_GroupScoreboard__apiList_scoreboards_entry:
    """_OmegaUp_Controllers_GroupScoreboard__apiList_scoreboards_entry"""
    alias: str
    create_time: int
    description: str
    group_id: int
    group_scoreboard_id: int
    name: str

    def __init__(
        self,
        *,
        alias: str,
        create_time: int,
        description: str,
        group_id: int,
        group_scoreboard_id: int,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.create_time = create_time
        self.description = description
        self.group_id = group_id
        self.group_scoreboard_id = group_scoreboard_id
        self.name = name


@dataclasses.dataclass
class _OmegaUp_Controllers_Group__apiDetails:
    """_OmegaUp_Controllers_Group__apiDetails"""
    group: '_OmegaUp_Controllers_Group__apiDetails_group'
    scoreboards: Sequence['_GroupScoreboard']

    def __init__(
        self,
        *,
        group: Dict[str, Any],
        scoreboards: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.group = _OmegaUp_Controllers_Group__apiDetails_group(**group)
        self.scoreboards = [_GroupScoreboard(**v) for v in scoreboards]


@dataclasses.dataclass
class _OmegaUp_Controllers_Group__apiDetails_group:
    """_OmegaUp_Controllers_Group__apiDetails_group"""
    alias: str
    create_time: int
    description: str
    name: str

    def __init__(
        self,
        *,
        alias: str,
        create_time: int,
        description: str,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.create_time = create_time
        self.description = description
        self.name = name


@dataclasses.dataclass
class _OmegaUp_Controllers_Group__apiMembers:
    """_OmegaUp_Controllers_Group__apiMembers"""
    identities: Sequence['_Identity']

    def __init__(
        self,
        *,
        identities: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.identities = [_Identity(**v) for v in identities]


@dataclasses.dataclass
class _OmegaUp_Controllers_Group__apiMyList:
    """_OmegaUp_Controllers_Group__apiMyList"""
    groups: Sequence['_OmegaUp_Controllers_Group__apiMyList_groups_entry']

    def __init__(
        self,
        *,
        groups: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.groups = [
            _OmegaUp_Controllers_Group__apiMyList_groups_entry(**v)
            for v in groups
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_Group__apiMyList_groups_entry:
    """_OmegaUp_Controllers_Group__apiMyList_groups_entry"""
    alias: str
    create_time: datetime.datetime
    description: str
    name: str

    def __init__(
        self,
        *,
        alias: str,
        create_time: int,
        description: str,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.create_time = datetime.datetime.fromtimestamp(create_time)
        self.description = description
        self.name = name


@dataclasses.dataclass
class _OmegaUp_Controllers_Identity__apiCreate:
    """_OmegaUp_Controllers_Identity__apiCreate"""
    username: str

    def __init__(
        self,
        *,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_Notification__apiMyList:
    """_OmegaUp_Controllers_Notification__apiMyList"""
    notifications: Sequence['_Notification']

    def __init__(
        self,
        *,
        notifications: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.notifications = [_Notification(**v) for v in notifications]


@dataclasses.dataclass
class _OmegaUp_Controllers_ProblemForfeited__apiGetCounts:
    """_OmegaUp_Controllers_ProblemForfeited__apiGetCounts"""
    allowed: int
    seen: int

    def __init__(
        self,
        *,
        allowed: int,
        seen: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.allowed = allowed
        self.seen = seen


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiAddTag:
    """_OmegaUp_Controllers_Problem__apiAddTag"""
    name: str

    def __init__(
        self,
        *,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiAdminList:
    """_OmegaUp_Controllers_Problem__apiAdminList"""
    pagerItems: Sequence['_PageItem']
    problems: Sequence['_ProblemListItem']

    def __init__(
        self,
        *,
        pagerItems: Sequence[Dict[str, Any]],
        problems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.pagerItems = [_PageItem(**v) for v in pagerItems]
        self.problems = [_ProblemListItem(**v) for v in problems]


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiAdmins:
    """_OmegaUp_Controllers_Problem__apiAdmins"""
    admins: Sequence['_ProblemAdmin']
    group_admins: Sequence['_ProblemGroupAdmin']

    def __init__(
        self,
        *,
        admins: Sequence[Dict[str, Any]],
        group_admins: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admins = [_ProblemAdmin(**v) for v in admins]
        self.group_admins = [_ProblemGroupAdmin(**v) for v in group_admins]


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiBestScore:
    """_OmegaUp_Controllers_Problem__apiBestScore"""
    score: float

    def __init__(
        self,
        *,
        score: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.score = score


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiClarifications:
    """_OmegaUp_Controllers_Problem__apiClarifications"""
    clarifications: Sequence['_Clarification']

    def __init__(
        self,
        *,
        clarifications: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.clarifications = [_Clarification(**v) for v in clarifications]


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiList:
    """_OmegaUp_Controllers_Problem__apiList"""
    results: Sequence['_ProblemListItem']
    total: int

    def __init__(
        self,
        *,
        results: Sequence[Dict[str, Any]],
        total: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.results = [_ProblemListItem(**v) for v in results]
        self.total = total


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiMyList:
    """_OmegaUp_Controllers_Problem__apiMyList"""
    pagerItems: Sequence['_PageItem']
    problems: Sequence['_ProblemListItem']

    def __init__(
        self,
        *,
        pagerItems: Sequence[Dict[str, Any]],
        problems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.pagerItems = [_PageItem(**v) for v in pagerItems]
        self.problems = [_ProblemListItem(**v) for v in problems]


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiRandomKarelProblem:
    """_OmegaUp_Controllers_Problem__apiRandomKarelProblem"""
    alias: str

    def __init__(
        self,
        *,
        alias: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiRandomLanguageProblem:
    """_OmegaUp_Controllers_Problem__apiRandomLanguageProblem"""
    alias: str

    def __init__(
        self,
        *,
        alias: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiRuns:
    """_OmegaUp_Controllers_Problem__apiRuns"""
    runs: Sequence['_Run']
    totalRuns: int

    def __init__(
        self,
        *,
        runs: Sequence[Dict[str, Any]],
        totalRuns: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.runs = [_Run(**v) for v in runs]
        self.totalRuns = totalRuns


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiRunsDiff:
    """_OmegaUp_Controllers_Problem__apiRunsDiff"""
    diff: Sequence['_RunsDiff']

    def __init__(
        self,
        *,
        diff: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.diff = [_RunsDiff(**v) for v in diff]


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiSolution:
    """_OmegaUp_Controllers_Problem__apiSolution"""
    solution: Optional['_ProblemStatement']

    def __init__(
        self,
        *,
        solution: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if solution is not None:
            self.solution = _ProblemStatement(**solution)
        else:
            self.solution = None


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiStats:
    """_OmegaUp_Controllers_Problem__apiStats"""
    cases_stats: Dict[str, int]
    pending_runs: Sequence[str]
    total_runs: int
    verdict_counts: Dict[str, int]

    def __init__(
        self,
        *,
        cases_stats: Dict[str, int],
        pending_runs: Sequence[str],
        total_runs: int,
        verdict_counts: Dict[str, int],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.cases_stats = {k: v for k, v in cases_stats.items()}
        self.pending_runs = [v for v in pending_runs]
        self.total_runs = total_runs
        self.verdict_counts = {k: v for k, v in verdict_counts.items()}


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiTags:
    """_OmegaUp_Controllers_Problem__apiTags"""
    tags: Sequence['_OmegaUp_Controllers_Problem__apiTags_tags_entry']

    def __init__(
        self,
        *,
        tags: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.tags = [
            _OmegaUp_Controllers_Problem__apiTags_tags_entry(**v) for v in tags
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiTags_tags_entry:
    """_OmegaUp_Controllers_Problem__apiTags_tags_entry"""
    name: str
    public: bool

    def __init__(
        self,
        *,
        name: str,
        public: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.public = public


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiUpdate:
    """_OmegaUp_Controllers_Problem__apiUpdate"""
    rejudged: bool

    def __init__(
        self,
        *,
        rejudged: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.rejudged = rejudged


@dataclasses.dataclass
class _OmegaUp_Controllers_Problem__apiVersions:
    """_OmegaUp_Controllers_Problem__apiVersions"""
    log: Sequence['_ProblemVersion']
    published: str

    def __init__(
        self,
        *,
        log: Sequence[Dict[str, Any]],
        published: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.log = [_ProblemVersion(**v) for v in log]
        self.published = published


@dataclasses.dataclass
class _OmegaUp_Controllers_Problemset__apiScoreboardEvents:
    """_OmegaUp_Controllers_Problemset__apiScoreboardEvents"""
    events: Sequence['_ScoreboardEvent']

    def __init__(
        self,
        *,
        events: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.events = [_ScoreboardEvent(**v) for v in events]


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiCreate:
    """_OmegaUp_Controllers_QualityNomination__apiCreate"""
    qualitynomination_id: int

    def __init__(
        self,
        *,
        qualitynomination_id: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.qualitynomination_id = qualitynomination_id


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiDetails:
    """_OmegaUp_Controllers_QualityNomination__apiDetails"""
    author: '_OmegaUp_Controllers_QualityNomination__apiDetails_author'
    contents: Optional[
        '_OmegaUp_Controllers_QualityNomination__apiDetails_contents']
    nomination: str
    nomination_status: str
    nominator: '_OmegaUp_Controllers_QualityNomination__apiDetails_nominator'
    original_contents: Optional[
        '_OmegaUp_Controllers_QualityNomination__apiDetails_original_contents']
    problem: '_OmegaUp_Controllers_QualityNomination__apiDetails_problem'
    qualitynomination_id: int
    reviewer: bool
    time: datetime.datetime
    votes: Sequence[
        '_OmegaUp_Controllers_QualityNomination__apiDetails_votes_entry']

    def __init__(
        self,
        *,
        author: Dict[str, Any],
        nomination: str,
        nomination_status: str,
        nominator: Dict[str, Any],
        problem: Dict[str, Any],
        qualitynomination_id: int,
        reviewer: bool,
        time: int,
        votes: Sequence[Dict[str, Any]],
        contents: Optional[Dict[str, Any]] = None,
        original_contents: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.author = _OmegaUp_Controllers_QualityNomination__apiDetails_author(
            **author)
        if contents is not None:
            self.contents = _OmegaUp_Controllers_QualityNomination__apiDetails_contents(
                **contents)
        else:
            self.contents = None
        self.nomination = nomination
        self.nomination_status = nomination_status
        self.nominator = _OmegaUp_Controllers_QualityNomination__apiDetails_nominator(
            **nominator)
        if original_contents is not None:
            self.original_contents = _OmegaUp_Controllers_QualityNomination__apiDetails_original_contents(
                **original_contents)
        else:
            self.original_contents = None
        self.problem = _OmegaUp_Controllers_QualityNomination__apiDetails_problem(
            **problem)
        self.qualitynomination_id = qualitynomination_id
        self.reviewer = reviewer
        self.time = datetime.datetime.fromtimestamp(time)
        self.votes = [
            _OmegaUp_Controllers_QualityNomination__apiDetails_votes_entry(**v)
            for v in votes
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiDetails_author:
    """_OmegaUp_Controllers_QualityNomination__apiDetails_author"""
    name: str
    username: str

    def __init__(
        self,
        *,
        name: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiDetails_contents:
    """_OmegaUp_Controllers_QualityNomination__apiDetails_contents"""
    before_ac: Optional[bool]
    difficulty: Optional[int]
    quality: Optional[int]
    rationale: Optional[str]
    reason: Optional[str]
    statements: Optional[Dict[str, str]]
    tags: Optional[Sequence[str]]

    def __init__(
        self,
        *,
        before_ac: Optional[bool] = None,
        difficulty: Optional[int] = None,
        quality: Optional[int] = None,
        rationale: Optional[str] = None,
        reason: Optional[str] = None,
        statements: Optional[Dict[str, str]] = None,
        tags: Optional[Sequence[str]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if before_ac is not None:
            self.before_ac = before_ac
        else:
            self.before_ac = None
        if difficulty is not None:
            self.difficulty = difficulty
        else:
            self.difficulty = None
        if quality is not None:
            self.quality = quality
        else:
            self.quality = None
        if rationale is not None:
            self.rationale = rationale
        else:
            self.rationale = None
        if reason is not None:
            self.reason = reason
        else:
            self.reason = None
        if statements is not None:
            self.statements = {k: v for k, v in statements.items()}
        else:
            self.statements = None
        if tags is not None:
            self.tags = [v for v in tags]
        else:
            self.tags = None


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiDetails_nominator:
    """_OmegaUp_Controllers_QualityNomination__apiDetails_nominator"""
    name: str
    username: str

    def __init__(
        self,
        *,
        name: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiDetails_original_contents:
    """_OmegaUp_Controllers_QualityNomination__apiDetails_original_contents"""
    source: str
    statements: Dict[str, '_ProblemStatement']
    tags: Optional[Sequence[
        '_OmegaUp_Controllers_QualityNomination__apiDetails_original_contents_tags_entry']]

    def __init__(
        self,
        *,
        source: str,
        statements: Dict[str, Dict[str, Any]],
        tags: Optional[Sequence[Dict[str, Any]]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.source = source
        self.statements = {
            k: _ProblemStatement(**v)
            for k, v in statements.items()
        }
        if tags is not None:
            self.tags = [
                _OmegaUp_Controllers_QualityNomination__apiDetails_original_contents_tags_entry(
                    **v) for v in tags
            ]
        else:
            self.tags = None


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiDetails_original_contents_tags_entry:
    """_OmegaUp_Controllers_QualityNomination__apiDetails_original_contents_tags_entry"""
    name: str
    source: str

    def __init__(
        self,
        *,
        name: str,
        source: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.source = source


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiDetails_problem:
    """_OmegaUp_Controllers_QualityNomination__apiDetails_problem"""
    alias: str
    title: str

    def __init__(
        self,
        *,
        alias: str,
        title: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.title = title


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiDetails_votes_entry:
    """_OmegaUp_Controllers_QualityNomination__apiDetails_votes_entry"""
    time: datetime.datetime
    user: '_OmegaUp_Controllers_QualityNomination__apiDetails_votes_entry_user'
    vote: int

    def __init__(
        self,
        *,
        time: int,
        user: Dict[str, Any],
        vote: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.time = datetime.datetime.fromtimestamp(time)
        self.user = _OmegaUp_Controllers_QualityNomination__apiDetails_votes_entry_user(
            **user)
        self.vote = vote


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiDetails_votes_entry_user:
    """_OmegaUp_Controllers_QualityNomination__apiDetails_votes_entry_user"""
    name: str
    username: str

    def __init__(
        self,
        *,
        name: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiList:
    """_OmegaUp_Controllers_QualityNomination__apiList"""
    nominations: Sequence['_NominationListItem']
    pager_items: Sequence['_PageItem']

    def __init__(
        self,
        *,
        nominations: Sequence[Dict[str, Any]],
        pager_items: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.nominations = [_NominationListItem(**v) for v in nominations]
        self.pager_items = [_PageItem(**v) for v in pager_items]


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiMyAssignedList:
    """_OmegaUp_Controllers_QualityNomination__apiMyAssignedList"""
    nominations: Sequence[
        '_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry']

    def __init__(
        self,
        *,
        nominations: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.nominations = [
            _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry(
                **v) for v in nominations
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry:
    """_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry"""
    author: '_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_author'
    contents: Optional[
        '_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_contents']
    nomination: str
    nominator: '_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_nominator'
    problem: '_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_problem'
    qualitynomination_id: int
    status: str
    time: datetime.datetime
    votes: Sequence[
        '_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_votes_entry']

    def __init__(
        self,
        *,
        author: Dict[str, Any],
        nomination: str,
        nominator: Dict[str, Any],
        problem: Dict[str, Any],
        qualitynomination_id: int,
        status: str,
        time: int,
        votes: Sequence[Dict[str, Any]],
        contents: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.author = _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_author(
            **author)
        if contents is not None:
            self.contents = _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_contents(
                **contents)
        else:
            self.contents = None
        self.nomination = nomination
        self.nominator = _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_nominator(
            **nominator)
        self.problem = _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_problem(
            **problem)
        self.qualitynomination_id = qualitynomination_id
        self.status = status
        self.time = datetime.datetime.fromtimestamp(time)
        self.votes = [
            _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_votes_entry(
                **v) for v in votes
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_author:
    """_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_author"""
    name: str
    username: str

    def __init__(
        self,
        *,
        name: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_contents:
    """_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_contents"""
    before_ac: Optional[bool]
    difficulty: Optional[int]
    quality: Optional[int]
    rationale: Optional[str]
    reason: Optional[str]
    statements: Optional[Dict[str, str]]
    tags: Optional[Sequence[str]]

    def __init__(
        self,
        *,
        before_ac: Optional[bool] = None,
        difficulty: Optional[int] = None,
        quality: Optional[int] = None,
        rationale: Optional[str] = None,
        reason: Optional[str] = None,
        statements: Optional[Dict[str, str]] = None,
        tags: Optional[Sequence[str]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if before_ac is not None:
            self.before_ac = before_ac
        else:
            self.before_ac = None
        if difficulty is not None:
            self.difficulty = difficulty
        else:
            self.difficulty = None
        if quality is not None:
            self.quality = quality
        else:
            self.quality = None
        if rationale is not None:
            self.rationale = rationale
        else:
            self.rationale = None
        if reason is not None:
            self.reason = reason
        else:
            self.reason = None
        if statements is not None:
            self.statements = {k: v for k, v in statements.items()}
        else:
            self.statements = None
        if tags is not None:
            self.tags = [v for v in tags]
        else:
            self.tags = None


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_nominator:
    """_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_nominator"""
    name: str
    username: str

    def __init__(
        self,
        *,
        name: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_problem:
    """_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_problem"""
    alias: str
    title: str

    def __init__(
        self,
        *,
        alias: str,
        title: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.title = title


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_votes_entry:
    """_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_votes_entry"""
    time: datetime.datetime
    user: '_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_votes_entry_user'
    vote: int

    def __init__(
        self,
        *,
        time: int,
        user: Dict[str, Any],
        vote: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.time = datetime.datetime.fromtimestamp(time)
        self.user = _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_votes_entry_user(
            **user)
        self.vote = vote


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_votes_entry_user:
    """_OmegaUp_Controllers_QualityNomination__apiMyAssignedList_nominations_entry_votes_entry_user"""
    name: str
    username: str

    def __init__(
        self,
        *,
        name: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_QualityNomination__apiMyList:
    """_OmegaUp_Controllers_QualityNomination__apiMyList"""
    nominations: Sequence['_NominationListItem']
    pager_items: Sequence['_PageItem']

    def __init__(
        self,
        *,
        nominations: Sequence[Dict[str, Any]],
        pager_items: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.nominations = [_NominationListItem(**v) for v in nominations]
        self.pager_items = [_PageItem(**v) for v in pager_items]


@dataclasses.dataclass
class _OmegaUp_Controllers_Reset__apiCreate:
    """_OmegaUp_Controllers_Reset__apiCreate"""
    message: Optional[str]
    token: Optional[str]

    def __init__(
        self,
        *,
        message: Optional[str] = None,
        token: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if message is not None:
            self.message = message
        else:
            self.message = None
        if token is not None:
            self.token = token
        else:
            self.token = None


@dataclasses.dataclass
class _OmegaUp_Controllers_Reset__apiGenerateToken:
    """_OmegaUp_Controllers_Reset__apiGenerateToken"""
    link: str
    token: str

    def __init__(
        self,
        *,
        link: str,
        token: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.link = link
        self.token = token


@dataclasses.dataclass
class _OmegaUp_Controllers_Reset__apiUpdate:
    """_OmegaUp_Controllers_Reset__apiUpdate"""
    message: str

    def __init__(
        self,
        *,
        message: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.message = message


@dataclasses.dataclass
class _OmegaUp_Controllers_Run__apiCounts:
    """_OmegaUp_Controllers_Run__apiCounts"""
    ac: Dict[str, int]
    total: Dict[str, int]

    def __init__(
        self,
        *,
        ac: Dict[str, int],
        total: Dict[str, int],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.ac = {k: v for k, v in ac.items()}
        self.total = {k: v for k, v in total.items()}


@dataclasses.dataclass
class _OmegaUp_Controllers_Run__apiCreate:
    """_OmegaUp_Controllers_Run__apiCreate"""
    guid: str
    nextSubmissionTimestamp: datetime.datetime
    submission_deadline: datetime.datetime
    submit_delay: int

    def __init__(
        self,
        *,
        guid: str,
        nextSubmissionTimestamp: int,
        submission_deadline: int,
        submit_delay: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.guid = guid
        self.nextSubmissionTimestamp = datetime.datetime.fromtimestamp(
            nextSubmissionTimestamp)
        self.submission_deadline = datetime.datetime.fromtimestamp(
            submission_deadline)
        self.submit_delay = submit_delay


@dataclasses.dataclass
class _OmegaUp_Controllers_Run__apiList:
    """_OmegaUp_Controllers_Run__apiList"""
    runs: Sequence['_Run']
    totalRuns: int

    def __init__(
        self,
        *,
        runs: Sequence[Dict[str, Any]],
        totalRuns: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.runs = [_Run(**v) for v in runs]
        self.totalRuns = totalRuns


@dataclasses.dataclass
class _OmegaUp_Controllers_Run__apiSource:
    """_OmegaUp_Controllers_Run__apiSource"""
    compile_error: Optional[str]
    details: Optional['_OmegaUp_Controllers_Run__apiSource_details']
    source: str

    def __init__(
        self,
        *,
        source: str,
        compile_error: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if compile_error is not None:
            self.compile_error = compile_error
        else:
            self.compile_error = None
        if details is not None:
            self.details = _OmegaUp_Controllers_Run__apiSource_details(
                **details)
        else:
            self.details = None
        self.source = source


@dataclasses.dataclass
class _OmegaUp_Controllers_Run__apiSource_details:
    """_OmegaUp_Controllers_Run__apiSource_details"""
    compile_meta: Optional[Dict[str, '_RunMetadata']]
    contest_score: float
    groups: Optional[
        Sequence['_OmegaUp_Controllers_Run__apiSource_details_groups_entry']]
    judged_by: str
    max_score: Optional[float]
    memory: Optional[float]
    score: float
    time: Optional[float]
    verdict: str
    wall_time: Optional[float]

    def __init__(
        self,
        *,
        contest_score: float,
        judged_by: str,
        score: float,
        verdict: str,
        compile_meta: Optional[Dict[str, Dict[str, Any]]] = None,
        groups: Optional[Sequence[Dict[str, Any]]] = None,
        max_score: Optional[float] = None,
        memory: Optional[float] = None,
        time: Optional[float] = None,
        wall_time: Optional[float] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if compile_meta is not None:
            self.compile_meta = {
                k: _RunMetadata(**v)
                for k, v in compile_meta.items()
            }
        else:
            self.compile_meta = None
        self.contest_score = contest_score
        if groups is not None:
            self.groups = [
                _OmegaUp_Controllers_Run__apiSource_details_groups_entry(**v)
                for v in groups
            ]
        else:
            self.groups = None
        self.judged_by = judged_by
        if max_score is not None:
            self.max_score = max_score
        else:
            self.max_score = None
        if memory is not None:
            self.memory = memory
        else:
            self.memory = None
        self.score = score
        if time is not None:
            self.time = time
        else:
            self.time = None
        self.verdict = verdict
        if wall_time is not None:
            self.wall_time = wall_time
        else:
            self.wall_time = None


@dataclasses.dataclass
class _OmegaUp_Controllers_Run__apiSource_details_groups_entry:
    """_OmegaUp_Controllers_Run__apiSource_details_groups_entry"""
    cases: Sequence['_CaseResult']
    contest_score: float
    group: str
    max_score: float
    score: float

    def __init__(
        self,
        *,
        cases: Sequence[Dict[str, Any]],
        contest_score: float,
        group: str,
        max_score: float,
        score: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.cases = [_CaseResult(**v) for v in cases]
        self.contest_score = contest_score
        self.group = group
        self.max_score = max_score
        self.score = score


@dataclasses.dataclass
class _OmegaUp_Controllers_School__apiCreate:
    """_OmegaUp_Controllers_School__apiCreate"""
    school_id: int

    def __init__(
        self,
        *,
        school_id: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.school_id = school_id


@dataclasses.dataclass
class _OmegaUp_Controllers_School__apiList_entry:
    """_OmegaUp_Controllers_School__apiList_entry"""
    id: int
    label: str
    value: str

    def __init__(
        self,
        *,
        id: int,
        label: str,
        value: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.id = id
        self.label = label
        self.value = value


@dataclasses.dataclass
class _OmegaUp_Controllers_Session__apiCurrentSession:
    """_OmegaUp_Controllers_Session__apiCurrentSession"""
    session: Optional['_CurrentSession']
    time: int

    def __init__(
        self,
        *,
        time: int,
        session: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if session is not None:
            self.session = _CurrentSession(**session)
        else:
            self.session = None
        self.time = time


@dataclasses.dataclass
class _OmegaUp_Controllers_Session__apiGoogleLogin:
    """_OmegaUp_Controllers_Session__apiGoogleLogin"""
    isAccountCreation: bool

    def __init__(
        self,
        *,
        isAccountCreation: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.isAccountCreation = isAccountCreation


@dataclasses.dataclass
class _OmegaUp_Controllers_Tag__apiFrequentTags:
    """_OmegaUp_Controllers_Tag__apiFrequentTags"""
    frequent_tags: Sequence['_TagWithProblemCount']

    def __init__(
        self,
        *,
        frequent_tags: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.frequent_tags = [_TagWithProblemCount(**v) for v in frequent_tags]


@dataclasses.dataclass
class _OmegaUp_Controllers_Tag__apiList_entry:
    """_OmegaUp_Controllers_Tag__apiList_entry"""
    name: str

    def __init__(
        self,
        *,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name


@dataclasses.dataclass
class _OmegaUp_Controllers_TeamsGroup__apiDetails:
    """_OmegaUp_Controllers_TeamsGroup__apiDetails"""
    team_group: '_OmegaUp_Controllers_TeamsGroup__apiDetails_team_group'

    def __init__(
        self,
        *,
        team_group: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.team_group = _OmegaUp_Controllers_TeamsGroup__apiDetails_team_group(
            **team_group)


@dataclasses.dataclass
class _OmegaUp_Controllers_TeamsGroup__apiDetails_team_group:
    """_OmegaUp_Controllers_TeamsGroup__apiDetails_team_group"""
    alias: str
    create_time: int
    description: str
    name: str

    def __init__(
        self,
        *,
        alias: str,
        create_time: int,
        description: str,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.create_time = create_time
        self.description = description
        self.name = name


@dataclasses.dataclass
class _OmegaUp_Controllers_TeamsGroup__apiTeams:
    """_OmegaUp_Controllers_TeamsGroup__apiTeams"""
    identities: Sequence['_Identity']

    def __init__(
        self,
        *,
        identities: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.identities = [_Identity(**v) for v in identities]


@dataclasses.dataclass
class _OmegaUp_Controllers_TeamsGroup__apiTeamsMembers:
    """_OmegaUp_Controllers_TeamsGroup__apiTeamsMembers"""
    pageNumber: int
    teamsUsers: Sequence['_TeamMember']
    totalRows: int

    def __init__(
        self,
        *,
        pageNumber: int,
        teamsUsers: Sequence[Dict[str, Any]],
        totalRows: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.pageNumber = pageNumber
        self.teamsUsers = [_TeamMember(**v) for v in teamsUsers]
        self.totalRows = totalRows


@dataclasses.dataclass
class _OmegaUp_Controllers_Time__apiGet:
    """_OmegaUp_Controllers_Time__apiGet"""
    time: int

    def __init__(
        self,
        *,
        time: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.time = time


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiCoderOfTheMonth:
    """_OmegaUp_Controllers_User__apiCoderOfTheMonth"""
    coderinfo: Optional['_UserProfile']

    def __init__(
        self,
        *,
        coderinfo: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if coderinfo is not None:
            self.coderinfo = _UserProfile(**coderinfo)
        else:
            self.coderinfo = None


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiCoderOfTheMonthList:
    """_OmegaUp_Controllers_User__apiCoderOfTheMonthList"""
    coders: Sequence['_CoderOfTheMonthList_entry']

    def __init__(
        self,
        *,
        coders: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.coders = [_CoderOfTheMonthList_entry(**v) for v in coders]


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiContestStats:
    """_OmegaUp_Controllers_User__apiContestStats"""
    contests: Dict[str, '_UserProfileContests_value']

    def __init__(
        self,
        *,
        contests: Dict[str, Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = {
            k: _UserProfileContests_value(**v)
            for k, v in contests.items()
        }


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiCreate:
    """_OmegaUp_Controllers_User__apiCreate"""
    username: str

    def __init__(
        self,
        *,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.username = username


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiCreateAPIToken:
    """_OmegaUp_Controllers_User__apiCreateAPIToken"""
    token: str

    def __init__(
        self,
        *,
        token: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.token = token


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiExtraInformation:
    """_OmegaUp_Controllers_User__apiExtraInformation"""
    birth_date: Optional[datetime.datetime]
    last_login: Optional[datetime.datetime]
    username: str
    verified: bool
    within_last_day: bool

    def __init__(
        self,
        *,
        username: str,
        verified: bool,
        within_last_day: bool,
        birth_date: Optional[int] = None,
        last_login: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if birth_date is not None:
            self.birth_date = datetime.datetime.fromtimestamp(birth_date)
        else:
            self.birth_date = None
        if last_login is not None:
            self.last_login = datetime.datetime.fromtimestamp(last_login)
        else:
            self.last_login = None
        self.username = username
        self.verified = verified
        self.within_last_day = within_last_day


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiGenerateGitToken:
    """_OmegaUp_Controllers_User__apiGenerateGitToken"""
    token: str

    def __init__(
        self,
        *,
        token: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.token = token


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiLastPrivacyPolicyAccepted:
    """_OmegaUp_Controllers_User__apiLastPrivacyPolicyAccepted"""
    hasAccepted: bool

    def __init__(
        self,
        *,
        hasAccepted: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.hasAccepted = hasAccepted


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiList:
    """_OmegaUp_Controllers_User__apiList"""
    results: Sequence['_ListItem']

    def __init__(
        self,
        *,
        results: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.results = [_ListItem(**v) for v in results]


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiListAPITokens:
    """_OmegaUp_Controllers_User__apiListAPITokens"""
    tokens: Sequence[
        '_OmegaUp_Controllers_User__apiListAPITokens_tokens_entry']

    def __init__(
        self,
        *,
        tokens: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.tokens = [
            _OmegaUp_Controllers_User__apiListAPITokens_tokens_entry(**v)
            for v in tokens
        ]


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiListAPITokens_tokens_entry:
    """_OmegaUp_Controllers_User__apiListAPITokens_tokens_entry"""
    last_used: datetime.datetime
    name: str
    rate_limit: '_OmegaUp_Controllers_User__apiListAPITokens_tokens_entry_rate_limit'
    timestamp: datetime.datetime

    def __init__(
        self,
        *,
        last_used: int,
        name: str,
        rate_limit: Dict[str, Any],
        timestamp: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.last_used = datetime.datetime.fromtimestamp(last_used)
        self.name = name
        self.rate_limit = _OmegaUp_Controllers_User__apiListAPITokens_tokens_entry_rate_limit(
            **rate_limit)
        self.timestamp = datetime.datetime.fromtimestamp(timestamp)


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiListAPITokens_tokens_entry_rate_limit:
    """_OmegaUp_Controllers_User__apiListAPITokens_tokens_entry_rate_limit"""
    limit: int
    remaining: int
    reset: datetime.datetime

    def __init__(
        self,
        *,
        limit: int,
        remaining: int,
        reset: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.limit = limit
        self.remaining = remaining
        self.reset = datetime.datetime.fromtimestamp(reset)


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiListAssociatedIdentities:
    """_OmegaUp_Controllers_User__apiListAssociatedIdentities"""
    identities: Sequence['_AssociatedIdentity']

    def __init__(
        self,
        *,
        identities: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.identities = [_AssociatedIdentity(**v) for v in identities]


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiListUnsolvedProblems:
    """_OmegaUp_Controllers_User__apiListUnsolvedProblems"""
    problems: Sequence['_Problem']

    def __init__(
        self,
        *,
        problems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.problems = [_Problem(**v) for v in problems]


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiLogin:
    """_OmegaUp_Controllers_User__apiLogin"""
    auth_token: str

    def __init__(
        self,
        *,
        auth_token: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.auth_token = auth_token


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiMailingListBackfill:
    """_OmegaUp_Controllers_User__apiMailingListBackfill"""
    users: Dict[str, bool]

    def __init__(
        self,
        *,
        users: Dict[str, bool],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.users = {k: v for k, v in users.items()}


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiProblemsCreated:
    """_OmegaUp_Controllers_User__apiProblemsCreated"""
    problems: Sequence['_Problem']

    def __init__(
        self,
        *,
        problems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.problems = [_Problem(**v) for v in problems]


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiProblemsSolved:
    """_OmegaUp_Controllers_User__apiProblemsSolved"""
    problems: Sequence['_Problem']

    def __init__(
        self,
        *,
        problems: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.problems = [_Problem(**v) for v in problems]


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiStats:
    """_OmegaUp_Controllers_User__apiStats"""
    runs: Sequence['_UserProfileStats']

    def __init__(
        self,
        *,
        runs: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.runs = [_UserProfileStats(**v) for v in runs]


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiStatusVerified:
    """_OmegaUp_Controllers_User__apiStatusVerified"""
    username: str
    verified: bool

    def __init__(
        self,
        *,
        username: str,
        verified: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.username = username
        self.verified = verified


@dataclasses.dataclass
class _OmegaUp_Controllers_User__apiValidateFilter:
    """_OmegaUp_Controllers_User__apiValidateFilter"""
    admin: bool
    contest_admin: Sequence[str]
    problem_admin: Sequence[str]
    problemset_admin: Sequence[int]
    user: Optional[str]

    def __init__(
        self,
        *,
        admin: bool,
        contest_admin: Sequence[str],
        problem_admin: Sequence[str],
        problemset_admin: Sequence[int],
        user: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = admin
        self.contest_admin = [v for v in contest_admin]
        self.problem_admin = [v for v in problem_admin]
        self.problemset_admin = [v for v in problemset_admin]
        if user is not None:
            self.user = user
        else:
            self.user = None


@dataclasses.dataclass
class _PageItem:
    """_PageItem"""
    class_: str
    label: str
    page: int
    url: Optional[str]

    def __init__(
        self,
        *,
        label: str,
        page: int,
        url: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.class_ = _kwargs['class']
        self.label = label
        self.page = page
        if url is not None:
            self.url = url
        else:
            self.url = None


@dataclasses.dataclass
class _Participant:
    """_Participant"""
    country_id: Optional[str]
    gender: Optional[str]
    name: Optional[str]
    participant_password: Optional[str]
    participant_username: str
    password: Optional[str]
    school_name: Optional[str]
    state_id: Optional[str]
    username: str

    def __init__(
        self,
        *,
        participant_username: str,
        username: str,
        country_id: Optional[str] = None,
        gender: Optional[str] = None,
        name: Optional[str] = None,
        participant_password: Optional[str] = None,
        password: Optional[str] = None,
        school_name: Optional[str] = None,
        state_id: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        if gender is not None:
            self.gender = gender
        else:
            self.gender = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        if participant_password is not None:
            self.participant_password = participant_password
        else:
            self.participant_password = None
        self.participant_username = participant_username
        if password is not None:
            self.password = password
        else:
            self.password = None
        if school_name is not None:
            self.school_name = school_name
        else:
            self.school_name = None
        if state_id is not None:
            self.state_id = state_id
        else:
            self.state_id = None
        self.username = username


@dataclasses.dataclass
class _PrivacyPolicyDetailsPayload:
    """_PrivacyPolicyDetailsPayload"""
    git_object_id: str
    has_accepted: bool
    policy_markdown: str
    statement_type: str

    def __init__(
        self,
        *,
        git_object_id: str,
        has_accepted: bool,
        policy_markdown: str,
        statement_type: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.git_object_id = git_object_id
        self.has_accepted = has_accepted
        self.policy_markdown = policy_markdown
        self.statement_type = statement_type


@dataclasses.dataclass
class _PrivacyStatement:
    """_PrivacyStatement"""
    gitObjectId: Optional[str]
    markdown: str
    statementType: str

    def __init__(
        self,
        *,
        markdown: str,
        statementType: str,
        gitObjectId: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if gitObjectId is not None:
            self.gitObjectId = gitObjectId
        else:
            self.gitObjectId = None
        self.markdown = markdown
        self.statementType = statementType


@dataclasses.dataclass
class _Problem:
    """_Problem"""
    accepted: int
    alias: str
    difficulty: float
    quality_seal: bool
    submissions: int
    title: str

    def __init__(
        self,
        *,
        accepted: int,
        alias: str,
        difficulty: float,
        quality_seal: bool,
        submissions: int,
        title: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.accepted = accepted
        self.alias = alias
        self.difficulty = difficulty
        self.quality_seal = quality_seal
        self.submissions = submissions
        self.title = title


@dataclasses.dataclass
class _ProblemAdmin:
    """_ProblemAdmin"""
    role: str
    username: str

    def __init__(
        self,
        *,
        role: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.role = role
        self.username = username


@dataclasses.dataclass
class _ProblemCasesContents_value:
    """_ProblemCasesContents_value"""
    contestantOutput: Optional[str]
    in_: str
    out: str

    def __init__(
        self,
        *,
        out: str,
        contestantOutput: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if contestantOutput is not None:
            self.contestantOutput = contestantOutput
        else:
            self.contestantOutput = None
        self.in_ = _kwargs['in']
        self.out = out


@dataclasses.dataclass
class _ProblemDetails:
    """_ProblemDetails"""
    accepted: int
    accepts_submissions: bool
    admin: Optional[bool]
    alias: str
    allow_user_add_tags: bool
    commit: str
    creation_date: datetime.datetime
    difficulty: Optional[float]
    email_clarifications: bool
    input_limit: int
    karel_problem: bool
    languages: Sequence[str]
    letter: Optional[str]
    limits: '_SettingLimits'
    nextSubmissionTimestamp: Optional[datetime.datetime]
    nominationStatus: '_NominationStatus'
    order: str
    points: float
    preferred_language: Optional[str]
    problem_id: int
    problemsetter: Optional['_ProblemsetterInfo']
    quality_seal: bool
    runs: Optional[Sequence['_RunWithDetails']]
    score: float
    settings: '_ProblemSettingsDistrib'
    show_diff: str
    solvers: Optional[Sequence['_BestSolvers']]
    source: Optional[str]
    statement: '_ProblemStatement'
    submissions: int
    title: str
    version: str
    visibility: int
    visits: int

    def __init__(
        self,
        *,
        accepted: int,
        accepts_submissions: bool,
        alias: str,
        allow_user_add_tags: bool,
        commit: str,
        creation_date: int,
        email_clarifications: bool,
        input_limit: int,
        karel_problem: bool,
        languages: Sequence[str],
        limits: Dict[str, Any],
        nominationStatus: Dict[str, Any],
        order: str,
        points: float,
        problem_id: int,
        quality_seal: bool,
        score: float,
        settings: Dict[str, Any],
        show_diff: str,
        statement: Dict[str, Any],
        submissions: int,
        title: str,
        version: str,
        visibility: int,
        visits: int,
        admin: Optional[bool] = None,
        difficulty: Optional[float] = None,
        letter: Optional[str] = None,
        nextSubmissionTimestamp: Optional[int] = None,
        preferred_language: Optional[str] = None,
        problemsetter: Optional[Dict[str, Any]] = None,
        runs: Optional[Sequence[Dict[str, Any]]] = None,
        solvers: Optional[Sequence[Dict[str, Any]]] = None,
        source: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.accepted = accepted
        self.accepts_submissions = accepts_submissions
        if admin is not None:
            self.admin = admin
        else:
            self.admin = None
        self.alias = alias
        self.allow_user_add_tags = allow_user_add_tags
        self.commit = commit
        self.creation_date = datetime.datetime.fromtimestamp(creation_date)
        if difficulty is not None:
            self.difficulty = difficulty
        else:
            self.difficulty = None
        self.email_clarifications = email_clarifications
        self.input_limit = input_limit
        self.karel_problem = karel_problem
        self.languages = [v for v in languages]
        if letter is not None:
            self.letter = letter
        else:
            self.letter = None
        self.limits = _SettingLimits(**limits)
        if nextSubmissionTimestamp is not None:
            self.nextSubmissionTimestamp = datetime.datetime.fromtimestamp(
                nextSubmissionTimestamp)
        else:
            self.nextSubmissionTimestamp = None
        self.nominationStatus = _NominationStatus(**nominationStatus)
        self.order = order
        self.points = points
        if preferred_language is not None:
            self.preferred_language = preferred_language
        else:
            self.preferred_language = None
        self.problem_id = problem_id
        if problemsetter is not None:
            self.problemsetter = _ProblemsetterInfo(**problemsetter)
        else:
            self.problemsetter = None
        self.quality_seal = quality_seal
        if runs is not None:
            self.runs = [_RunWithDetails(**v) for v in runs]
        else:
            self.runs = None
        self.score = score
        self.settings = _ProblemSettingsDistrib(**settings)
        self.show_diff = show_diff
        if solvers is not None:
            self.solvers = [_BestSolvers(**v) for v in solvers]
        else:
            self.solvers = None
        if source is not None:
            self.source = source
        else:
            self.source = None
        self.statement = _ProblemStatement(**statement)
        self.submissions = submissions
        self.title = title
        self.version = version
        self.visibility = visibility
        self.visits = visits


@dataclasses.dataclass
class _ProblemDetailsPayload:
    """_ProblemDetailsPayload"""
    allRuns: Optional[Sequence['_Run']]
    allowUserAddTags: Optional[bool]
    clarifications: Optional[Sequence['_Clarification']]
    histogram: '_Histogram'
    levelTags: Optional[Sequence[str]]
    nominationStatus: Optional['_NominationStatus']
    problem: '_ProblemInfo'
    problemLevel: Optional[str]
    publicTags: Optional[Sequence[str]]
    runs: Optional[Sequence['_Run']]
    selectedPrivateTags: Optional[Sequence[str]]
    selectedPublicTags: Optional[Sequence[str]]
    solutionStatus: Optional[str]
    solvers: Sequence['_BestSolvers']
    totalRuns: Optional[int]
    user: '_UserInfoForProblem'

    def __init__(
        self,
        *,
        histogram: Dict[str, Any],
        problem: Dict[str, Any],
        solvers: Sequence[Dict[str, Any]],
        user: Dict[str, Any],
        allRuns: Optional[Sequence[Dict[str, Any]]] = None,
        allowUserAddTags: Optional[bool] = None,
        clarifications: Optional[Sequence[Dict[str, Any]]] = None,
        levelTags: Optional[Sequence[str]] = None,
        nominationStatus: Optional[Dict[str, Any]] = None,
        problemLevel: Optional[str] = None,
        publicTags: Optional[Sequence[str]] = None,
        runs: Optional[Sequence[Dict[str, Any]]] = None,
        selectedPrivateTags: Optional[Sequence[str]] = None,
        selectedPublicTags: Optional[Sequence[str]] = None,
        solutionStatus: Optional[str] = None,
        totalRuns: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if allRuns is not None:
            self.allRuns = [_Run(**v) for v in allRuns]
        else:
            self.allRuns = None
        if allowUserAddTags is not None:
            self.allowUserAddTags = allowUserAddTags
        else:
            self.allowUserAddTags = None
        if clarifications is not None:
            self.clarifications = [_Clarification(**v) for v in clarifications]
        else:
            self.clarifications = None
        self.histogram = _Histogram(**histogram)
        if levelTags is not None:
            self.levelTags = [v for v in levelTags]
        else:
            self.levelTags = None
        if nominationStatus is not None:
            self.nominationStatus = _NominationStatus(**nominationStatus)
        else:
            self.nominationStatus = None
        self.problem = _ProblemInfo(**problem)
        if problemLevel is not None:
            self.problemLevel = problemLevel
        else:
            self.problemLevel = None
        if publicTags is not None:
            self.publicTags = [v for v in publicTags]
        else:
            self.publicTags = None
        if runs is not None:
            self.runs = [_Run(**v) for v in runs]
        else:
            self.runs = None
        if selectedPrivateTags is not None:
            self.selectedPrivateTags = [v for v in selectedPrivateTags]
        else:
            self.selectedPrivateTags = None
        if selectedPublicTags is not None:
            self.selectedPublicTags = [v for v in selectedPublicTags]
        else:
            self.selectedPublicTags = None
        if solutionStatus is not None:
            self.solutionStatus = solutionStatus
        else:
            self.solutionStatus = None
        self.solvers = [_BestSolvers(**v) for v in solvers]
        if totalRuns is not None:
            self.totalRuns = totalRuns
        else:
            self.totalRuns = None
        self.user = _UserInfoForProblem(**user)


@dataclasses.dataclass
class _ProblemEditPayload:
    """_ProblemEditPayload"""
    admins: Sequence['_ProblemAdmin']
    alias: str
    allowUserAddTags: bool
    emailClarifications: bool
    extraWallTime: float
    groupAdmins: Sequence['_ProblemGroupAdmin']
    groupScorePolicy: Optional[str]
    inputLimit: int
    languages: str
    levelTags: Sequence[str]
    log: Sequence['_ProblemVersion']
    memoryLimit: float
    outputLimit: int
    overallWallTimeLimit: float
    problemLevel: Optional[str]
    problemsetter: Optional['_ProblemsetterInfo']
    publicTags: Sequence[str]
    publishedRevision: Optional['_ProblemVersion']
    selectedPrivateTags: Sequence[str]
    selectedPublicTags: Sequence[str]
    showDiff: str
    solution: Optional['_ProblemStatement']
    source: str
    statement: '_ProblemStatement'
    statusError: Optional[str]
    statusSuccess: bool
    timeLimit: float
    title: str
    validLanguages: Dict[str, str]
    validator: str
    validatorTimeLimit: Union[float, int]
    validatorTypes: Dict[str, Optional[str]]
    visibility: int
    visibilityStatuses: Dict[str, int]

    def __init__(
        self,
        *,
        admins: Sequence[Dict[str, Any]],
        alias: str,
        allowUserAddTags: bool,
        emailClarifications: bool,
        extraWallTime: float,
        groupAdmins: Sequence[Dict[str, Any]],
        inputLimit: int,
        languages: str,
        levelTags: Sequence[str],
        log: Sequence[Dict[str, Any]],
        memoryLimit: float,
        outputLimit: int,
        overallWallTimeLimit: float,
        publicTags: Sequence[str],
        selectedPrivateTags: Sequence[str],
        selectedPublicTags: Sequence[str],
        showDiff: str,
        source: str,
        statement: Dict[str, Any],
        statusSuccess: bool,
        timeLimit: float,
        title: str,
        validLanguages: Dict[str, str],
        validator: str,
        validatorTimeLimit: Union[float, int],
        validatorTypes: Dict[str, Optional[str]],
        visibility: int,
        visibilityStatuses: Dict[str, int],
        groupScorePolicy: Optional[str] = None,
        problemLevel: Optional[str] = None,
        problemsetter: Optional[Dict[str, Any]] = None,
        publishedRevision: Optional[Dict[str, Any]] = None,
        solution: Optional[Dict[str, Any]] = None,
        statusError: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admins = [_ProblemAdmin(**v) for v in admins]
        self.alias = alias
        self.allowUserAddTags = allowUserAddTags
        self.emailClarifications = emailClarifications
        self.extraWallTime = extraWallTime
        self.groupAdmins = [_ProblemGroupAdmin(**v) for v in groupAdmins]
        if groupScorePolicy is not None:
            self.groupScorePolicy = groupScorePolicy
        else:
            self.groupScorePolicy = None
        self.inputLimit = inputLimit
        self.languages = languages
        self.levelTags = [v for v in levelTags]
        self.log = [_ProblemVersion(**v) for v in log]
        self.memoryLimit = memoryLimit
        self.outputLimit = outputLimit
        self.overallWallTimeLimit = overallWallTimeLimit
        if problemLevel is not None:
            self.problemLevel = problemLevel
        else:
            self.problemLevel = None
        if problemsetter is not None:
            self.problemsetter = _ProblemsetterInfo(**problemsetter)
        else:
            self.problemsetter = None
        self.publicTags = [v for v in publicTags]
        if publishedRevision is not None:
            self.publishedRevision = _ProblemVersion(**publishedRevision)
        else:
            self.publishedRevision = None
        self.selectedPrivateTags = [v for v in selectedPrivateTags]
        self.selectedPublicTags = [v for v in selectedPublicTags]
        self.showDiff = showDiff
        if solution is not None:
            self.solution = _ProblemStatement(**solution)
        else:
            self.solution = None
        self.source = source
        self.statement = _ProblemStatement(**statement)
        if statusError is not None:
            self.statusError = statusError
        else:
            self.statusError = None
        self.statusSuccess = statusSuccess
        self.timeLimit = timeLimit
        self.title = title
        self.validLanguages = {k: v for k, v in validLanguages.items()}
        self.validator = validator
        self.validatorTimeLimit = validatorTimeLimit
        self.validatorTypes = {
            k: v if v is not None else None
            for k, v in validatorTypes.items()
        }
        self.visibility = visibility
        self.visibilityStatuses = {k: v for k, v in visibilityStatuses.items()}


@dataclasses.dataclass
class _ProblemFormPayload:
    """_ProblemFormPayload"""
    alias: str
    allowUserAddTags: bool
    emailClarifications: bool
    extraWallTime: Union[int, str]
    groupScorePolicy: Optional[str]
    inputLimit: Union[int, str]
    languages: str
    levelTags: Sequence[str]
    memoryLimit: Union[int, str]
    message: Optional[str]
    outputLimit: Union[int, str]
    overallWallTimeLimit: Union[int, str]
    parameter: Optional[str]
    problem_level: str
    publicTags: Sequence[str]
    selectedTags: Optional[Sequence['_SelectedTag']]
    showDiff: str
    source: str
    statusError: str
    tags: Sequence['_ProblemFormPayload_tags_entry']
    timeLimit: Union[int, str]
    title: str
    validLanguages: Dict[str, str]
    validator: str
    validatorTimeLimit: Union[int, str]
    validatorTypes: Dict[str, Optional[str]]
    visibility: int
    visibilityStatuses: Dict[str, int]

    def __init__(
        self,
        *,
        alias: str,
        allowUserAddTags: bool,
        emailClarifications: bool,
        extraWallTime: Union[int, str],
        inputLimit: Union[int, str],
        languages: str,
        levelTags: Sequence[str],
        memoryLimit: Union[int, str],
        outputLimit: Union[int, str],
        overallWallTimeLimit: Union[int, str],
        problem_level: str,
        publicTags: Sequence[str],
        showDiff: str,
        source: str,
        statusError: str,
        tags: Sequence[Dict[str, Any]],
        timeLimit: Union[int, str],
        title: str,
        validLanguages: Dict[str, str],
        validator: str,
        validatorTimeLimit: Union[int, str],
        validatorTypes: Dict[str, Optional[str]],
        visibility: int,
        visibilityStatuses: Dict[str, int],
        groupScorePolicy: Optional[str] = None,
        message: Optional[str] = None,
        parameter: Optional[str] = None,
        selectedTags: Optional[Sequence[Dict[str, Any]]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.allowUserAddTags = allowUserAddTags
        self.emailClarifications = emailClarifications
        self.extraWallTime = extraWallTime
        if groupScorePolicy is not None:
            self.groupScorePolicy = groupScorePolicy
        else:
            self.groupScorePolicy = None
        self.inputLimit = inputLimit
        self.languages = languages
        self.levelTags = [v for v in levelTags]
        self.memoryLimit = memoryLimit
        if message is not None:
            self.message = message
        else:
            self.message = None
        self.outputLimit = outputLimit
        self.overallWallTimeLimit = overallWallTimeLimit
        if parameter is not None:
            self.parameter = parameter
        else:
            self.parameter = None
        self.problem_level = problem_level
        self.publicTags = [v for v in publicTags]
        if selectedTags is not None:
            self.selectedTags = [_SelectedTag(**v) for v in selectedTags]
        else:
            self.selectedTags = None
        self.showDiff = showDiff
        self.source = source
        self.statusError = statusError
        self.tags = [_ProblemFormPayload_tags_entry(**v) for v in tags]
        self.timeLimit = timeLimit
        self.title = title
        self.validLanguages = {k: v for k, v in validLanguages.items()}
        self.validator = validator
        self.validatorTimeLimit = validatorTimeLimit
        self.validatorTypes = {
            k: v if v is not None else None
            for k, v in validatorTypes.items()
        }
        self.visibility = visibility
        self.visibilityStatuses = {k: v for k, v in visibilityStatuses.items()}


@dataclasses.dataclass
class _ProblemFormPayload_tags_entry:
    """_ProblemFormPayload_tags_entry"""
    name: Optional[str]

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if name is not None:
            self.name = name
        else:
            self.name = None


@dataclasses.dataclass
class _ProblemGroupAdmin:
    """_ProblemGroupAdmin"""
    alias: str
    name: str
    role: str

    def __init__(
        self,
        *,
        alias: str,
        name: str,
        role: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.name = name
        self.role = role


@dataclasses.dataclass
class _ProblemInfo:
    """_ProblemInfo"""
    accepts_submissions: bool
    alias: str
    commit: str
    input_limit: int
    karel_problem: bool
    languages: Sequence[str]
    letter: Optional[str]
    limits: '_SettingLimits'
    nextSubmissionTimestamp: Optional[datetime.datetime]
    points: float
    preferred_language: Optional[str]
    problem_id: int
    problemsetter: Optional['_ProblemsetterInfo']
    quality_seal: bool
    sample_input: Optional[str]
    settings: '_ProblemSettingsDistrib'
    source: Optional[str]
    statement: '_ProblemStatement'
    title: str
    visibility: int

    def __init__(
        self,
        *,
        accepts_submissions: bool,
        alias: str,
        commit: str,
        input_limit: int,
        karel_problem: bool,
        languages: Sequence[str],
        limits: Dict[str, Any],
        points: float,
        problem_id: int,
        quality_seal: bool,
        settings: Dict[str, Any],
        statement: Dict[str, Any],
        title: str,
        visibility: int,
        letter: Optional[str] = None,
        nextSubmissionTimestamp: Optional[int] = None,
        preferred_language: Optional[str] = None,
        problemsetter: Optional[Dict[str, Any]] = None,
        sample_input: Optional[str] = None,
        source: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.accepts_submissions = accepts_submissions
        self.alias = alias
        self.commit = commit
        self.input_limit = input_limit
        self.karel_problem = karel_problem
        self.languages = [v for v in languages]
        if letter is not None:
            self.letter = letter
        else:
            self.letter = None
        self.limits = _SettingLimits(**limits)
        if nextSubmissionTimestamp is not None:
            self.nextSubmissionTimestamp = datetime.datetime.fromtimestamp(
                nextSubmissionTimestamp)
        else:
            self.nextSubmissionTimestamp = None
        self.points = points
        if preferred_language is not None:
            self.preferred_language = preferred_language
        else:
            self.preferred_language = None
        self.problem_id = problem_id
        if problemsetter is not None:
            self.problemsetter = _ProblemsetterInfo(**problemsetter)
        else:
            self.problemsetter = None
        self.quality_seal = quality_seal
        if sample_input is not None:
            self.sample_input = sample_input
        else:
            self.sample_input = None
        self.settings = _ProblemSettingsDistrib(**settings)
        if source is not None:
            self.source = source
        else:
            self.source = None
        self.statement = _ProblemStatement(**statement)
        self.title = title
        self.visibility = visibility


@dataclasses.dataclass
class _ProblemListCollectionPayload:
    """_ProblemListCollectionPayload"""
    allTags: Sequence['_Tag']
    levelTags: Sequence[str]
    problemCount: Sequence['_ProblemListCollectionPayload_problemCount_entry']

    def __init__(
        self,
        *,
        allTags: Sequence[Dict[str, Any]],
        levelTags: Sequence[str],
        problemCount: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.allTags = [_Tag(**v) for v in allTags]
        self.levelTags = [v for v in levelTags]
        self.problemCount = [
            _ProblemListCollectionPayload_problemCount_entry(**v)
            for v in problemCount
        ]


@dataclasses.dataclass
class _ProblemListCollectionPayload_problemCount_entry:
    """_ProblemListCollectionPayload_problemCount_entry"""
    name: str
    problems_per_tag: int

    def __init__(
        self,
        *,
        name: str,
        problems_per_tag: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.problems_per_tag = problems_per_tag


@dataclasses.dataclass
class _ProblemListItem:
    """_ProblemListItem"""
    alias: str
    difficulty: Optional[float]
    difficulty_histogram: Sequence[int]
    points: float
    problem_id: int
    quality: Optional[float]
    quality_histogram: Sequence[int]
    quality_seal: bool
    ratio: float
    score: float
    tags: Sequence['_ProblemListItem_tags_entry']
    title: str
    visibility: int

    def __init__(
        self,
        *,
        alias: str,
        difficulty_histogram: Sequence[int],
        points: float,
        problem_id: int,
        quality_histogram: Sequence[int],
        quality_seal: bool,
        ratio: float,
        score: float,
        tags: Sequence[Dict[str, Any]],
        title: str,
        visibility: int,
        difficulty: Optional[float] = None,
        quality: Optional[float] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        if difficulty is not None:
            self.difficulty = difficulty
        else:
            self.difficulty = None
        self.difficulty_histogram = [v for v in difficulty_histogram]
        self.points = points
        self.problem_id = problem_id
        if quality is not None:
            self.quality = quality
        else:
            self.quality = None
        self.quality_histogram = [v for v in quality_histogram]
        self.quality_seal = quality_seal
        self.ratio = ratio
        self.score = score
        self.tags = [_ProblemListItem_tags_entry(**v) for v in tags]
        self.title = title
        self.visibility = visibility


@dataclasses.dataclass
class _ProblemListItem_tags_entry:
    """_ProblemListItem_tags_entry"""
    name: str
    source: str

    def __init__(
        self,
        *,
        name: str,
        source: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.source = source


@dataclasses.dataclass
class _ProblemListPayload:
    """_ProblemListPayload"""
    column: str
    columns: Sequence[str]
    keyword: str
    language: str
    languages: Sequence[str]
    loggedIn: bool
    mode: str
    modes: Sequence[str]
    pagerItems: Sequence['_PageItem']
    problems: Sequence['_ProblemListItem']
    selectedTags: Sequence[str]
    tagData: Sequence['_ProblemListPayload_tagData_entry']
    tags: Sequence[str]

    def __init__(
        self,
        *,
        column: str,
        columns: Sequence[str],
        keyword: str,
        language: str,
        languages: Sequence[str],
        loggedIn: bool,
        mode: str,
        modes: Sequence[str],
        pagerItems: Sequence[Dict[str, Any]],
        problems: Sequence[Dict[str, Any]],
        selectedTags: Sequence[str],
        tagData: Sequence[Dict[str, Any]],
        tags: Sequence[str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.column = column
        self.columns = [v for v in columns]
        self.keyword = keyword
        self.language = language
        self.languages = [v for v in languages]
        self.loggedIn = loggedIn
        self.mode = mode
        self.modes = [v for v in modes]
        self.pagerItems = [_PageItem(**v) for v in pagerItems]
        self.problems = [_ProblemListItem(**v) for v in problems]
        self.selectedTags = [v for v in selectedTags]
        self.tagData = [
            _ProblemListPayload_tagData_entry(**v) for v in tagData
        ]
        self.tags = [v for v in tags]


@dataclasses.dataclass
class _ProblemListPayload_tagData_entry:
    """_ProblemListPayload_tagData_entry"""
    name: Optional[str]

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if name is not None:
            self.name = name
        else:
            self.name = None


@dataclasses.dataclass
class _ProblemPrintDetailsPayload:
    """_ProblemPrintDetailsPayload"""
    details: '_ProblemDetails'

    def __init__(
        self,
        *,
        details: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.details = _ProblemDetails(**details)


@dataclasses.dataclass
class _ProblemQualityPayload:
    """_ProblemQualityPayload"""
    canNominateProblem: bool
    dismissed: bool
    dismissedBeforeAc: bool
    language: Optional[str]
    nominated: bool
    nominatedBeforeAc: bool
    problemAlias: str
    solved: bool
    tried: bool

    def __init__(
        self,
        *,
        canNominateProblem: bool,
        dismissed: bool,
        dismissedBeforeAc: bool,
        nominated: bool,
        nominatedBeforeAc: bool,
        problemAlias: str,
        solved: bool,
        tried: bool,
        language: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.canNominateProblem = canNominateProblem
        self.dismissed = dismissed
        self.dismissedBeforeAc = dismissedBeforeAc
        if language is not None:
            self.language = language
        else:
            self.language = None
        self.nominated = nominated
        self.nominatedBeforeAc = nominatedBeforeAc
        self.problemAlias = problemAlias
        self.solved = solved
        self.tried = tried


@dataclasses.dataclass
class _ProblemSettings:
    """_ProblemSettings"""
    Cases: Sequence['_ProblemSettings_Cases_entry']
    Interactive: Optional['_ProblemSettings_Interactive']
    Limits: '_LimitsSettings'
    Slow: bool
    Validator: '_ProblemSettings_Validator'

    def __init__(
        self,
        *,
        Cases: Sequence[Dict[str, Any]],
        Limits: Dict[str, Any],
        Slow: bool,
        Validator: Dict[str, Any],
        Interactive: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.Cases = [_ProblemSettings_Cases_entry(**v) for v in Cases]
        if Interactive is not None:
            self.Interactive = _ProblemSettings_Interactive(**Interactive)
        else:
            self.Interactive = None
        self.Limits = _LimitsSettings(**Limits)
        self.Slow = Slow
        self.Validator = _ProblemSettings_Validator(**Validator)


@dataclasses.dataclass
class _ProblemSettingsDistrib:
    """_ProblemSettingsDistrib"""
    cases: Dict[str, '_ProblemSettingsDistrib_cases_value']
    interactive: Optional['_InteractiveSettingsDistrib']
    limits: '_LimitsSettings'
    validator: '_ProblemSettingsDistrib_validator'

    def __init__(
        self,
        *,
        cases: Dict[str, Dict[str, Any]],
        limits: Dict[str, Any],
        validator: Dict[str, Any],
        interactive: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.cases = {
            k: _ProblemSettingsDistrib_cases_value(**v)
            for k, v in cases.items()
        }
        if interactive is not None:
            self.interactive = _InteractiveSettingsDistrib(**interactive)
        else:
            self.interactive = None
        self.limits = _LimitsSettings(**limits)
        self.validator = _ProblemSettingsDistrib_validator(**validator)


@dataclasses.dataclass
class _ProblemSettingsDistrib_cases_value:
    """_ProblemSettingsDistrib_cases_value"""
    in_: str
    out: str
    weight: Optional[float]

    def __init__(
        self,
        *,
        out: str,
        weight: Optional[float] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.in_ = _kwargs['in']
        self.out = out
        if weight is not None:
            self.weight = weight
        else:
            self.weight = None


@dataclasses.dataclass
class _ProblemSettingsDistrib_validator:
    """_ProblemSettingsDistrib_validator"""
    custom_validator: Optional[
        '_ProblemSettingsDistrib_validator_custom_validator']
    group_score_policy: Optional[str]
    name: str
    tolerance: Optional[float]

    def __init__(
        self,
        *,
        name: str,
        custom_validator: Optional[Dict[str, Any]] = None,
        group_score_policy: Optional[str] = None,
        tolerance: Optional[float] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if custom_validator is not None:
            self.custom_validator = _ProblemSettingsDistrib_validator_custom_validator(
                **custom_validator)
        else:
            self.custom_validator = None
        if group_score_policy is not None:
            self.group_score_policy = group_score_policy
        else:
            self.group_score_policy = None
        self.name = name
        if tolerance is not None:
            self.tolerance = tolerance
        else:
            self.tolerance = None


@dataclasses.dataclass
class _ProblemSettingsDistrib_validator_custom_validator:
    """_ProblemSettingsDistrib_validator_custom_validator"""
    language: str
    limits: Optional['_LimitsSettings']
    source: str

    def __init__(
        self,
        *,
        language: str,
        source: str,
        limits: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.language = language
        if limits is not None:
            self.limits = _LimitsSettings(**limits)
        else:
            self.limits = None
        self.source = source


@dataclasses.dataclass
class _ProblemSettings_Cases_entry:
    """_ProblemSettings_Cases_entry"""
    Cases: Sequence['_ProblemSettings_Cases_entry_Cases_entry']
    Name: str

    def __init__(
        self,
        *,
        Cases: Sequence[Dict[str, Any]],
        Name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.Cases = [
            _ProblemSettings_Cases_entry_Cases_entry(**v) for v in Cases
        ]
        self.Name = Name


@dataclasses.dataclass
class _ProblemSettings_Cases_entry_Cases_entry:
    """_ProblemSettings_Cases_entry_Cases_entry"""
    Name: str
    Weight: float

    def __init__(
        self,
        *,
        Name: str,
        Weight: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.Name = Name
        self.Weight = Weight


@dataclasses.dataclass
class _ProblemSettings_Interactive:
    """_ProblemSettings_Interactive"""
    Interfaces: Dict[str, Dict[str, '_InteractiveInterface']]
    LibinteractiveVersion: str
    Main: str
    ModuleName: str
    ParentLang: str
    Templates: Dict[str, str]

    def __init__(
        self,
        *,
        Interfaces: Dict[str, Dict[str, Dict[str, Any]]],
        LibinteractiveVersion: str,
        Main: str,
        ModuleName: str,
        ParentLang: str,
        Templates: Dict[str, str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.Interfaces = {
            k: {k: _InteractiveInterface(**v)
                for k, v in v.items()}
            for k, v in Interfaces.items()
        }
        self.LibinteractiveVersion = LibinteractiveVersion
        self.Main = Main
        self.ModuleName = ModuleName
        self.ParentLang = ParentLang
        self.Templates = {k: v for k, v in Templates.items()}


@dataclasses.dataclass
class _ProblemSettings_Validator:
    """_ProblemSettings_Validator"""
    GroupScorePolicy: Optional[str]
    Lang: Optional[str]
    Limits: Optional['_LimitsSettings']
    Name: str
    Tolerance: float

    def __init__(
        self,
        *,
        Name: str,
        Tolerance: float,
        GroupScorePolicy: Optional[str] = None,
        Lang: Optional[str] = None,
        Limits: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if GroupScorePolicy is not None:
            self.GroupScorePolicy = GroupScorePolicy
        else:
            self.GroupScorePolicy = None
        if Lang is not None:
            self.Lang = Lang
        else:
            self.Lang = None
        if Limits is not None:
            self.Limits = _LimitsSettings(**Limits)
        else:
            self.Limits = None
        self.Name = Name
        self.Tolerance = Tolerance


@dataclasses.dataclass
class _ProblemStatement:
    """_ProblemStatement"""
    images: Dict[str, str]
    language: str
    markdown: str
    sources: Dict[str, str]

    def __init__(
        self,
        *,
        images: Dict[str, str],
        language: str,
        markdown: str,
        sources: Dict[str, str],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.images = {k: v for k, v in images.items()}
        self.language = language
        self.markdown = markdown
        self.sources = {k: v for k, v in sources.items()}


@dataclasses.dataclass
class _ProblemVersion:
    """_ProblemVersion"""
    author: '_Signature'
    commit: str
    committer: '_Signature'
    message: str
    parents: Sequence[str]
    tree: Dict[str, str]
    version: str

    def __init__(
        self,
        *,
        author: Dict[str, Any],
        commit: str,
        committer: Dict[str, Any],
        message: str,
        parents: Sequence[str],
        tree: Dict[str, str],
        version: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.author = _Signature(**author)
        self.commit = commit
        self.committer = _Signature(**committer)
        self.message = message
        self.parents = [v for v in parents]
        self.tree = {k: v for k, v in tree.items()}
        self.version = version


@dataclasses.dataclass
class _ProblemsMineInfoPayload:
    """_ProblemsMineInfoPayload"""
    isSysadmin: bool
    privateProblemsAlert: bool
    query: Optional[str]
    visibilityStatuses: Dict[str, int]

    def __init__(
        self,
        *,
        isSysadmin: bool,
        privateProblemsAlert: bool,
        visibilityStatuses: Dict[str, int],
        query: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.isSysadmin = isSysadmin
        self.privateProblemsAlert = privateProblemsAlert
        if query is not None:
            self.query = query
        else:
            self.query = None
        self.visibilityStatuses = {k: v for k, v in visibilityStatuses.items()}


@dataclasses.dataclass
class _Problemset:
    """_Problemset"""
    admin: Optional[bool]
    admission_mode: Optional[str]
    alias: Optional[str]
    archived: Optional[bool]
    assignment_type: Optional[str]
    contest_alias: Optional[str]
    courseAssignments: Optional[Sequence['_CourseAssignment']]
    description: Optional[str]
    director: Optional[str]
    feedback: Optional[str]
    finish_time: Optional[datetime.datetime]
    has_submissions: Optional[bool]
    languages: Optional[Sequence[str]]
    name: Optional[str]
    needs_basic_information: Optional[bool]
    opened: Optional[bool]
    original_contest_alias: Optional[str]
    original_problemset_id: Optional[int]
    partial_score: Optional[bool]
    penalty: Optional[int]
    penalty_calc_policy: Optional[str]
    penalty_type: Optional[str]
    points_decay_factor: Optional[float]
    problems: Optional[Sequence['_ProblemsetProblem']]
    problemset_id: Optional[int]
    requests_user_information: Optional[str]
    rerun_id: Optional[int]
    scoreboard: Optional[int]
    scoreboard_url: Optional[str]
    scoreboard_url_admin: Optional[str]
    show_penalty: Optional[bool]
    show_scoreboard_after: Optional[bool]
    start_time: Optional[datetime.datetime]
    submission_deadline: Optional[datetime.datetime]
    submissions_gap: Optional[int]
    title: Optional[str]
    users: Optional[Sequence['_Problemset_users_entry']]
    window_length: Optional[int]

    def __init__(
        self,
        *,
        admin: Optional[bool] = None,
        admission_mode: Optional[str] = None,
        alias: Optional[str] = None,
        archived: Optional[bool] = None,
        assignment_type: Optional[str] = None,
        contest_alias: Optional[str] = None,
        courseAssignments: Optional[Sequence[Dict[str, Any]]] = None,
        description: Optional[str] = None,
        director: Optional[str] = None,
        feedback: Optional[str] = None,
        finish_time: Optional[int] = None,
        has_submissions: Optional[bool] = None,
        languages: Optional[Sequence[str]] = None,
        name: Optional[str] = None,
        needs_basic_information: Optional[bool] = None,
        opened: Optional[bool] = None,
        original_contest_alias: Optional[str] = None,
        original_problemset_id: Optional[int] = None,
        partial_score: Optional[bool] = None,
        penalty: Optional[int] = None,
        penalty_calc_policy: Optional[str] = None,
        penalty_type: Optional[str] = None,
        points_decay_factor: Optional[float] = None,
        problems: Optional[Sequence[Dict[str, Any]]] = None,
        problemset_id: Optional[int] = None,
        requests_user_information: Optional[str] = None,
        rerun_id: Optional[int] = None,
        scoreboard: Optional[int] = None,
        scoreboard_url: Optional[str] = None,
        scoreboard_url_admin: Optional[str] = None,
        show_penalty: Optional[bool] = None,
        show_scoreboard_after: Optional[bool] = None,
        start_time: Optional[int] = None,
        submission_deadline: Optional[int] = None,
        submissions_gap: Optional[int] = None,
        title: Optional[str] = None,
        users: Optional[Sequence[Dict[str, Any]]] = None,
        window_length: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if admin is not None:
            self.admin = admin
        else:
            self.admin = None
        if admission_mode is not None:
            self.admission_mode = admission_mode
        else:
            self.admission_mode = None
        if alias is not None:
            self.alias = alias
        else:
            self.alias = None
        if archived is not None:
            self.archived = archived
        else:
            self.archived = None
        if assignment_type is not None:
            self.assignment_type = assignment_type
        else:
            self.assignment_type = None
        if contest_alias is not None:
            self.contest_alias = contest_alias
        else:
            self.contest_alias = None
        if courseAssignments is not None:
            self.courseAssignments = [
                _CourseAssignment(**v) for v in courseAssignments
            ]
        else:
            self.courseAssignments = None
        if description is not None:
            self.description = description
        else:
            self.description = None
        if director is not None:
            self.director = director
        else:
            self.director = None
        if feedback is not None:
            self.feedback = feedback
        else:
            self.feedback = None
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        if has_submissions is not None:
            self.has_submissions = has_submissions
        else:
            self.has_submissions = None
        if languages is not None:
            self.languages = [v for v in languages]
        else:
            self.languages = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        if needs_basic_information is not None:
            self.needs_basic_information = needs_basic_information
        else:
            self.needs_basic_information = None
        if opened is not None:
            self.opened = opened
        else:
            self.opened = None
        if original_contest_alias is not None:
            self.original_contest_alias = original_contest_alias
        else:
            self.original_contest_alias = None
        if original_problemset_id is not None:
            self.original_problemset_id = original_problemset_id
        else:
            self.original_problemset_id = None
        if partial_score is not None:
            self.partial_score = partial_score
        else:
            self.partial_score = None
        if penalty is not None:
            self.penalty = penalty
        else:
            self.penalty = None
        if penalty_calc_policy is not None:
            self.penalty_calc_policy = penalty_calc_policy
        else:
            self.penalty_calc_policy = None
        if penalty_type is not None:
            self.penalty_type = penalty_type
        else:
            self.penalty_type = None
        if points_decay_factor is not None:
            self.points_decay_factor = points_decay_factor
        else:
            self.points_decay_factor = None
        if problems is not None:
            self.problems = [_ProblemsetProblem(**v) for v in problems]
        else:
            self.problems = None
        if problemset_id is not None:
            self.problemset_id = problemset_id
        else:
            self.problemset_id = None
        if requests_user_information is not None:
            self.requests_user_information = requests_user_information
        else:
            self.requests_user_information = None
        if rerun_id is not None:
            self.rerun_id = rerun_id
        else:
            self.rerun_id = None
        if scoreboard is not None:
            self.scoreboard = scoreboard
        else:
            self.scoreboard = None
        if scoreboard_url is not None:
            self.scoreboard_url = scoreboard_url
        else:
            self.scoreboard_url = None
        if scoreboard_url_admin is not None:
            self.scoreboard_url_admin = scoreboard_url_admin
        else:
            self.scoreboard_url_admin = None
        if show_penalty is not None:
            self.show_penalty = show_penalty
        else:
            self.show_penalty = None
        if show_scoreboard_after is not None:
            self.show_scoreboard_after = show_scoreboard_after
        else:
            self.show_scoreboard_after = None
        if start_time is not None:
            self.start_time = datetime.datetime.fromtimestamp(start_time)
        else:
            self.start_time = None
        if submission_deadline is not None:
            self.submission_deadline = datetime.datetime.fromtimestamp(
                submission_deadline)
        else:
            self.submission_deadline = None
        if submissions_gap is not None:
            self.submissions_gap = submissions_gap
        else:
            self.submissions_gap = None
        if title is not None:
            self.title = title
        else:
            self.title = None
        if users is not None:
            self.users = [_Problemset_users_entry(**v) for v in users]
        else:
            self.users = None
        if window_length is not None:
            self.window_length = window_length
        else:
            self.window_length = None


@dataclasses.dataclass
class _ProblemsetProblem:
    """_ProblemsetProblem"""
    accepted: int
    accepts_submissions: bool
    alias: str
    commit: str
    difficulty: float
    has_submissions: bool
    input_limit: int
    is_extra_problem: bool
    languages: str
    letter: Optional[str]
    order: int
    points: float
    problem_id: Optional[int]
    quality_payload: Optional['_ProblemQualityPayload']
    quality_seal: bool
    submissions: int
    title: str
    version: str
    visibility: int
    visits: int

    def __init__(
        self,
        *,
        accepted: int,
        accepts_submissions: bool,
        alias: str,
        commit: str,
        difficulty: float,
        has_submissions: bool,
        input_limit: int,
        is_extra_problem: bool,
        languages: str,
        order: int,
        points: float,
        quality_seal: bool,
        submissions: int,
        title: str,
        version: str,
        visibility: int,
        visits: int,
        letter: Optional[str] = None,
        problem_id: Optional[int] = None,
        quality_payload: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.accepted = accepted
        self.accepts_submissions = accepts_submissions
        self.alias = alias
        self.commit = commit
        self.difficulty = difficulty
        self.has_submissions = has_submissions
        self.input_limit = input_limit
        self.is_extra_problem = is_extra_problem
        self.languages = languages
        if letter is not None:
            self.letter = letter
        else:
            self.letter = None
        self.order = order
        self.points = points
        if problem_id is not None:
            self.problem_id = problem_id
        else:
            self.problem_id = None
        if quality_payload is not None:
            self.quality_payload = _ProblemQualityPayload(**quality_payload)
        else:
            self.quality_payload = None
        self.quality_seal = quality_seal
        self.submissions = submissions
        self.title = title
        self.version = version
        self.visibility = visibility
        self.visits = visits


@dataclasses.dataclass
class _ProblemsetProblemWithVersions:
    """_ProblemsetProblemWithVersions"""
    accepted: int
    accepts_submissions: bool
    alias: str
    commit: str
    difficulty: float
    has_submissions: bool
    input_limit: int
    languages: str
    letter: Optional[str]
    order: int
    points: float
    quality_payload: Optional['_ProblemQualityPayload']
    quality_seal: bool
    submissions: int
    title: str
    version: str
    versions: '_ProblemsetProblemWithVersions_versions'
    visibility: int
    visits: int

    def __init__(
        self,
        *,
        accepted: int,
        accepts_submissions: bool,
        alias: str,
        commit: str,
        difficulty: float,
        has_submissions: bool,
        input_limit: int,
        languages: str,
        order: int,
        points: float,
        quality_seal: bool,
        submissions: int,
        title: str,
        version: str,
        versions: Dict[str, Any],
        visibility: int,
        visits: int,
        letter: Optional[str] = None,
        quality_payload: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.accepted = accepted
        self.accepts_submissions = accepts_submissions
        self.alias = alias
        self.commit = commit
        self.difficulty = difficulty
        self.has_submissions = has_submissions
        self.input_limit = input_limit
        self.languages = languages
        if letter is not None:
            self.letter = letter
        else:
            self.letter = None
        self.order = order
        self.points = points
        if quality_payload is not None:
            self.quality_payload = _ProblemQualityPayload(**quality_payload)
        else:
            self.quality_payload = None
        self.quality_seal = quality_seal
        self.submissions = submissions
        self.title = title
        self.version = version
        self.versions = _ProblemsetProblemWithVersions_versions(**versions)
        self.visibility = visibility
        self.visits = visits


@dataclasses.dataclass
class _ProblemsetProblemWithVersions_versions:
    """_ProblemsetProblemWithVersions_versions"""
    log: Sequence['_ProblemVersion']
    published: str

    def __init__(
        self,
        *,
        log: Sequence[Dict[str, Any]],
        published: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.log = [_ProblemVersion(**v) for v in log]
        self.published = published


@dataclasses.dataclass
class _Problemset_users_entry:
    """_Problemset_users_entry"""
    access_time: Optional[datetime.datetime]
    country: Optional[str]
    email: Optional[str]
    user_id: Optional[int]
    username: str

    def __init__(
        self,
        *,
        username: str,
        access_time: Optional[int] = None,
        country: Optional[str] = None,
        email: Optional[str] = None,
        user_id: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if access_time is not None:
            self.access_time = datetime.datetime.fromtimestamp(access_time)
        else:
            self.access_time = None
        if country is not None:
            self.country = country
        else:
            self.country = None
        if email is not None:
            self.email = email
        else:
            self.email = None
        if user_id is not None:
            self.user_id = user_id
        else:
            self.user_id = None
        self.username = username


@dataclasses.dataclass
class _ProblemsetterInfo:
    """_ProblemsetterInfo"""
    classname: str
    creation_date: Optional[datetime.datetime]
    name: str
    username: str

    def __init__(
        self,
        *,
        classname: str,
        name: str,
        username: str,
        creation_date: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        if creation_date is not None:
            self.creation_date = datetime.datetime.fromtimestamp(creation_date)
        else:
            self.creation_date = None
        self.name = name
        self.username = username


@dataclasses.dataclass
class _Progress:
    """_Progress"""
    max_score: float
    score: float

    def __init__(
        self,
        *,
        max_score: float,
        score: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.max_score = max_score
        self.score = score


@dataclasses.dataclass
class _Run:
    """_Run"""
    alias: str
    classname: str
    contest_alias: Optional[str]
    contest_score: Optional[float]
    country: str
    guid: str
    language: str
    memory: int
    penalty: int
    runtime: int
    score: float
    status: str
    submit_delay: int
    time: datetime.datetime
    type: Optional[str]
    username: str
    verdict: str

    def __init__(
        self,
        *,
        alias: str,
        classname: str,
        country: str,
        guid: str,
        language: str,
        memory: int,
        penalty: int,
        runtime: int,
        score: float,
        status: str,
        submit_delay: int,
        time: int,
        username: str,
        verdict: str,
        contest_alias: Optional[str] = None,
        contest_score: Optional[float] = None,
        type: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.classname = classname
        if contest_alias is not None:
            self.contest_alias = contest_alias
        else:
            self.contest_alias = None
        if contest_score is not None:
            self.contest_score = contest_score
        else:
            self.contest_score = None
        self.country = country
        self.guid = guid
        self.language = language
        self.memory = memory
        self.penalty = penalty
        self.runtime = runtime
        self.score = score
        self.status = status
        self.submit_delay = submit_delay
        self.time = datetime.datetime.fromtimestamp(time)
        if type is not None:
            self.type = type
        else:
            self.type = None
        self.username = username
        self.verdict = verdict


@dataclasses.dataclass
class _RunDetails:
    """_RunDetails"""
    admin: bool
    alias: str
    cases: Dict[str, '_ProblemCasesContents_value']
    compile_error: Optional[str]
    details: Optional['_RunDetails_details']
    feedback: Optional['_SubmissionFeedback']
    guid: str
    judged_by: Optional[str]
    language: str
    logs: Optional[str]
    show_diff: str
    source: Optional[str]
    source_link: Optional[bool]
    source_name: Optional[str]
    source_url: Optional[str]

    def __init__(
        self,
        *,
        admin: bool,
        alias: str,
        cases: Dict[str, Dict[str, Any]],
        guid: str,
        language: str,
        show_diff: str,
        compile_error: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        feedback: Optional[Dict[str, Any]] = None,
        judged_by: Optional[str] = None,
        logs: Optional[str] = None,
        source: Optional[str] = None,
        source_link: Optional[bool] = None,
        source_name: Optional[str] = None,
        source_url: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = admin
        self.alias = alias
        self.cases = {
            k: _ProblemCasesContents_value(**v)
            for k, v in cases.items()
        }
        if compile_error is not None:
            self.compile_error = compile_error
        else:
            self.compile_error = None
        if details is not None:
            self.details = _RunDetails_details(**details)
        else:
            self.details = None
        if feedback is not None:
            self.feedback = _SubmissionFeedback(**feedback)
        else:
            self.feedback = None
        self.guid = guid
        if judged_by is not None:
            self.judged_by = judged_by
        else:
            self.judged_by = None
        self.language = language
        if logs is not None:
            self.logs = logs
        else:
            self.logs = None
        self.show_diff = show_diff
        if source is not None:
            self.source = source
        else:
            self.source = None
        if source_link is not None:
            self.source_link = source_link
        else:
            self.source_link = None
        if source_name is not None:
            self.source_name = source_name
        else:
            self.source_name = None
        if source_url is not None:
            self.source_url = source_url
        else:
            self.source_url = None


@dataclasses.dataclass
class _RunDetailsGroup:
    """_RunDetailsGroup"""
    cases: Sequence['_CaseResult']
    contest_score: float
    group: str
    max_score: float
    score: float
    verdict: Optional[str]

    def __init__(
        self,
        *,
        cases: Sequence[Dict[str, Any]],
        contest_score: float,
        group: str,
        max_score: float,
        score: float,
        verdict: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.cases = [_CaseResult(**v) for v in cases]
        self.contest_score = contest_score
        self.group = group
        self.max_score = max_score
        self.score = score
        if verdict is not None:
            self.verdict = verdict
        else:
            self.verdict = None


@dataclasses.dataclass
class _RunDetailsV2:
    """_RunDetailsV2"""
    admin: bool
    cases: Dict[str, '_ProblemCasesContents_value']
    compile_error: Optional[str]
    details: Optional['_RunDetailsV2_details']
    feedback: Optional['_SubmissionFeedback']
    judged_by: Optional[str]
    logs: Optional[str]
    show_diff: str
    source: Optional[str]
    source_link: Optional[bool]
    source_name: Optional[str]
    source_url: Optional[str]

    def __init__(
        self,
        *,
        admin: bool,
        cases: Dict[str, Dict[str, Any]],
        show_diff: str,
        compile_error: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        feedback: Optional[Dict[str, Any]] = None,
        judged_by: Optional[str] = None,
        logs: Optional[str] = None,
        source: Optional[str] = None,
        source_link: Optional[bool] = None,
        source_name: Optional[str] = None,
        source_url: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = admin
        self.cases = {
            k: _ProblemCasesContents_value(**v)
            for k, v in cases.items()
        }
        if compile_error is not None:
            self.compile_error = compile_error
        else:
            self.compile_error = None
        if details is not None:
            self.details = _RunDetailsV2_details(**details)
        else:
            self.details = None
        if feedback is not None:
            self.feedback = _SubmissionFeedback(**feedback)
        else:
            self.feedback = None
        if judged_by is not None:
            self.judged_by = judged_by
        else:
            self.judged_by = None
        if logs is not None:
            self.logs = logs
        else:
            self.logs = None
        self.show_diff = show_diff
        if source is not None:
            self.source = source
        else:
            self.source = None
        if source_link is not None:
            self.source_link = source_link
        else:
            self.source_link = None
        if source_name is not None:
            self.source_name = source_name
        else:
            self.source_name = None
        if source_url is not None:
            self.source_url = source_url
        else:
            self.source_url = None


@dataclasses.dataclass
class _RunDetailsV2_details:
    """_RunDetailsV2_details"""
    compile_meta: Optional[Dict[str, '_RunMetadata']]
    groups: Optional[Sequence['_RunDetailsGroup']]
    judged_by: str
    max_score: Optional[float]
    memory: Optional[float]
    score: float
    time: Optional[float]
    verdict: str
    wall_time: Optional[float]

    def __init__(
        self,
        *,
        judged_by: str,
        score: float,
        verdict: str,
        compile_meta: Optional[Dict[str, Dict[str, Any]]] = None,
        groups: Optional[Sequence[Dict[str, Any]]] = None,
        max_score: Optional[float] = None,
        memory: Optional[float] = None,
        time: Optional[float] = None,
        wall_time: Optional[float] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if compile_meta is not None:
            self.compile_meta = {
                k: _RunMetadata(**v)
                for k, v in compile_meta.items()
            }
        else:
            self.compile_meta = None
        if groups is not None:
            self.groups = [_RunDetailsGroup(**v) for v in groups]
        else:
            self.groups = None
        self.judged_by = judged_by
        if max_score is not None:
            self.max_score = max_score
        else:
            self.max_score = None
        if memory is not None:
            self.memory = memory
        else:
            self.memory = None
        self.score = score
        if time is not None:
            self.time = time
        else:
            self.time = None
        self.verdict = verdict
        if wall_time is not None:
            self.wall_time = wall_time
        else:
            self.wall_time = None


@dataclasses.dataclass
class _RunDetails_details:
    """_RunDetails_details"""
    compile_meta: Optional[Dict[str, '_RunMetadata']]
    contest_score: float
    groups: Optional[Sequence['_RunDetailsGroup']]
    judged_by: str
    max_score: Optional[float]
    memory: Optional[float]
    score: float
    time: Optional[float]
    verdict: str
    wall_time: Optional[float]

    def __init__(
        self,
        *,
        contest_score: float,
        judged_by: str,
        score: float,
        verdict: str,
        compile_meta: Optional[Dict[str, Dict[str, Any]]] = None,
        groups: Optional[Sequence[Dict[str, Any]]] = None,
        max_score: Optional[float] = None,
        memory: Optional[float] = None,
        time: Optional[float] = None,
        wall_time: Optional[float] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if compile_meta is not None:
            self.compile_meta = {
                k: _RunMetadata(**v)
                for k, v in compile_meta.items()
            }
        else:
            self.compile_meta = None
        self.contest_score = contest_score
        if groups is not None:
            self.groups = [_RunDetailsGroup(**v) for v in groups]
        else:
            self.groups = None
        self.judged_by = judged_by
        if max_score is not None:
            self.max_score = max_score
        else:
            self.max_score = None
        if memory is not None:
            self.memory = memory
        else:
            self.memory = None
        self.score = score
        if time is not None:
            self.time = time
        else:
            self.time = None
        self.verdict = verdict
        if wall_time is not None:
            self.wall_time = wall_time
        else:
            self.wall_time = None


@dataclasses.dataclass
class _RunMetadata:
    """_RunMetadata"""
    memory: int
    sys_time: int
    time: float
    verdict: str
    wall_time: float

    def __init__(
        self,
        *,
        memory: int,
        sys_time: int,
        time: float,
        verdict: str,
        wall_time: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.memory = memory
        self.sys_time = sys_time
        self.time = time
        self.verdict = verdict
        self.wall_time = wall_time


@dataclasses.dataclass
class _RunWithDetails:
    """_RunWithDetails"""
    alias: str
    classname: str
    contest_alias: Optional[str]
    contest_score: Optional[float]
    country: str
    details: Optional['_RunDetailsV2']
    guid: str
    language: str
    memory: int
    penalty: int
    runtime: int
    score: float
    status: str
    submit_delay: int
    time: datetime.datetime
    type: Optional[str]
    username: str
    verdict: str

    def __init__(
        self,
        *,
        alias: str,
        classname: str,
        country: str,
        guid: str,
        language: str,
        memory: int,
        penalty: int,
        runtime: int,
        score: float,
        status: str,
        submit_delay: int,
        time: int,
        username: str,
        verdict: str,
        contest_alias: Optional[str] = None,
        contest_score: Optional[float] = None,
        details: Optional[Dict[str, Any]] = None,
        type: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.classname = classname
        if contest_alias is not None:
            self.contest_alias = contest_alias
        else:
            self.contest_alias = None
        if contest_score is not None:
            self.contest_score = contest_score
        else:
            self.contest_score = None
        self.country = country
        if details is not None:
            self.details = _RunDetailsV2(**details)
        else:
            self.details = None
        self.guid = guid
        self.language = language
        self.memory = memory
        self.penalty = penalty
        self.runtime = runtime
        self.score = score
        self.status = status
        self.submit_delay = submit_delay
        self.time = datetime.datetime.fromtimestamp(time)
        if type is not None:
            self.type = type
        else:
            self.type = None
        self.username = username
        self.verdict = verdict


@dataclasses.dataclass
class _RunsDiff:
    """_RunsDiff"""
    guid: str
    new_score: Optional[float]
    new_status: Optional[str]
    new_verdict: Optional[str]
    old_score: Optional[float]
    old_status: Optional[str]
    old_verdict: Optional[str]
    problemset_id: Optional[int]
    username: str

    def __init__(
        self,
        *,
        guid: str,
        username: str,
        new_score: Optional[float] = None,
        new_status: Optional[str] = None,
        new_verdict: Optional[str] = None,
        old_score: Optional[float] = None,
        old_status: Optional[str] = None,
        old_verdict: Optional[str] = None,
        problemset_id: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.guid = guid
        if new_score is not None:
            self.new_score = new_score
        else:
            self.new_score = None
        if new_status is not None:
            self.new_status = new_status
        else:
            self.new_status = None
        if new_verdict is not None:
            self.new_verdict = new_verdict
        else:
            self.new_verdict = None
        if old_score is not None:
            self.old_score = old_score
        else:
            self.old_score = None
        if old_status is not None:
            self.old_status = old_status
        else:
            self.old_status = None
        if old_verdict is not None:
            self.old_verdict = old_verdict
        else:
            self.old_verdict = None
        if problemset_id is not None:
            self.problemset_id = problemset_id
        else:
            self.problemset_id = None
        self.username = username


@dataclasses.dataclass
class _School:
    """_School"""
    country_id: Optional[str]
    name: str
    ranking: Optional[int]
    school_id: int
    score: float

    def __init__(
        self,
        *,
        name: str,
        school_id: int,
        score: float,
        country_id: Optional[str] = None,
        ranking: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        self.name = name
        if ranking is not None:
            self.ranking = ranking
        else:
            self.ranking = None
        self.school_id = school_id
        self.score = score


@dataclasses.dataclass
class _SchoolCoderOfTheMonth:
    """_SchoolCoderOfTheMonth"""
    classname: str
    time: str
    username: str

    def __init__(
        self,
        *,
        classname: str,
        time: str,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        self.time = time
        self.username = username


@dataclasses.dataclass
class _SchoolOfTheMonthPayload:
    """_SchoolOfTheMonthPayload"""
    candidatesToSchoolOfTheMonth: Sequence[
        '_SchoolOfTheMonthPayload_candidatesToSchoolOfTheMonth_entry']
    isMentor: bool
    options: Optional['_SchoolOfTheMonthPayload_options']
    schoolsOfPreviousMonth: Sequence[
        '_SchoolOfTheMonthPayload_schoolsOfPreviousMonth_entry']
    schoolsOfPreviousMonths: Sequence[
        '_SchoolOfTheMonthPayload_schoolsOfPreviousMonths_entry']

    def __init__(
        self,
        *,
        candidatesToSchoolOfTheMonth: Sequence[Dict[str, Any]],
        isMentor: bool,
        schoolsOfPreviousMonth: Sequence[Dict[str, Any]],
        schoolsOfPreviousMonths: Sequence[Dict[str, Any]],
        options: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.candidatesToSchoolOfTheMonth = [
            _SchoolOfTheMonthPayload_candidatesToSchoolOfTheMonth_entry(**v)
            for v in candidatesToSchoolOfTheMonth
        ]
        self.isMentor = isMentor
        if options is not None:
            self.options = _SchoolOfTheMonthPayload_options(**options)
        else:
            self.options = None
        self.schoolsOfPreviousMonth = [
            _SchoolOfTheMonthPayload_schoolsOfPreviousMonth_entry(**v)
            for v in schoolsOfPreviousMonth
        ]
        self.schoolsOfPreviousMonths = [
            _SchoolOfTheMonthPayload_schoolsOfPreviousMonths_entry(**v)
            for v in schoolsOfPreviousMonths
        ]


@dataclasses.dataclass
class _SchoolOfTheMonthPayload_candidatesToSchoolOfTheMonth_entry:
    """_SchoolOfTheMonthPayload_candidatesToSchoolOfTheMonth_entry"""
    country_id: str
    name: str
    ranking: int
    school_id: int
    school_of_the_month_id: int
    score: float

    def __init__(
        self,
        *,
        country_id: str,
        name: str,
        ranking: int,
        school_id: int,
        school_of_the_month_id: int,
        score: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.country_id = country_id
        self.name = name
        self.ranking = ranking
        self.school_id = school_id
        self.school_of_the_month_id = school_of_the_month_id
        self.score = score


@dataclasses.dataclass
class _SchoolOfTheMonthPayload_options:
    """_SchoolOfTheMonthPayload_options"""
    canChooseSchool: bool
    schoolIsSelected: bool

    def __init__(
        self,
        *,
        canChooseSchool: bool,
        schoolIsSelected: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.canChooseSchool = canChooseSchool
        self.schoolIsSelected = schoolIsSelected


@dataclasses.dataclass
class _SchoolOfTheMonthPayload_schoolsOfPreviousMonth_entry:
    """_SchoolOfTheMonthPayload_schoolsOfPreviousMonth_entry"""
    country_id: str
    name: str
    ranking: int
    school_id: int

    def __init__(
        self,
        *,
        country_id: str,
        name: str,
        ranking: int,
        school_id: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.country_id = country_id
        self.name = name
        self.ranking = ranking
        self.school_id = school_id


@dataclasses.dataclass
class _SchoolOfTheMonthPayload_schoolsOfPreviousMonths_entry:
    """_SchoolOfTheMonthPayload_schoolsOfPreviousMonths_entry"""
    country_id: str
    name: str
    school_id: int
    time: str

    def __init__(
        self,
        *,
        country_id: str,
        name: str,
        school_id: int,
        time: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.country_id = country_id
        self.name = name
        self.school_id = school_id
        self.time = time


@dataclasses.dataclass
class _SchoolProblemsSolved:
    """_SchoolProblemsSolved"""
    month: int
    problems_solved: int
    year: int

    def __init__(
        self,
        *,
        month: int,
        problems_solved: int,
        year: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.month = month
        self.problems_solved = problems_solved
        self.year = year


@dataclasses.dataclass
class _SchoolProfileDetailsPayload:
    """_SchoolProfileDetailsPayload"""
    coders_of_the_month: Sequence['_SchoolCoderOfTheMonth']
    country: Optional['_SchoolProfileDetailsPayload_country']
    monthly_solved_problems: Sequence['_SchoolProblemsSolved']
    ranking: int
    school_id: int
    school_name: str
    school_users: Sequence['_SchoolUser']
    state_name: Optional[str]

    def __init__(
        self,
        *,
        coders_of_the_month: Sequence[Dict[str, Any]],
        monthly_solved_problems: Sequence[Dict[str, Any]],
        ranking: int,
        school_id: int,
        school_name: str,
        school_users: Sequence[Dict[str, Any]],
        country: Optional[Dict[str, Any]] = None,
        state_name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.coders_of_the_month = [
            _SchoolCoderOfTheMonth(**v) for v in coders_of_the_month
        ]
        if country is not None:
            self.country = _SchoolProfileDetailsPayload_country(**country)
        else:
            self.country = None
        self.monthly_solved_problems = [
            _SchoolProblemsSolved(**v) for v in monthly_solved_problems
        ]
        self.ranking = ranking
        self.school_id = school_id
        self.school_name = school_name
        self.school_users = [_SchoolUser(**v) for v in school_users]
        if state_name is not None:
            self.state_name = state_name
        else:
            self.state_name = None


@dataclasses.dataclass
class _SchoolProfileDetailsPayload_country:
    """_SchoolProfileDetailsPayload_country"""
    id: str
    name: str

    def __init__(
        self,
        *,
        id: str,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.id = id
        self.name = name


@dataclasses.dataclass
class _SchoolRankPayload:
    """_SchoolRankPayload"""
    length: int
    page: int
    pagerItems: Sequence['_PageItem']
    rank: Sequence['_School']
    showHeader: bool
    totalRows: int

    def __init__(
        self,
        *,
        length: int,
        page: int,
        pagerItems: Sequence[Dict[str, Any]],
        rank: Sequence[Dict[str, Any]],
        showHeader: bool,
        totalRows: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.length = length
        self.page = page
        self.pagerItems = [_PageItem(**v) for v in pagerItems]
        self.rank = [_School(**v) for v in rank]
        self.showHeader = showHeader
        self.totalRows = totalRows


@dataclasses.dataclass
class _SchoolUser:
    """_SchoolUser"""
    classname: str
    created_problems: int
    organized_contests: int
    solved_problems: int
    username: str

    def __init__(
        self,
        *,
        classname: str,
        created_problems: int,
        organized_contests: int,
        solved_problems: int,
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        self.created_problems = created_problems
        self.organized_contests = organized_contests
        self.solved_problems = solved_problems
        self.username = username


@dataclasses.dataclass
class _Scoreboard:
    """_Scoreboard"""
    finish_time: Optional[datetime.datetime]
    problems: Sequence['_Scoreboard_problems_entry']
    ranking: Sequence['_ScoreboardRankingEntry']
    start_time: datetime.datetime
    time: datetime.datetime
    title: str

    def __init__(
        self,
        *,
        problems: Sequence[Dict[str, Any]],
        ranking: Sequence[Dict[str, Any]],
        start_time: int,
        time: int,
        title: str,
        finish_time: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if finish_time is not None:
            self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        else:
            self.finish_time = None
        self.problems = [_Scoreboard_problems_entry(**v) for v in problems]
        self.ranking = [_ScoreboardRankingEntry(**v) for v in ranking]
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        self.time = datetime.datetime.fromtimestamp(time)
        self.title = title


@dataclasses.dataclass
class _ScoreboardContest:
    """_ScoreboardContest"""
    acl_id: int
    admission_mode: str
    alias: str
    contest_id: int
    description: str
    feedback: str
    finish_time: datetime.datetime
    languages: str
    last_updated: int
    only_ac: Optional[bool]
    partial_score: bool
    penalty: str
    penalty_calc_policy: str
    points_decay_factor: float
    problemset_id: int
    recommended: bool
    rerun_id: int
    scoreboard: int
    show_scoreboard_after: bool
    start_time: datetime.datetime
    submissions_gap: int
    title: str
    urgent: bool
    weight: Optional[float]
    window_length: Optional[int]

    def __init__(
        self,
        *,
        acl_id: int,
        admission_mode: str,
        alias: str,
        contest_id: int,
        description: str,
        feedback: str,
        finish_time: int,
        languages: str,
        last_updated: int,
        partial_score: bool,
        penalty: str,
        penalty_calc_policy: str,
        points_decay_factor: float,
        problemset_id: int,
        recommended: bool,
        rerun_id: int,
        scoreboard: int,
        show_scoreboard_after: bool,
        start_time: int,
        submissions_gap: int,
        title: str,
        urgent: bool,
        only_ac: Optional[bool] = None,
        weight: Optional[float] = None,
        window_length: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.acl_id = acl_id
        self.admission_mode = admission_mode
        self.alias = alias
        self.contest_id = contest_id
        self.description = description
        self.feedback = feedback
        self.finish_time = datetime.datetime.fromtimestamp(finish_time)
        self.languages = languages
        self.last_updated = last_updated
        if only_ac is not None:
            self.only_ac = only_ac
        else:
            self.only_ac = None
        self.partial_score = partial_score
        self.penalty = penalty
        self.penalty_calc_policy = penalty_calc_policy
        self.points_decay_factor = points_decay_factor
        self.problemset_id = problemset_id
        self.recommended = recommended
        self.rerun_id = rerun_id
        self.scoreboard = scoreboard
        self.show_scoreboard_after = show_scoreboard_after
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        self.submissions_gap = submissions_gap
        self.title = title
        self.urgent = urgent
        if weight is not None:
            self.weight = weight
        else:
            self.weight = None
        if window_length is not None:
            self.window_length = window_length
        else:
            self.window_length = None


@dataclasses.dataclass
class _ScoreboardDetails:
    """_ScoreboardDetails"""
    alias: str
    create_time: int
    description: str
    group_id: int
    group_scoreboard_id: int
    name: str

    def __init__(
        self,
        *,
        alias: str,
        create_time: int,
        description: str,
        group_id: int,
        group_scoreboard_id: int,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.create_time = create_time
        self.description = description
        self.group_id = group_id
        self.group_scoreboard_id = group_scoreboard_id
        self.name = name


@dataclasses.dataclass
class _ScoreboardEvent:
    """_ScoreboardEvent"""
    classname: str
    country: str
    delta: float
    is_invited: bool
    name: Optional[str]
    problem: '_ScoreboardEvent_problem'
    total: '_ScoreboardEvent_total'
    username: str

    def __init__(
        self,
        *,
        classname: str,
        country: str,
        delta: float,
        is_invited: bool,
        problem: Dict[str, Any],
        total: Dict[str, Any],
        username: str,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        self.country = country
        self.delta = delta
        self.is_invited = is_invited
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.problem = _ScoreboardEvent_problem(**problem)
        self.total = _ScoreboardEvent_total(**total)
        self.username = username


@dataclasses.dataclass
class _ScoreboardEvent_problem:
    """_ScoreboardEvent_problem"""
    alias: str
    penalty: float
    points: float

    def __init__(
        self,
        *,
        alias: str,
        penalty: float,
        points: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.penalty = penalty
        self.points = points


@dataclasses.dataclass
class _ScoreboardEvent_total:
    """_ScoreboardEvent_total"""
    penalty: float
    points: float

    def __init__(
        self,
        *,
        penalty: float,
        points: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.penalty = penalty
        self.points = points


@dataclasses.dataclass
class _ScoreboardMergePayload:
    """_ScoreboardMergePayload"""
    contests: Sequence['_ContestListItem']

    def __init__(
        self,
        *,
        contests: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = [_ContestListItem(**v) for v in contests]


@dataclasses.dataclass
class _ScoreboardRanking:
    """_ScoreboardRanking"""
    contests: Dict[str, '_ScoreboardRanking_contests_value']
    name: Optional[str]
    total: '_ScoreboardRanking_total'
    username: str

    def __init__(
        self,
        *,
        contests: Dict[str, Dict[str, Any]],
        total: Dict[str, Any],
        username: str,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.contests = {
            k: _ScoreboardRanking_contests_value(**v)
            for k, v in contests.items()
        }
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.total = _ScoreboardRanking_total(**total)
        self.username = username


@dataclasses.dataclass
class _ScoreboardRankingEntry:
    """_ScoreboardRankingEntry"""
    classname: str
    country: str
    is_invited: bool
    name: Optional[str]
    place: Optional[int]
    problems: Sequence['_ScoreboardRankingProblem']
    total: '_ScoreboardRankingEntry_total'
    username: str

    def __init__(
        self,
        *,
        classname: str,
        country: str,
        is_invited: bool,
        problems: Sequence[Dict[str, Any]],
        total: Dict[str, Any],
        username: str,
        name: Optional[str] = None,
        place: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        self.country = country
        self.is_invited = is_invited
        if name is not None:
            self.name = name
        else:
            self.name = None
        if place is not None:
            self.place = place
        else:
            self.place = None
        self.problems = [_ScoreboardRankingProblem(**v) for v in problems]
        self.total = _ScoreboardRankingEntry_total(**total)
        self.username = username


@dataclasses.dataclass
class _ScoreboardRankingEntry_total:
    """_ScoreboardRankingEntry_total"""
    penalty: float
    points: float

    def __init__(
        self,
        *,
        penalty: float,
        points: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.penalty = penalty
        self.points = points


@dataclasses.dataclass
class _ScoreboardRankingProblem:
    """_ScoreboardRankingProblem"""
    alias: str
    penalty: float
    pending: Optional[int]
    percent: float
    place: Optional[int]
    points: float
    run_details: Optional['_ScoreboardRankingProblem_run_details']
    runs: int

    def __init__(
        self,
        *,
        alias: str,
        penalty: float,
        percent: float,
        points: float,
        runs: int,
        pending: Optional[int] = None,
        place: Optional[int] = None,
        run_details: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.penalty = penalty
        if pending is not None:
            self.pending = pending
        else:
            self.pending = None
        self.percent = percent
        if place is not None:
            self.place = place
        else:
            self.place = None
        self.points = points
        if run_details is not None:
            self.run_details = _ScoreboardRankingProblem_run_details(
                **run_details)
        else:
            self.run_details = None
        self.runs = runs


@dataclasses.dataclass
class _ScoreboardRankingProblemDetailsGroup:
    """_ScoreboardRankingProblemDetailsGroup"""
    cases: Sequence['_ScoreboardRankingProblemDetailsGroup_cases_entry']

    def __init__(
        self,
        *,
        cases: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.cases = [
            _ScoreboardRankingProblemDetailsGroup_cases_entry(**v)
            for v in cases
        ]


@dataclasses.dataclass
class _ScoreboardRankingProblemDetailsGroup_cases_entry:
    """_ScoreboardRankingProblemDetailsGroup_cases_entry"""
    meta: '_RunMetadata'

    def __init__(
        self,
        *,
        meta: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.meta = _RunMetadata(**meta)


@dataclasses.dataclass
class _ScoreboardRankingProblem_run_details:
    """_ScoreboardRankingProblem_run_details"""
    cases: Optional[Sequence['_CaseResult']]
    details: '_ScoreboardRankingProblem_run_details_details'

    def __init__(
        self,
        *,
        details: Dict[str, Any],
        cases: Optional[Sequence[Dict[str, Any]]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if cases is not None:
            self.cases = [_CaseResult(**v) for v in cases]
        else:
            self.cases = None
        self.details = _ScoreboardRankingProblem_run_details_details(**details)


@dataclasses.dataclass
class _ScoreboardRankingProblem_run_details_details:
    """_ScoreboardRankingProblem_run_details_details"""
    groups: Sequence['_ScoreboardRankingProblemDetailsGroup']

    def __init__(
        self,
        *,
        groups: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.groups = [
            _ScoreboardRankingProblemDetailsGroup(**v) for v in groups
        ]


@dataclasses.dataclass
class _ScoreboardRanking_contests_value:
    """_ScoreboardRanking_contests_value"""
    penalty: float
    points: float

    def __init__(
        self,
        *,
        penalty: float,
        points: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.penalty = penalty
        self.points = points


@dataclasses.dataclass
class _ScoreboardRanking_total:
    """_ScoreboardRanking_total"""
    penalty: float
    points: float

    def __init__(
        self,
        *,
        penalty: float,
        points: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.penalty = penalty
        self.points = points


@dataclasses.dataclass
class _Scoreboard_problems_entry:
    """_Scoreboard_problems_entry"""
    alias: str
    order: int

    def __init__(
        self,
        *,
        alias: str,
        order: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.order = order


@dataclasses.dataclass
class _SelectedTag:
    """_SelectedTag"""
    public: bool
    tagname: str

    def __init__(
        self,
        *,
        public: bool,
        tagname: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.public = public
        self.tagname = tagname


@dataclasses.dataclass
class _SettingLimits:
    """_SettingLimits"""
    input_limit: str
    memory_limit: str
    overall_wall_time_limit: str
    time_limit: str

    def __init__(
        self,
        *,
        input_limit: str,
        memory_limit: str,
        overall_wall_time_limit: str,
        time_limit: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.input_limit = input_limit
        self.memory_limit = memory_limit
        self.overall_wall_time_limit = overall_wall_time_limit
        self.time_limit = time_limit


@dataclasses.dataclass
class _Signature:
    """_Signature"""
    email: str
    name: str
    time: datetime.datetime

    def __init__(
        self,
        *,
        email: str,
        name: str,
        time: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.email = email
        self.name = name
        self.time = datetime.datetime.fromtimestamp(time)


@dataclasses.dataclass
class _StatsPayload:
    """_StatsPayload"""
    alias: str
    cases_stats: Optional[Dict[str, int]]
    distribution: Optional[Dict[int, int]]
    entity_type: str
    max_wait_time: Optional[datetime.datetime]
    max_wait_time_guid: Optional[str]
    pending_runs: Sequence[str]
    size_of_bucket: Optional[float]
    total_points: Optional[float]
    total_runs: int
    verdict_counts: Dict[str, int]

    def __init__(
        self,
        *,
        alias: str,
        entity_type: str,
        pending_runs: Sequence[str],
        total_runs: int,
        verdict_counts: Dict[str, int],
        cases_stats: Optional[Dict[str, int]] = None,
        distribution: Optional[Dict[int, int]] = None,
        max_wait_time: Optional[int] = None,
        max_wait_time_guid: Optional[str] = None,
        size_of_bucket: Optional[float] = None,
        total_points: Optional[float] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        if cases_stats is not None:
            self.cases_stats = {k: v for k, v in cases_stats.items()}
        else:
            self.cases_stats = None
        if distribution is not None:
            self.distribution = {k: v for k, v in distribution.items()}
        else:
            self.distribution = None
        self.entity_type = entity_type
        if max_wait_time is not None:
            self.max_wait_time = datetime.datetime.fromtimestamp(max_wait_time)
        else:
            self.max_wait_time = None
        if max_wait_time_guid is not None:
            self.max_wait_time_guid = max_wait_time_guid
        else:
            self.max_wait_time_guid = None
        self.pending_runs = [v for v in pending_runs]
        if size_of_bucket is not None:
            self.size_of_bucket = size_of_bucket
        else:
            self.size_of_bucket = None
        if total_points is not None:
            self.total_points = total_points
        else:
            self.total_points = None
        self.total_runs = total_runs
        self.verdict_counts = {k: v for k, v in verdict_counts.items()}


@dataclasses.dataclass
class _StudentProgress:
    """_StudentProgress"""
    classname: str
    country_id: Optional[str]
    name: Optional[str]
    points: Dict[str, Dict[str, float]]
    progress: Dict[str, Dict[str, float]]
    score: Dict[str, Dict[str, float]]
    username: str

    def __init__(
        self,
        *,
        classname: str,
        points: Dict[str, Dict[str, float]],
        progress: Dict[str, Dict[str, float]],
        score: Dict[str, Dict[str, float]],
        username: str,
        country_id: Optional[str] = None,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.points = {
            k: {k: v
                for k, v in v.items()}
            for k, v in points.items()
        }
        self.progress = {
            k: {k: v
                for k, v in v.items()}
            for k, v in progress.items()
        }
        self.score = {
            k: {k: v
                for k, v in v.items()}
            for k, v in score.items()
        }
        self.username = username


@dataclasses.dataclass
class _StudentProgressByAssignmentPayload:
    """_StudentProgressByAssignmentPayload"""
    assignment: str
    course: '_CourseDetails'
    problems: Sequence['_CourseProblem']
    student: str
    students: Sequence['_StudentProgress']

    def __init__(
        self,
        *,
        assignment: str,
        course: Dict[str, Any],
        problems: Sequence[Dict[str, Any]],
        student: str,
        students: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.assignment = assignment
        self.course = _CourseDetails(**course)
        self.problems = [_CourseProblem(**v) for v in problems]
        self.student = student
        self.students = [_StudentProgress(**v) for v in students]


@dataclasses.dataclass
class _StudentProgressInCourse:
    """_StudentProgressInCourse"""
    assignments: Dict[str, '_StudentProgressInCourse_assignments_value']
    classname: str
    country_id: Optional[str]
    courseProgress: float
    courseScore: float
    name: Optional[str]
    username: str

    def __init__(
        self,
        *,
        assignments: Dict[str, Dict[str, Any]],
        classname: str,
        courseProgress: float,
        courseScore: float,
        username: str,
        country_id: Optional[str] = None,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.assignments = {
            k: _StudentProgressInCourse_assignments_value(**v)
            for k, v in assignments.items()
        }
        self.classname = classname
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        self.courseProgress = courseProgress
        self.courseScore = courseScore
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.username = username


@dataclasses.dataclass
class _StudentProgressInCourse_assignments_value:
    """_StudentProgressInCourse_assignments_value"""
    problems: Dict[str,
                   '_StudentProgressInCourse_assignments_value_problems_value']
    progress: float
    score: float

    def __init__(
        self,
        *,
        problems: Dict[str, Dict[str, Any]],
        progress: float,
        score: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.problems = {
            k: _StudentProgressInCourse_assignments_value_problems_value(**v)
            for k, v in problems.items()
        }
        self.progress = progress
        self.score = score


@dataclasses.dataclass
class _StudentProgressInCourse_assignments_value_problems_value:
    """_StudentProgressInCourse_assignments_value_problems_value"""
    progress: float
    score: float

    def __init__(
        self,
        *,
        progress: float,
        score: float,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.progress = progress
        self.score = score


@dataclasses.dataclass
class _StudentProgressPayload:
    """_StudentProgressPayload"""
    course: '_CourseDetails'
    student: str
    students: Sequence['_StudentProgress']

    def __init__(
        self,
        *,
        course: Dict[str, Any],
        student: str,
        students: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.course = _CourseDetails(**course)
        self.student = student
        self.students = [_StudentProgress(**v) for v in students]


@dataclasses.dataclass
class _StudentsProgressPayload:
    """_StudentsProgressPayload"""
    assignmentsProblems: Sequence['_AssignmentsProblemsPoints']
    course: '_CourseDetails'
    length: int
    page: int
    pagerItems: Sequence['_PageItem']
    students: Sequence['_StudentProgressInCourse']
    totalRows: int

    def __init__(
        self,
        *,
        assignmentsProblems: Sequence[Dict[str, Any]],
        course: Dict[str, Any],
        length: int,
        page: int,
        pagerItems: Sequence[Dict[str, Any]],
        students: Sequence[Dict[str, Any]],
        totalRows: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.assignmentsProblems = [
            _AssignmentsProblemsPoints(**v) for v in assignmentsProblems
        ]
        self.course = _CourseDetails(**course)
        self.length = length
        self.page = page
        self.pagerItems = [_PageItem(**v) for v in pagerItems]
        self.students = [_StudentProgressInCourse(**v) for v in students]
        self.totalRows = totalRows


@dataclasses.dataclass
class _Submission:
    """_Submission"""
    alias: str
    language: str
    memory: int
    runtime: int
    school_id: Optional[int]
    school_name: Optional[str]
    time: datetime.datetime
    title: str
    username: str
    verdict: str

    def __init__(
        self,
        *,
        alias: str,
        language: str,
        memory: int,
        runtime: int,
        time: int,
        title: str,
        username: str,
        verdict: str,
        school_id: Optional[int] = None,
        school_name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.language = language
        self.memory = memory
        self.runtime = runtime
        if school_id is not None:
            self.school_id = school_id
        else:
            self.school_id = None
        if school_name is not None:
            self.school_name = school_name
        else:
            self.school_name = None
        self.time = datetime.datetime.fromtimestamp(time)
        self.title = title
        self.username = username
        self.verdict = verdict


@dataclasses.dataclass
class _SubmissionFeedback:
    """_SubmissionFeedback"""
    author: str
    author_classname: str
    date: datetime.datetime
    feedback: str

    def __init__(
        self,
        *,
        author: str,
        author_classname: str,
        date: int,
        feedback: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.author = author
        self.author_classname = author_classname
        self.date = datetime.datetime.fromtimestamp(date)
        self.feedback = feedback


@dataclasses.dataclass
class _SubmissionsListPayload:
    """_SubmissionsListPayload"""
    includeUser: bool
    submissions: Sequence['_Submission']

    def __init__(
        self,
        *,
        includeUser: bool,
        submissions: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.includeUser = includeUser
        self.submissions = [_Submission(**v) for v in submissions]


@dataclasses.dataclass
class _Tag:
    """_Tag"""
    name: str

    def __init__(
        self,
        *,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name


@dataclasses.dataclass
class _TagWithProblemCount:
    """_TagWithProblemCount"""
    name: str
    problemCount: int

    def __init__(
        self,
        *,
        name: str,
        problemCount: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.problemCount = problemCount


@dataclasses.dataclass
class _TeamGroupEditPayload:
    """_TeamGroupEditPayload"""
    countries: Sequence['_OmegaUp_DAO_VO_Countries']
    identities: Sequence['_Identity']
    isOrganizer: bool
    maxNumberOfContestants: int
    teamGroup: '_TeamGroupEditPayload_teamGroup'
    teamsMembers: Sequence['_TeamMember']

    def __init__(
        self,
        *,
        countries: Sequence[Dict[str, Any]],
        identities: Sequence[Dict[str, Any]],
        isOrganizer: bool,
        maxNumberOfContestants: int,
        teamGroup: Dict[str, Any],
        teamsMembers: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.countries = [_OmegaUp_DAO_VO_Countries(**v) for v in countries]
        self.identities = [_Identity(**v) for v in identities]
        self.isOrganizer = isOrganizer
        self.maxNumberOfContestants = maxNumberOfContestants
        self.teamGroup = _TeamGroupEditPayload_teamGroup(**teamGroup)
        self.teamsMembers = [_TeamMember(**v) for v in teamsMembers]


@dataclasses.dataclass
class _TeamGroupEditPayload_teamGroup:
    """_TeamGroupEditPayload_teamGroup"""
    alias: str
    description: Optional[str]
    name: Optional[str]
    numberOfContestants: int

    def __init__(
        self,
        *,
        alias: str,
        numberOfContestants: int,
        description: Optional[str] = None,
        name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        if description is not None:
            self.description = description
        else:
            self.description = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.numberOfContestants = numberOfContestants


@dataclasses.dataclass
class _TeamGroupNewPayload:
    """_TeamGroupNewPayload"""
    maxNumberOfContestants: int
    numberOfContestants: int

    def __init__(
        self,
        *,
        maxNumberOfContestants: int,
        numberOfContestants: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.maxNumberOfContestants = maxNumberOfContestants
        self.numberOfContestants = numberOfContestants


@dataclasses.dataclass
class _TeamMember:
    """_TeamMember"""
    classname: str
    isMainUserIdentity: bool
    name: Optional[str]
    team_alias: str
    team_name: Optional[str]
    username: str

    def __init__(
        self,
        *,
        classname: str,
        isMainUserIdentity: bool,
        team_alias: str,
        username: str,
        name: Optional[str] = None,
        team_name: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        self.isMainUserIdentity = isMainUserIdentity
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.team_alias = team_alias
        if team_name is not None:
            self.team_name = team_name
        else:
            self.team_name = None
        self.username = username


@dataclasses.dataclass
class _TeamsGroup:
    """_TeamsGroup"""
    alias: str
    create_time: datetime.datetime
    description: Optional[str]
    name: str

    def __init__(
        self,
        *,
        alias: str,
        create_time: int,
        name: str,
        description: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.alias = alias
        self.create_time = datetime.datetime.fromtimestamp(create_time)
        if description is not None:
            self.description = description
        else:
            self.description = None
        self.name = name


@dataclasses.dataclass
class _TeamsGroupListPayload:
    """_TeamsGroupListPayload"""
    teamsGroups: Sequence['_TeamsGroup']

    def __init__(
        self,
        *,
        teamsGroups: Sequence[Dict[str, Any]],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.teamsGroups = [_TeamsGroup(**v) for v in teamsGroups]


@dataclasses.dataclass
class _UserDetailsPayload:
    """_UserDetailsPayload"""
    emails: Sequence[str]
    experiments: Sequence[str]
    roleNames: Sequence['_UserRole']
    systemExperiments: Sequence['_Experiment']
    systemRoles: Sequence[str]
    username: str
    verified: bool

    def __init__(
        self,
        *,
        emails: Sequence[str],
        experiments: Sequence[str],
        roleNames: Sequence[Dict[str, Any]],
        systemExperiments: Sequence[Dict[str, Any]],
        systemRoles: Sequence[str],
        username: str,
        verified: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.emails = [v for v in emails]
        self.experiments = [v for v in experiments]
        self.roleNames = [_UserRole(**v) for v in roleNames]
        self.systemExperiments = [_Experiment(**v) for v in systemExperiments]
        self.systemRoles = [v for v in systemRoles]
        self.username = username
        self.verified = verified


@dataclasses.dataclass
class _UserInfoForProblem:
    """_UserInfoForProblem"""
    admin: bool
    loggedIn: bool
    reviewer: bool

    def __init__(
        self,
        *,
        admin: bool,
        loggedIn: bool,
        reviewer: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.admin = admin
        self.loggedIn = loggedIn
        self.reviewer = reviewer


@dataclasses.dataclass
class _UserProfile:
    """_UserProfile"""
    birth_date: Optional[datetime.datetime]
    classname: str
    country: str
    country_id: Optional[str]
    email: Optional[str]
    gender: Optional[str]
    graduation_date: Optional[datetime.datetime]
    gravatar_92: str
    has_competitive_objective: Optional[bool]
    has_learning_objective: Optional[bool]
    has_scholar_objective: Optional[bool]
    has_teaching_objective: Optional[bool]
    hide_problem_tags: bool
    is_own_profile: bool
    is_private: bool
    locale: str
    name: Optional[str]
    preferred_language: Optional[str]
    scholar_degree: Optional[str]
    school: Optional[str]
    school_id: Optional[int]
    state: Optional[str]
    state_id: Optional[str]
    username: Optional[str]
    verified: bool

    def __init__(
        self,
        *,
        classname: str,
        country: str,
        gravatar_92: str,
        hide_problem_tags: bool,
        is_own_profile: bool,
        is_private: bool,
        locale: str,
        verified: bool,
        birth_date: Optional[int] = None,
        country_id: Optional[str] = None,
        email: Optional[str] = None,
        gender: Optional[str] = None,
        graduation_date: Optional[int] = None,
        has_competitive_objective: Optional[bool] = None,
        has_learning_objective: Optional[bool] = None,
        has_scholar_objective: Optional[bool] = None,
        has_teaching_objective: Optional[bool] = None,
        name: Optional[str] = None,
        preferred_language: Optional[str] = None,
        scholar_degree: Optional[str] = None,
        school: Optional[str] = None,
        school_id: Optional[int] = None,
        state: Optional[str] = None,
        state_id: Optional[str] = None,
        username: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if birth_date is not None:
            self.birth_date = datetime.datetime.fromtimestamp(birth_date)
        else:
            self.birth_date = None
        self.classname = classname
        self.country = country
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        if email is not None:
            self.email = email
        else:
            self.email = None
        if gender is not None:
            self.gender = gender
        else:
            self.gender = None
        if graduation_date is not None:
            self.graduation_date = datetime.datetime.fromtimestamp(
                graduation_date)
        else:
            self.graduation_date = None
        self.gravatar_92 = gravatar_92
        if has_competitive_objective is not None:
            self.has_competitive_objective = has_competitive_objective
        else:
            self.has_competitive_objective = None
        if has_learning_objective is not None:
            self.has_learning_objective = has_learning_objective
        else:
            self.has_learning_objective = None
        if has_scholar_objective is not None:
            self.has_scholar_objective = has_scholar_objective
        else:
            self.has_scholar_objective = None
        if has_teaching_objective is not None:
            self.has_teaching_objective = has_teaching_objective
        else:
            self.has_teaching_objective = None
        self.hide_problem_tags = hide_problem_tags
        self.is_own_profile = is_own_profile
        self.is_private = is_private
        self.locale = locale
        if name is not None:
            self.name = name
        else:
            self.name = None
        if preferred_language is not None:
            self.preferred_language = preferred_language
        else:
            self.preferred_language = None
        if scholar_degree is not None:
            self.scholar_degree = scholar_degree
        else:
            self.scholar_degree = None
        if school is not None:
            self.school = school
        else:
            self.school = None
        if school_id is not None:
            self.school_id = school_id
        else:
            self.school_id = None
        if state is not None:
            self.state = state
        else:
            self.state = None
        if state_id is not None:
            self.state_id = state_id
        else:
            self.state_id = None
        if username is not None:
            self.username = username
        else:
            self.username = None
        self.verified = verified


@dataclasses.dataclass
class _UserProfileContests_value:
    """_UserProfileContests_value"""
    data: '_ContestParticipated'
    place: int

    def __init__(
        self,
        *,
        data: Dict[str, Any],
        place: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.data = _ContestParticipated(**data)
        self.place = place


@dataclasses.dataclass
class _UserProfileDetailsPayload:
    """_UserProfileDetailsPayload"""
    countries: Sequence['_OmegaUp_DAO_VO_Countries']
    extraProfileDetails: Optional['_ExtraProfileDetails']
    identities: Sequence['_AssociatedIdentity']
    profile: '_UserProfileInfo'
    programmingLanguages: Dict[str, str]

    def __init__(
        self,
        *,
        countries: Sequence[Dict[str, Any]],
        identities: Sequence[Dict[str, Any]],
        profile: Dict[str, Any],
        programmingLanguages: Dict[str, str],
        extraProfileDetails: Optional[Dict[str, Any]] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.countries = [_OmegaUp_DAO_VO_Countries(**v) for v in countries]
        if extraProfileDetails is not None:
            self.extraProfileDetails = _ExtraProfileDetails(
                **extraProfileDetails)
        else:
            self.extraProfileDetails = None
        self.identities = [_AssociatedIdentity(**v) for v in identities]
        self.profile = _UserProfileInfo(**profile)
        self.programmingLanguages = {
            k: v
            for k, v in programmingLanguages.items()
        }


@dataclasses.dataclass
class _UserProfileInfo:
    """_UserProfileInfo"""
    birth_date: Optional[datetime.datetime]
    classname: str
    country: Optional[str]
    country_id: Optional[str]
    email: Optional[str]
    gender: Optional[str]
    graduation_date: Optional[datetime.datetime]
    gravatar_92: Optional[str]
    has_competitive_objective: Optional[bool]
    has_learning_objective: Optional[bool]
    has_scholar_objective: Optional[bool]
    has_teaching_objective: Optional[bool]
    hide_problem_tags: bool
    is_own_profile: bool
    is_private: bool
    locale: Optional[str]
    name: Optional[str]
    preferred_language: Optional[str]
    programming_languages: Dict[str, str]
    rankinfo: '_UserProfileInfo_rankinfo'
    scholar_degree: Optional[str]
    school: Optional[str]
    school_id: Optional[int]
    state: Optional[str]
    state_id: Optional[str]
    username: Optional[str]
    verified: Optional[bool]

    def __init__(
        self,
        *,
        classname: str,
        hide_problem_tags: bool,
        is_own_profile: bool,
        is_private: bool,
        programming_languages: Dict[str, str],
        rankinfo: Dict[str, Any],
        birth_date: Optional[int] = None,
        country: Optional[str] = None,
        country_id: Optional[str] = None,
        email: Optional[str] = None,
        gender: Optional[str] = None,
        graduation_date: Optional[int] = None,
        gravatar_92: Optional[str] = None,
        has_competitive_objective: Optional[bool] = None,
        has_learning_objective: Optional[bool] = None,
        has_scholar_objective: Optional[bool] = None,
        has_teaching_objective: Optional[bool] = None,
        locale: Optional[str] = None,
        name: Optional[str] = None,
        preferred_language: Optional[str] = None,
        scholar_degree: Optional[str] = None,
        school: Optional[str] = None,
        school_id: Optional[int] = None,
        state: Optional[str] = None,
        state_id: Optional[str] = None,
        username: Optional[str] = None,
        verified: Optional[bool] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if birth_date is not None:
            self.birth_date = datetime.datetime.fromtimestamp(birth_date)
        else:
            self.birth_date = None
        self.classname = classname
        if country is not None:
            self.country = country
        else:
            self.country = None
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        if email is not None:
            self.email = email
        else:
            self.email = None
        if gender is not None:
            self.gender = gender
        else:
            self.gender = None
        if graduation_date is not None:
            self.graduation_date = datetime.datetime.fromtimestamp(
                graduation_date)
        else:
            self.graduation_date = None
        if gravatar_92 is not None:
            self.gravatar_92 = gravatar_92
        else:
            self.gravatar_92 = None
        if has_competitive_objective is not None:
            self.has_competitive_objective = has_competitive_objective
        else:
            self.has_competitive_objective = None
        if has_learning_objective is not None:
            self.has_learning_objective = has_learning_objective
        else:
            self.has_learning_objective = None
        if has_scholar_objective is not None:
            self.has_scholar_objective = has_scholar_objective
        else:
            self.has_scholar_objective = None
        if has_teaching_objective is not None:
            self.has_teaching_objective = has_teaching_objective
        else:
            self.has_teaching_objective = None
        self.hide_problem_tags = hide_problem_tags
        self.is_own_profile = is_own_profile
        self.is_private = is_private
        if locale is not None:
            self.locale = locale
        else:
            self.locale = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        if preferred_language is not None:
            self.preferred_language = preferred_language
        else:
            self.preferred_language = None
        self.programming_languages = {
            k: v
            for k, v in programming_languages.items()
        }
        self.rankinfo = _UserProfileInfo_rankinfo(**rankinfo)
        if scholar_degree is not None:
            self.scholar_degree = scholar_degree
        else:
            self.scholar_degree = None
        if school is not None:
            self.school = school
        else:
            self.school = None
        if school_id is not None:
            self.school_id = school_id
        else:
            self.school_id = None
        if state is not None:
            self.state = state
        else:
            self.state = None
        if state_id is not None:
            self.state_id = state_id
        else:
            self.state_id = None
        if username is not None:
            self.username = username
        else:
            self.username = None
        if verified is not None:
            self.verified = verified
        else:
            self.verified = None


@dataclasses.dataclass
class _UserProfileInfo_rankinfo:
    """_UserProfileInfo_rankinfo"""
    author_ranking: Optional[int]
    name: Optional[str]
    problems_solved: Optional[int]
    rank: Optional[int]

    def __init__(
        self,
        *,
        author_ranking: Optional[int] = None,
        name: Optional[str] = None,
        problems_solved: Optional[int] = None,
        rank: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if author_ranking is not None:
            self.author_ranking = author_ranking
        else:
            self.author_ranking = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        if problems_solved is not None:
            self.problems_solved = problems_solved
        else:
            self.problems_solved = None
        if rank is not None:
            self.rank = rank
        else:
            self.rank = None


@dataclasses.dataclass
class _UserProfileStats:
    """_UserProfileStats"""
    date: Optional[str]
    runs: int
    verdict: str

    def __init__(
        self,
        *,
        runs: int,
        verdict: str,
        date: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if date is not None:
            self.date = date
        else:
            self.date = None
        self.runs = runs
        self.verdict = verdict


@dataclasses.dataclass
class _UserRank:
    """_UserRank"""
    rank: Sequence['_UserRank_rank_entry']
    total: int

    def __init__(
        self,
        *,
        rank: Sequence[Dict[str, Any]],
        total: int,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.rank = [_UserRank_rank_entry(**v) for v in rank]
        self.total = total


@dataclasses.dataclass
class _UserRankInfo:
    """_UserRankInfo"""
    author_ranking: Optional[int]
    name: str
    problems_solved: int
    rank: int

    def __init__(
        self,
        *,
        name: str,
        problems_solved: int,
        rank: int,
        author_ranking: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if author_ranking is not None:
            self.author_ranking = author_ranking
        else:
            self.author_ranking = None
        self.name = name
        self.problems_solved = problems_solved
        self.rank = rank


@dataclasses.dataclass
class _UserRankTablePayload:
    """_UserRankTablePayload"""
    availableFilters: '_UserRankTablePayload_availableFilters'
    filter: str
    isIndex: bool
    isLogged: bool
    length: int
    page: int
    pagerItems: Sequence['_PageItem']
    ranking: '_UserRank'

    def __init__(
        self,
        *,
        availableFilters: Dict[str, Any],
        filter: str,
        isIndex: bool,
        isLogged: bool,
        length: int,
        page: int,
        pagerItems: Sequence[Dict[str, Any]],
        ranking: Dict[str, Any],
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.availableFilters = _UserRankTablePayload_availableFilters(
            **availableFilters)
        self.filter = filter
        self.isIndex = isIndex
        self.isLogged = isLogged
        self.length = length
        self.page = page
        self.pagerItems = [_PageItem(**v) for v in pagerItems]
        self.ranking = _UserRank(**ranking)


@dataclasses.dataclass
class _UserRankTablePayload_availableFilters:
    """_UserRankTablePayload_availableFilters"""
    country: Optional[str]
    school: Optional[str]
    state: Optional[str]

    def __init__(
        self,
        *,
        country: Optional[str] = None,
        school: Optional[str] = None,
        state: Optional[str] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        if country is not None:
            self.country = country
        else:
            self.country = None
        if school is not None:
            self.school = school
        else:
            self.school = None
        if state is not None:
            self.state = state
        else:
            self.state = None


@dataclasses.dataclass
class _UserRank_rank_entry:
    """_UserRank_rank_entry"""
    classname: str
    country_id: Optional[str]
    name: Optional[str]
    problems_solved: int
    ranking: Optional[int]
    score: float
    user_id: int
    username: str

    def __init__(
        self,
        *,
        classname: str,
        problems_solved: int,
        score: float,
        user_id: int,
        username: str,
        country_id: Optional[str] = None,
        name: Optional[str] = None,
        ranking: Optional[int] = None,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.classname = classname
        if country_id is not None:
            self.country_id = country_id
        else:
            self.country_id = None
        if name is not None:
            self.name = name
        else:
            self.name = None
        self.problems_solved = problems_solved
        if ranking is not None:
            self.ranking = ranking
        else:
            self.ranking = None
        self.score = score
        self.user_id = user_id
        self.username = username


@dataclasses.dataclass
class _UserRole:
    """_UserRole"""
    name: str

    def __init__(
        self,
        *,
        name: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name


@dataclasses.dataclass
class _UserRolesPayload:
    """_UserRolesPayload"""
    userSystemGroups: Dict[int, '_UserRolesPayload_userSystemGroups_value']
    userSystemRoles: Dict[int, '_UserRolesPayload_userSystemRoles_value']
    username: str

    def __init__(
        self,
        *,
        userSystemGroups: Dict[int, Dict[str, Any]],
        userSystemRoles: Dict[int, Dict[str, Any]],
        username: str,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.userSystemGroups = {
            k: _UserRolesPayload_userSystemGroups_value(**v)
            for k, v in userSystemGroups.items()
        }
        self.userSystemRoles = {
            k: _UserRolesPayload_userSystemRoles_value(**v)
            for k, v in userSystemRoles.items()
        }
        self.username = username


@dataclasses.dataclass
class _UserRolesPayload_userSystemGroups_value:
    """_UserRolesPayload_userSystemGroups_value"""
    name: str
    value: bool

    def __init__(
        self,
        *,
        name: str,
        value: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.value = value


@dataclasses.dataclass
class _UserRolesPayload_userSystemRoles_value:
    """_UserRolesPayload_userSystemRoles_value"""
    name: str
    value: bool

    def __init__(
        self,
        *,
        name: str,
        value: bool,
        # Ignore any unknown arguments
        **_kwargs: Any,
    ):
        self.name = name
        self.value = value


AdminPlatformReportStatsResponse = _OmegaUp_Controllers_Admin__apiPlatformReportStats
"""The return type of the AdminPlatformReportStats API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> AdminPlatformReportStatsResponse:
        r"""Get stats for an overall platform report.

        Args:
            end_time:
            start_time:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if end_time is not None:
            parameters['end_time'] = str(end_time)
        if start_time is not None:
            parameters['start_time'] = str(start_time)
        return _OmegaUp_Controllers_Admin__apiPlatformReportStats(
            **self._client.query('/api/admin/platformReportStats/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


AuthorizationProblemResponse = _OmegaUp_Controllers_Authorization__apiProblem
"""The return type of the AuthorizationProblem API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> AuthorizationProblemResponse:
        r"""

        Args:
            problem_alias:
            token:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
            'token': token,
        }
        if username is not None:
            parameters['username'] = str(username)
        return _OmegaUp_Controllers_Authorization__apiProblem(
            **self._client.query('/api/authorization/problem/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


BadgeListResponse = Sequence[str]
"""The return type of the BadgeList API."""

BadgeMyListResponse = _OmegaUp_Controllers_Badge__apiMyList
"""The return type of the BadgeMyList API."""

BadgeUserListResponse = _OmegaUp_Controllers_Badge__apiUserList
"""The return type of the BadgeUserList API."""

BadgeMyBadgeAssignationTimeResponse = _OmegaUp_Controllers_Badge__apiMyBadgeAssignationTime
"""The return type of the BadgeMyBadgeAssignationTime API."""

BadgeBadgeDetailsResponse = _Badge
"""The return type of the BadgeBadgeDetails API."""


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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> BadgeListResponse:
        r"""Returns a list of existing badges

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return [
            v for v in self._client.query('/api/badge/list/',
                                          payload=parameters,
                                          files_=files_,
                                          timeout_=timeout_,
                                          check_=check_)
        ]

    def myList(
        self,
        *,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> BadgeMyListResponse:
        r"""Returns a list of badges owned by current user

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_Badge__apiMyList(
            **self._client.query('/api/badge/myList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def userList(
        self,
        *,
        target_username: Optional[Any] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> BadgeUserListResponse:
        r"""Returns a list of badges owned by a certain user

        Args:
            target_username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if target_username is not None:
            parameters['target_username'] = str(target_username)
        return _OmegaUp_Controllers_Badge__apiUserList(
            **self._client.query('/api/badge/userList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def myBadgeAssignationTime(
        self,
        *,
        badge_alias: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> BadgeMyBadgeAssignationTimeResponse:
        r"""Returns a the assignation timestamp of a badge
        for current user.

        Args:
            badge_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if badge_alias is not None:
            parameters['badge_alias'] = badge_alias
        return _OmegaUp_Controllers_Badge__apiMyBadgeAssignationTime(
            **self._client.query('/api/badge/myBadgeAssignationTime/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def badgeDetails(
        self,
        *,
        badge_alias: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> BadgeBadgeDetailsResponse:
        r"""Returns the number of owners and the first
        assignation timestamp for a certain badge

        Args:
            badge_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if badge_alias is not None:
            parameters['badge_alias'] = badge_alias
        return _Badge(**self._client.query('/api/badge/badgeDetails/',
                                           payload=parameters,
                                           files_=files_,
                                           timeout_=timeout_,
                                           check_=check_))


ClarificationCreateResponse = _Clarification
"""The return type of the ClarificationCreate API."""

ClarificationDetailsResponse = _OmegaUp_Controllers_Clarification__apiDetails
"""The return type of the ClarificationDetails API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ClarificationCreateResponse:
        r"""Creates a Clarification for a contest or an assignment of a course

        Args:
            message:
            problem_alias:
            assignment_alias:
            contest_alias:
            course_alias:
            username:

        Returns:
            The API result object.
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
        return _Clarification(
            **self._client.query('/api/clarification/create/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def details(
        self,
        *,
        clarification_id: int,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ClarificationDetailsResponse:
        r"""API for getting a clarification

        Args:
            clarification_id:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'clarification_id': str(clarification_id),
        }
        return _OmegaUp_Controllers_Clarification__apiDetails(
            **self._client.query('/api/clarification/details/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Update a clarification

        Args:
            clarification_id:
            answer:
            message:
            public:

        Returns:
            The API result object.
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
        self._client.query('/api/clarification/update/',
                           payload=parameters,
                           files_=files_,
                           timeout_=timeout_,
                           check_=check_)


ContestListResponse = _OmegaUp_Controllers_Contest__apiList
"""The return type of the ContestList API."""

ContestAdminListResponse = _OmegaUp_Controllers_Contest__apiAdminList
"""The return type of the ContestAdminList API."""

ContestMyListResponse = _OmegaUp_Controllers_Contest__apiMyList
"""The return type of the ContestMyList API."""

ContestListParticipatingResponse = _OmegaUp_Controllers_Contest__apiListParticipating
"""The return type of the ContestListParticipating API."""

ContestPublicDetailsResponse = _ContestPublicDetails
"""The return type of the ContestPublicDetails API."""

ContestDetailsResponse = _ContestDetails
"""The return type of the ContestDetails API."""

ContestAdminDetailsResponse = _ContestAdminDetails
"""The return type of the ContestAdminDetails API."""

ContestActivityReportResponse = _OmegaUp_Controllers_Contest__apiActivityReport
"""The return type of the ContestActivityReport API."""

ContestCloneResponse = _OmegaUp_Controllers_Contest__apiClone
"""The return type of the ContestClone API."""

ContestCreateVirtualResponse = _OmegaUp_Controllers_Contest__apiCreateVirtual
"""The return type of the ContestCreateVirtual API."""

ContestProblemsResponse = _OmegaUp_Controllers_Contest__apiProblems
"""The return type of the ContestProblems API."""

ContestRunsDiffResponse = _OmegaUp_Controllers_Contest__apiRunsDiff
"""The return type of the ContestRunsDiff API."""

ContestClarificationsResponse = _OmegaUp_Controllers_Contest__apiClarifications
"""The return type of the ContestClarifications API."""

ContestProblemClarificationsResponse = _OmegaUp_Controllers_Contest__apiProblemClarifications
"""The return type of the ContestProblemClarifications API."""

ContestScoreboardEventsResponse = _OmegaUp_Controllers_Contest__apiScoreboardEvents
"""The return type of the ContestScoreboardEvents API."""

ContestScoreboardResponse = _Scoreboard
"""The return type of the ContestScoreboard API."""

ContestScoreboardMergeResponse = _OmegaUp_Controllers_Contest__apiScoreboardMerge
"""The return type of the ContestScoreboardMerge API."""

ContestRequestsResponse = _OmegaUp_Controllers_Contest__apiRequests
"""The return type of the ContestRequests API."""

ContestUsersResponse = _OmegaUp_Controllers_Contest__apiUsers
"""The return type of the ContestUsers API."""

ContestSearchUsersResponse = _OmegaUp_Controllers_Contest__apiSearchUsers
"""The return type of the ContestSearchUsers API."""

ContestAdminsResponse = _OmegaUp_Controllers_Contest__apiAdmins
"""The return type of the ContestAdmins API."""

ContestUpdateResponse = _OmegaUp_Controllers_Contest__apiUpdate
"""The return type of the ContestUpdate API."""

ContestRunsResponse = _OmegaUp_Controllers_Contest__apiRuns
"""The return type of the ContestRuns API."""

ContestStatsResponse = _OmegaUp_Controllers_Contest__apiStats
"""The return type of the ContestStats API."""

ContestReportResponse = _OmegaUp_Controllers_Contest__apiReport
"""The return type of the ContestReport API."""

ContestRoleResponse = _OmegaUp_Controllers_Contest__apiRole
"""The return type of the ContestRole API."""

ContestContestantsResponse = _OmegaUp_Controllers_Contest__apiContestants
"""The return type of the ContestContestants API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestListResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_Contest__apiList(
            **self._client.query('/api/contest/list/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def adminList(
        self,
        *,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        show_archived: Optional[bool] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestAdminListResponse:
        r"""Returns a list of contests where current user has admin rights (or is
        the director).

        Args:
            page:
            page_size:
            show_archived:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if page is not None:
            parameters['page'] = str(page)
        if page_size is not None:
            parameters['page_size'] = str(page_size)
        if show_archived is not None:
            parameters['show_archived'] = str(show_archived)
        return _OmegaUp_Controllers_Contest__apiAdminList(
            **self._client.query('/api/contest/adminList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestMyListResponse:
        r"""Returns a list of contests where current user is the director

        Args:
            page:
            page_size:
            query:
            show_archived:

        Returns:
            The API result object.
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
        return _OmegaUp_Controllers_Contest__apiMyList(
            **self._client.query('/api/contest/myList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestListParticipatingResponse:
        r"""Returns a list of contests where current user is participating in

        Args:
            page:
            page_size:
            query:
            show_archived:

        Returns:
            The API result object.
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
        return _OmegaUp_Controllers_Contest__apiListParticipating(
            **self._client.query('/api/contest/listParticipating/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def publicDetails(
        self,
        *,
        contest_alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestPublicDetailsResponse:
        r"""

        Args:
            contest_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return _ContestPublicDetails(
            **self._client.query('/api/contest/publicDetails/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def registerForContest(
            self,
            *,
            contest_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""

        Args:
            contest_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        self._client.query('/api/contest/registerForContest/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Joins a contest - explicitly adds a identity to a contest.

        Args:
            contest_alias:
            privacy_git_object_id:
            statement_type:
            share_user_information:
            token:

        Returns:
            The API result object.
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
        self._client.query('/api/contest/open/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestDetailsResponse:
        r"""Returns details of a Contest. Requesting the details of a contest will
        not start the current user into that contest. In order to participate
        in the contest, \OmegaUp\Controllers\Contest::apiOpen() must be used.

        Args:
            contest_alias:
            token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if token is not None:
            parameters['token'] = token
        return _ContestDetails(**self._client.query('/api/contest/details/',
                                                    payload=parameters,
                                                    files_=files_,
                                                    timeout_=timeout_,
                                                    check_=check_))

    def adminDetails(
        self,
        *,
        contest_alias: str,
        token: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestAdminDetailsResponse:
        r"""Returns details of a Contest, for administrators. This differs from
        apiDetails in the sense that it does not attempt to calculate the
        remaining time from the contest, or register the opened time.

        Args:
            contest_alias:
            token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if token is not None:
            parameters['token'] = token
        return _ContestAdminDetails(
            **self._client.query('/api/contest/adminDetails/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestActivityReportResponse:
        r"""Returns a report with all user activity for a contest.

        Args:
            contest_alias:
            length:
            page:
            token:

        Returns:
            The API result object.
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
        return _OmegaUp_Controllers_Contest__apiActivityReport(
            **self._client.query('/api/contest/activityReport/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestCloneResponse:
        r"""Clone a contest

        Args:
            contest_alias:
            description:
            start_time:
            title:
            alias:
            auth_token:

        Returns:
            The API result object.
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
        return _OmegaUp_Controllers_Contest__apiClone(
            **self._client.query('/api/contest/clone/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def createVirtual(
        self,
        *,
        alias: str,
        start_time: int,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestCreateVirtualResponse:
        r"""

        Args:
            alias:
            start_time:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'start_time': str(start_time),
        }
        return _OmegaUp_Controllers_Contest__apiCreateVirtual(
            **self._client.query('/api/contest/createVirtual/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/contest/create/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestProblemsResponse:
        r"""Gets the problems from a contest

        Args:
            contest_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return _OmegaUp_Controllers_Contest__apiProblems(
            **self._client.query('/api/contest/problems/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds a problem to a contest

        Args:
            contest_alias:
            order_in_contest:
            points:
            problem_alias:
            commit:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'order_in_contest': str(order_in_contest),
            'points': str(points),
            'problem_alias': problem_alias,
        }
        if commit is not None:
            parameters['commit'] = commit
        self._client.query('/api/contest/addProblem/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes a problem from a contest

        Args:
            contest_alias:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'problem_alias': problem_alias,
        }
        self._client.query('/api/contest/removeProblem/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestRunsDiffResponse:
        r"""Return a report of which runs would change due to a version change.

        Args:
            contest_alias:
            version:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'version': version,
        }
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        return _OmegaUp_Controllers_Contest__apiRunsDiff(
            **self._client.query('/api/contest/runsDiff/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def addUser(
            self,
            *,
            contest_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds a user to a contest.
        By default, any user can view details of public contests.
        Only users added through this API can view private contests

        Args:
            contest_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/contest/addUser/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Remove a user from a private contest

        Args:
            contest_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/contest/removeUser/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Replace the teams group assigned to a contest

        Args:
            contest_alias: The alias of the contest
            teams_group_alias: The alias of the teams group

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'teams_group_alias': teams_group_alias,
        }
        self._client.query('/api/contest/replaceTeamsGroup/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds a group to a contest

        Args:
            contest_alias:
            group:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group': group,
        }
        self._client.query('/api/contest/addGroup/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes a group from a contest

        Args:
            contest_alias:
            group:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group': group,
        }
        self._client.query('/api/contest/removeGroup/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds an admin to a contest

        Args:
            contest_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/contest/addAdmin/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes an admin from a contest

        Args:
            contest_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/contest/removeAdmin/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds a group admin to a contest

        Args:
            contest_alias:
            group:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group': group,
        }
        self._client.query('/api/contest/addGroupAdmin/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes a group admin from a contest

        Args:
            contest_alias:
            group:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group': group,
        }
        self._client.query('/api/contest/removeGroupAdmin/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestClarificationsResponse:
        r"""Get clarifications of a contest

        Args:
            contest_alias:
            offset:
            rowcount:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'offset': str(offset),
            'rowcount': str(rowcount),
        }
        return _OmegaUp_Controllers_Contest__apiClarifications(
            **self._client.query('/api/contest/clarifications/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestProblemClarificationsResponse:
        r"""Get clarifications of problem in a contest

        Args:
            contest_alias:
            offset:
            problem_alias:
            rowcount:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'offset': str(offset),
            'problem_alias': problem_alias,
            'rowcount': str(rowcount),
        }
        return _OmegaUp_Controllers_Contest__apiProblemClarifications(
            **self._client.query('/api/contest/problemClarifications/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def scoreboardEvents(
        self,
        *,
        contest_alias: str,
        token: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestScoreboardEventsResponse:
        r"""Returns the Scoreboard events

        Args:
            contest_alias:
            token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if token is not None:
            parameters['token'] = token
        return _OmegaUp_Controllers_Contest__apiScoreboardEvents(
            **self._client.query('/api/contest/scoreboardEvents/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def scoreboard(
        self,
        *,
        contest_alias: str,
        token: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestScoreboardResponse:
        r"""Returns the Scoreboard

        Args:
            contest_alias:
            token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if token is not None:
            parameters['token'] = token
        return _Scoreboard(**self._client.query('/api/contest/scoreboard/',
                                                payload=parameters,
                                                files_=files_,
                                                timeout_=timeout_,
                                                check_=check_))

    def scoreboardMerge(
        self,
        *,
        contest_aliases: str,
        contest_params: Optional[Any] = None,
        usernames_filter: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestScoreboardMergeResponse:
        r"""Gets the accomulative scoreboard for an array of contests

        Args:
            contest_aliases:
            contest_params:
            usernames_filter:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_aliases': contest_aliases,
        }
        if contest_params is not None:
            parameters['contest_params'] = str(contest_params)
        if usernames_filter is not None:
            parameters['usernames_filter'] = usernames_filter
        return _OmegaUp_Controllers_Contest__apiScoreboardMerge(
            **self._client.query('/api/contest/scoreboardMerge/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def requests(
        self,
        *,
        contest_alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestRequestsResponse:
        r"""

        Args:
            contest_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return _OmegaUp_Controllers_Contest__apiRequests(
            **self._client.query('/api/contest/requests/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""

        Args:
            contest_alias:
            username:
            note:
            resolution:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'username': username,
        }
        if note is not None:
            parameters['note'] = note
        if resolution is not None:
            parameters['resolution'] = str(resolution)
        self._client.query('/api/contest/arbitrateRequest/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestUsersResponse:
        r"""Returns ALL identities participating in a contest

        Args:
            contest_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return _OmegaUp_Controllers_Contest__apiUsers(
            **self._client.query('/api/contest/users/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def searchUsers(
        self,
        *,
        contest_alias: str,
        query: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestSearchUsersResponse:
        r"""Search users in contest

        Args:
            contest_alias:
            query:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if query is not None:
            parameters['query'] = query
        return _OmegaUp_Controllers_Contest__apiSearchUsers(
            **self._client.query('/api/contest/searchUsers/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def admins(
        self,
        *,
        contest_alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestAdminsResponse:
        r"""Returns all contest administrators

        Args:
            contest_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return _OmegaUp_Controllers_Contest__apiAdmins(
            **self._client.query('/api/contest/admins/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestUpdateResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_Contest__apiUpdate(
            **self._client.query('/api/contest/update/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def updateEndTimeForIdentity(
            self,
            *,
            contest_alias: str,
            end_time: datetime.datetime,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Update Contest end time for an identity when window_length
        option is turned on

        Args:
            contest_alias:
            end_time:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'end_time': str(int(end_time.timestamp())),
            'username': username,
        }
        self._client.query('/api/contest/updateEndTimeForIdentity/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestRunsResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_Contest__apiRuns(
            **self._client.query('/api/contest/runs/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def stats(
        self,
        *,
        contest_alias: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestStatsResponse:
        r"""Stats of a contest

        Args:
            contest_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if contest_alias is not None:
            parameters['contest_alias'] = contest_alias
        return _OmegaUp_Controllers_Contest__apiStats(
            **self._client.query('/api/contest/stats/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def report(
        self,
        *,
        contest_alias: str,
        auth_token: Optional[str] = None,
        filterBy: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestReportResponse:
        r"""Returns a detailed report of the contest

        Args:
            contest_alias:
            auth_token:
            filterBy:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if auth_token is not None:
            parameters['auth_token'] = auth_token
        if filterBy is not None:
            parameters['filterBy'] = filterBy
        return _OmegaUp_Controllers_Contest__apiReport(
            **self._client.query('/api/contest/report/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def role(
        self,
        *,
        contest_alias: str,
        token: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestRoleResponse:
        r"""

        Args:
            contest_alias:
            token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if token is not None:
            parameters['token'] = token
        return _OmegaUp_Controllers_Contest__apiRole(
            **self._client.query('/api/contest/role/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def setRecommended(
            self,
            *,
            contest_alias: str,
            value: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Given a contest_alias, sets the recommended flag on/off.
        Only omegaUp admins can call this API.

        Args:
            contest_alias:
            value:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if value is not None:
            parameters['value'] = str(value)
        self._client.query('/api/contest/setRecommended/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ContestContestantsResponse:
        r"""Return users who participate in a contest, as long as contest admin
        has chosen to ask for users information and contestants have
        previously agreed to share their information.

        Args:
            contest_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        return _OmegaUp_Controllers_Contest__apiContestants(
            **self._client.query('/api/contest/contestants/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def archive(
            self,
            *,
            contest_alias: str,
            archive: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Archives or Unarchives a contest if user is the creator

        Args:
            contest_alias:
            archive:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
        }
        if archive is not None:
            parameters['archive'] = str(archive)
        self._client.query('/api/contest/archive/',
                           payload=parameters,
                           files_=files_,
                           timeout_=timeout_,
                           check_=check_)


CourseGenerateTokenForCloneCourseResponse = _OmegaUp_Controllers_Course__apiGenerateTokenForCloneCourse
"""The return type of the CourseGenerateTokenForCloneCourse API."""

CourseCloneResponse = _OmegaUp_Controllers_Course__apiClone
"""The return type of the CourseClone API."""

CourseGetProblemUsersResponse = _OmegaUp_Controllers_Course__apiGetProblemUsers
"""The return type of the CourseGetProblemUsers API."""

CourseListAssignmentsResponse = _OmegaUp_Controllers_Course__apiListAssignments
"""The return type of the CourseListAssignments API."""

CourseRequestsResponse = _OmegaUp_Controllers_Course__apiRequests
"""The return type of the CourseRequests API."""

CourseListStudentsResponse = _OmegaUp_Controllers_Course__apiListStudents
"""The return type of the CourseListStudents API."""

CourseStudentProgressResponse = _OmegaUp_Controllers_Course__apiStudentProgress
"""The return type of the CourseStudentProgress API."""

CourseMyProgressResponse = _OmegaUp_Controllers_Course__apiMyProgress
"""The return type of the CourseMyProgress API."""

CourseSearchUsersResponse = _OmegaUp_Controllers_Course__apiSearchUsers
"""The return type of the CourseSearchUsers API."""

CourseAdminsResponse = _OmegaUp_Controllers_Course__apiAdmins
"""The return type of the CourseAdmins API."""

CourseIntroDetailsResponse = _IntroDetailsPayload
"""The return type of the CourseIntroDetails API."""

CourseStudentsProgressResponse = _OmegaUp_Controllers_Course__apiStudentsProgress
"""The return type of the CourseStudentsProgress API."""

CourseAdminDetailsResponse = _CourseDetails
"""The return type of the CourseAdminDetails API."""

CourseActivityReportResponse = _OmegaUp_Controllers_Course__apiActivityReport
"""The return type of the CourseActivityReport API."""

CourseAssignmentDetailsResponse = _OmegaUp_Controllers_Course__apiAssignmentDetails
"""The return type of the CourseAssignmentDetails API."""

CourseRunsResponse = _OmegaUp_Controllers_Course__apiRuns
"""The return type of the CourseRuns API."""

CourseDetailsResponse = _CourseDetails
"""The return type of the CourseDetails API."""

CourseClarificationsResponse = _OmegaUp_Controllers_Course__apiClarifications
"""The return type of the CourseClarifications API."""

CourseProblemClarificationsResponse = _OmegaUp_Controllers_Course__apiProblemClarifications
"""The return type of the CourseProblemClarifications API."""

CourseAssignmentScoreboardResponse = _Scoreboard
"""The return type of the CourseAssignmentScoreboard API."""

CourseAssignmentScoreboardEventsResponse = _OmegaUp_Controllers_Course__apiAssignmentScoreboardEvents
"""The return type of the CourseAssignmentScoreboardEvents API."""

CourseListSolvedProblemsResponse = _OmegaUp_Controllers_Course__apiListSolvedProblems
"""The return type of the CourseListSolvedProblems API."""

CourseListUnsolvedProblemsResponse = _OmegaUp_Controllers_Course__apiListUnsolvedProblems
"""The return type of the CourseListUnsolvedProblems API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseGenerateTokenForCloneCourseResponse:
        r"""

        Args:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return _OmegaUp_Controllers_Course__apiGenerateTokenForCloneCourse(
            **self._client.query('/api/course/generateTokenForCloneCourse/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseCloneResponse:
        r"""Clone a course

        Args:
            alias:
            course_alias:
            name:
            start_time:
            token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'course_alias': course_alias,
            'name': name,
            'start_time': str(int(start_time.timestamp())),
        }
        if token is not None:
            parameters['token'] = token
        return _OmegaUp_Controllers_Course__apiClone(
            **self._client.query('/api/course/clone/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/course/create/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/course/createAssignment/',
                           payload=parameters,
                           files_=files_,
                           timeout_=timeout_,
                           check_=check_)

    def updateAssignment(
            self,
            *,
            assignment: str,
            course: str,
            finish_time: Optional[datetime.datetime] = None,
            start_time: Optional[datetime.datetime] = None,
            unlimited_duration: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Update an assignment

        Args:
            assignment:
            course:
            finish_time:
            start_time:
            unlimited_duration:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'course': course,
        }
        if finish_time is not None:
            parameters['finish_time'] = str(int(finish_time.timestamp()))
        if start_time is not None:
            parameters['start_time'] = str(int(start_time.timestamp()))
        if unlimited_duration is not None:
            parameters['unlimited_duration'] = str(unlimited_duration)
        self._client.query('/api/course/updateAssignment/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds a problem to an assignment

        Args:
            assignment_alias:
            course_alias:
            points:
            problem_alias:
            commit:
            is_extra_problem:

        Returns:
            The API result object.
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
        self._client.query('/api/course/addProblem/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""

        Args:
            assignment_alias:
            course_alias:
            problems:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'problems': problems,
        }
        self._client.query('/api/course/updateProblemsOrder/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""

        Args:
            assignments:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignments': assignments,
            'course_alias': course_alias,
        }
        self._client.query('/api/course/updateAssignmentsOrder/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseGetProblemUsersResponse:
        r"""

        Args:
            course_alias:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'problem_alias': problem_alias,
        }
        return _OmegaUp_Controllers_Course__apiGetProblemUsers(
            **self._client.query('/api/course/getProblemUsers/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def removeProblem(
            self,
            *,
            assignment_alias: str,
            course_alias: str,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Remove a problem from an assignment

        Args:
            assignment_alias:
            course_alias:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'problem_alias': problem_alias,
        }
        self._client.query('/api/course/removeProblem/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseListAssignmentsResponse:
        r"""List course assignments

        Args:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return _OmegaUp_Controllers_Course__apiListAssignments(
            **self._client.query('/api/course/listAssignments/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def removeAssignment(
            self,
            *,
            assignment_alias: str,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Remove an assignment from a course

        Args:
            assignment_alias:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
        }
        self._client.query('/api/course/removeAssignment/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseRequestsResponse:
        r"""Returns the list of requests made by participants who are interested to
        join the course

        Args:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return _OmegaUp_Controllers_Course__apiRequests(
            **self._client.query('/api/course/requests/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def arbitrateRequest(
            self,
            *,
            course_alias: str,
            resolution: bool,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Stores the resolution given to a certain request made by a contestant
        interested to join the course.

        Args:
            course_alias:
            resolution:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'resolution': str(resolution),
            'username': username,
        }
        self._client.query('/api/course/arbitrateRequest/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseListStudentsResponse:
        r"""List students in a course

        Args:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return _OmegaUp_Controllers_Course__apiListStudents(
            **self._client.query('/api/course/listStudents/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def studentProgress(
        self,
        *,
        assignment_alias: str,
        course_alias: str,
        usernameOrEmail: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseStudentProgressResponse:
        r"""

        Args:
            assignment_alias:
            course_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        return _OmegaUp_Controllers_Course__apiStudentProgress(
            **self._client.query('/api/course/studentProgress/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def myProgress(
        self,
        *,
        alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseMyProgressResponse:
        r"""Returns details of a given course

        Args:
            alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
        }
        return _OmegaUp_Controllers_Course__apiMyProgress(
            **self._client.query('/api/course/myProgress/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/course/addStudent/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Remove Student from Course

        Args:
            course_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/course/removeStudent/',
                           payload=parameters,
                           files_=files_,
                           timeout_=timeout_,
                           check_=check_)

    def searchUsers(
        self,
        *,
        assignment_alias: str,
        course_alias: str,
        query: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseSearchUsersResponse:
        r"""Search users in course assignment

        Args:
            assignment_alias:
            course_alias:
            query:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
        }
        if query is not None:
            parameters['query'] = query
        return _OmegaUp_Controllers_Course__apiSearchUsers(
            **self._client.query('/api/course/searchUsers/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def admins(
        self,
        *,
        course_alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseAdminsResponse:
        r"""Returns all course administrators

        Args:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return _OmegaUp_Controllers_Course__apiAdmins(
            **self._client.query('/api/course/admins/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def addAdmin(
            self,
            *,
            course_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds an admin to a course

        Args:
            course_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/course/addAdmin/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes an admin from a course

        Args:
            course_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/course/removeAdmin/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds an group admin to a course

        Args:
            course_alias:
            group:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'group': group,
        }
        self._client.query('/api/course/addGroupAdmin/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes a group admin from a course

        Args:
            course_alias:
            group:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'group': group,
        }
        self._client.query('/api/course/removeGroupAdmin/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseIntroDetailsResponse:
        r"""Show course intro only on public courses when user is not yet registered

        Args:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return _IntroDetailsPayload(
            **self._client.query('/api/course/introDetails/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def studentsProgress(
        self,
        *,
        course: str,
        length: int,
        page: int,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseStudentsProgressResponse:
        r"""

        Args:
            course:
            length:
            page:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course': course,
            'length': str(length),
            'page': str(page),
        }
        return _OmegaUp_Controllers_Course__apiStudentsProgress(
            **self._client.query('/api/course/studentsProgress/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def registerForCourse(
            self,
            *,
            course_alias: str,
            accept_teacher: Optional[bool] = None,
            share_user_information: Optional[bool] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""

        Args:
            course_alias:
            accept_teacher:
            share_user_information:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        if accept_teacher is not None:
            parameters['accept_teacher'] = str(accept_teacher)
        if share_user_information is not None:
            parameters['share_user_information'] = str(share_user_information)
        self._client.query('/api/course/registerForCourse/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseAdminDetailsResponse:
        r"""Returns all details of a given Course

        Args:
            alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
        }
        return _CourseDetails(**self._client.query('/api/course/adminDetails/',
                                                   payload=parameters,
                                                   files_=files_,
                                                   timeout_=timeout_,
                                                   check_=check_))

    def activityReport(
        self,
        *,
        course_alias: str,
        length: Optional[int] = None,
        page: Optional[int] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseActivityReportResponse:
        r"""Returns a report with all user activity for a course.

        Args:
            course_alias:
            length:
            page:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        if length is not None:
            parameters['length'] = str(length)
        if page is not None:
            parameters['page'] = str(page)
        return _OmegaUp_Controllers_Course__apiActivityReport(
            **self._client.query('/api/course/activityReport/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def archive(
            self,
            *,
            archive: bool,
            course_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Archives or un-archives a course

        Args:
            archive:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'archive': str(archive),
            'course_alias': course_alias,
        }
        self._client.query('/api/course/archive/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseAssignmentDetailsResponse:
        r"""Returns details of a given assignment

        Args:
            assignment:
            course:
            token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'course': course,
        }
        if token is not None:
            parameters['token'] = token
        return _OmegaUp_Controllers_Course__apiAssignmentDetails(
            **self._client.query('/api/course/assignmentDetails/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseRunsResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_Course__apiRuns(
            **self._client.query('/api/course/runs/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def details(
        self,
        *,
        alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseDetailsResponse:
        r"""Returns details of a given course

        Args:
            alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
        }
        return _CourseDetails(**self._client.query('/api/course/details/',
                                                   payload=parameters,
                                                   files_=files_,
                                                   timeout_=timeout_,
                                                   check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/course/update/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseClarificationsResponse:
        r"""Gets the clarifications of all assignments in a course

        Args:
            course_alias:
            offset:
            rowcount:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
            'offset': str(offset),
            'rowcount': str(rowcount),
        }
        return _OmegaUp_Controllers_Course__apiClarifications(
            **self._client.query('/api/course/clarifications/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseProblemClarificationsResponse:
        r"""Get clarifications of problem in a contest

        Args:
            assignment_alias:
            course_alias:
            offset:
            problem_alias:
            rowcount:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'offset': str(offset),
            'problem_alias': problem_alias,
            'rowcount': str(rowcount),
        }
        return _OmegaUp_Controllers_Course__apiProblemClarifications(
            **self._client.query('/api/course/problemClarifications/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def assignmentScoreboard(
        self,
        *,
        assignment: str,
        course: str,
        token: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseAssignmentScoreboardResponse:
        r"""Gets Scoreboard for an assignment

        Args:
            assignment:
            course:
            token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'course': course,
        }
        if token is not None:
            parameters['token'] = token
        return _Scoreboard(
            **self._client.query('/api/course/assignmentScoreboard/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def assignmentScoreboardEvents(
        self,
        *,
        assignment: str,
        course: str,
        token: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseAssignmentScoreboardEventsResponse:
        r"""Returns the Scoreboard events

        Args:
            assignment:
            course:
            token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment': assignment,
            'course': course,
        }
        if token is not None:
            parameters['token'] = token
        return _OmegaUp_Controllers_Course__apiAssignmentScoreboardEvents(
            **self._client.query('/api/course/assignmentScoreboardEvents/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def listSolvedProblems(
        self,
        *,
        course_alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseListSolvedProblemsResponse:
        r"""Get Problems solved by users of a course

        Args:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return _OmegaUp_Controllers_Course__apiListSolvedProblems(
            **self._client.query('/api/course/listSolvedProblems/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def listUnsolvedProblems(
        self,
        *,
        course_alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> CourseListUnsolvedProblemsResponse:
        r"""Get Problems unsolved by users of a course

        Args:
            course_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'course_alias': course_alias,
        }
        return _OmegaUp_Controllers_Course__apiListUnsolvedProblems(
            **self._client.query('/api/course/listUnsolvedProblems/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


GraderStatusResponse = _OmegaUp_Controllers_Grader__apiStatus
"""The return type of the GraderStatus API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> GraderStatusResponse:
        r"""Calls to /status grader

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_Grader__apiStatus(
            **self._client.query('/api/grader/status/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


GroupMyListResponse = _OmegaUp_Controllers_Group__apiMyList
"""The return type of the GroupMyList API."""

GroupListResponse = Sequence['_GroupListItem']
"""The return type of the GroupList API."""

GroupDetailsResponse = _OmegaUp_Controllers_Group__apiDetails
"""The return type of the GroupDetails API."""

GroupMembersResponse = _OmegaUp_Controllers_Group__apiMembers
"""The return type of the GroupMembers API."""


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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""New group

        Args:
            alias:
            description:
            name:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'description': description,
            'name': name,
        }
        self._client.query('/api/group/create/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Update an existing group

        Args:
            alias:
            description:
            name:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'description': description,
            'name': name,
        }
        self._client.query('/api/group/update/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Add identity to group

        Args:
            group_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/group/addUser/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Remove user from group

        Args:
            group_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/group/removeUser/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> GroupMyListResponse:
        r"""Returns a list of groups by owner

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_Group__apiMyList(
            **self._client.query('/api/group/myList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def list(
            self,
            *,
            query: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> GroupListResponse:
        r"""Returns a list of groups that match a partial name. This returns an
        array instead of an object since it is used by typeahead.

        Args:
            query:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if query is not None:
            parameters['query'] = query
        return [
            _GroupListItem(**v) for v in self._client.query('/api/group/list/',
                                                            payload=parameters,
                                                            files_=files_,
                                                            timeout_=timeout_,
                                                            check_=check_)
        ]

    def details(
        self,
        *,
        group_alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> GroupDetailsResponse:
        r"""Details of a group (scoreboards)

        Args:
            group_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
        }
        return _OmegaUp_Controllers_Group__apiDetails(
            **self._client.query('/api/group/details/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def members(
        self,
        *,
        group_alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> GroupMembersResponse:
        r"""Members of a group (usernames only).

        Args:
            group_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
        }
        return _OmegaUp_Controllers_Group__apiMembers(
            **self._client.query('/api/group/members/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Create a scoreboard set to a group

        Args:
            group_alias:
            name:
            alias:
            description:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
            'name': name,
        }
        if alias is not None:
            parameters['alias'] = alias
        if description is not None:
            parameters['description'] = description
        self._client.query('/api/group/createScoreboard/',
                           payload=parameters,
                           files_=files_,
                           timeout_=timeout_,
                           check_=check_)


GroupScoreboardDetailsResponse = _GroupScoreboardDetails
"""The return type of the GroupScoreboardDetails API."""

GroupScoreboardListResponse = _OmegaUp_Controllers_GroupScoreboard__apiList
"""The return type of the GroupScoreboardList API."""


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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Add contest to a group scoreboard

        Args:
            contest_alias:
            group_alias:
            scoreboard_alias:
            weight:
            only_ac:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group_alias': group_alias,
            'scoreboard_alias': scoreboard_alias,
            'weight': str(weight),
        }
        if only_ac is not None:
            parameters['only_ac'] = str(only_ac)
        self._client.query('/api/groupScoreboard/addContest/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Add contest to a group scoreboard

        Args:
            contest_alias:
            group_alias:
            scoreboard_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contest_alias': contest_alias,
            'group_alias': group_alias,
            'scoreboard_alias': scoreboard_alias,
        }
        self._client.query('/api/groupScoreboard/removeContest/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> GroupScoreboardDetailsResponse:
        r"""Details of a scoreboard. Returns a list with all contests that belong to
        the given scoreboard_alias

        Args:
            group_alias:
            scoreboard_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'group_alias': group_alias,
            'scoreboard_alias': scoreboard_alias,
        }
        return _GroupScoreboardDetails(
            **self._client.query('/api/groupScoreboard/details/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def list(
        self,
        *,
        group_alias: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> GroupScoreboardListResponse:
        r"""Details of a scoreboard

        Args:
            group_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if group_alias is not None:
            parameters['group_alias'] = group_alias
        return _OmegaUp_Controllers_GroupScoreboard__apiList(
            **self._client.query('/api/groupScoreboard/list/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


IdentityCreateResponse = _OmegaUp_Controllers_Identity__apiCreate
"""The return type of the IdentityCreate API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> IdentityCreateResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_Identity__apiCreate(
            **self._client.query('/api/identity/create/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Entry point for Create bulk Identities API

        Args:
            identities:
            group_alias:
            name:
            username:

        Returns:
            The API result object.
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
        self._client.query('/api/identity/bulkCreate/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Entry point for Create bulk Identities for teams API

        Args:
            team_group_alias:
            team_identities:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
            'team_identities': team_identities,
        }
        self._client.query('/api/identity/bulkCreateForTeams/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/identity/updateIdentityTeam/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/identity/update/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Entry point for change passowrd of an identity

        Args:
            group_alias:
            password:
            username:
            identities:
            name:

        Returns:
            The API result object.
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
        self._client.query('/api/identity/changePassword/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Entry point for switching between associated identities for a user

        Args:
            usernameOrEmail:
            auth_token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'usernameOrEmail': usernameOrEmail,
        }
        if auth_token is not None:
            parameters['auth_token'] = auth_token
        self._client.query('/api/identity/selectIdentity/',
                           payload=parameters,
                           files_=files_,
                           timeout_=timeout_,
                           check_=check_)


NotificationMyListResponse = _OmegaUp_Controllers_Notification__apiMyList
"""The return type of the NotificationMyList API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> NotificationMyListResponse:
        r"""Returns a list of unread notifications for user

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_Notification__apiMyList(
            **self._client.query('/api/notification/myList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def readNotifications(
            self,
            *,
            notifications: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Updates notifications as read in database

        Args:
            notifications:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if notifications is not None:
            parameters['notifications'] = str(notifications)
        self._client.query('/api/notification/readNotifications/',
                           payload=parameters,
                           files_=files_,
                           timeout_=timeout_,
                           check_=check_)


ProblemAddTagResponse = _OmegaUp_Controllers_Problem__apiAddTag
"""The return type of the ProblemAddTag API."""

ProblemAdminsResponse = _OmegaUp_Controllers_Problem__apiAdmins
"""The return type of the ProblemAdmins API."""

ProblemTagsResponse = _OmegaUp_Controllers_Problem__apiTags
"""The return type of the ProblemTags API."""

ProblemUpdateResponse = _OmegaUp_Controllers_Problem__apiUpdate
"""The return type of the ProblemUpdate API."""

ProblemDetailsResponse = _ProblemDetails
"""The return type of the ProblemDetails API."""

ProblemSolutionResponse = _OmegaUp_Controllers_Problem__apiSolution
"""The return type of the ProblemSolution API."""

ProblemVersionsResponse = _OmegaUp_Controllers_Problem__apiVersions
"""The return type of the ProblemVersions API."""

ProblemRunsDiffResponse = _OmegaUp_Controllers_Problem__apiRunsDiff
"""The return type of the ProblemRunsDiff API."""

ProblemRunsResponse = _OmegaUp_Controllers_Problem__apiRuns
"""The return type of the ProblemRuns API."""

ProblemClarificationsResponse = _OmegaUp_Controllers_Problem__apiClarifications
"""The return type of the ProblemClarifications API."""

ProblemStatsResponse = _OmegaUp_Controllers_Problem__apiStats
"""The return type of the ProblemStats API."""

ProblemListResponse = _OmegaUp_Controllers_Problem__apiList
"""The return type of the ProblemList API."""

ProblemAdminListResponse = _OmegaUp_Controllers_Problem__apiAdminList
"""The return type of the ProblemAdminList API."""

ProblemMyListResponse = _OmegaUp_Controllers_Problem__apiMyList
"""The return type of the ProblemMyList API."""

ProblemBestScoreResponse = _OmegaUp_Controllers_Problem__apiBestScore
"""The return type of the ProblemBestScore API."""

ProblemRandomLanguageProblemResponse = _OmegaUp_Controllers_Problem__apiRandomLanguageProblem
"""The return type of the ProblemRandomLanguageProblem API."""

ProblemRandomKarelProblemResponse = _OmegaUp_Controllers_Problem__apiRandomKarelProblem
"""The return type of the ProblemRandomKarelProblem API."""


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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/problem/create/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds an admin to a problem

        Args:
            problem_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/problem/addAdmin/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds a group admin to a problem

        Args:
            group:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'group': group,
            'problem_alias': problem_alias,
        }
        self._client.query('/api/problem/addGroupAdmin/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Updates the problem level of a problem

        Args:
            problem_alias:
            level_tag:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        if level_tag is not None:
            parameters['level_tag'] = level_tag
        self._client.query('/api/problem/updateProblemLevel/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemAddTagResponse:
        r"""Adds a tag to a problem

        Args:
            name:
            problem_alias:
            public:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'name': name,
            'problem_alias': problem_alias,
        }
        if public is not None:
            parameters['public'] = str(public)
        return _OmegaUp_Controllers_Problem__apiAddTag(
            **self._client.query('/api/problem/addTag/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def removeAdmin(
            self,
            *,
            problem_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes an admin from a problem

        Args:
            problem_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/problem/removeAdmin/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes a group admin from a problem

        Args:
            group:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'group': group,
            'problem_alias': problem_alias,
        }
        self._client.query('/api/problem/removeGroupAdmin/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes a tag from a contest

        Args:
            name:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'name': name,
            'problem_alias': problem_alias,
        }
        self._client.query('/api/problem/removeTag/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes a problem whether user is the creator

        Args:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        self._client.query('/api/problem/delete/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemAdminsResponse:
        r"""Returns all problem administrators

        Args:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        return _OmegaUp_Controllers_Problem__apiAdmins(
            **self._client.query('/api/problem/admins/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def tags(
        self,
        *,
        problem_alias: str,
        include_voted: Optional[Any] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemTagsResponse:
        r"""Returns every tag associated to a given problem.

        Args:
            problem_alias:
            include_voted:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        if include_voted is not None:
            parameters['include_voted'] = str(include_voted)
        return _OmegaUp_Controllers_Problem__apiTags(
            **self._client.query('/api/problem/tags/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def rejudge(
            self,
            *,
            problem_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Rejudge problem

        Args:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        self._client.query('/api/problem/rejudge/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemUpdateResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_Problem__apiUpdate(
            **self._client.query('/api/problem/update/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/problem/updateStatement/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/problem/updateSolution/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemDetailsResponse:
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
            The API result object.
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
        return _ProblemDetails(**self._client.query('/api/problem/details/',
                                                    payload=parameters,
                                                    files_=files_,
                                                    timeout_=timeout_,
                                                    check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemSolutionResponse:
        r"""Returns the solution for a problem if conditions are satisfied.

        Args:
            contest_alias:
            forfeit_problem:
            lang:
            problem_alias:
            problemset_id:
            statement_type:

        Returns:
            The API result object.
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
        return _OmegaUp_Controllers_Problem__apiSolution(
            **self._client.query('/api/problem/solution/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def versions(
        self,
        *,
        problem_alias: Optional[str] = None,
        problemset_id: Optional[int] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemVersionsResponse:
        r"""Entry point for Problem Versions API

        Args:
            problem_alias:
            problemset_id:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        if problemset_id is not None:
            parameters['problemset_id'] = str(problemset_id)
        return _OmegaUp_Controllers_Problem__apiVersions(
            **self._client.query('/api/problem/versions/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def selectVersion(
            self,
            *,
            commit: Optional[str] = None,
            problem_alias: Optional[str] = None,
            update_published: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Change the version of the problem.

        Args:
            commit:
            problem_alias:
            update_published:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if commit is not None:
            parameters['commit'] = commit
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        if update_published is not None:
            parameters['update_published'] = update_published
        self._client.query('/api/problem/selectVersion/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemRunsDiffResponse:
        r"""Return a report of which runs would change due to a version change.

        Args:
            version:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'version': version,
        }
        if problem_alias is not None:
            parameters['problem_alias'] = problem_alias
        return _OmegaUp_Controllers_Problem__apiRunsDiff(
            **self._client.query('/api/problem/runsDiff/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemRunsResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_Problem__apiRuns(
            **self._client.query('/api/problem/runs/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def clarifications(
        self,
        *,
        problem_alias: str,
        offset: Optional[int] = None,
        rowcount: Optional[int] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemClarificationsResponse:
        r"""Entry point for Problem clarifications API

        Args:
            problem_alias:
            offset:
            rowcount:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        if offset is not None:
            parameters['offset'] = str(offset)
        if rowcount is not None:
            parameters['rowcount'] = str(rowcount)
        return _OmegaUp_Controllers_Problem__apiClarifications(
            **self._client.query('/api/problem/clarifications/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def stats(
        self,
        *,
        problem_alias: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemStatsResponse:
        r"""Stats of a problem

        Args:
            problem_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
        }
        return _OmegaUp_Controllers_Problem__apiStats(
            **self._client.query('/api/problem/stats/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemListResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_Problem__apiList(
            **self._client.query('/api/problem/list/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def adminList(
        self,
        *,
        page: int,
        page_size: int,
        query: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemAdminListResponse:
        r"""Returns a list of problems where current user has admin rights (or is
        the owner).

        Args:
            page:
            page_size:
            query:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'page': str(page),
            'page_size': str(page_size),
        }
        if query is not None:
            parameters['query'] = query
        return _OmegaUp_Controllers_Problem__apiAdminList(
            **self._client.query('/api/problem/adminList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def myList(
        self,
        *,
        page: int,
        query: Optional[str] = None,
        rowcount: Optional[int] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemMyListResponse:
        r"""Gets a list of problems where current user is the owner

        Args:
            page:
            query:
            rowcount:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'page': str(page),
        }
        if query is not None:
            parameters['query'] = query
        if rowcount is not None:
            parameters['rowcount'] = str(rowcount)
        return _OmegaUp_Controllers_Problem__apiMyList(
            **self._client.query('/api/problem/myList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemBestScoreResponse:
        r"""Returns the best score for a problem

        Args:
            contest_alias:
            problem_alias:
            problemset_id:
            statement_type:
            username:

        Returns:
            The API result object.
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
        return _OmegaUp_Controllers_Problem__apiBestScore(
            **self._client.query('/api/problem/bestScore/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def randomLanguageProblem(
        self,
        *,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemRandomLanguageProblemResponse:
        r"""

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_Problem__apiRandomLanguageProblem(
            **self._client.query('/api/problem/randomLanguageProblem/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def randomKarelProblem(
        self,
        *,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemRandomKarelProblemResponse:
        r"""

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_Problem__apiRandomKarelProblem(
            **self._client.query('/api/problem/randomKarelProblem/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


ProblemForfeitedGetCountsResponse = _OmegaUp_Controllers_ProblemForfeited__apiGetCounts
"""The return type of the ProblemForfeitedGetCounts API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemForfeitedGetCountsResponse:
        r"""Returns the number of solutions allowed
        and the number of solutions already seen

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_ProblemForfeited__apiGetCounts(
            **self._client.query('/api/problemForfeited/getCounts/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


ProblemsetDetailsResponse = _Problemset
"""The return type of the ProblemsetDetails API."""

ProblemsetScoreboardResponse = _Scoreboard
"""The return type of the ProblemsetScoreboard API."""

ProblemsetScoreboardEventsResponse = _OmegaUp_Controllers_Problemset__apiScoreboardEvents
"""The return type of the ProblemsetScoreboardEvents API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemsetDetailsResponse:
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
            The API result object.
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
        return _Problemset(**self._client.query('/api/problemset/details/',
                                                payload=parameters,
                                                files_=files_,
                                                timeout_=timeout_,
                                                check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemsetScoreboardResponse:
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
            The API result object.
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
        return _Scoreboard(**self._client.query('/api/problemset/scoreboard/',
                                                payload=parameters,
                                                files_=files_,
                                                timeout_=timeout_,
                                                check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ProblemsetScoreboardEventsResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_Problemset__apiScoreboardEvents(
            **self._client.query('/api/problemset/scoreboardEvents/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


QualityNominationCreateResponse = _OmegaUp_Controllers_QualityNomination__apiCreate
"""The return type of the QualityNominationCreate API."""

QualityNominationListResponse = _OmegaUp_Controllers_QualityNomination__apiList
"""The return type of the QualityNominationList API."""

QualityNominationMyAssignedListResponse = _OmegaUp_Controllers_QualityNomination__apiMyAssignedList
"""The return type of the QualityNominationMyAssignedList API."""

QualityNominationMyListResponse = _OmegaUp_Controllers_QualityNomination__apiMyList
"""The return type of the QualityNominationMyList API."""

QualityNominationDetailsResponse = _OmegaUp_Controllers_QualityNomination__apiDetails
"""The return type of the QualityNominationDetails API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> QualityNominationCreateResponse:
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
            The API result object.
        """
        parameters: Dict[str, str] = {
            'contents': contents,
            'nomination': nomination,
            'problem_alias': problem_alias,
        }
        return _OmegaUp_Controllers_QualityNomination__apiCreate(
            **self._client.query('/api/qualityNomination/create/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Marks a problem of a nomination (only the demotion type supported for now) as (resolved, banned, warning).

        Args:
            problem_alias:
            qualitynomination_id:
            rationale:
            status:
            all:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problem_alias': problem_alias,
            'qualitynomination_id': str(qualitynomination_id),
            'rationale': rationale,
            'status': status,
        }
        if all is not None:
            parameters['all'] = str(all)
        self._client.query('/api/qualityNomination/resolve/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> QualityNominationListResponse:
        r"""

        Args:
            offset:
            rowcount:
            column:
            query:
            status:

        Returns:
            The API result object.
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
        return _OmegaUp_Controllers_QualityNomination__apiList(
            **self._client.query('/api/qualityNomination/list/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def myAssignedList(
        self,
        *,
        page: int,
        page_size: int,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> QualityNominationMyAssignedListResponse:
        r"""Displays the nominations that this user has been assigned.

        Args:
            page:
            page_size:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'page': str(page),
            'page_size': str(page_size),
        }
        return _OmegaUp_Controllers_QualityNomination__apiMyAssignedList(
            **self._client.query('/api/qualityNomination/myAssignedList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def myList(
        self,
        *,
        offset: int,
        rowcount: int,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> QualityNominationMyListResponse:
        r"""

        Args:
            offset:
            rowcount:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'offset': str(offset),
            'rowcount': str(rowcount),
        }
        return _OmegaUp_Controllers_QualityNomination__apiMyList(
            **self._client.query('/api/qualityNomination/myList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def details(
        self,
        *,
        qualitynomination_id: int,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> QualityNominationDetailsResponse:
        r"""Displays the details of a nomination. The user needs to be either the
        nominator or a member of the reviewer group.

        Args:
            qualitynomination_id:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'qualitynomination_id': str(qualitynomination_id),
        }
        return _OmegaUp_Controllers_QualityNomination__apiDetails(
            **self._client.query('/api/qualityNomination/details/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


ResetCreateResponse = _OmegaUp_Controllers_Reset__apiCreate
"""The return type of the ResetCreate API."""

ResetGenerateTokenResponse = _OmegaUp_Controllers_Reset__apiGenerateToken
"""The return type of the ResetGenerateToken API."""

ResetUpdateResponse = _OmegaUp_Controllers_Reset__apiUpdate
"""The return type of the ResetUpdate API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ResetCreateResponse:
        r"""Creates a reset operation, the first of two steps needed to reset a
        password. The first step consist of sending an email to the user with
        instructions to reset he's password, if and only if the email is valid.

        Args:
            email:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'email': email,
        }
        return _OmegaUp_Controllers_Reset__apiCreate(
            **self._client.query('/api/reset/create/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def generateToken(
        self,
        *,
        email: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ResetGenerateTokenResponse:
        r"""Creates a reset operation, support team members can generate a valid
        token and then they can send it to end user

        Args:
            email:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'email': email,
        }
        return _OmegaUp_Controllers_Reset__apiGenerateToken(
            **self._client.query('/api/reset/generateToken/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> ResetUpdateResponse:
        r"""Updates the password of a given user, this is the second and last step
        in order to reset the password. This operation is done if and only if
        the correct parameters are suplied.

        Args:
            email:
            password:
            password_confirmation:
            reset_token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'email': email,
            'password': password,
            'password_confirmation': password_confirmation,
            'reset_token': reset_token,
        }
        return _OmegaUp_Controllers_Reset__apiUpdate(
            **self._client.query('/api/reset/update/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


RunCreateResponse = _OmegaUp_Controllers_Run__apiCreate
"""The return type of the RunCreate API."""

RunStatusResponse = _Run
"""The return type of the RunStatus API."""

RunDetailsResponse = _RunDetails
"""The return type of the RunDetails API."""

RunSourceResponse = _OmegaUp_Controllers_Run__apiSource
"""The return type of the RunSource API."""

RunCountsResponse = _OmegaUp_Controllers_Run__apiCounts
"""The return type of the RunCounts API."""

RunListResponse = _OmegaUp_Controllers_Run__apiList
"""The return type of the RunList API."""


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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> RunCreateResponse:
        r"""Create a new run

        Args:
            contest_alias:
            problem_alias:
            source:
            language:
            problemset_id:

        Returns:
            The API result object.
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
        return _OmegaUp_Controllers_Run__apiCreate(
            **self._client.query('/api/run/create/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def status(
            self,
            *,
            run_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> RunStatusResponse:
        r"""Get basic details of a run

        Args:
            run_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        return _Run(**self._client.query('/api/run/status/',
                                         payload=parameters,
                                         files_=files_,
                                         timeout_=timeout_,
                                         check_=check_))

    def rejudge(
            self,
            *,
            run_alias: str,
            debug: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Re-sends a problem to Grader.

        Args:
            run_alias:
            debug:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        if debug is not None:
            parameters['debug'] = str(debug)
        self._client.query('/api/run/rejudge/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Disqualify a submission

        Args:
            run_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        self._client.query('/api/run/disqualify/',
                           payload=parameters,
                           files_=files_,
                           timeout_=timeout_,
                           check_=check_)

    def requalify(
            self,
            *,
            run_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Requalify a submission previously disqualified

        Args:
            run_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        self._client.query('/api/run/requalify/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> RunDetailsResponse:
        r"""Gets the details of a run. Includes admin details if admin.

        Args:
            run_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        return _RunDetails(**self._client.query('/api/run/details/',
                                                payload=parameters,
                                                files_=files_,
                                                timeout_=timeout_,
                                                check_=check_))

    def source(
            self,
            *,
            run_alias: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> RunSourceResponse:
        r"""Given the run alias, returns the source code and any compile errors if any
        Used in the arena, any contestant can view its own codes and compile errors

        Args:
            run_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'run_alias': run_alias,
        }
        return _OmegaUp_Controllers_Run__apiSource(
            **self._client.query('/api/run/source/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def counts(
            self,
            *,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> RunCountsResponse:
        r"""Get total of last 6 months

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_Run__apiCounts(
            **self._client.query('/api/run/counts/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> RunListResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_Run__apiList(
            **self._client.query('/api/run/list/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


SchoolListResponse = Sequence['_OmegaUp_Controllers_School__apiList_entry']
"""The return type of the SchoolList API."""

SchoolCreateResponse = _OmegaUp_Controllers_School__apiCreate
"""The return type of the SchoolCreate API."""


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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> SchoolListResponse:
        r"""Gets a list of schools

        Args:
            query:
            term:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if query is not None:
            parameters['query'] = str(query)
        if term is not None:
            parameters['term'] = str(term)
        return [
            _OmegaUp_Controllers_School__apiList_entry(**v)
            for v in self._client.query('/api/school/list/',
                                        payload=parameters,
                                        files_=files_,
                                        timeout_=timeout_,
                                        check_=check_)
        ]

    def create(
        self,
        *,
        name: str,
        country_id: Optional[str] = None,
        state_id: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> SchoolCreateResponse:
        r"""Api to create new school

        Args:
            name:
            country_id:
            state_id:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'name': name,
        }
        if country_id is not None:
            parameters['country_id'] = country_id
        if state_id is not None:
            parameters['state_id'] = state_id
        return _OmegaUp_Controllers_School__apiCreate(
            **self._client.query('/api/school/create/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def selectSchoolOfTheMonth(
            self,
            *,
            school_id: int,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Selects a certain school as school of the month

        Args:
            school_id:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'school_id': str(school_id),
        }
        self._client.query('/api/school/selectSchoolOfTheMonth/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Returns a list of contests

        Args:
            alias:
            course_alias:
            token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
        }
        if course_alias is not None:
            parameters['course_alias'] = course_alias
        if token is not None:
            parameters['token'] = str(token)
        self._client.query('/api/scoreboard/refresh/',
                           payload=parameters,
                           files_=files_,
                           timeout_=timeout_,
                           check_=check_)


SessionCurrentSessionResponse = _OmegaUp_Controllers_Session__apiCurrentSession
"""The return type of the SessionCurrentSession API."""

SessionGoogleLoginResponse = _OmegaUp_Controllers_Session__apiGoogleLogin
"""The return type of the SessionGoogleLogin API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> SessionCurrentSessionResponse:
        r"""Returns information about current session. In order to avoid one full
        server roundtrip (about ~100msec on each pageload), it also returns the
        current time to be able to calculate the time delta between the
        contestant's machine and the server.

        Args:
            auth_token:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if auth_token is not None:
            parameters['auth_token'] = auth_token
        return _OmegaUp_Controllers_Session__apiCurrentSession(
            **self._client.query('/api/session/currentSession/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def googleLogin(
        self,
        *,
        storeToken: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> SessionGoogleLoginResponse:
        r"""

        Args:
            storeToken:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'storeToken': storeToken,
        }
        return _OmegaUp_Controllers_Session__apiGoogleLogin(
            **self._client.query('/api/session/googleLogin/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Updates the admin feedback for a submission

        Args:
            assignment_alias:
            course_alias:
            feedback:
            guid:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'assignment_alias': assignment_alias,
            'course_alias': course_alias,
            'feedback': feedback,
            'guid': guid,
        }
        self._client.query('/api/submission/setFeedback/',
                           payload=parameters,
                           files_=files_,
                           timeout_=timeout_,
                           check_=check_)


TagListResponse = Sequence['_OmegaUp_Controllers_Tag__apiList_entry']
"""The return type of the TagList API."""

TagFrequentTagsResponse = _OmegaUp_Controllers_Tag__apiFrequentTags
"""The return type of the TagFrequentTags API."""


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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> TagListResponse:
        r"""Gets a list of tags

        Args:
            query:
            term:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if query is not None:
            parameters['query'] = str(query)
        if term is not None:
            parameters['term'] = str(term)
        return [
            _OmegaUp_Controllers_Tag__apiList_entry(**v)
            for v in self._client.query('/api/tag/list/',
                                        payload=parameters,
                                        files_=files_,
                                        timeout_=timeout_,
                                        check_=check_)
        ]

    def frequentTags(
        self,
        *,
        problemLevel: str,
        rows: int,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> TagFrequentTagsResponse:
        r"""Return most frequent public tags of a certain level

        Args:
            problemLevel:
            rows:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'problemLevel': problemLevel,
            'rows': str(rows),
        }
        return _OmegaUp_Controllers_Tag__apiFrequentTags(
            **self._client.query('/api/tag/frequentTags/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


TeamsGroupDetailsResponse = _OmegaUp_Controllers_TeamsGroup__apiDetails
"""The return type of the TeamsGroupDetails API."""

TeamsGroupTeamsResponse = _OmegaUp_Controllers_TeamsGroup__apiTeams
"""The return type of the TeamsGroupTeams API."""

TeamsGroupListResponse = Sequence['_ListItem']
"""The return type of the TeamsGroupList API."""

TeamsGroupTeamsMembersResponse = _OmegaUp_Controllers_TeamsGroup__apiTeamsMembers
"""The return type of the TeamsGroupTeamsMembers API."""


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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> TeamsGroupDetailsResponse:
        r"""Details of a team group

        Args:
            team_group_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
        }
        return _OmegaUp_Controllers_TeamsGroup__apiDetails(
            **self._client.query('/api/teamsGroup/details/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""New team group

        Args:
            alias:
            description:
            name:
            numberOfContestants:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'description': description,
            'name': name,
        }
        if numberOfContestants is not None:
            parameters['numberOfContestants'] = str(numberOfContestants)
        self._client.query('/api/teamsGroup/create/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Update an existing teams group

        Args:
            alias:
            description:
            name:
            numberOfContestants:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'alias': alias,
            'description': description,
            'name': name,
        }
        if numberOfContestants is not None:
            parameters['numberOfContestants'] = str(numberOfContestants)
        self._client.query('/api/teamsGroup/update/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> TeamsGroupTeamsResponse:
        r"""Teams of a teams group

        Args:
            team_group_alias:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
        }
        return _OmegaUp_Controllers_TeamsGroup__apiTeams(
            **self._client.query('/api/teamsGroup/teams/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def removeTeam(
            self,
            *,
            team_group_alias: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Remove team from teams group

        Args:
            team_group_alias:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
            'usernameOrEmail': usernameOrEmail,
        }
        self._client.query('/api/teamsGroup/removeTeam/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Add one or more users to a given team

        Args:
            team_group_alias: The username of the team.
            usernames: Username of all members to add

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
            'usernames': usernames,
        }
        self._client.query('/api/teamsGroup/addMembers/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> TeamsGroupListResponse:
        r"""Gets a list of teams groups. This returns an array instead of an object
        since it is used by typeahead.

        Args:
            query:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if query is not None:
            parameters['query'] = query
        return [
            _ListItem(**v) for v in self._client.query('/api/teamsGroup/list/',
                                                       payload=parameters,
                                                       files_=files_,
                                                       timeout_=timeout_,
                                                       check_=check_)
        ]

    def removeMember(
            self,
            *,
            team_group_alias: str,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Remove an existing team member of a teams group

        Args:
            team_group_alias: The username of the team
            username: The username of user to remove

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'team_group_alias': team_group_alias,
            'username': username,
        }
        self._client.query('/api/teamsGroup/removeMember/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> TeamsGroupTeamsMembersResponse:
        r"""Get a list of team members of a teams group

        Args:
            page:
            page_size:
            team_group_alias: The username of the team.

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'page': str(page),
            'page_size': str(page_size),
            'team_group_alias': team_group_alias,
        }
        return _OmegaUp_Controllers_TeamsGroup__apiTeamsMembers(
            **self._client.query('/api/teamsGroup/teamsMembers/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


TimeGetResponse = _OmegaUp_Controllers_Time__apiGet
"""The return type of the TimeGet API."""


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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> TimeGetResponse:
        r"""Entry point for /time API

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_Time__apiGet(
            **self._client.query('/api/time/get/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))


UserCreateResponse = _OmegaUp_Controllers_User__apiCreate
"""The return type of the UserCreate API."""

UserLoginResponse = _OmegaUp_Controllers_User__apiLogin
"""The return type of the UserLogin API."""

UserMailingListBackfillResponse = _OmegaUp_Controllers_User__apiMailingListBackfill
"""The return type of the UserMailingListBackfill API."""

UserGenerateOmiUsersResponse = Dict[str, str]
"""The return type of the UserGenerateOmiUsers API."""

UserProfileResponse = _UserProfileInfo
"""The return type of the UserProfile API."""

UserStatusVerifiedResponse = _OmegaUp_Controllers_User__apiStatusVerified
"""The return type of the UserStatusVerified API."""

UserExtraInformationResponse = _OmegaUp_Controllers_User__apiExtraInformation
"""The return type of the UserExtraInformation API."""

UserCoderOfTheMonthResponse = _OmegaUp_Controllers_User__apiCoderOfTheMonth
"""The return type of the UserCoderOfTheMonth API."""

UserCoderOfTheMonthListResponse = _OmegaUp_Controllers_User__apiCoderOfTheMonthList
"""The return type of the UserCoderOfTheMonthList API."""

UserContestStatsResponse = _OmegaUp_Controllers_User__apiContestStats
"""The return type of the UserContestStats API."""

UserProblemsSolvedResponse = _OmegaUp_Controllers_User__apiProblemsSolved
"""The return type of the UserProblemsSolved API."""

UserListUnsolvedProblemsResponse = _OmegaUp_Controllers_User__apiListUnsolvedProblems
"""The return type of the UserListUnsolvedProblems API."""

UserProblemsCreatedResponse = _OmegaUp_Controllers_User__apiProblemsCreated
"""The return type of the UserProblemsCreated API."""

UserListResponse = _OmegaUp_Controllers_User__apiList
"""The return type of the UserList API."""

UserStatsResponse = _OmegaUp_Controllers_User__apiStats
"""The return type of the UserStats API."""

UserValidateFilterResponse = _OmegaUp_Controllers_User__apiValidateFilter
"""The return type of the UserValidateFilter API."""

UserLastPrivacyPolicyAcceptedResponse = _OmegaUp_Controllers_User__apiLastPrivacyPolicyAccepted
"""The return type of the UserLastPrivacyPolicyAccepted API."""

UserListAssociatedIdentitiesResponse = _OmegaUp_Controllers_User__apiListAssociatedIdentities
"""The return type of the UserListAssociatedIdentities API."""

UserGenerateGitTokenResponse = _OmegaUp_Controllers_User__apiGenerateGitToken
"""The return type of the UserGenerateGitToken API."""

UserCreateAPITokenResponse = _OmegaUp_Controllers_User__apiCreateAPIToken
"""The return type of the UserCreateAPIToken API."""

UserListAPITokensResponse = _OmegaUp_Controllers_User__apiListAPITokens
"""The return type of the UserListAPITokens API."""


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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserCreateResponse:
        r"""Entry point for Create a User API

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_User__apiCreate(
            **self._client.query('/api/user/create/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def login(
            self,
            *,
            password: str,
            usernameOrEmail: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserLoginResponse:
        r"""Exposes API /user/login
        Expects in request:
        user
        password

        Args:
            password:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'password': password,
            'usernameOrEmail': usernameOrEmail,
        }
        return _OmegaUp_Controllers_User__apiLogin(
            **self._client.query('/api/user/login/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Changes the password of a user

        Args:
            old_password:
            username:
            password:
            permission_key:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'old_password': old_password,
            'username': username,
        }
        if password is not None:
            parameters['password'] = password
        if permission_key is not None:
            parameters['permission_key'] = str(permission_key)
        self._client.query('/api/user/changePassword/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Verifies the user given its verification id

        Args:
            id:
            usernameOrEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'id': id,
        }
        if usernameOrEmail is not None:
            parameters['usernameOrEmail'] = usernameOrEmail
        self._client.query('/api/user/verifyEmail/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserMailingListBackfillResponse:
        r"""Registers to the mailing list all users that have not been added before. Admin only

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_User__apiMailingListBackfill(
            **self._client.query('/api/user/mailingListBackfill/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserGenerateOmiUsersResponse:
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
            The API result object.
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
        return {
            k: v
            for k, v in self._client.query('/api/user/generateOmiUsers/',
                                           payload=parameters,
                                           files_=files_,
                                           timeout_=timeout_,
                                           check_=check_).items()
        }

    def profile(
        self,
        *,
        category: Optional[Any] = None,
        omit_rank: Optional[bool] = None,
        username: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserProfileResponse:
        r"""Get general user info

        Args:
            category:
            omit_rank:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if category is not None:
            parameters['category'] = str(category)
        if omit_rank is not None:
            parameters['omit_rank'] = str(omit_rank)
        if username is not None:
            parameters['username'] = username
        return _UserProfileInfo(**self._client.query('/api/user/profile/',
                                                     payload=parameters,
                                                     files_=files_,
                                                     timeout_=timeout_,
                                                     check_=check_))

    def statusVerified(
        self,
        *,
        email: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserStatusVerifiedResponse:
        r"""Gets verify status of a user

        Args:
            email:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'email': email,
        }
        return _OmegaUp_Controllers_User__apiStatusVerified(
            **self._client.query('/api/user/statusVerified/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def extraInformation(
        self,
        *,
        email: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserExtraInformationResponse:
        r"""Gets extra information of the identity:
        - last password change request
        - verify status
        - birth date to verify the user identity

        Args:
            email:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'email': email,
        }
        return _OmegaUp_Controllers_User__apiExtraInformation(
            **self._client.query('/api/user/extraInformation/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def coderOfTheMonth(
        self,
        *,
        category: Optional[Any] = None,
        date: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserCoderOfTheMonthResponse:
        r"""Get coder of the month by trying to find it in the table using the first
        day of the current month. If there's no coder of the month for the given
        date, calculate it and save it.

        Args:
            category:
            date:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if category is not None:
            parameters['category'] = str(category)
        if date is not None:
            parameters['date'] = date
        return _OmegaUp_Controllers_User__apiCoderOfTheMonth(
            **self._client.query('/api/user/coderOfTheMonth/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def coderOfTheMonthList(
        self,
        *,
        category: Optional[Any] = None,
        date: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserCoderOfTheMonthListResponse:
        r"""Returns the list of coders of the month

        Args:
            category:
            date:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if category is not None:
            parameters['category'] = str(category)
        if date is not None:
            parameters['date'] = date
        return _OmegaUp_Controllers_User__apiCoderOfTheMonthList(
            **self._client.query('/api/user/coderOfTheMonthList/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def selectCoderOfTheMonth(
            self,
            *,
            username: str,
            category: Optional[Any] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Selects coder of the month for next month.

        Args:
            username:
            category:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'username': username,
        }
        if category is not None:
            parameters['category'] = str(category)
        self._client.query('/api/user/selectCoderOfTheMonth/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserContestStatsResponse:
        r"""Get Contests which a certain user has participated in

        Args:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return _OmegaUp_Controllers_User__apiContestStats(
            **self._client.query('/api/user/contestStats/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def problemsSolved(
        self,
        *,
        username: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserProblemsSolvedResponse:
        r"""Get Problems solved by user

        Args:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return _OmegaUp_Controllers_User__apiProblemsSolved(
            **self._client.query('/api/user/problemsSolved/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def listUnsolvedProblems(
        self,
        *,
        username: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserListUnsolvedProblemsResponse:
        r"""Get Problems unsolved by user

        Args:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return _OmegaUp_Controllers_User__apiListUnsolvedProblems(
            **self._client.query('/api/user/listUnsolvedProblems/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def problemsCreated(
        self,
        *,
        username: Optional[str] = None,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserProblemsCreatedResponse:
        r"""Get Problems created by user

        Args:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return _OmegaUp_Controllers_User__apiProblemsCreated(
            **self._client.query('/api/user/problemsCreated/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def list(
            self,
            *,
            query: Optional[str] = None,
            rowcount: Optional[int] = None,
            term: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserListResponse:
        r"""Gets a list of users.

        Args:
            query:
            rowcount:
            term:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if query is not None:
            parameters['query'] = query
        if rowcount is not None:
            parameters['rowcount'] = str(rowcount)
        if term is not None:
            parameters['term'] = term
        return _OmegaUp_Controllers_User__apiList(
            **self._client.query('/api/user/list/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def stats(
            self,
            *,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserStatsResponse:
        r"""Get stats

        Args:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return _OmegaUp_Controllers_User__apiStats(
            **self._client.query('/api/user/stats/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def updateBasicInfo(
            self,
            *,
            password: str,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Update basic user profile info when logged with fb/gool

        Args:
            password:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'password': password,
            'username': username,
        }
        self._client.query('/api/user/updateBasicInfo/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
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
            The API result object.
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
        self._client.query('/api/user/update/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Updates the main email of the current user

        Args:
            email:
            originalEmail:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'email': email,
        }
        if originalEmail is not None:
            parameters['originalEmail'] = originalEmail
        self._client.query('/api/user/updateMainEmail/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserValidateFilterResponse:
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
            The API result object.
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
        return _OmegaUp_Controllers_User__apiValidateFilter(
            **self._client.query('/api/user/validateFilter/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def addRole(
            self,
            *,
            role: str,
            username: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds the role to the user.

        Args:
            role:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'role': role,
            'username': username,
        }
        self._client.query('/api/user/addRole/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes the role from the user.

        Args:
            role:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'role': role,
            'username': username,
        }
        self._client.query('/api/user/removeRole/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds the identity to the group.

        Args:
            group:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'group': group,
        }
        self._client.query('/api/user/addGroup/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes the user to the group.

        Args:
            group:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'group': group,
        }
        self._client.query('/api/user/removeGroup/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Adds the experiment to the user.

        Args:
            experiment:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'experiment': experiment,
            'username': username,
        }
        self._client.query('/api/user/addExperiment/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Removes the experiment from the user.

        Args:
            experiment:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'experiment': experiment,
            'username': username,
        }
        self._client.query('/api/user/removeExperiment/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserLastPrivacyPolicyAcceptedResponse:
        r"""Gets the last privacy policy accepted by user

        Args:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        if username is not None:
            parameters['username'] = username
        return _OmegaUp_Controllers_User__apiLastPrivacyPolicyAccepted(
            **self._client.query('/api/user/lastPrivacyPolicyAccepted/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def acceptPrivacyPolicy(
            self,
            *,
            privacy_git_object_id: str,
            statement_type: str,
            username: Optional[str] = None,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Keeps a record of a user who accepts the privacy policy

        Args:
            privacy_git_object_id:
            statement_type:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'privacy_git_object_id': privacy_git_object_id,
            'statement_type': statement_type,
        }
        if username is not None:
            parameters['username'] = username
        self._client.query('/api/user/acceptPrivacyPolicy/',
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
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Associates an identity to the logged user given the username

        Args:
            password:
            username:

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'password': password,
            'username': username,
        }
        self._client.query('/api/user/associateIdentity/',
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
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserListAssociatedIdentitiesResponse:
        r"""Get the identities that have been associated to the logged user

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_User__apiListAssociatedIdentities(
            **self._client.query('/api/user/listAssociatedIdentities/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def generateGitToken(
        self,
        *,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserGenerateGitTokenResponse:
        r"""Generate a new gitserver token. This token can be used to authenticate
        against the gitserver.

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_User__apiGenerateGitToken(
            **self._client.query('/api/user/generateGitToken/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def createAPIToken(
        self,
        *,
        name: str,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserCreateAPITokenResponse:
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
            The API result object.
        """
        parameters: Dict[str, str] = {
            'name': name,
        }
        return _OmegaUp_Controllers_User__apiCreateAPIToken(
            **self._client.query('/api/user/createAPIToken/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def listAPITokens(
        self,
        *,
        # Out-of-band parameters:
        files_: Optional[Mapping[str, BinaryIO]] = None,
        check_: bool = True,
        timeout_: datetime.timedelta = _DEFAULT_TIMEOUT
    ) -> UserListAPITokensResponse:
        r"""Returns a list of all the API tokens associated with the user.

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {}
        return _OmegaUp_Controllers_User__apiListAPITokens(
            **self._client.query('/api/user/listAPITokens/',
                                 payload=parameters,
                                 files_=files_,
                                 timeout_=timeout_,
                                 check_=check_))

    def revokeAPIToken(
            self,
            *,
            name: str,
            # Out-of-band parameters:
            files_: Optional[Mapping[str, BinaryIO]] = None,
            check_: bool = True,
            timeout_: datetime.timedelta = _DEFAULT_TIMEOUT) -> None:
        r"""Revokes an API token associated with the user.

        Args:
            name: A non-empty alphanumeric string. May contain underscores and dashes.

        Returns:
            The API result object.
        """
        parameters: Dict[str, str] = {
            'name': name,
        }
        self._client.query('/api/user/revokeAPIToken/',
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
