# from openai import OpenAI
# client = OpenAI(api_key="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")


# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )

# print(chat_completion)

import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)


async def main() -> None:

    audio_file= open("./lauren3.mp3", "rb")
    transcript = await client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

    recording_text = str(transcript.text)
    print(recording_text)

    chat_completion = await client.chat.completions.create(

        messages=[
            {
                "role": "system",
                "content": "You are a personal assistant who extracts information from a transcript. \
                    Define all people and created a bulleted list of any information about them.\
                    Respond only in the format:\
                        - Person: <name> \n\t - <information about them> \n\t - <information about them> \n\n",
            },
            {
                "role": "user",
                "content": recording_text,
            }
        ],
        model="gpt-3.5-turbo",
    )

    transcript_notes = str(chat_completion.choices[0].message.content)
    print(transcript_notes)

    #read in people.md as string
    people_file = open("./people.md", "r")
    people_text = people_file.read()
    people_file.close()

    prompt_text = f"""Combine the information from the given list of people with the content of the markdown file. The new information is as follows:\
\
{transcript_notes}\
\
Text file content:\
{people_text}\
\
Now, using the provided information, update the markdown file with any new details about the individuals from the list. Ensure that the combined information is well-organized and easy to read.\
The output must be in markdown format."""

    combined_notes = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a personal assistant to manage a list of people. You will keep the structure of the provided file, but update the information about the people."
            },
            {
                "role": "user",
                "content": prompt_text,
            }
        ],
        model="gpt-3.5-turbo",
    )

    return combined_notes.choices[0]




compl = asyncio.run(main())
print(compl.message.content)
#write to people.md
people_file = open("./People.md", "w")
people_file.write(compl.message.content)
people_file.close()

