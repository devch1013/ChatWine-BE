from wine.models import Conversation, Utterance, ChatExamples


def save_conversation(
    conversation_object: Conversation,
    user_input: str,
    response: str,
    stage: str,
    time_to_response: int,
):

    utterance = Utterance(
        conversation=conversation_object,
        stage=stage,
        time_to_response=time_to_response,
        user_side=user_input,
        ai_side=response,
    )
    utterance.save()
    if conversation_object.stage_history == "":
        conversation_object.stage_history = stage
    else:
        conversation_object.stage_history = conversation_object.stage_history + f", {stage}"
    conversation_object.length += 1
    conversation_object.save()

    return utterance


def save_example(
    utterance_obj: Utterance,
    chat_example: list,
):
    ex_obj = ChatExamples(utterance=utterance_obj, example="|".join(chat_example))
    ex_obj.save()
    return str(ex_obj.id)
