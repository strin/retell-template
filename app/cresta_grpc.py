import json

import grpc

from cresta.ai_service.virtualagent.virtual_agent_service_pb2 import (  # Assuming path to your protobuf file
    GenerateReplyRequest,
    GenerateReplyResponse,
)
from cresta.ai_service.virtualagent.virtual_agent_service_pb2_grpc import (  # Assuming path to your protobuf file
    VirtualAgentServiceStub,
)

from cresta.v1.virtualagent.virtual_agent_service_pb2 import GenerateReplyRequest as PublicRequest


def generate_reply_stream(
    address, conversation, conversation_history, conversation_usecase_id, virtual_agent_id
):
    """Performs an RPC call to GenerateReplyStream on the specified address.

    Args:
        address (str): The address of the gRPC server (e.g., 'localhost:8081').
        conversation (str): The conversation ID.
        conversation_history (list): A list of dictionaries representing conversation history entries,
            each with 'text' (str) and 'speaker_role' (str) keys.
        conversation_usecase_id (str): The conversation use case ID (e.g., 'faq').
        virtual_agent_id (str): The virtual agent ID.

    Returns:
        grpc.aio.UnaryStream: A stream of GenerateReplyResponse messages.
    """

    with grpc.insecure_channel(address) as channel:
        stub = VirtualAgentServiceStub(channel)

        public_request = PublicRequest(
            conversation=conversation,
            conversation_history=conversation_history,
        )

        request = GenerateReplyRequest(
            public_request=public_request,
            conversation_usecase_id=conversation_usecase_id,
            serving_unit_id={},  # Assuming empty serving_unit_id
            virtual_agent_id=virtual_agent_id,
        )

        # Handle the stream of responses
        for response in stub.GenerateReplyStream(request):
            yield response  # Process each response in the stream


# Example usage (assuming you have the protobuf definitions)
address = "localhost:8081"
conversation = "customers/cresta/profiles/walter-dev/conversations/1234"
conversation_history = [{"text": "hi", "speaker_role": "VISITOR"}]
conversation_usecase_id = "faq"
virtual_agent_id = "f0eb6857-dea8-48bd-838f-b704e1aede87"

stream = generate_reply_stream(
    address, conversation, conversation_history, conversation_usecase_id, virtual_agent_id
)

for response in stream:
    print(response.public_response.text)  # Process each response received from the stream
