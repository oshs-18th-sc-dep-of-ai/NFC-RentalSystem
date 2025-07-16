from typing import Union


def get_year(student_id: Union[int, str]) -> int:
    """
    학번 -> 입학 연도
    :param student_id: `int` 또는 `str` 타입의 학번
    :return: `int`형의 입학 연도 반환
    """
    student_id = str(student_id)
    return int(student_id[0:2])


def get_grade(student_id: Union[int, str]) -> int:
    """
    학번 -> 학년
    :param student_id: `int` 또는 `str` 타입의 학번
    :return: `int`형의 학년 반환
    """
    student_id = str(student_id)
    return int(student_id[2])


def get_class(student_id: Union[int, str]) -> int:
    """
    학번 -> 반
    :param student_id: `int` 또는 `str` 타입의 학번
    :return: `int`형의 반 반환
    """
    student_id = str(student_id)
    return int(student_id[3:5])


def get_number(student_id: Union[int, str]) -> int:
    """
    학번 -> 번호
    :param student_id: `int` 또는 `str` 타입의 학번
    :return: `int`형의 번호 반환
    """
    student_id = str(student_id)
    return int(student_id[5:7])
