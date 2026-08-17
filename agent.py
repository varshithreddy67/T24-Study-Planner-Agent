import os
import json
from datetime import date

from dotenv import load_dotenv
from groq import Groq

from tools import add_task, build_schedule, memory


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a study task with its deadline.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the study task"
                    },
                    "due": {
                        "type": "string",
                        "description": "Deadline in YYYY-MM-DD format"
                    }
                },
                "required": ["name", "due"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "build_schedule",
            "description": "Build a study schedule from all tasks stored in memory.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


available_functions = {
    "add_task": add_task,
    "build_schedule": build_schedule
}


SYSTEM_MESSAGE = f"""
You are a Study Planner Agent.

Today's date is {date.today().isoformat()}.

Your job is to help students organize study tasks around deadlines.

Rules:

1. When the user gives a new study task, use add_task().
2. When the user asks for a schedule, use build_schedule().
3. Use information from previous conversation turns.
4. Use tool results to decide your next action.
5. Never claim that a task was added unless add_task() succeeded.
6. Never invent tasks or deadlines.
7. If the user gives a month and day without a year, assume the current year ({date.today().year}).
8. If the deadline has already passed this year, consider whether the user probably means the next occurrence.
9. If the user asks which task to prioritize, compare the stored deadlines.
"""


def run_agent(user_goal):

    # Get previous conversation from memory
    conversation = memory.get_conversation()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }
    ]

    # Restore previous conversation
    messages.extend(conversation)

    # Add the new user message
    messages.append(
        {
            "role": "user",
            "content": user_goal
        }
    )

    # Store user message in memory
    memory.add_message("user", user_goal)

    print("\n" + "=" * 70)
    print("USER")
    print("=" * 70)
    print(user_goal)

    for step in range(5):

        print("\n" + "-" * 70)
        print(f"AGENT STEP {step + 1}")
        print("-" * 70)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Add assistant message to current conversation
        messages.append(message)

        if message.tool_calls:

            for tool_call in message.tool_calls:

                function_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print(f"AGENT DECISION: Call {function_name}()")
                print(f"ARGUMENTS: {arguments}")

                function = available_functions.get(function_name)

                if function is None:

                    result = {
                        "success": False,
                        "message": "Unknown tool"
                    }

                else:

                    result = function(**arguments)

                print(f"TOOL RESULT: {result}")

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    }
                )

        else:

            final_answer = message.content

            print("\n" + "=" * 70)
            print("FINAL ANSWER")
            print("=" * 70)
            print(final_answer)

            # Save final answer to memory
            memory.add_message(
                "assistant",
                final_answer
            )

            return final_answer

    return "Agent stopped after maximum steps."