import falcon

from src.services import KubernetesService


class HealthCheck:
    def on_get(self, request, response):
        response.media = {'status': 'ok'}
        response.status = falcon.HTTP_200


class WorkflowTermination:

    def __init__(self, kubernetes_service: KubernetesService):
        self.kubernetes_service = kubernetes_service

    def on_post(self, request, response):
        workflow_name = request.media.get('workflow_name')
        self.kubernetes_service.terminate_workflow_pods(workflow_name)
        response.status = falcon.HTTP_200
