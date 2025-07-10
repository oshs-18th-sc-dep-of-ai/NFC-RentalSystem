from dataclasses import dataclass
from typing import Any, List

import pymysql


@dataclass
class QueryResult:
    affected_rows: int
    result: Any


class DatabaseUtil:
    def __init__(self, host: str, username: str, password: str) -> None:
        """
        클래스를 초기화화며 데이터베이스 연결을 시도함
        :param host: DB 주소
        :param username: DB ID
        :param password: DB 비밀번호
        """
        self.db_conn = pymysql.connect(
            host=host,
            user=username,
            passwd=password,
            db="student24_db",
        )
        self.cursor = self.db_conn.cursor()

    def query(self, sql: str, **kwargs) -> QueryResult:
        """
        쿼리를 실행함
        :param sql: 실행할 SQL문
        :param kwargs: 인자로 들어갈 객체들의 딕셔너리
        :return: `QueryResult` 타입의 결과
        """
        affected = self.cursor.execute(sql, kwargs)
        result = self.cursor.fetchall()
        return QueryResult(affected, result)

    def query_many(self, sql: str, args: List[Any]) -> QueryResult:
        """
        다수의 데이터를 처리할 수 있는 `query` 메서드
        :param sql: 실행할 SQL문
        :param args: 인자로 들어갈 객체들의 딕셔너리로 이루어진 리스트
        :return: `QueryResult` 타입의 결과
        """
        affected = self.cursor.executemany(sql, args)
        result = self.cursor.fetchall()
        return QueryResult(affected, result)

    def commit(self) -> None:
        """
        쿼리 기록을 확정함
        :return:
        """
        self.db_conn.commit()

    def close(self) -> None:
        """
        데이터베이스와의 연결을 해제함
        :return:
        """
        self.db_conn.close()