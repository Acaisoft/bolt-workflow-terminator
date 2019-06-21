import logging
from kubernetes import client
from kubernetes import config
from kubernetes.config import ConfigException

logger = logging.getLogger()


class KubernetesService:
    namespace = "argo"

    def __init__(self):
        self._load_config()
        self._cr_cli = client.CustomObjectsApi()
        self._core_cli = client.CoreV1Api()

    def _load_config(self):
        try:
            config.load_incluster_config()
        except ConfigException as e:
            logger.error("Failed to load Kubernetes config in-cluster mode.")
            logger.info("Kubernetes config loaded in-cluster mode.")
        else:
            logger.info("Kubernetes config loaded in-cluster.")
            return

        try:
            config.load_kube_config()
        except ConfigException as e:
            logger.error("Failed to load Kubernetes config kube-config mode.")
            raise e
        else:
            logger.info("Kubernetes config loaded from kube-config file.")
            return

    def terminate_workflow_pods(self, workflow_name):
        pods = self._core_cli.list_namespaced_pod(
            self.namespace,
            label_selector=f"workflows.argoproj.io/workflow={workflow_name}",
        )
        for pod in pods.items:
            self._core_cli.delete_namespaced_pod(pod.metadata.name, self.namespace)
