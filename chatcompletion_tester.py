from openai import OpenAI
import os
from dotenv import load_dotenv
import argparse

client = OpenAI()

load_dotenv()
client.api_key = os.getenv("OPENAI_API_KEY")

def generate_responses(input_file, output_file, n):
    pre_prompt = """あなたは乙女ゲームの悪役令嬢です。以下の設定に従い、ユーザと会話してください
一人称:私,わたくし
自己紹介:私こそが、この学園でも最も美しく優雅な令嬢、名門家の令嬢、アリシア・ヴァンデルヴァルトよ。この世界で最も美しくて、最も賢いと言っても過言ではないわ。私に会えるなんて、貴女も幸運ね。でも、私の敵にはならないでちょうだい。私を敵に回すことが、あなたの運命を悲惨なものにするわよ。
"""
    post_prompt = """あなたは乙女ゲームの悪役令嬢です。悪役令嬢らしく答えて
first_person:わたくし
second_person:貴女
Answer in 100 characters in Japanease.
"""

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        queries = infile.readlines()
        total_queries = len(queries)
        print(f"Total queries: {total_queries}")

        for index, query in enumerate(queries):
            query = query.strip()
            responses = []
            for _ in range(n):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # モデルは適宜調整してください
                    messages=[
                        {"role": "system", "content": pre_prompt},
                        {"role": "user", "content": query},
                        {"role": "system", "content": post_prompt}
                    ],
                    max_tokens=100,
                    temperature=0.7
                )
                answer = response.choices[0].message.content.strip()
                responses.append(answer)
            
            outfile.write(f"{query}\t" + "\t".join(responses) + "\n")
            print(f"Processed query {index + 1} of {total_queries}")

def main():
    parser = argparse.ArgumentParser(description="Generate responses for queries using OpenAI's ChatCompletion API.")
    parser.add_argument("input_file", help="The path of the input text file containing queries.")
    parser.add_argument("output_file", help="The path of the output TSV file.")
    parser.add_argument("-n", type=int, default=5, help="The number of responses to generate for each query (default: 5).")

    args = parser.parse_args()

    generate_responses(args.input_file, args.output_file, args.n)

if __name__ == "__main__":
    main()
