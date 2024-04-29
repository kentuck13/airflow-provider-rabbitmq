__version__ = "1.0.0"

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "airflow-provider-rabbitmq",  # Required
        "name": "Airflow rabbitmq provider",  # Required
        "description": "A sample template for Apache Airflow providers.",  # Required
        "connection-types": [
            {
                "connection-type": "Rabbitmq",
                "hook-class-name": "rabbitmq_provider.hooks.RabbitmqHook"
            }
        ],
        "versions": [__version__],  # Required
    }
