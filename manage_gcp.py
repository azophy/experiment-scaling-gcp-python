GCP_PROJECT_ID=None
GCP_ZONE=None
GCP_INSTANCE_NAME=None

## copied from https://cloud.google.com/compute/docs/api/libraries#client-libraries-usage-python

from typing import Iterable

from google.cloud import compute_v1


def list_instances(project_id: str, zone: str) -> Iterable[compute_v1.Instance]:
    """
    List all instances in the given zone in the specified project.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
    Returns:
        An iterable collection of Instance objects.
    """
    instance_client = compute_v1.InstancesClient()
    instance_list = instance_client.list(project=project_id, zone=zone)

    print(f"Instances found in zone {zone}:")
    for instance in instance_list:
        print(f" - {instance.name} ({instance.machine_type})")

    return instance_list

## copy from https://cloud.google.com/compute/docs/instances/stop-start-instance#python
import sys
import time
from typing import Any

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    """
    This method will wait for the extended (long-running) operation to
    complete. If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


def stop_instance() -> None:
    """
    Stops a running Google Compute Engine instance.
    """
    instance_client = compute_v1.InstancesClient()

    operation = instance_client.stop(
        project=GCP_PROJECT_ID, zone=GCP_ZONE, instance=GCP_INSTANCE_NAME
    )
    wait_for_extended_operation(operation, "instance stopping")
    return

def start_instance() -> None:
    """
    Starts a stopped Google Compute Engine instance (with unencrypted disks).
    """
    instance_client = compute_v1.InstancesClient()

    operation = instance_client.start(
        project=GCP_PROJECT_ID, zone=GCP_ZONE, instance=GCP_INSTANCE_NAME
    )
    wait_for_extended_operation(operation, "instance startping")
    return

##################################

def get_spec_info():
    """
    Harusnya mengacu ke sini: https://cloud.google.com/compute/docs/reference/rest/v1/instances/get
    """
    instance_client = compute_v1.InstancesClient()

    return instance_client.get(
        project=GCP_PROJECT_ID, zone=GCP_ZONE, instance=GCP_INSTANCE_NAME
    )

def change_machine_type(instance_name, machine_type):
    """
    Referensi:
    - https://cloud.google.com/compute/docs/reference/rest/v1/instances/setMachineType
    - https://cloud.google.com/compute/docs/instances/changing-machine-type-of-stopped-instance#changing_a_machine_type

    Machine type string format harusnya mengacu ke sini: https://cloud.google.com/compute/docs/reference/rest/v1/instances/setMachineType#request-body
    contoh: `zones/us-central1-f/machineTypes/n1-standard-1`
    """
    pass
