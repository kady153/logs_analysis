#!/usr/bin/python3
import psycopg2


# What are the most popular three articles of all time?
# substring function is assuming that the slug is never more than 100 words
query1 = '''
select articles.title, COUNT(*) AS num
from articles,log
where substring(log.path,10,110) = articles.slug
group by articles.title
order by num DESC
limit 3;
'''
# Who are the most popular article authors of all time?
query2 = '''
select authors.name, count(*)as num
from authors,articles,log
where authors.id=articles.author
and substring(log.path,10,100) = articles.slug
group by authors.name
ORDER BY num DESC
limit 4;
'''
# On which days did more than 1% of requests lead to errors?
query3 = '''
select errors.date,
round(((cast(errors.num as decimal)/total.num)*100),2)as error
from errors,total
where errors.date=total.date
and cast(errors.num as decimal)/total.num>0.01;
'''


# return query results
def run_query(query):
    db = psycopg2.connect("dbname= news")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


# the following three functions are for printing results
def top_three_articles(query):
    result = run_query(query)
    print("\n\t\t\tTop three articles are:\n")
    for i in result:
        print("-"+i[0]+"--->"+str(i[1])+" views")


def top_authors(query):
    result = run_query(query)
    print("\n\t\t\tTop authors of all time are:\n")
    for i in result:
        print("-"+i[0]+"--->"+str(i[1])+" views")


def error_results(query):
    result = run_query(query)
    print("\n\t\t\tDays with more than 1% of bad requests:\n")
    for i in result:
        print(str(i[0])+"--->"+str(i[1])+"% errors")


top_three_articles(query1)
top_authors(query2)
error_results(query3)
