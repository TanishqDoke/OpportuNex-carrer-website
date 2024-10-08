from sqlalchemy.sql.expression import text
import pymysql
import os


def load_jobs_from_db():
    try:
        # Establish the connection
        connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=10,
            cursorclass=pymysql.cursors.DictCursor,
            db=os.environ['DB_NAME'],
            host=os.environ['DB_HOST'],
            password=os.environ['DB_PASSWORD'],
            read_timeout=10,
            port=26415,
            user=os.environ['DB_USER'],
            write_timeout=10,
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM jobs")
            result_all = cursor.fetchall()

        # Process results
        jobs = []
        for row in result_all:
            jobs.append(dict(row))

        return jobs

    except pymysql.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return []  # Return an empty list or handle the error appropriately
    except Exception as e:
        print(f"General error: {e}")
        return []  # Return an empty list or handle the error appropriately


def load_jobs_from_db_id(id):
    # Establish the connection
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=10,
        cursorclass=pymysql.cursors.DictCursor,
        db=os.environ['DB_NAME'],
        host=os.environ['DB_HOST'],
        password=os.environ['DB_PASSWORD'],
        read_timeout=10,
        port=26415,
        user=os.environ['DB_USER'],
        write_timeout=10,
    )

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM jobs WHERE id = %s", (id, ))
        rows = cursor.fetchall()

    if len(rows) == 0:
        return None

    else:
        return dict(rows[0])


def add_application_to_db(job_id, application):

    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=10,
        cursorclass=pymysql.cursors.DictCursor,
        db=os.environ['DB_NAME'],
        host=os.environ['DB_HOST'],
        password=os.environ['DB_PASSWORD'],
        read_timeout=10,
        port=26415,
        user=os.environ['DB_USER'],
        write_timeout=10,
    )

    with connection.cursor() as cursor:
        # Define the query using %s as placeholders for MySQL
        query = """
            INSERT INTO applications 
            (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

        # Execute the query by passing values from the `application` dictionary
        cursor.execute(
            query, (job_id, application['full_name'], application['email'],
                    application['linkedin_url'], application['education'],
                    application['work_experience'], application['resume_url']))

        # Commit the transaction to save the data
        connection.commit()
