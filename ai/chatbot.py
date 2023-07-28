from ai.tools import WineBarDatabaseTool, WineDatabaseTool, KakaoMapTool, SearchTool
from ai.assistant import Assistant
from ai.agent import Agent
from ai.user_response_generator import UserResponseGenerator
import threading
import time
from queue import Queue, Empty
from time import time
from ai.utils.streaming_queue import StreamingQueue

import asyncio


class Audrey:
    def __init__(self):

        tools = [
            KakaoMapTool(),
            WineBarDatabaseTool(),
            WineDatabaseTool(),
            SearchTool(),
        ]

        verbose = False
        self.assistant = Assistant(verbose=verbose)
        self.user_response_generator = UserResponseGenerator(verbose=verbose)
        self.agent = Agent(tools=tools, verbose=verbose)
        ## 이우선: ㅁㅇㅁㄴㅇ<>, \n User

    def user_chat(self, user_message, chat_history):

        return chat_history + f"User: {user_message} <END_OF_TURN>\n"

    def bot_stage_pred(self, user_response, chat_history, stage_history):
        print(stage_history)
        pre_chat_history = "<END_OF_TURN>".join(chat_history.split("<END_OF_TURN>")[:-2])
        if pre_chat_history != "":
            pre_chat_history += "<END_OF_TURN>"
        # stage_number = unified_chain.stage_analyzer_chain.run({'conversation_history': pre_chat_history, 'stage_history': stage_history.replace('stage history: ', ''), 'last_user_saying':user_response+' <END_OF_TURN>\n'})
        stage_number = self.assistant.run(
            conversation_history=pre_chat_history,
            stage_history=stage_history.replace("stage history: ", ""),
            last_user_saying=user_response + " <END_OF_TURN>\n",
        )
        stage_number = stage_number[-1]
        # stage_history += stage_number if stage_history == "stage history: " else ", " + stage_number

        return stage_number  # , stage_history

    def bot_chat(
        self,
        user_response,
        chat_history,
        current_stage,
        conversation_object,
    ):  # stream output by yielding
        from wine.utils.chat import save_conversation, save_example

        pre_chat_history = "<END_OF_TURN>".join(chat_history.split("<END_OF_TURN>")[:-2])
        if pre_chat_history != "":
            pre_chat_history += "<END_OF_TURN>"

        streaming_queue = StreamingQueue()
        streaming_queue.set_anchor("###")
        print("before thread")
        start = time()

        user_str = "User: " + user_response + " <END_OF_TURN>"

        def chat_task():
            self.agent.run(
                queue=streaming_queue,
                input=user_str,
                conversation_history=pre_chat_history,
                stage_number=current_stage,
            )
            streaming_queue.end_job()

        # t = threading.Thread(target = self.agent.run, args=sender, kwargs= {"input": user_response+' <END_OF_TURN>\n', "conversation_history": pre_chat_history, "stage_number": current_stage})
        t = threading.Thread(target=chat_task)
        t.start()
        print("threading started")
        # yield "이우선: "
        content = ""
        next_token = None
        while True:
            if not streaming_queue.is_waiting():
                if streaming_queue.is_end():
                    break
                ## 4개
                if streaming_queue.is_streaming_end():
                    next_token = streaming_queue.get()
                    content += next_token
                    print(next_token)
                    yield next_token
                else:
                    if len(streaming_queue) > 3:
                        next_token = streaming_queue.get()
                        ## 3개
                        if streaming_queue.is_streaming_end() == False:
                            anchor_point = streaming_queue.check_anchor_point()
                            if anchor_point:
                                if anchor_point == "Front":
                                    card_content = ""
                                elif anchor_point == "Back":
                                    ## 대기
                                    card_content = ""
                                    next_token += streaming_queue.get()
                                streaming_queue.wait()
                        content += next_token
                        print(next_token)
                        yield next_token
                    # print(next_token, end="")

            else:  ##
                if not streaming_queue.is_empty():
                    if streaming_queue.is_end():
                        break
                    next_token = streaming_queue.get()

                    card_content += next_token
                    print("card content: ", card_content)
                    # print(card_content)
                    if "###" in card_content:
                        ## DB 찾기
                        inform = """{
                                'title': '우나니메 말벡 \nUNANIME MALBEC',
                                'image':
                                    'https://www.winenara.com/uploads/product/550/2636_detail_091.png',
                                'description':
                                    '라 마스코타의 블렌딩 철학을 일축한 마스코타 코어 레인지, 프리미엄 레드 와인. 우나니메의 뜻은 만장일치 라는 뜻으로, 모든 메이커의 만장일치로 뽑은 최고의 포도로 탄생한 와인',
                                "price": "59,000",
                                }"""
                        print("wine: ", inform)
                        yield inform
                        streaming_queue.release()

        print("context: ", content)
        time_to_response = int((time() - start) * 1000)
        utter = save_conversation(
            conversation_object=conversation_object,
            user_input=user_response,
            response=content,
            stage=current_stage,
            time_to_response=time_to_response,
        )

        print(chat_history + user_str + f"이우선: {content}<END_OF_TURN>")

        response_examples = self.bot_response_pred(
            chat_history=chat_history + user_str + f"이우선: {content}<END_OF_TURN>",
        )

        ex_id = save_example(utter, response_examples)
        yield "#####chat_id:" + str(conversation_object.id) + "#####ex_id:" + ex_id
        print(response_examples)
        # return response_examples

        # yield "<END_OF_TURN>\n"
        # yield chat_history_list, chat_history + f"이우선: {sender[0]}<END_OF_TURN>\n"
        # yield chat_history + f"이우선: {sender[0]}<END_OF_TURN>\n"

    async def bot_response_pred_async(self, chat_history):
        response_examples = []
        pre_chat_history = "<END_OF_TURN>".join(chat_history.split("<END_OF_TURN>")[-3:])
        out = await self.user_response_generator.arun(conversation_history=pre_chat_history)
        for user_response_example in out.split("|"):
            response_examples.append([user_response_example])
        # return [response_examples, out, ""]
        return response_examples

    def bot_response_pred(self, chat_history):
        response_examples = []
        pre_chat_history = "<END_OF_TURN>".join(chat_history.split("<END_OF_TURN>")[-3:])
        out = self.user_response_generator.run(conversation_history=pre_chat_history)
        for user_response_example in out.split("|"):
            response_examples.append(user_response_example)
        # return [response_examples, out, ""]

        return response_examples

    def forward(self, msg, conversation_object, chat_history):
        """
        유저 입력과 최근 대화 두번 필요
        """
        print("user_chat")
        chat_hist = self.user_chat(msg, chat_history=chat_history)
        print("stage_pred")
        cur_stage = self.bot_stage_pred(
            msg,
            chat_hist,
            "stage history: " + conversation_object.stage_history,
        )
        return self.bot_chat(
            msg,
            chat_hist,
            cur_stage,
            conversation_object=conversation_object,
        )
        # return self.bot_response_pred(chat_hist)


def check_anchor(q: list, anchor: str = "###"):
    print(q)
    text = "".join(q)
    if text.endswith(anchor):
        return True, text[:-3]
    else:
        return False, ""
