# CRUD
# C- Create , R - Retrieve , U - Update , D - Delete
from datetime import datetime

import mysql.connector
from contextlib import contextmanager
import logging

# -------------------------
# Setup logging
# -------------------------
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Context manager for database connection
@contextmanager
def get_connection():
    conn = None
    try:
        logger.info("Attempting database connection...")
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='expense_manager'
        )
        if conn.is_connected():
            logger.info("✅ Connection successful")
            yield conn
        else:
            logger.error("❌ Connection unsuccessful")
            yield None
    except mysql.connector.Error as e:
        logger.exception(f"Connection failed: {e}")
        yield None
    finally:
        if conn and conn.is_connected():
            conn.close()
            logger.info("🔒 Connection closed")


# Context manager for cursor
@contextmanager
def get_cursor(connection):
    cursor = None
    try:
        logger.info("Opening cursor...")
        cursor = connection.cursor(dictionary=True)
        yield cursor
    except mysql.connector.Error as e:
        logger.exception(f"Cursor error: {e}")
        yield None
    finally:
        if cursor:
            cursor.close()
            logger.info("Cursor closed")


# Function to fetch all records
def fetch_all_records():
    logger.info("fetch_all_records called")
    with get_connection() as conn:
        if conn is None:
            logger.warning("fetch_all_records: No connection available")
            return
        with get_cursor(conn) as cursor:
            if cursor is None:
                logger.warning("fetch_all_records: No cursor available")
                return
            cursor.execute("SELECT * FROM expenses")
            expenses = cursor.fetchall()
            logger.info(f"Fetched {len(expenses)} records")
            return expenses


# Function to fetch expenses for a specific date
def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_connection() as conn:
        if conn is None:
            logger.warning("No connection available")
            return []
        with get_cursor(conn) as cursor:
            if cursor is None:
                logger.warning("No cursor available")
                return []
            cursor.execute(
                "SELECT * FROM expenses WHERE expense_date = %s",
                (expense_date,)
            )
            expenses = cursor.fetchall()
            logger.info(f"Fetched {len(expenses)} expenses for {expense_date}")
            return expenses


# Function to insert an expense
def insert_expense(expense_date, amount, category, notes):
    logger.info(
        f"insert_expense called with date={expense_date}, amount={amount}, "
        f"category={category}, notes={notes}"
    )
    with get_connection() as conn:
        if conn is None:
            logger.error("Insert aborted: No connection")
            return
        with get_cursor(conn) as cursor:
            if cursor is None:
                logger.error("Insert aborted: No cursor")
                return
            try:
                cursor.execute(
                    '''
                    INSERT INTO expenses (expense_date, amount, category, notes)
                    VALUES (%s, %s, %s, %s)
                    ''',
                    (expense_date, amount, category, notes)
                )
                conn.commit()
                logger.info("✅ Expense inserted successfully")
            except mysql.connector.Error as e:
                logger.exception(f"Insert failed: {e}")


# Function to delete an expense by ID
def delete_expense(expense_id: int):
    logger.info(f"delete_expense called with ID={expense_id}")
    with get_connection() as conn:
        if conn is None:
            logger.error("Delete aborted: No connection")
            return
        with get_cursor(conn) as cursor:
            if cursor is None:
                logger.error("Delete aborted: No cursor")
                return
            try:
                cursor.execute(
                    "DELETE FROM expenses WHERE id = %s",
                    (expense_id,)
                )
                conn.commit()
                logger.info(f"✅ Expense with ID {expense_id} deleted successfully")
            except mysql.connector.Error as e:
                logger.exception(f"Failed to delete expense: {e}")


# Function to delete all expenses for a specific date
def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date called with {expense_date}")
    with get_connection() as conn:
        if conn is None:
            logger.error("Delete aborted: No connection")
            return
        with get_cursor(conn) as cursor:
            if cursor is None:
                logger.error("Delete aborted: No cursor")
                return
            try:
                cursor.execute(
                    "DELETE FROM expenses WHERE expense_date = %s",
                    (expense_date,)
                )
                conn.commit()
                logger.info(f"✅ All expenses for {expense_date} deleted successfully")
            except mysql.connector.Error as e:
                logger.exception(f"Failed to delete expenses for {expense_date}: {e}")


# Function to fetch summary of expenses grouped by category
def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start={start_date}, end={end_date}")
    with get_connection() as conn:
        if conn is None:
            logger.error("Summary fetch aborted: No connection")
            return
        with get_cursor(conn) as cursor:
            if cursor is None:
                logger.error("Summary fetch aborted: No cursor")
                return
            cursor.execute(
                '''
                SELECT category, SUM(amount) AS total
                FROM expenses
                WHERE expense_date BETWEEN %s AND %s
                GROUP BY category
                ''',
                (start_date, end_date)
            )
            summary = cursor.fetchall()
            logger.info(f"Fetched {len(summary)} summary rows")
            return summary


def get_analytics_month():
    logger.info("get_analytics_month called")  # Simplified log message

    with get_connection() as conn:
        if conn is None:
            logger.error("Fetch by month aborted: No connection")
            return []  # Return empty list instead of None
        with get_cursor(conn) as cursor:
            if cursor is None:
                logger.error("Fetch by month aborted: No cursor")
                return []  # Return empty list instead of None
            cursor.execute(
                '''
                SELECT MONTHNAME(expense_date) AS Month_Name, SUM(amount) AS Total
                FROM expenses
                GROUP BY MONTHNAME(expense_date), MONTH(expense_date)
                ORDER BY MONTH(expense_date)
                '''
            )
            monthly = cursor.fetchall()
            logger.info(f"Fetched {len(monthly)} summary rows")
            return monthly

# --- Usage ---
if __name__ == '__main__':
    # insert_expense('2025-09-02', 160, 'Course', 'GENAI')
    # delete_expense(3)
    # print(fetch_expenses_for_date('2024-08-15'))
    # print(fetch_expense_summary('2024-08-01', '2024-08-05'))
    print(get_analytics_month())
