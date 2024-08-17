from events.screen_event import ScreenEventSub
from services.context_service import ContextService
from injector import singleton, Binder
from services.document_service import DocumentService

def configure_services(binder:Binder):
    binder.bind(ContextService, to= ContextService,scope=singleton)
    binder.bind(DocumentService, to= DocumentService,scope=singleton)

def configure_events(binder:Binder):
    binder.bind(ScreenEventSub, to= ScreenEventSub,scope=singleton)