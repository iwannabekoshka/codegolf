import subprocess
import os
import tempfile

from .constants import cpp_code_default, cpp_input_data


def execute_cpp_code(cpp_code, input_data=None):
    return {'output': cpp_code}

    # дефолтные значения для отладки
    if not cpp_code:
        cpp_code, input_data = cpp_code_default, cpp_input_data

    # Шаг 1: Сохранение C++ кода во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.cpp') as cpp_file:
        cpp_file.write(cpp_code.encode('utf-8'))
        cpp_file_name = cpp_file.name

    # Шаг 2: Компиляция C++ кода
    executable_file_name = cpp_file_name[:-4]  # Удаляем .cpp из имени файла
    compile_process = subprocess.run(['g++', cpp_file_name, '-o', executable_file_name],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Проверяем, успешно ли прошла компиляция
    if compile_process.returncode != 0:
        os.remove(cpp_file_name)
        return {'error': 'Compilation failed', 'details': compile_process.stderr.decode('utf-8')}

    # Шаг 3: Запуск скомпилированного кода
    try:
        run_process = subprocess.run([executable_file_name],
                                     input=input_data,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Шаг 4: Получение вывода и очистка временных файлов
        output = run_process.stdout
        os.remove(cpp_file_name)
        os.remove(executable_file_name)

        if run_process.returncode != 0:
            return {'error': 'Runtime error', 'details': run_process.stderr}

        return {'output': output}

    except Exception as e:
        os.remove(cpp_file_name)
        os.remove(executable_file_name)
        return {'error': str(e)}


# # Пример использования
# cpp_code = """
# #include <iostream>
# int main() {
#     std::cout << "Hello, World!" << std::endl;
#     return 0;
# }
# """
#
# result = execute_cpp_code(cpp_code)
