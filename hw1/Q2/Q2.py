########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error, Connection
import csv
from typing import Any
#################################################################################

## Change to False to disable Sample
SHOW = False

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

############### DO NOT MODIFY THIS SECTION ###########################
######################################################################
def create_connection(path: str) -> Connection:
    connection = None
    try:
        connection = sqlite3.connect(path)
        connection.text_factory = str
    except Error as e:
        print("Error occurred: " + str(e))

    return connection


def execute_query(connection: Connection, query: str) -> str:
    cursor = connection.cursor()
    try:
        if query == "":
            return "Query Blank"
        else:
            cursor.execute(query)
            connection.commit()
            return "Query executed successfully"
    except Error as e:
        return "Error occurred: " + str(e)


def execute_query_and_get_result(connection: Connection, query: str) -> Any:
    cursor = connection.execute(query)
    return cursor.fetchall()
######################################################################
######################################################################


def GTusername() -> str:
    gt_username = ""
    return gt_username


def part_1_a_i() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
    CREATE TABLE incidents (
        report_id TEXT PRIMARY KEY,
        category TEXT,
        date TEXT
    )
    """
    ######################################################################
    return query


def part_1_a_ii() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
    CREATE TABLE details (
        report_id TEXT,
        subject TEXT,
        transport_mode TEXT,
        detection TEXT,
        FOREIGN KEY (report_id) REFERENCES incidents(report_id)
    )
    """
    ######################################################################
    return query


def part_1_a_iii() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
    CREATE TABLE outcomes (
        report_id TEXT,
        outcome TEXT,
        num_ppl_fined INTEGER,
        fine REAL,
        num_ppl_arrested INTEGER,
        prison_time REAL,
        prison_time_unit TEXT,
        FOREIGN KEY (report_id) REFERENCES incidents(report_id)
    )
    """
    ######################################################################
    return query


def part_1_b_i(connection: Connection, path: str) -> None:
    ############### CREATE IMPORT CODE BELOW ############################
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            connection.execute(
                "INSERT INTO incidents (report_id, category, date) VALUES (?, ?, ?)",
                (row['report_id'], row['category'], row['date'])
            )
        connection.commit()
    ######################################################################


def part_1_b_ii(connection: Connection, path: str) -> None:
    ############### CREATE IMPORT CODE BELOW ############################
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            connection.execute(
                "INSERT INTO details (report_id, subject, transport_mode, detection) VALUES (?, ?, ?, ?)",
                (row['report_id'], row['subject'], row['transport_mode'], row['detection'])
            )
        connection.commit()
    ######################################################################


def part_1_b_iii(connection: Connection, path: str) -> None:
    ############### CREATE IMPORT CODE BELOW ############################
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Handle numeric conversions
            num_ppl_fined = int(row['num_ppl_fined']) if row['num_ppl_fined'] else 0
            fine = float(row['fine']) if row['fine'] else 0.0
            num_ppl_arrested = int(row['num_ppl_arrested']) if row['num_ppl_arrested'] else 0
            prison_time = float(row['prison_time']) if row['prison_time'] else 0.0
            
            connection.execute(
                "INSERT INTO outcomes (report_id, outcome, num_ppl_fined, fine, num_ppl_arrested, prison_time, prison_time_unit) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (row['report_id'], row['outcome'], num_ppl_fined, fine, num_ppl_arrested, prison_time, row['prison_time_unit'])
            )
        connection.commit()
    ######################################################################


def part_2_a() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = "CREATE INDEX idx_incidents_report_id ON incidents(report_id)"
    ######################################################################
    return query


def part_2_b() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = "CREATE INDEX idx_details_report_id ON details(report_id)"
    ######################################################################
    return query


def part_2_c() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = "CREATE INDEX idx_outcomes_report_id ON outcomes(report_id)"
    ######################################################################
    return query


def part_3() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
    SELECT ROUND(CAST(COUNT(*) AS REAL) * 100.0 / (SELECT COUNT(*) FROM incidents), 2) AS percentage
    FROM incidents
    WHERE date BETWEEN '2018-01-01' AND '2020-12-31'
    """
    ######################################################################
    return query


def part_4() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
    SELECT transport_mode, COUNT(*) as count
    FROM details
    WHERE detection = 'Intelligence'
    AND transport_mode IS NOT NULL
    AND transport_mode != ''
    GROUP BY transport_mode
    ORDER BY count DESC
    LIMIT 3
    """
    ######################################################################
    return query


def part_5() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
    WITH dd AS (
        SELECT DISTINCT report_id, detection
        FROM details
        WHERE detection IS NOT NULL AND TRIM(detection) != ''
    )
    SELECT dd.detection,
           COUNT(*) AS count,
           ROUND(AVG(o.num_ppl_arrested * 1.0), 2) AS avg_arrests
    FROM dd
    JOIN outcomes o ON dd.report_id = o.report_id
    WHERE o.num_ppl_arrested > 0
    GROUP BY dd.detection
    HAVING COUNT(*) >= 100
    ORDER BY AVG(o.num_ppl_arrested * 1.0) DESC, count DESC, dd.detection ASC
    LIMIT 3
    """
    ######################################################################
    return query


def part_6() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
    WITH category_counts AS (
        SELECT category, COUNT(*) AS total_incidents
        FROM incidents
        GROUP BY category
    ),
    category_prison_stats AS (
        SELECT i.category AS category,
               COUNT(*) AS total_joined,
               AVG(CASE
                   WHEN LOWER(o.prison_time_unit) = 'years' THEN COALESCE(o.prison_time, 0) * 365
                   WHEN LOWER(o.prison_time_unit) = 'months' THEN COALESCE(o.prison_time, 0) * 30
                   WHEN LOWER(o.prison_time_unit) = 'weeks' THEN COALESCE(o.prison_time, 0) * 7
                   WHEN LOWER(o.prison_time_unit) = 'days' THEN COALESCE(o.prison_time, 0)
                   WHEN LOWER(o.prison_time_unit) = 'n/a' THEN COALESCE(o.prison_time, 0)
                   ELSE COALESCE(o.prison_time, 0)
               END) AS avg_prison_days
        FROM incidents i
        JOIN outcomes o ON i.report_id = o.report_id
        GROUP BY i.category
    )
    SELECT c.category,
           c.total_incidents AS count,
           ROUND(p.avg_prison_days, 2) AS avg_prison_days
    FROM category_counts c
    JOIN category_prison_stats p ON c.category = p.category
    WHERE c.total_incidents > 50
    ORDER BY p.avg_prison_days DESC, count DESC, c.category ASC
    """
    ######################################################################
    return query


def part_7_a() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
    CREATE VIEW fines AS
    SELECT i.report_id, i.category, i.date, o.fine, o.num_ppl_fined
    FROM incidents i
    JOIN outcomes o ON i.report_id = o.report_id
    WHERE o.num_ppl_fined >= 1
    """
    ######################################################################
    return query


def part_7_b() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
    SELECT strftime('%Y', date) AS year,
           SUM(num_ppl_fined) AS total_ppl_fined,
           ROUND(SUM(fine), 2) AS total_fine_amount
    FROM fines
    GROUP BY strftime('%Y', date)
    ORDER BY total_fine_amount DESC, total_ppl_fined DESC, year ASC
    LIMIT 3
    """
    ######################################################################
    return query


def part_8_a() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
    CREATE VIRTUAL TABLE incident_overviews USING fts5(
        report_id,
        category,
        subject,
        outcome
    )
    """
    ######################################################################
    return query


def part_8_b() -> str:
    ############### EDIT SQL STATEMENT ############################
    query = """
    INSERT INTO incident_overviews (report_id, category, subject, outcome)
    SELECT i.report_id, i.category, d.subject, o.outcome
    FROM incidents i
    LEFT JOIN details d ON i.report_id = d.report_id
    LEFT JOIN outcomes o ON i.report_id = o.report_id
    """
    ######################################################################
    return query

    
def part_8_c():
    ############### EDIT SQL STATEMENT ###################################
    query = """
    SELECT COUNT(*)
    FROM incident_overviews
    WHERE incident_overviews MATCH 'NEAR(dead pangolin, 2)'
    """
    ######################################################################
    return query


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    try:
        conn = create_connection("Q2")
    except Exception as e:
        print("Database Creation Error:", e)

    try:
        conn.execute("DROP TABLE IF EXISTS incidents;")
        conn.execute("DROP TABLE IF EXISTS details;")
        conn.execute("DROP TABLE IF EXISTS outcomes;")
        conn.execute("DROP VIEW IF EXISTS fines;")
        conn.execute("DROP TABLE IF EXISTS incident_overviews;")
    except Exception as e:
        print("Error in Table Drops:", e)

    try:
        print('\033[32m' + "part 1.a.i: " + '\033[m' + execute_query(conn, part_1_a_i()))
        print('\033[32m' + "part 1.a.ii: " + '\033[m' + execute_query(conn, part_1_a_ii()))
        print('\033[32m' + "part 1.a.iii: " + '\033[m' + execute_query(conn, part_1_a_iii()))
    except Exception as e:
         print("Error in part 1.a:", e)

    try:
        part_1_b_i(conn,"data/incidents.csv")
        print('\033[32m' + "Row count for Incidents Table: " + '\033[m' + str(execute_query_and_get_result(conn, "select count(*) from incidents")[0][0]))
        part_1_b_ii(conn, "data/details.csv")
        print('\033[32m' + "Row count for Details Table: " + '\033[m' + str(execute_query_and_get_result(conn,"select count(*) from details")[0][0]))
        part_1_b_iii(conn, "data/outcomes.csv")
        print('\033[32m' + "Row count for Outcomes Table: " + '\033[m' + str(execute_query_and_get_result(conn,"select count(*) from outcomes")[0][0]))
    except Exception as e:
        print("Error in part 1.b:", e)

    try:
        print('\033[32m' + "part 2.a: " + '\033[m' + execute_query(conn, part_2_a()))
        print('\033[32m' + "part 2.b: " + '\033[m' + execute_query(conn, part_2_b()))
        print('\033[32m' + "part 2.c: " + '\033[m' + execute_query(conn, part_2_c()))
    except Exception as e:
        print("Error in part 2:", e)

    try:
        print('\033[32m' + "part 3: " + '\033[m' + str(execute_query_and_get_result(conn, part_3())[0][0]))
    except Exception as e:
        print("Error in part 3:", e)

    try:
        print('\033[32m' + "part 4: " + '\033[m')
        for line in execute_query_and_get_result(conn, part_4()):
            print(line[0],line[1])
    except Exception as e:
        print("Error in part 4:", e)

    try:
        print('\033[32m' + "part 5: " + '\033[m')
        for line in execute_query_and_get_result(conn, part_5()):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part 5:", e)

    try:
        print('\033[32m' + "part 6: " + '\033[m')
        for line in execute_query_and_get_result(conn, part_6()):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part 6:", e)
    
    try:
        execute_query(conn, part_7_a())
        print('\033[32m' + "part 7.a: " + '\033[m' + str(execute_query_and_get_result(conn,"select count(*) from fines")[0][0]))
        print('\033[32m' + "part 7.b: " + '\033[m')
        for line in execute_query_and_get_result(conn, part_7_b()):
            print(line[0],line[1], line[2])
    except Exception as e:
        print("Error in part 7:", e)

    try:   
        print('\033[32m' + "part 8.a: " + '\033[m'+ execute_query(conn, part_8_a()))
        execute_query(conn, part_8_b())
        print('\033[32m' + "part 8.b: " + '\033[m' + str(execute_query_and_get_result(conn, "select count(*) from incident_overviews")[0][0]))
        print('\033[32m' + "part 8.c: " + '\033[m' + str(execute_query_and_get_result(conn, part_8_c())[0][0]))
    except Exception as e:
        print("Error in part 8:", e)

    conn.close()
    #################################################################################
    #################################################################################
  