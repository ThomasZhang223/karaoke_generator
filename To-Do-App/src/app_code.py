from datetime import datetime, date, timedelta
from typing import List, Tuple
import pymysql
import logging


def configureLogging():
    # Only configure if no handlers exist (so pytest can override)
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            filename="todo.log",
            filemode="a",
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )

class Task:
    _item: str
    _type: str
    _started: datetime
    _due: datetime
    _done: datetime | None
    def __init__(self, item: str, type: str, started: datetime, due: datetime, done: datetime | None = None):
        self._item = item
        self._type = type
        self._started = started
        self._due = due
        self._done = done
    def __repr__(self) -> str:
        return f"Task(item={self._item}, type={self._type}, started={self._started}, due={self._due}, done={self._done})"
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return (self._item == other._item and
                self._type == other._type and
                self._started == other._started and
                self._due == other._due and
                self._done == other._done)
    def to_tuple(self) -> Tuple[str, str, datetime, datetime, datetime | None]:
        return (self._item, self._type, self._started, self._due, self._done)
    @staticmethod
    def from_tuple(t: Tuple[str, str, datetime, datetime, datetime | None]) -> 'Task':
        return Task(*t)
    # generate all getters
    def item(self) -> str:
        return self._item
    def type(self) -> str:
        return self._type
    def started(self) -> datetime:
        return self._started
    def due(self) -> datetime:
        return self._due
    def done(self) -> datetime | None:
        return self._done
    def is_done(self) -> bool:
        return self._done is not None
    def is_overdue(self) -> bool:
        if self._done is not None:
            return False
        return date.today() > self._due.date()

class User:
    _representative_username: str
    _representative_password: str
    _database: str
    _hostname: str
    _connection: pymysql.connections.Connection | None
    _mylogger: logging.Logger
    DEFAULT_HOST = "riku.shoshin.uwaterloo.ca"
    DEFAULT_DATABASE = "SE101_Team_27"
    DEFAULT_USERNAME = "a88mehta"
    DEFAULT_PASSWORD = "251016"
    def __init__(
        self,
        representative_username: str | None = None,
        representative_password: str | None = None,
        database: str | None = None,
        hostname: str | None = None,
    ):
        # Use provided values or fall back to the defaults from the block above
        self._mylogger = logging.getLogger("User")
        self._representative_username = representative_username or User.DEFAULT_USERNAME
        self._representative_password = representative_password or User.DEFAULT_PASSWORD
        self._database = database or User.DEFAULT_DATABASE
        self._hostname = hostname or User.DEFAULT_HOST
        self._login()



    def username(self) -> str:
        return self._representative_username

    def password(self) -> str:
        return self._representative_password

    def database(self) -> str:
        return self._database

    def hostname(self) -> str:
        return self._hostname
    
    def _login(self) -> bool:
        logger = self._mylogger
        logger.info(f"_login(username={self._representative_username}, host={self._hostname}, db={self._database})")
        try:
            # establish and keep the connection on the user instance
            self._connection = pymysql.connect(
                host=self._hostname,
                user=self._representative_username,
                password=self._representative_password,
                database=self._database,
            )
            logger.info("Database connection established")
            return True
        except pymysql.Error as err:
            logger.error(f"Database connection failed: {err}")
            self._connection = None
            return False
    def connection(self) -> pymysql.connections.Connection | None:
        if self._connection is None:
            if not self._login():
                return None
        return self._connection
    def fetch_tasks(self) -> List[Task]:
        logger = self._mylogger
        logger.info("User.fetch_tasks()")
        conn = self.connection()
        if conn is None:
            logger.error("No DB connection available for fetch_tasks")
            return []
        try:
            cur = conn.cursor()
            # fetch only tasks for this representative username
            cur.execute("SELECT item, type, started, due, done FROM ToDoData WHERE username=%s", (self._representative_username,))
            rows = cur.fetchall()
            return [Task.from_tuple(r) for r in rows]
        except pymysql.Error as e:
            logger.error(f"fetch_tasks error: {e}")
            return []
        finally:
            try:
                cur.close()
            except Exception:
                pass

    def add_task(self, task: Task) -> bool:
        logger = self._mylogger
        logger.info(f"User.add_task(item={task.item()})")
        conn = self.connection()
        if conn is None:
            logger.error("No DB connection available for add_task")
            return False
        try:
            cur = conn.cursor()
            # include the representative username when inserting
            cur.execute(
                "INSERT INTO ToDoData (item, type, started, due, done, username) VALUES (%s, %s, %s, %s, %s, %s)",
                (*task.to_tuple(), self._representative_username)
            )
            conn.commit()
            return True
        except pymysql.Error as e:
            if getattr(e, "args", None) and e.args[0] == 1062:
                logger.warning(f"add_task duplicate: {task.item()}")
            else:
                logger.error(f"add_task error: {e}")
            return False
        finally:
            try:
                cur.close()
            except Exception:
                pass
    
    def update_task(self, task: Task) -> bool:
        logger = self._mylogger
        logger.info(f"User.update_task(item={task.item()})")
        conn = self.connection()
        if conn is None:
            logger.error("No DB connection available for update_task")
            return False
        try:
            cur = conn.cursor()
            affected = cur.execute(
                "UPDATE ToDoData SET type=%s, started=%s, due=%s, done=%s WHERE item=%s AND username=%s",
                (task.type(), task.started(), task.due(), task.done(), task.item(), self._representative_username)
            )
            conn.commit()
            if affected == 0:
                logger.warning(f"update_task: no such item {task.item()}")
                return False
            return True
        except pymysql.Error as e:
            logger.error(f"update_task error: {e}")
            return False
        finally:
            try:
                cur.close()
            except Exception:
                pass

    def delete_task(self, item_name: str) -> bool:
        logger = self._mylogger
        logger.info(f"User.delete_task(item={item_name})")
        conn = self.connection()
        if conn is None:
            logger.error("No DB connection available for delete_task")
            return False
        try:
            cur = conn.cursor()
            affected = cur.execute("DELETE FROM ToDoData WHERE item=%s AND username=%s", (item_name, self._representative_username))
            conn.commit()
            if affected == 0:
                logger.warning(f"delete_task: no such item {item_name}")
                return False
            return True
        except pymysql.Error as e:
            logger.error(f"delete_task error: {e}")
            return False
        finally:
            try:
                cur.close()
            except Exception:
                pass


    def next_task(self) -> Task | None:
        logger = self._mylogger
        logger.info("User.next_task()")
        conn = self.connection()
        if conn is None:
            logger.error("No DB connection available for next_task")
            return None
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT item, type, started, due, done FROM ToDoData WHERE done IS NULL AND username=%s ORDER BY due ASC LIMIT 1",
                (self._representative_username,)
            )
            row = cur.fetchone()
            if row:
                return Task.from_tuple(row)
            return None
        except pymysql.Error as e:
            logger.error(f"next_task error: {e}")
            return None
        finally:
            try:
                cur.close()
            except Exception:
                pass


    def today_tasks(self) -> List[Task]:
        logger = self._mylogger
        logger.info("User.today_tasks()")
        conn = self.connection()
        if conn is None:
            logger.error("No DB connection available for today_tasks")
            return []
        try:
            cur = conn.cursor()
            # select tasks due today for this username and not done
            cur.execute(
                "SELECT item, type, started, due, done FROM ToDoData WHERE username=%s AND done IS NULL AND DATE(due)=CURDATE()",
                (self._representative_username,)
            )
            rows = cur.fetchall()
            return [Task.from_tuple(r) for r in rows]
        except pymysql.Error as e:
            logger.error(f"today_tasks error: {e}")
            return []
        finally:
            try:
                cur.close()
            except Exception:
                pass
            
    def tomorrow_tasks(self) -> List[Task]:
        logger = self._mylogger
        logger.info("User.tomorrow_tasks()")
        conn = self.connection()
        if conn is None:
            logger.error("No DB connection available for tomorrow_tasks")
            return []
        try:
            cur = conn.cursor()
            # select tasks due strictly tomorrow for this username and not done
            cur.execute(
                "SELECT item, type, started, due, done FROM ToDoData WHERE username=%s AND done IS NULL AND DATE(due)=DATE_ADD(CURDATE(), INTERVAL 1 DAY)",
                (self._representative_username,)
            )
            rows = cur.fetchall()
            return [Task.from_tuple(r) for r in rows]
        except pymysql.Error as e:
            logger.error(f"tomorrow_tasks error: {e}")
            return [] 
        finally:
            try:
                cur.close()
            except Exception:
                pass
    