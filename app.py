from tasks import parse_xml, fetch_tender
from celery import group


def main():
    res = (group(fetch_tender.s(i) for i in range(1,3)) | parse_xml.s())()
    for i in res.get():
        print(i)




if __name__ == "__main__":
    main()