import falcon

from src.resources import WorkflowTermination
from src.resources import HealthCheck
from src.services import KubernetesService


def create_app(kubernetes_service):
    app = falcon.API()
    app.add_route('/workflow-termination', WorkflowTermination(kubernetes_service))
    app.add_route('/health-check', HealthCheck())
    return app


def serve_app():
    kubernetes_service = KubernetesService()
    return create_app(kubernetes_service)
