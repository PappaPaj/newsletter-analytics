from src.bindings import ConvertKit

API_SECRET = None
API_KEY = None

ck = ConvertKit(API_SECRET, API_KEY)

tags = ck.fetch_tags()

for tag in tags:
    print(tag)

course_tag = next(tag for tag in tags if tag['name'] == 'email-course-organic')
course_subs = ck.fetch_tag_subscribers(course_tag['id'])

print(len(course_subs))
print(course_subs[0])

my_sub = ck.list_subscribers(email_address="test@gmail.com")[0]


print(my_sub)



