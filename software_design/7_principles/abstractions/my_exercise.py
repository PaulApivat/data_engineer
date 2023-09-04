from exercises.google import GoogleCredentials, GoogleServiceProvider, GoogleStorage
from dataclasses import dataclass
from typing import Protocol

""" Abstract CloudService direct dependence on Google-services by creating 3 Abstracted Protocols: 
    - CloudCredentials(Protocol) 
    - CloudServiceProvider(Protocol)
    - CloudStorage(Protocol)

    Now, the CloudService class doesn't directly depend on Google-services, but Google-services are still imported and used in main()
"""


class CloudCredentials(Protocol):
    def retrieve_credentials(self) -> str:
        ...


class CloudServiceProvider(Protocol):
    def connect(self, credentials: str) -> None:
        ...

    def get_context(self) -> str:
        ...


class CloudStorage(Protocol):
    def initialize(self, context: str) -> None:
        ...


@dataclass
class CloudService:
    auth_provider: CloudCredentials
    service: CloudServiceProvider
    storage_manager: CloudStorage

    def connect(self) -> None:
        print("Connecting to the cloud service.")
        credentials = self.auth_provider.retrieve_credentials()
        self.service.connect(credentials)
        context = self.service.get_context()
        self.storage_manager.initialize(context)
        print("Cloud service connected.")


def main():
    # Create instances of classes that implement the protocols
    auth_provider = GoogleCredentials()  # Replace with the appropriate implementation
    service_provider = (
        GoogleServiceProvider()
    )  # Replace with the appropriate implementation
    storage_manager = GoogleStorage()  # Replace with the appropriate implementation

    # Pass the instances to the CloudService constructor
    cloud_service = CloudService(auth_provider, service_provider, storage_manager)

    # Call the connect method on the cloud_service instance
    cloud_service.connect()


if __name__ == "__main__":
    main()
