from functions.run_python_file import run_python_file


def show(header: str, result: str) -> None:
    print(header)
    print(result)
    print()


def main() -> None:
    show("Result for main.py:", run_python_file("calculator", "main.py"))
    show(
        "Result for main.py 3 + 5:", run_python_file("calculator", "main.py", ["3 + 5"])
    )
    show("Result for tests.py:", run_python_file("calculator", "tests.py"))
    show("Result for ../main.py:", run_python_file("calculator", "../main.py"))
    show("Result for nonexistent.py:", run_python_file("calculator", "nonexistent.py"))
    show("Result for lorem.txt:", run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()
