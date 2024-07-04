cpp_code_default = """
#include <iostream>
#include <string>

int main() {
    std::string input;
    std::getline(std::cin, input);
    std::cout << "Received: " << input << std::endl;
    return 0;
}
"""

cpp_input_data = "Hello, input data!\n"


CODE_LANGUAGES = (
  ('cpp', 'C++'),
  ('python', 'Python'),
  ('javascript', 'JS'),
  ('c', 'C'),
)
