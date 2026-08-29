from functions.write_file import write_file


def show(header: str, result: str) -> None:
    print(header)
    print(f"  {result}")
    print()


def main() -> None:
    show(
        "Result for lorem.txt:",
        write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    )
    show(
        "Result for pkg/morelorem.txt:",
        write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    )
    show(
        "Result for /tmp/temp.txt:",
        write_file("calculator", "/tmp/temp.txt", "this should not be allowed"),
    )


if __name__ == "__main__":
    main()
