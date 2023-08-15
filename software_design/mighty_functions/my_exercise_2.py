from dataclasses import dataclass


@dataclass
class Laptop:
    machine_name: str = "DULL"

    def install_os(self) -> None:
        print("Installing OS")

    def format_hd(self) -> None:
        print("Formatting the hard drive")

    def create_admin_user(self, password: str) -> None:
        print(f"Creating admin user with password {password}")

    # Object-oriented extension
    def reset_to_factory(self) -> None:
        self.format_hd()
        self.machine_name = "DULL"
        self.install_os()
        self.create_admin_user("admin")


# Functional extension
# def reset_to_factory(laptop: Laptop) -> None:
#    laptop.format_hd()
#    laptop.machine_name = "DULL"
#    laptop.install_os()
#    laptop.create_admin_user("admin")


def main() -> None:
    laptop = Laptop()
    # reset_to_factory(laptop)
    laptop.reset_to_factory()
    print(laptop)


if __name__ == "__main__":
    main()
