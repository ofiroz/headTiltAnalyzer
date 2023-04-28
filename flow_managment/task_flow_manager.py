

class FlowManager:
    @staticmethod
    @abstractmethod
    def init_parsing_file(file_object, document_id, tenant_id, document_name, state: AtomicState) -> AtomicState:
        pass
