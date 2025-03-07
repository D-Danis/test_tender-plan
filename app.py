from tasks import fetch_tender_numbers, parse_xml_form, URL_XML



def main():
    for page_number in range(1, 3):
        result = fetch_tender_numbers.apply_async(args=(page_number,)) # Запуск задачи
        tender_numbers = result.get(timeout=10)  # Получаем результат
        print("start page numer : ", page_number)
        for reg_number in tender_numbers:
            # Запускаем задачу на парсинг XML формы для каждого тендера
            publish_date_result = parse_xml_form.delay(reg_number).get(timeout=10)
            print(f"{URL_XML}{reg_number} - {publish_date_result}")




if __name__ == "__main__":
    main()