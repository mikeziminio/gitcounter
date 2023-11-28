import aiohttp
import asyncio


class GithubAPI:

    api_url = "https://api.github.com/graphql"

    def __init__(self, token, *, echo=False):
        self.token = token
        self.echo = echo

    async def call(self, req_json):
        req_headers = {
            "Authorization": f"Bearer {self.token}"
        }
        async with aiohttp.ClientSession() as session:
            if self.echo:
                print("GRAPHQL REQUEST:")
                print(req_json)
            async with session.post(self.api_url, headers=req_headers, json=req_json) as response:
                r = await response.json()
                if self.echo:
                    print("GRAPHQL RESPONSE:")
                    print(r)
                return r

    async def query(self, query_body: str, variables: dict = None):
        req_json = {"query": query_body}
        if variables is not None:
            req_json["variables"] = variables
        return await self.call(req_json)

    async def mutation(self, mutation_body: str, variables: dict = None):
        req_json = {"mutation": mutation_body}
        if variables is not None:
            req_json["variables"] = variables
        return await self.call(req_json)

    async def get_type(self, id: str):
        r = await self.query(f"""
            query {{
                node(id: "{id}") {{
                    __typename
                }}
            }}
        """)
        return r["data"]["node"]["__typename"]
