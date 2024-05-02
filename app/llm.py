import os
from typing import List
from .custom_types import (
    ResponseRequiredRequest,
    ResponseResponse,
    Utterance,
)

from .cresta_grpc import generate_reply_stream

begin_sentence = "Hey there, I'm your Cresta Voice assistant, how can I help you?"


class LlmClient:
    def __init__(self):
        pass

    def draft_begin_message(self):
        response = ResponseResponse(
            response_id=0,
            content=begin_sentence,
            content_complete=True,
            end_call=False,
        )
        return response

    def convert_transcript_to_cresta_messages(self, transcript: List[Utterance]):
        messages = []
        for utterance in transcript:
            if utterance.role == "agent":
                messages.append({"speaker_role": "AGENT", "text": utterance.content})
            else:
                messages.append({"speaker_role": "VISITOR", "text": utterance.content})
        return messages

    async def draft_response(self, request: ResponseRequiredRequest):
        address = "localhost:8081"
        conversation = "customers/cresta/profiles/walter-dev/conversations/1234"
        conversation_history = self.convert_transcript_to_cresta_messages(request.transcript)
        conversation_usecase_id = "faq"
        virtual_agent_id = "f0eb6857-dea8-48bd-838f-b704e1aede87"

        stream = generate_reply_stream(
            address, conversation, conversation_history, conversation_usecase_id, virtual_agent_id
        )

        for response in stream:
            print(response.public_response.text)  # Process each response received from the stream
            response = ResponseResponse(
                response_id=request.response_id,
                content=response.public_response.text,
                content_complete=False,
                end_call=False,
            )
            yield response

        # Send final response with "content_complete" set to True to signal completion
        response = ResponseResponse(
            response_id=request.response_id,
            content="",
            content_complete=True,
            end_call=False,
        )
        yield response
