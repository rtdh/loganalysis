# !/usr/bin/env python

import psycopg2

DBNAME = "news"

request_1 = "What are the most popular articles of all time?"

query_1 = ("SELECT title, count(*) as views FROM articles \n"
           "  JOIN log\n"
           "    ON articles.slug = substring(log.path, 10)\n"
           "    GROUP BY title ORDER BY views DESC LIMIT 3;")

request_2 = "Who are the most popular article authors of all time?"

query_2 = ("SELECT authors.name, count(*) as views\n"
           "    FROM articles \n"
           "    JOIN authors\n"
           "      ON articles.author = authors.id \n"
           "      JOIN log \n"
           "      ON articles.slug = substring(log.path, 10)\n"
           "      WHERE log.status LIKE '200 OK'\n"
           "      GROUP BY authors.name ORDER BY views DESC;")

request_3 = "On which days more than 1% of the requests led to error?"

query_3 = ("SELECT round((stat*100.0)/visitors, 3) as\n"
           "        result, to_char(errortime, 'Mon DD, YYYY')\n"
           "        FROM errorcount ORDER BY result desc limit 1;")

# Connect to the database and feed query to extract results


def get_queryResults(sql_query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql_query)
    results = c.fetchall()
    db.close()
    return results

result1 = get_queryResults(query_1)
result2 = get_queryResults(query_2)
result3 = get_queryResults(query_3)


# Create a function to print query results


def print_results(q_list):
    for i in range(len(q_list)):
        title = q_list[i][0]
        res = q_list[i][1]
        print("\t" + "%s - %d" % (title, res) + " views")
    print("\n")

print(request_1)
print_results(result1)
print(request_2)
print_results(result2)
print(request_3)
print("\t" + result3[0][1] + " - " + str(result3[0][0]) + "%")
