from functions.get_files_info import get_files_info


def show(header: str, result: str) -> None:
    print(header)
    for line in result.split("\n"):
        print(f" {line}")
    print()


def main() -> None:
    show("Result for current directory:", get_files_info("calculator", "."))
    show("Result for 'pkg' directory:", get_files_info("calculator", "pkg"))
    show("Result for '/bin' directory:", get_files_info("calculator", "/bin"))
    show("Result for '../' directory:", get_files_info("calculator", "../"))


if __name__ == "__main__":
    main()
