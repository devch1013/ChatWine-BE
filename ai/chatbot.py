from ai.tools import WineBarDatabaseTool, WineDatabaseTool, KakaoMapTool, SearchTool
from ai.assistant import Assistant
from ai.agent import Agent
from ai.user_response_generator import UserResponseGenerator
import threading
import time

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
    def user_chat(self, user_message, chat_history_list, chat_history):
        return (chat_history_list + [[user_message, None]], chat_history + f"User: {user_message} <END_OF_TURN>\n")

    async def bot_stage_pred_async(self, user_response, chat_history, stage_history):
        pre_chat_history = '<END_OF_TURN>'.join(chat_history.split('<END_OF_TURN>')[:-2])
        if pre_chat_history != '':
            pre_chat_history += '<END_OF_TURN>'
        # stage_number = unified_chain.stage_analyzer_chain.run({'conversation_history': pre_chat_history, 'stage_history': stage_history.replace('stage history: ', ''), 'last_user_saying':user_response+' <END_OF_TURN>\n'})
        stage_number = await self.assistant.arun(conversation_history=pre_chat_history, stage_history= stage_history.replace('stage history: ', ''), last_user_saying=user_response+' <END_OF_TURN>\n')
        stage_number = stage_number[-1]
        stage_history += stage_number if stage_history == "stage history: " else ", " + stage_number

        return stage_number, stage_history
    
    def bot_stage_pred(self, user_response, chat_history, stage_history):
        pre_chat_history = '<END_OF_TURN>'.join(chat_history.split('<END_OF_TURN>')[:-2])
        if pre_chat_history != '':
            pre_chat_history += '<END_OF_TURN>'
        # stage_number = unified_chain.stage_analyzer_chain.run({'conversation_history': pre_chat_history, 'stage_history': stage_history.replace('stage history: ', ''), 'last_user_saying':user_response+' <END_OF_TURN>\n'})
        stage_number = self.assistant.run(conversation_history=pre_chat_history, stage_history= stage_history.replace('stage history: ', ''), last_user_saying=user_response+' <END_OF_TURN>\n')
        stage_number = stage_number[-1]
        stage_history += stage_number if stage_history == "stage history: " else ", " + stage_number

        return stage_number, stage_history

    async def bot_chat_async(self, user_response, chat_history, chat_history_list, current_stage): # stream output by yielding
        
        pre_chat_history = '<END_OF_TURN>'.join(chat_history.split('<END_OF_TURN>')[:-2])
        if pre_chat_history != '':
            pre_chat_history += '<END_OF_TURN>'

        sender = ["", False]
        task = asyncio.create_task(self.agent.run(sender = sender, input=user_response+' <END_OF_TURN>\n', conversation_history=pre_chat_history, stage_number= current_stage))
        await asyncio.sleep(0)
        yield "이우선: "
        while(sender[1] == False):
            await asyncio.sleep(0.2)
            chat_history_list[-1][1] = sender[0]
            # yield chat_history_list, chat_history + f"이우선: {sender[0]}<END_OF_TURN>\n"
            yield sender[0]
        # resp = agent.run(sender = sender, input=user_response+' <END_OF_TURN>\n', conversation_history=pre_chat_history, stage_number= current_stage)

        chat_history_list[-1][1] = sender[0]
        yield "<END_OF_TURN>\n"
        # chat_history_list[-1][1] = resp
        yield chat_history_list, chat_history + f"이우선: {sender[0]}<END_OF_TURN>\n"
        
    def bot_chat(self, user_response, chat_history, chat_history_list, current_stage): # stream output by yielding
        
        pre_chat_history = '<END_OF_TURN>'.join(chat_history.split('<END_OF_TURN>')[:-2])
        if pre_chat_history != '':
            pre_chat_history += '<END_OF_TURN>'

        sender = ["", False]
        print("before thread")
        self.agent.run(sender = sender, input=user_response+' <END_OF_TURN>\n', conversation_history=pre_chat_history, stage_number= current_stage)
        t = threading.Thread(target = self.agent.run, args=sender, kwargs= {"input": user_response+' <END_OF_TURN>\n', "conversation_history": pre_chat_history, "stage_number": current_stage})
        t.start()
        print("threading started")
        # yield "이우선: "
        while(t.is_alive()):
            time.sleep(0.05)
            print("asdasdasd")
            # chat_history_list[-1][1] = sender[0]
            # yield chat_history_list, chat_history + f"이우선: {sender[0]}<END_OF_TURN>\n"
            print("sender: ", sender)
            yield sender
        # resp = agent.run(sender = sender, input=user_response+' <END_OF_TURN>\n', conversation_history=pre_chat_history, stage_number= current_stage)
        t.join()
        # chat_history_list[-1][1] = sender[0]
        yield "<END_OF_TURN>\n"
        # chat_history_list[-1][1] = resp
        # yield chat_history_list, chat_history + f"이우선: {sender[0]}<END_OF_TURN>\n"
        yield chat_history + f"이우선: {sender[0]}<END_OF_TURN>\n"
        ##########################3
        # unified_agent = UnifiedAgent()
        # t = threading.Thread(target = agent_run, args=(unified_agent.agent_executor, {'input':user_response, 'conversation_history': chat_history, 'stage_number': current_stage}, unified_agent.sender))
        # t.start()

        # while(t.is_alive()):
        #     time.sleep(0.05)
        #     response = unified_agent.sender[0]
        #     chat_history_list[-1][1] = response
        #     yield chat_history_list, chat_history + f"이우선: {response}\n"

        # t.join()
        # response = unified_agent.sender[0]
        # chat_history_list[-1][1] = response
        # return chat_history_list, chat_history + f"이우선: {response}\n"

    async def bot_response_pred_async(self, chat_history):
        response_examples = []
        pre_chat_history = '<END_OF_TURN>'.join(chat_history.split('<END_OF_TURN>')[-3:])
        out = await self.user_response_generator.arun(conversation_history=pre_chat_history)
        for user_response_example in out.split('|'):
            response_examples.append([user_response_example])
        # return [response_examples, out, ""]
        return response_examples
    
    def bot_response_pred(self, chat_history):
        response_examples = []
        pre_chat_history = '<END_OF_TURN>'.join(chat_history.split('<END_OF_TURN>')[-3:])
        out = self.user_response_generator.run(conversation_history=pre_chat_history)
        for user_response_example in out.split('|'):
            response_examples.append([user_response_example])
        # return [response_examples, out, ""]
        return response_examples
    
    def forward(self, msg):
        print("user_chat")
        chatbot, chat_hist = self.user_chat(msg, [], "")
        print("stage_pred")
        cur_stage, stage_hist = self.bot_stage_pred(msg, chat_hist, "stage history: ")
        return self.bot_chat(msg, chat_hist, chatbot, cur_stage)
        # return self.bot_response_pred(chat_hist)