import cgi
from urllib.parse import parse_qs

def application(environ, start_response):
    # Печатаем все переменные окружения, чтобы увидеть запрос целиком
    print("Request Environment:", environ)

    # Печатаем строку запроса
    query_string = environ.get('QUERY_STRING', '')
    print("Query String:", query_string)  # Покажет параметры из URL

    # Печатаем метод запроса (GET/POST)
    method = environ.get('REQUEST_METHOD', 'GET')
    print("Request Method:", method)

    if method == 'GET':
        params = parse_qs(query_string)  # Получаем параметры из URL
    elif method == 'POST':
        try:
            # Для POST запроса читаем тело запроса
            length = int(environ.get('CONTENT_LENGTH', 0))  # Получаем длину данных POST
            post_data = environ['wsgi.input'].read(length).decode()  # Читаем тело запроса
            print("POST Data:", post_data)  # Выводим тело запроса
            params = parse_qs(post_data)  # Разбираем данные из POST
        except (ValueError, KeyError):
            params = {}  # В случае ошибки парсим пустой словарь

    # Ответ с выводом параметров
    response_body = f"GET and POST parameters: {params}"

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, response_headers)

    return [response_body.encode('utf-8')]
