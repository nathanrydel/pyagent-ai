from functions.get_file_content import get_file_content


def show(header: str, result: str) -> None:
    print(header)
    print(f"  {result}")
    print()


def main() -> None:
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    print()

    show("Result for main.py:", get_file_content("calculator", "main.py"))
    show(
        "Result for pkg/calculator.py:",
        get_file_content("calculator", "pkg/calculator.py"),
    )
    show("Result for /bin/cat:", get_file_content("calculator", "/bin/cat"))
    show(
        "Result for pkg/does_not_exist.py:",
        get_file_content("calculator", "pkg/does_not_exist.py"),
    )


if __name__ == "__main__":
    main()
